# FFmpeg Audio Encoder v5

This branch contains a clean PySide6 successor to the original Tkinter application. The
maintained legacy source remains available in [`legacy_v4`](legacy_v4/README.md).

## Development

```console
uv sync --group dev
uv run ffmpeg-audio-encoder
```

Install FFmpeg and ffprobe on `PATH`, or select their executables in application settings.
Optional opusenc, qaac, fdkaac, and DeeZy executables can also be found on `PATH` or
selected in settings. DeeZy adapters additionally require Dolby Encoding Engine (DEE);
Atmos and AC-4 require TrueHDD. The DeeZy toolchain is resolved from `PATH` first, then
from DeeZy's conventional `apps/dee` and `apps/truehdd` folders beside `deezy.exe`, and
finally from the paths configured in settings.

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

Standalone Opus and AAC adapters are also available:

| Adapter | Profiles / modes | Output |
| --- | --- | --- |
| opusenc | VBR, constrained VBR, or hard CBR; music/speech tuning | Ogg Opus |
| qaac (Apple AAC) | AAC-LC or HE-AAC; TVBR, CVBR, ABR, or CBR | M4A or ADTS |
| fdkaac (Fraunhofer FDK AAC) | AAC-LC, HE-AAC, or HE-AAC v2; CBR or VBR | M4A or ADTS |

DeeZy provides licensed Dolby encoding modes:

| Adapter | Target / source constraint | Metering modes | Format-specific controls | Output |
| --- | --- | --- | --- | --- |
| DeeZy DD | Auto, mono, stereo, or 5.1; downmix only, except explicit 5.0-to-5.1 | BS.1770-1/-2/-3, Leq(A) | Standard DRC, dialnorm, downmix, DD processing | AC-3 |
| DeeZy DDP | Auto, mono, stereo, 5.1, or 7.1; downmix only, except explicit 5.0-to-5.1 | BS.1770-1/-2/-3, Leq(A) | Standard DRC, dialnorm, downmix, DDP processing | E-AC-3 |
| DeeZy DDP-BluRay | Fixed 7.1 from an 8-channel source | BS.1770-1/-2/-3, Leq(A) | BluRay bitrates, standard DRC/downmix; no upmix | E-AC-3 |
| DeeZy Atmos | Streaming 5.1 or BluRay 7.1 from a valid Atmos source | BS.1770-1/-2/-3/-4, Leq(A) | Atmos mode, standard DRC/downmix, TrueHDD warp/bed controls | E-AC-3 with Atmos |
| DeeZy AC-4 | Immersive stereo from 6+ channels or TrueHD Atmos | BS.1770-1/-2/-3/-4, Leq(A) | IMS/IMS Music, five AC-4 DRC profiles, TrueHDD warp/bed controls | AC-4 |

The application invokes DeeZy with its clean progress mode, converts DeeZy's numbered
FFmpeg/measurement/encode stage percentages into queue progress, and keeps the plain output
in the job log. The selected stream index, signed delay, dependency paths, and job-specific
temporary output are always passed explicitly. Generic gain, tempo, and sample-rate controls
are disabled for DeeZy because preprocessing can discard immersive metadata. DeeZy's own
configuration remains available for automatic bitrate defaults.

The UI stores readable values, while generated commands use DeeZy's enum *member* names -
`MODE_1770_1` through `MODE_1770_4` and `MODE_LEQA` for metering, `NOT_INDICATED`/`DPLII` for
stereo downmix, `DPLII` for the Pro Logic IIx warp mode. The packaged DeeZy CLI coerces every
enum argument by member name or bare digit and rejects the value spellings printed by its own
help. Dialogue Intelligence and its speech threshold are omitted for BS.1770-1 and Leq(A),
where DEE ignores those settings.

DeeZy runs as a single child process that spawns FFmpeg, TrueHDD, and DEE itself. Those
grandchildren are held in a Windows job object (a process-group walk elsewhere) so cancelling
a job, or DeeZy exiting unexpectedly, cannot leave a TrueHD decode running. DeeZy's
intermediates are redirected to an application cache folder rather than the `<name>_deezy`
folder it would otherwise create beside the source file, and anything a cancelled run leaves
there is removed at startup.

Bitrate is presented as a discrete, configuration-aware list sourced from DeeZy's channel and
profile tables. Changing DD/DDP output layout or the Atmos streaming/BluRay mode immediately
refreshes the list; Automatic leaves DeeZy's configured default in control. The adapter also
rejects stale preset or queue values that are not valid for the selected configuration instead
of allowing DeeZy to silently substitute another bitrate.

External adapters use FFmpeg to decode the selected source stream to PCM over a pipe. opusenc
receives 24-bit WAV while the AAC encoders receive 16-bit WAV. The external encoder writes
directly to the queue's temporary output, preserving the same atomic publish, cancellation, and
progress behavior as the internal FFmpeg adapters. qaac also requires a working Apple
CoreAudioToolbox installation; its startup check determines availability.

Each adapter exposes curated rate-control and quality settings plus codec-aware channel layouts.
Common audio controls include gain, tempo, and a signed millisecond delay: positive delay prepends
silence and negative delay trims the beginning before encoding.
Container delays are detected per audio track with the bundled MediaInfo library. For single-track
audio-only inputs, case-insensitive filename markers such as `[DELAY -21ms]` are detected instead.
The detected value remains editable and is baked into the encoded samples; filename-derived delay
markers are removed from automatically generated output names.
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
