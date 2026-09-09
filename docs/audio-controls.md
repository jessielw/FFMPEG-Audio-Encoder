# Audio controls

The **General** tab carries the controls that apply regardless of which encoder you pick. Not every encoder honours all of them - the [encoder reference](encoders/reference.md) says which apply to each, and the DeeZy adapters disable most of them deliberately.

## Sample rate and channel layout

Both default to **Preserve**, meaning the source value is carried through untouched.

The choices offered are the encoder's, not a generic list: `ffmpeg.libopus` offers Opus's five rates, `ffmpeg.libmp3lame` offers MP3's nine, and the layouts are similarly restricted to what the codec can actually represent.

The [DeeZy adapters](encoders/deezy.md) go further and reject layouts that would require an upmix, since Dolby encoding treats that as a different operation entirely.

## Gain

−30 to +30 dB, in 0.5 dB steps, applied by FFmpeg before the encoder sees the audio. Leave it at 0 dB unless you have a reason.

## Tempo

0.25× to 4×. This changes duration without changing pitch. As with gain, it is applied during decode, so it is unavailable for the DeeZy adapters.

## Audio delay

The delay field takes a signed value in milliseconds, and it is applied by editing the samples rather than by writing a container offset:

- **Positive** - prepend that much silence.
- **Negative** - trim that much from the beginning.

The application detects a starting value per track and shows where it came from in the line beneath the field. The value stays editable; detection is a suggestion, not a lock.

### Container delays

For inputs that contain video, the bundled MediaInfo library reports each audio track's delay relative to the reference video track. This is the normal case for a file demuxed from a Blu-ray or a broadcast capture, where the audio genuinely starts at a different point from the picture.

Detection is per track, so switching **Audio stream** updates the delay. When MediaInfo cannot match its track list to the ffprobe stream list unambiguously, the status line says so and the field stays at zero rather than guessing.

### Filename markers

For **single-track, audio-only** inputs there is no video to measure against, so the filename is used instead. A marker is recognised in three shapes, case-insensitively:

| Shape         | Example                    |
| ------------- | -------------------------- |
| Bracketed     | `Track [DELAY -21ms].ac3`  |
| Parenthesised | `Track (delay 120 ms).ac3` |
| Bare          | `Track delay_-21ms.ac3`    |

The separator between `delay` and the number can be whitespace, `_`, `.`, `:`, or `=`. The number may be signed and fractional.

Two rules keep this from misfiring:

- **Exactly one marker** must be present. A filename containing two is ignored entirely.
- The value must be finite and no larger than 24 hours (86,400,000 ms).

When a marker is used, it is **stripped from the generated output name** - the delay has been baked into the samples, so carrying the marker forward would be a lie about the new file. Leftover separator runs are tidied up, so `Track [DELAY -21ms].ac3` becomes `Track.opus` rather than `Track -.opus`.

## Custom FFmpeg output arguments

Most FFmpeg adapters expose a **Custom FFmpeg output arguments** text field at the bottom of their **Options** tab, for the occasional flag the curated options do not cover - `-cutoff 18000`, for instance.

Two things to know:

- The field is **parsed into an argument list and never run through a shell**. Shell metacharacters are not interpreted, so quoting behaves like a command line, not like `bash`.
- Managed progress, muxer, and output arguments stay under the application's control. Your arguments are appended after the codec settings; they cannot redirect the output or break progress parsing.

The field is saved in [presets](presets.md) along with everything else.
