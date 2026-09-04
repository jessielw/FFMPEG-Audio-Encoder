# FFmpeg Audio Encoder v5

This branch contains a clean PySide6 successor to the original Tkinter application. The
maintained legacy source remains available in [`legacy_v4`](legacy_v4/README.md).

## Development

```console
uv sync --group dev
uv run ffmpeg-audio-encoder
```

Install FFmpeg and ffprobe on `PATH`, or select their executables in application settings.
Optional qaac and fdkaac executables can also be found on `PATH` or selected in settings.

The PySide6 application includes:

- drag-and-drop input, stream inspection, and per-stream encoding;
- presets plus automatic restoration of the last encoder configuration;
- sample-rate, channel-layout, gain, and tempo controls;
- a durable queue with selected-job starts, stop-after-current, retry, cancellation, and
  crash-safe temporary outputs;
- live per-job progress, command/error details, bounded session logs, and output-folder actions;
- asynchronous tool detection, bounded media probing, rotating application logs, and
  single-instance protection.

```console
uv run ruff format --check .
uv run ruff check .
uv run basedpyright
uv run pytest
uv run ffmpeg-audio-encoder --diagnostics
```

Build a native one-folder application bundle with `uv sync --group build` followed by
`uv run python build.py`.

FFmpeg and third-party encoders are intentionally not bundled. The application detects the
encoders and muxers exposed by the configured FFmpeg build and disables unavailable choices.

| Codec | FFmpeg encoder | Output |
| --- | --- | --- |
| Opus | `libopus` | Ogg Opus (`.opus`) |
| FLAC | `flac` | FLAC (`.flac`) |
| AAC | `aac` | M4A (`.m4a`) or ADTS (`.aac`) |
| MP3 | `libmp3lame` | MP3 (`.mp3`) |
| AC-3 | `ac3` | Raw AC-3 (`.ac3`) |
| E-AC-3 | `eac3` | Raw E-AC-3 (`.eac3`) |
| DTS | `dca` | Raw DTS (`.dts`) |
| ALAC | `alac` | M4A (`.m4a`) |

Two external AAC adapters are also available:

| Adapter | Profiles / modes | Output |
| --- | --- | --- |
| qaac (Apple AAC) | AAC-LC or HE-AAC; TVBR, CVBR, ABR, or CBR | M4A or ADTS |
| fdkaac (Fraunhofer FDK AAC) | AAC-LC, HE-AAC, or HE-AAC v2; CBR or VBR | M4A or ADTS |

External adapters use FFmpeg to decode the selected source stream to PCM over a pipe. The
external encoder writes directly to the queue's temporary output, preserving the same atomic
publish, cancellation, and progress behavior as the internal FFmpeg adapters. qaac also requires
a working Apple CoreAudioToolbox installation; its startup check determines availability.

Each adapter exposes curated rate-control and quality settings plus codec-aware channel layouts.
Common audio controls include gain, tempo, and a signed millisecond delay: positive delay prepends
silence and negative delay trims the beginning before encoding.
The custom FFmpeg output-arguments field is saved in presets and is parsed into an argument list;
it is never executed through a shell. Managed progress, muxer, and output arguments remain under
application control.

The encoding queue is saved atomically to a versioned `jobs.json` file in the application
configuration directory. Queued jobs remain paused after restart. A job that was running when
the application exited is restored as failed so it can be reviewed and retried safely. Corrupt
settings, preset, and queue files are renamed with a `corrupt-<timestamp>` suffix instead of
being overwritten.

Outputs are encoded to job-specific `.part` files and published atomically only after a
successful encode. The application rejects source/output self-overwrites and duplicate active
destinations; generated destination-name collisions are numbered automatically.

## Legacy v4

The original program depends on working-directory-relative paths:

```console
cd legacy_v4
uv sync
uv run python FFMPEGAudioEncoder.py
```
