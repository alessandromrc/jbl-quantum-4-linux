#!/usr/bin/env python3
"""Render a frequency-response PNG for every Easy Effects preset in easyeffects/.

Reads each preset's equalizer#0 bands and plots the combined curve (Bell,
Hi-shelf, Lo-shelf, Hi-pass), assuming a 48 kHz digital biquad per the RBJ
Audio EQ Cookbook. The limiter stage is dynamics, not frequency shaping, so
it's left out of the graph.
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = REPO_ROOT / "easyeffects"
GRAPH_DIR = SOURCE_DIR / "graphs"
FS = 48000.0
FREQS = np.logspace(np.log10(20), np.log10(20000), 500)


def biquad_coeffs(band, fs):
    freq = band["frequency"]
    gain = band["gain"]
    q = band["q"] or 0.01
    kind = band["type"]

    w0 = 2 * np.pi * freq / fs
    cos_w0 = np.cos(w0)
    sin_w0 = np.sin(w0)
    alpha = sin_w0 / (2 * q)
    a_amp = 10 ** (gain / 40)

    if kind == "Bell":
        b0 = 1 + alpha * a_amp
        b1 = -2 * cos_w0
        b2 = 1 - alpha * a_amp
        a0 = 1 + alpha / a_amp
        a1 = -2 * cos_w0
        a2 = 1 - alpha / a_amp
    elif kind == "Lo-shelf":
        sqrt_a = np.sqrt(a_amp)
        b0 = a_amp * ((a_amp + 1) - (a_amp - 1) * cos_w0 + 2 * sqrt_a * alpha)
        b1 = 2 * a_amp * ((a_amp - 1) - (a_amp + 1) * cos_w0)
        b2 = a_amp * ((a_amp + 1) - (a_amp - 1) * cos_w0 - 2 * sqrt_a * alpha)
        a0 = (a_amp + 1) + (a_amp - 1) * cos_w0 + 2 * sqrt_a * alpha
        a1 = -2 * ((a_amp - 1) + (a_amp + 1) * cos_w0)
        a2 = (a_amp + 1) + (a_amp - 1) * cos_w0 - 2 * sqrt_a * alpha
    elif kind == "Hi-shelf":
        sqrt_a = np.sqrt(a_amp)
        b0 = a_amp * ((a_amp + 1) + (a_amp - 1) * cos_w0 + 2 * sqrt_a * alpha)
        b1 = -2 * a_amp * ((a_amp - 1) + (a_amp + 1) * cos_w0)
        b2 = a_amp * ((a_amp + 1) + (a_amp - 1) * cos_w0 - 2 * sqrt_a * alpha)
        a0 = (a_amp + 1) - (a_amp - 1) * cos_w0 + 2 * sqrt_a * alpha
        a1 = 2 * ((a_amp - 1) - (a_amp + 1) * cos_w0)
        a2 = (a_amp + 1) - (a_amp - 1) * cos_w0 - 2 * sqrt_a * alpha
    elif kind == "Hi-pass":
        b0 = (1 + cos_w0) / 2
        b1 = -(1 + cos_w0)
        b2 = (1 + cos_w0) / 2
        a0 = 1 + alpha
        a1 = -2 * cos_w0
        a2 = 1 - alpha
    else:
        return None

    return (b0 / a0, b1 / a0, b2 / a0, 1.0, a1 / a0, a2 / a0)


def response_db(bands, freqs, fs):
    total_db = np.zeros_like(freqs)
    w = 2 * np.pi * freqs / fs
    z1 = np.exp(-1j * w)
    z2 = np.exp(-2j * w)
    for band in bands:
        if band.get("mute") or band.get("type") in (None, "Off"):
            continue
        coeffs = biquad_coeffs(band, fs)
        if coeffs is None:
            continue
        b0, b1, b2, a0, a1, a2 = coeffs
        h = (b0 + b1 * z1 + b2 * z2) / (a0 + a1 * z1 + a2 * z2)
        total_db += 20 * np.log10(np.clip(np.abs(h), 1e-6, None))
    return total_db


JBL_ORANGE = "#FF6A00"
INK = "#1c1c1c"
PANEL = "#141414"


def plot_preset(json_path: Path, png_path: Path):
    data = json.loads(json_path.read_text())
    eq = data.get("output", {}).get("equalizer#0")
    if not eq:
        return False

    bands = eq.get("left", {}).values()
    db = response_db(bands, FREQS, FS)

    fig, ax = plt.subplots(figsize=(6, 3.2), dpi=140)
    fig.patch.set_facecolor(INK)
    ax.set_facecolor(PANEL)

    ax.fill_between(FREQS, db, 0, color=JBL_ORANGE, alpha=0.25, linewidth=0)
    ax.plot(FREQS, db, color=JBL_ORANGE, linewidth=2.4, solid_capstyle="round")
    ax.axhline(0, color="#777777", linewidth=0.8, linestyle="--", zorder=0)

    ax.set_xscale("log")
    ax.set_xlim(20, 20000)
    ax.set_ylim(-16, 16)

    ax.set_xlabel("Hz", color="#bbbbbb", fontsize=9)
    ax.set_ylabel("dB", color="#bbbbbb", fontsize=9)
    ax.set_title(json_path.stem, fontsize=12, color="white", fontweight="bold", pad=10)

    ax.tick_params(colors="#999999", labelsize=8)
    ax.grid(True, which="both", color="#3a3a3a", linewidth=0.4, alpha=0.8)
    for spine in ax.spines.values():
        spine.set_color("#444444")

    fig.tight_layout()

    png_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(png_path, facecolor=INK)
    plt.close(fig)
    return True


def main():
    count = 0
    for json_path in sorted(SOURCE_DIR.rglob("*.json")):
        rel = json_path.relative_to(SOURCE_DIR)
        png_name = rel.with_suffix(".png").name.replace(" ", "_")
        png_path = GRAPH_DIR / rel.parent / png_name
        if plot_preset(json_path, png_path):
            count += 1
    print(f"Generated {count} graphs in {GRAPH_DIR}")


if __name__ == "__main__":
    main()
