# FFmpeg Audio Encoder

A cross-platform desktop front end for FFmpeg and the audio encoders that surround it. Drag files in, inspect their audio streams, configure an encoder, and queue the work.

Version 5 is a rewrite. The Tkinter interface of v4 has been replaced by a PySide6 one built on a new codebase, with a durable encoding queue, crash-safe outputs, and adapters for external and licensed encoders alongside FFmpeg's own.

[Install](install.md)

: Download a bundle for your platform and get past the first-launch warnings.

[Set up your tools](tools.md)

: FFmpeg is required. opusenc, qaac, fdkaac, and DeeZy are optional and discovered automatically.

[Encode something](first-encode.md)

: From dropped file to finished output.

[Encoder reference](encoders/reference.md)

: Every encoder and every option, generated from the source.

## What it does

- **Per-stream encoding.** Inputs are probed with ffprobe and MediaInfo, every audio stream is listed with its codec, layout, and duration, and you pick which one to encode.
- **Sixteen encoders in three families.** Eight built into FFmpeg, three standalone command-line encoders, and five DeeZy adapters for licensed Dolby formats.
- **A durable queue.** Jobs survive a restart. Start selected jobs, stop after the current one, retry a failure, or cancel outright.
- **Crash-safe outputs.** Every encode writes to a job-specific `.part` file that is published only after the encoder exits successfully.
- **Delay handling.** Container delays are detected per track; filename markers such as `[DELAY -21ms]` are a fallback for single-track audio-only inputs.
- **Presets**, plus automatic restoration of the last encoder configuration you used.

## What it does not do

**FFmpeg is not bundled.** Neither are the optional encoders. The application detects what is installed and disables what is missing rather than failing at encode time; see [Required and optional tools](tools.md).

The application does not transcode video, mux into video containers, or edit metadata. It encodes one audio stream to one audio file.

## Getting help

`Help ▸ Copy diagnostics` puts a summary of the detected toolchain on the clipboard, and `ffmpeg-audio-encoder --diagnostics` prints the same information as JSON. Attach one of those to any [issue you open](https://github.com/jessielw/FFMPEG-Audio-Encoder/issues/new/choose).

!!! info "Still on v4?"

    The Tkinter application remains available in the repository under `legacy_v4`, and its
    documentation is the [project wiki](https://github.com/jessielw/FFMPEG-Audio-Encoder/wiki).
    Nothing here applies to it.
