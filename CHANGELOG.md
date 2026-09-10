# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Time modification presets**, restoring the named framerate conversions v4 offered and dropping the arithmetic v5 required in their place. The **General** tab gains a list of every conversion between 23.976, 24, 25, 29.97, 30, 50, 59.94, and 60 fps, grouped by source rate, plus speed multipliers from 0.25× to 4×. Picking one fills in the **Tempo** ratio; editing the ratio by hand sets the list to **Custom**. Ratios are derived from the exact framerates (23.976 fps is 24000/1001), so `24 → 23.976` is exactly 0.999001 rather than a rounded approximation. v4's 2.5× to 4× entries, which it emitted as a single `atempo=` that FFmpeg rejects outright, work here because the filter chain is built by halving and doubling.

### Changed

- Build automatic spinbox that trims 0 decimals from delay (2480ms will be displayed as 2480 ms vs. 2480,000 ms)

### Fixed

- The **Tempo** field held three decimals, which could not express the PAL speed-up (23.976 → 25 is 1.042708) and drifted by seconds over a feature-length file. It now holds six, and trims padded zeros so an unchanged ratio still reads `1x`.
- The `atempo` filter value was formatted with `%g`, which caps at six _significant_ digits and turned the 24 → 25 conversion's 1.041667 into 1.04167 - about 23 ms of drift over two hours.
- The presets documentation claimed a preset stores the audio delay, and advised zeroing the field before saving to avoid baking in one file's value. Presets have never stored the delay - it is excluded deliberately, because it belongs to a particular file - so the advice was for a hazard that does not exist. Documentation only; no behaviour changed.

## [5.0.0] - 2026-09-08

First release of the rewritten application. v5 replaces the Tkinter front end with a PySide6 one built on a new codebase; v4 remains available under [`legacy_v4`](legacy_v4/README.md) and is unaffected.

### Added

- **PySide6 interface** with drag-and-drop input, per-stream inspection and encoding, light/dark/automatic themes, a collapsible queue panel, and restored window geometry.
- **Durable encoding queue** saved atomically to a versioned `jobs.json`. Queued jobs stay paused across restarts, and a job that was running when the application exited is restored as failed so it can be reviewed and retried rather than silently resumed.
- **Crash-safe outputs.** Every encode writes to a job-specific `.part` file that is published atomically only on success. Source/output self-overwrites and duplicate active destinations are rejected, and generated name collisions are numbered automatically.
- **DeeZy adapters** for DD, DDP, DDP-BluRay, Atmos, and AC-4, including configuration-aware bitrate lists, BS.1770 and Leq(A) metering, DRC and downmix controls, and TrueHDD warp/bed controls. DeeZy's child processes are held in a Windows job object (a process-group walk elsewhere) so cancelling a job cannot leave a TrueHD decode running, and its intermediates are redirected to an application cache folder that is pruned at startup.
- **Standalone encoder adapters** for opusenc, qaac (Apple AAC), and fdkaac (Fraunhofer FDK AAC), fed PCM from FFmpeg over a pipe and writing straight to the queue's temporary output.
- **FFmpeg adapters** for Opus, FLAC, AAC, MP3, AC-3, E-AC-3, DTS, and ALAC, each with curated rate-control and quality settings plus codec-aware channel layouts.
- **Per-track delay handling.** Container delays are detected with the bundled MediaInfo library, with filename markers such as `[DELAY -21ms]` as a fallback for single-track audio-only inputs. The detected value stays editable, is baked into the encoded samples, and filename markers are stripped from generated output names.
- **Presets** plus automatic restoration of the last encoder configuration, with stale values rejected rather than silently substituted.
- **Live per-job progress**, command and error details, bounded session logs, output-folder actions, and a `Help ▸ Copy diagnostics` action that summarizes the detected toolchain.
- **Asynchronous, parallel tool detection**, bounded media probing, rotating application logs, single-instance protection, and a `--diagnostics` command-line report.
- Corrupt settings, preset, and queue files are quarantined with a `corrupt-<timestamp>` suffix instead of being overwritten.

[5.0.0]: https://github.com/jessielw/FFMPEG-Audio-Encoder/releases/tag/v5.0.0
