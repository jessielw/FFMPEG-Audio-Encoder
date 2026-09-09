# FFmpeg Audio Encoder v5

A cross-platform PySide6 front end for FFmpeg and the audio encoders around it. Drag files
in, inspect their audio streams, configure an encoder, and queue the work.

**[Documentation](https://jessielw.github.io/FFMPEG-Audio-Encoder/)** ·
[Install](https://jessielw.github.io/FFMPEG-Audio-Encoder/install/) ·
[Encoder reference](https://jessielw.github.io/FFMPEG-Audio-Encoder/encoders/reference/) ·
[Changelog](CHANGELOG.md)

A clean successor to the original Tkinter application. The maintained legacy source remains
available in [`legacy_v4`](legacy_v4/README.md).

## Download

Grab the bundle for your platform from the
[latest release](https://github.com/jessielw/FFMPEG-Audio-Encoder/releases/latest):

| Platform | Archive |
| --- | --- |
| Windows (x64) | `FFMPEGAudioEncoder-<version>-windows-x64.zip` |
| macOS (Intel) | `FFMPEGAudioEncoder-<version>-macos-x64.zip` |
| macOS (Apple silicon) | `FFMPEGAudioEncoder-<version>-macos-arm64.zip` |
| Linux (x64) | `FFMPEGAudioEncoder-<version>-linux-x64.tar.gz` |

Unpack the archive anywhere and run `FFMPEGAudioEncoder` from inside it. Nothing is
installed system-wide and no runtime is required.

The bundles are unsigned. macOS Gatekeeper blocks them on first launch, so open the app
once with right-click ▸ Open and confirm; Windows SmartScreen needs *More info* ▸
*Run anyway*.

**FFmpeg and ffprobe are not bundled.** Install them and leave them on `PATH`, or point at
the executables in Settings. opusenc, qaac, fdkaac, and DeeZy are optional and discovered
the same way; the encoders you have not installed are shown as unavailable rather than
failing at encode time. `Help ▸ Copy diagnostics` reports exactly what was found. See
[Required and optional tools](https://jessielw.github.io/FFMPEG-Audio-Encoder/tools/).

## What it does

- Drag-and-drop input, stream inspection, and per-stream encoding.
- Sixteen encoders in three families - eight built into FFmpeg, three standalone
  command-line encoders (opusenc, qaac, fdkaac), and five DeeZy adapters for licensed Dolby
  formats. Every option is in the
  [encoder reference](https://jessielw.github.io/FFMPEG-Audio-Encoder/encoders/reference/).
- Presets, plus automatic restoration of the last encoder configuration.
- Sample-rate, channel-layout, gain, tempo, and per-track delay controls.
- A durable queue with selected-job starts, stop-after-current, retry, cancellation, and
  crash-safe temporary outputs.
- Live per-job progress, command and error details, bounded session logs, and output-folder
  actions.
- Asynchronous tool detection, bounded media probing, rotating application logs, and
  single-instance protection.

## Development

```console
uv sync --group dev
uv run ffmpeg-audio-encoder
```

```console
uv run ruff format --check .
uv run ruff check .
uv run basedpyright
uv run pytest
uv run ffmpeg-audio-encoder --diagnostics
```

Build a native one-folder application bundle with `uv sync --group build` followed by
`uv run python build.py`.

Preview the documentation site with `uv sync --group docs` and
`uv run zensical serve --open`.

More detail: [development setup](https://jessielw.github.io/FFMPEG-Audio-Encoder/dev/setup/),
[architecture](https://jessielw.github.io/FFMPEG-Audio-Encoder/dev/architecture/),
[adding an encoder](https://jessielw.github.io/FFMPEG-Audio-Encoder/dev/adding-an-encoder/),
[building bundles](https://jessielw.github.io/FFMPEG-Audio-Encoder/dev/building/).

## Legacy v4

The original program depends on working-directory-relative paths:

```console
cd legacy_v4
uv sync
uv run python FFMPEGAudioEncoder.py
```
