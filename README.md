<div align="center">

# JBL Quantum on Linux

**QuantumENGINE's headset EQ and surround, without Windows.**

![platform](https://img.shields.io/badge/platform-Linux-FF6A00?style=flat-square)
![pipewire](https://img.shields.io/badge/audio-PipeWire-FF6A00?style=flat-square)
![presets](https://img.shields.io/badge/presets-91-FF6A00?style=flat-square)
![jbl](https://img.shields.io/badge/JBL-lol-FF6A00?style=flat-square)

<img src="easyeffects/graphs/Q950.png" width="520" alt="Q950 frequency response">

</div>

JBL's QuantumENGINE software is Windows-only, and the Quantum spatial/surround
engine itself does not run on Linux. This repo doesn't try to rebuild that
engine. Instead it gives you two independent pieces that cover most of what
people actually want from it:

- **Headset EQ**: the per-model driver curve QuantumENGINE applies, converted
  to [Easy Effects](https://github.com/wwmm/easyeffects) presets.
- **Surround**: 7.1-to-headphone virtual surround via
  [Virtual Surround Manager](https://github.com/Bern23/virtual-surround-manager),
  using an impulse response file instead of the Quantum spatial engine.

> [!WARNING]
> JBL not supporting Linux is honestly the least funny thing about JBL.
> Their "spatial engine" is an 18 MB mystery blob that nobody, including
> possibly JBL, can read, running on software that needs a Windows install
> just to move a slider. Meanwhile the headband creaks louder than the bass.
> Anyway, you can just use Virtual Surround Manager instead and skip the
> whole bit.

> **I don't own any JBL Quantum headset.** These presets were derived from
> QuantumENGINE's own config files, not tuned by ear, and I have no way to
> test them myself. [**@DefSteam**](https://github.com/DefSteam), who does
> own the hardware, tested them and confirmed they sound right, but if
> something's off for your model, please open an issue.

**Jump to:** [What's in this repo](#whats-in-this-repo) ·
[Headset EQ](#1-headset-eq-in-easy-effects) ·
[Surround](#2-surround-in-virtual-surround-manager) ·
[Use both together](#3-use-both-together) ·
[Graphs](#4-frequency-response-graphs)

## What's in this repo

```
easyeffects/
├── <Model>.json            headset EQ, surround/spatial mode on
├── <Model>-stereo.json      headset EQ, surround/spatial mode off
├── <Model>-mac.json         Mac-specific variant, for models that have one
├── graphs/                  frequency response PNG for every preset below
└── presets/
    ├── 8-band/               QuantumENGINE's 8-band game/genre EQ presets
    ├── 10-band/              QuantumENGINE's 10-band game/genre EQ presets
    └── mic/                  QuantumENGINE's mic (QuantumSTREAM) presets
scripts/
└── generate_eq_graphs.py    regenerates everything in easyeffects/graphs/
```

## 1. Headset EQ in Easy Effects

Copy the preset for your model into Easy Effects' output folder:

```bash
mkdir -p ~/.config/easyeffects/output
cp easyeffects/Q950.json ~/.config/easyeffects/output/
```

Replace `Q950` with your model. Then, in Easy Effects, open the **Output**
tab and load that preset.

Two files exist for most models:

| File | Use it when |
|---|---|
| `Q950.json` | Surround is **on**. This is the driver curve Quantum applies on top of spatial audio. |
| `Q950-stereo.json` | Surround is **off**. On most models this is only a small bass cut. **Quantum ONE** is the exception: its stereo file is a full second EQ. |

A few models share a curve, so the matching files are identical presets:

- `Q520`, `Q520X`, `Q650`, `Q650X`
- `Q950`, `Q950X`

`EqConfig.xml` is a duplicate of the `Q50C` curve and wasn't exported.
`EqConfig-FlatITDon.xml` and `EqConfig-FlatITDoff.xml` are silent placeholder
filters and weren't exported either.

Each preset is an equalizer in APO mode plus that model's limiter. The JBL
limiter looks ahead 50 ms; Easy Effects caps lookahead at 20 ms, so it's
clamped. Threshold, attack, and release are unchanged.

### Game and mic presets

`easyeffects/presets/` has the extra EQ curves QuantumENGINE ships per game
and genre (Apex Legends, CS2, Valorant, Fortnite, FPS, MOBA, RPG, Cinematic,
Bass Boost, etc.), in both 8-band and 10-band form, plus the QuantumSTREAM /
Quantum mic presets (Bright, Natural, Powerful). Load whichever one matches
your model's band count and taste the same way you load the output preset
above; these go in the **Output** tab for the game/genre curves, or the
**Input** tab for the mic presets.

## 2. Surround in Virtual Surround Manager

Install Virtual Surround Manager from Flathub, the AUR, or an AppImage. It
needs PipeWire, which current desktops already use.

A profile is a 14-channel WAV, the same format as HeSuVi's `hrir/*.wav`
files. It is **not** JSON, and it is **not** `qeSpatial.bin`.

The app already includes `dtshx.wav`, `atmos.wav`, `sonic.wav`, `sbx33.wav`,
`sbx100.wav`, and `oal_dflt.wav`. Pick one from **Virtualization Profiles**.
`dtshx.wav` is a community DTS-like impulse shipped by HeSuVi. It is not
extracted from any JBL/DTS files.

To add more:

1. Click **Open folder** on the Virtualization Profiles card.
2. Copy plain `hrir/*.wav` files into that folder. The usual source is the
   HeSuVi `hrir` directory.
3. Skip any name ending in `-.wav`. Those are a stereo matrix made for
   Equalizer APO, and this app won't map them onto the seven speakers.
4. Click **Reload** and select the new file.
5. Leave the channel mode on 7.1 unless the game only outputs 5.1.

Folder locations, if you copy files yourself:

- Normal install: `~/.local/share/virtual-surround-manager/hrir_wav/`
- Flatpak: `~/.var/app/de.berny23.virtual_surround_manager/data/virtual-surround-manager/hrir_wav/`

The 14 channels, in order: left ear then right ear for front left, side
left, and rear left; then the center's left ear; then right ear then left
ear for front right, side right, and rear right; then the center's right
ear. The subwoofer is played through the center impulse, so there's no
fifteenth channel. 48 kHz is the usual rate, and 44.1 kHz files work too,
since PipeWire resamples them.

In the game, select real 7.1 or 5.1 output, and turn off the game's own
headphone/3D profile, otherwise the sound gets spatialized twice.

## 3. Use both together

Easy Effects only sees stereo, so it has to sit **after** the surround
fold-down:

```
game (7.1) → Virtual Surround Manager → stereo → Easy Effects → headset
```

In Easy Effects:

1. Turn off **Process all output streams**.
2. Enable processing for Virtual Surround Manager.
3. Exclude the game.

Load the plain model preset (`Q950.json`), not the stereo one. That curve
is the one meant to sit on the spatial path.

Music players and voice chat should skip Virtual Surround Manager. In its
app list, enable those apps so they go straight to Easy Effects, and load
`Q950-stereo.json` for them if you want the surround-off tone.

If audio goes silent after changing this, toggle Virtual Surround Manager
off and on once so PipeWire reconnects the nodes.
[coppwr](https://github.com/wwmm/coppwr) should show the game entering the
surround sink, stereo leaving it, and that stereo entering the Easy Effects
sink.

## 4. Frequency response graphs

Every preset in this repo gets a graph, generated from its actual EQ bands with
`scripts/generate_eq_graphs.py` (RBJ cookbook biquads, 48 kHz, limiter excluded
since it doesn't shape frequency). Flat means that curve does nothing; it exists
for completeness or as a baseline, not because it does something interesting.

<details>
<summary><strong>Headset EQ</strong> (per model, surround on/off/mac)</summary>

<table>
<tr>
<td align="center"><img src="easyeffects/graphs/Q300.png" width="220"><br><sub>Q300</sub></td>
<td align="center"><img src="easyeffects/graphs/Q300-stereo.png" width="220"><br><sub>Q300-stereo</sub></td>
<td align="center"><img src="easyeffects/graphs/Q350.png" width="220"><br><sub>Q350</sub></td>
<td align="center"><img src="easyeffects/graphs/Q350-stereo.png" width="220"><br><sub>Q350-stereo</sub></td>
</tr>
<tr>
<td align="center"><img src="easyeffects/graphs/Q360.png" width="220"><br><sub>Q360</sub></td>
<td align="center"><img src="easyeffects/graphs/Q360P.png" width="220"><br><sub>Q360P</sub></td>
<td align="center"><img src="easyeffects/graphs/Q360X.png" width="220"><br><sub>Q360X</sub></td>
<td align="center"><img src="easyeffects/graphs/Q400.png" width="220"><br><sub>Q400</sub></td>
</tr>
<tr>
<td align="center"><img src="easyeffects/graphs/Q400-mac.png" width="220"><br><sub>Q400-mac</sub></td>
<td align="center"><img src="easyeffects/graphs/Q400-mac-stereo.png" width="220"><br><sub>Q400-mac-stereo</sub></td>
<td align="center"><img src="easyeffects/graphs/Q400-stereo.png" width="220"><br><sub>Q400-stereo</sub></td>
<td align="center"><img src="easyeffects/graphs/Q50C.png" width="220"><br><sub>Q50C</sub></td>
</tr>
<tr>
<td align="center"><img src="easyeffects/graphs/Q50C-stereo.png" width="220"><br><sub>Q50C-stereo</sub></td>
<td align="center"><img src="easyeffects/graphs/Q520.png" width="220"><br><sub>Q520</sub></td>
<td align="center"><img src="easyeffects/graphs/Q520-stereo.png" width="220"><br><sub>Q520-stereo</sub></td>
<td align="center"><img src="easyeffects/graphs/Q520X.png" width="220"><br><sub>Q520X</sub></td>
</tr>
<tr>
<td align="center"><img src="easyeffects/graphs/Q520X-stereo.png" width="220"><br><sub>Q520X-stereo</sub></td>
<td align="center"><img src="easyeffects/graphs/Q600.png" width="220"><br><sub>Q600</sub></td>
<td align="center"><img src="easyeffects/graphs/Q600-stereo.png" width="220"><br><sub>Q600-stereo</sub></td>
<td align="center"><img src="easyeffects/graphs/Q610.png" width="220"><br><sub>Q610</sub></td>
</tr>
<tr>
<td align="center"><img src="easyeffects/graphs/Q610-mac.png" width="220"><br><sub>Q610-mac</sub></td>
<td align="center"><img src="easyeffects/graphs/Q610-mac-stereo.png" width="220"><br><sub>Q610-mac-stereo</sub></td>
<td align="center"><img src="easyeffects/graphs/Q610-stereo.png" width="220"><br><sub>Q610-stereo</sub></td>
<td align="center"><img src="easyeffects/graphs/Q650.png" width="220"><br><sub>Q650</sub></td>
</tr>
<tr>
<td align="center"><img src="easyeffects/graphs/Q650-stereo.png" width="220"><br><sub>Q650-stereo</sub></td>
<td align="center"><img src="easyeffects/graphs/Q650X.png" width="220"><br><sub>Q650X</sub></td>
<td align="center"><img src="easyeffects/graphs/Q650X-stereo.png" width="220"><br><sub>Q650X-stereo</sub></td>
<td align="center"><img src="easyeffects/graphs/Q800.png" width="220"><br><sub>Q800</sub></td>
</tr>
<tr>
<td align="center"><img src="easyeffects/graphs/Q800-stereo.png" width="220"><br><sub>Q800-stereo</sub></td>
<td align="center"><img src="easyeffects/graphs/Q810.png" width="220"><br><sub>Q810</sub></td>
<td align="center"><img src="easyeffects/graphs/Q810-stereo.png" width="220"><br><sub>Q810-stereo</sub></td>
<td align="center"><img src="easyeffects/graphs/Q850.png" width="220"><br><sub>Q850</sub></td>
</tr>
<tr>
<td align="center"><img src="easyeffects/graphs/Q850-stereo.png" width="220"><br><sub>Q850-stereo</sub></td>
<td align="center"><img src="easyeffects/graphs/Q910.png" width="220"><br><sub>Q910</sub></td>
<td align="center"><img src="easyeffects/graphs/Q910P.png" width="220"><br><sub>Q910P</sub></td>
<td align="center"><img src="easyeffects/graphs/Q910X.png" width="220"><br><sub>Q910X</sub></td>
</tr>
<tr>
<td align="center"><img src="easyeffects/graphs/Q950.png" width="220"><br><sub>Q950</sub></td>
<td align="center"><img src="easyeffects/graphs/Q950-stereo.png" width="220"><br><sub>Q950-stereo</sub></td>
<td align="center"><img src="easyeffects/graphs/Q950X.png" width="220"><br><sub>Q950X</sub></td>
<td align="center"><img src="easyeffects/graphs/Q950X-stereo.png" width="220"><br><sub>Q950X-stereo</sub></td>
</tr>
<tr>
<td align="center"><img src="easyeffects/graphs/QOne.png" width="220"><br><sub>QOne</sub></td>
<td align="center"><img src="easyeffects/graphs/QOne-mac.png" width="220"><br><sub>QOne-mac</sub></td>
<td align="center"><img src="easyeffects/graphs/QOne-mac-stereo.png" width="220"><br><sub>QOne-mac-stereo</sub></td>
<td align="center"><img src="easyeffects/graphs/QOne-stereo.png" width="220"><br><sub>QOne-stereo</sub></td>
</tr>
<tr>
<td align="center"><img src="easyeffects/graphs/TWS.png" width="220"><br><sub>TWS</sub></td>
<td align="center"><img src="easyeffects/graphs/TWS-stereo.png" width="220"><br><sub>TWS-stereo</sub></td>
<td align="center"><img src="easyeffects/graphs/TWSAir.png" width="220"><br><sub>TWSAir</sub></td>
<td></td>
</tr>
</table>

</details>

<details>
<summary><strong>Game &amp; genre presets, 8-band</strong></summary>

<table>
<tr>
<td align="center"><img src="easyeffects/graphs/presets/8-band/Apex_Legends.png" width="220"><br><sub>Apex Legends</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/8-band/BASS_BOOST.png" width="220"><br><sub>BASS BOOST</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/8-band/CINEMATIC.png" width="220"><br><sub>CINEMATIC</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/8-band/CS2.png" width="220"><br><sub>CS2</sub></td>
</tr>
<tr>
<td align="center"><img src="easyeffects/graphs/presets/8-band/Dota_2.png" width="220"><br><sub>Dota 2</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/8-band/Escape_from_Tarkov.png" width="220"><br><sub>Escape from Tarkov</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/8-band/FLAT.png" width="220"><br><sub>FLAT</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/8-band/Fortnite.png" width="220"><br><sub>Fortnite</sub></td>
</tr>
<tr>
<td align="center"><img src="easyeffects/graphs/presets/8-band/FPS.png" width="220"><br><sub>FPS</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/8-band/GTA_5.png" width="220"><br><sub>GTA 5</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/8-band/LN3_Immersion.png" width="220"><br><sub>LN3 Immersion</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/8-band/LN3_Thrill.png" width="220"><br><sub>LN3 Thrill</sub></td>
</tr>
<tr>
<td align="center"><img src="easyeffects/graphs/presets/8-band/LOL.png" width="220"><br><sub>LOL</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/8-band/MOBA.png" width="220"><br><sub>MOBA</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/8-band/Overwatch_2.png" width="220"><br><sub>Overwatch 2</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/8-band/PUBG.png" width="220"><br><sub>PUBG</sub></td>
</tr>
<tr>
<td align="center"><img src="easyeffects/graphs/presets/8-band/RPG.png" width="220"><br><sub>RPG</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/8-band/Valorant.png" width="220"><br><sub>Valorant</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/8-band/WoW.png" width="220"><br><sub>WoW</sub></td>
<td></td>
</tr>
</table>

</details>

<details>
<summary><strong>Game &amp; genre presets, 10-band</strong></summary>

<table>
<tr>
<td align="center"><img src="easyeffects/graphs/presets/10-band/Apex_Legends.png" width="220"><br><sub>Apex Legends</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/10-band/BASS_BOOST.png" width="220"><br><sub>BASS BOOST</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/10-band/CINEMATIC.png" width="220"><br><sub>CINEMATIC</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/10-band/CS2.png" width="220"><br><sub>CS2</sub></td>
</tr>
<tr>
<td align="center"><img src="easyeffects/graphs/presets/10-band/Dota_2.png" width="220"><br><sub>Dota 2</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/10-band/Escape_from_Tarkov.png" width="220"><br><sub>Escape from Tarkov</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/10-band/FLAT.png" width="220"><br><sub>FLAT</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/10-band/Fortnite.png" width="220"><br><sub>Fortnite</sub></td>
</tr>
<tr>
<td align="center"><img src="easyeffects/graphs/presets/10-band/FPS.png" width="220"><br><sub>FPS</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/10-band/GTA_5.png" width="220"><br><sub>GTA 5</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/10-band/LN3_Immersion.png" width="220"><br><sub>LN3 Immersion</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/10-band/LN3_Thrill.png" width="220"><br><sub>LN3 Thrill</sub></td>
</tr>
<tr>
<td align="center"><img src="easyeffects/graphs/presets/10-band/LOL.png" width="220"><br><sub>LOL</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/10-band/MOBA.png" width="220"><br><sub>MOBA</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/10-band/Overwatch_2.png" width="220"><br><sub>Overwatch 2</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/10-band/PUBG.png" width="220"><br><sub>PUBG</sub></td>
</tr>
<tr>
<td align="center"><img src="easyeffects/graphs/presets/10-band/RPG.png" width="220"><br><sub>RPG</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/10-band/Valorant.png" width="220"><br><sub>Valorant</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/10-band/WoW.png" width="220"><br><sub>WoW</sub></td>
<td></td>
</tr>
</table>

</details>

<details>
<summary><strong>Mic presets</strong></summary>

<table>
<tr>
<td align="center"><img src="easyeffects/graphs/presets/mic/QStream-Bright.png" width="220"><br><sub>QStream-Bright</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/mic/QStream-Natural.png" width="220"><br><sub>QStream-Natural</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/mic/QStream-Powerful.png" width="220"><br><sub>QStream-Powerful</sub></td>
</tr>
<tr>
<td align="center"><img src="easyeffects/graphs/presets/mic/Quantum-Bright.png" width="220"><br><sub>Quantum-Bright</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/mic/Quantum-Natural.png" width="220"><br><sub>Quantum-Natural</sub></td>
<td align="center"><img src="easyeffects/graphs/presets/mic/Quantum-Powerful.png" width="220"><br><sub>Quantum-Powerful</sub></td>
</tr>
</table>

</details>

