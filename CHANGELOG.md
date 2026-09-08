# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
