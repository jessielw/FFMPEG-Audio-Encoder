# Troubleshooting

## Start here: the diagnostics report

Almost every "why is this not working" question is answered by the toolchain report.

`Help ▸ Copy diagnostics` puts a readable summary on the clipboard. For the full, machine-readable version, run the executable with `--diagnostics`:

```console
ffmpeg-audio-encoder --diagnostics
```

It prints JSON and exits without opening the interface. See [Required and optional tools](tools.md#checking-what-was-found) for the exact command on each platform.

### Reading the diagnostics report

```json
{
  "ok": true,
  "ffmpeg": "/usr/bin/ffmpeg",
  "ffprobe": "/usr/bin/ffprobe",
  "ffmpeg_version": "...",
  "ffprobe_version": "...",
  "mediainfo_available": true,
  "qaac": null,
  "qaac_version": null,
  "fdkaac": null,
  "fdkaac_version": null,
  "opusenc": "/usr/bin/opusenc",
  "opusenc_version": "...",
  "deezy": null,
  "deezy_version": null,
  "dee": null,
  "dee_version": null,
  "truehdd": null,
  "truehdd_version": null,
  "encoders": { "ffmpeg.libopus": true, "deezy.dd": false },
  "muxers": ["ac3", "flac", "ipod", "..."]
}
```

| Field | Means |
| --- | --- |
| `ok` | Whether the required toolchain resolved at all |
| `<tool>` | Resolved absolute path, or `null` when not found |
| `<tool>_version` | What the tool reported when asked. `null` with a non-null path means it was found but would not run |
| `mediainfo_available` | Whether the bundled MediaInfo library loaded - this drives [delay detection](audio-controls.md#container-delays) |
| `encoders` | Every adapter id mapped to whether it is currently usable |
| `muxers` | The output muxers the configured FFmpeg exposes |

When the required tools cannot be resolved, the output is instead:

```json
{ "ok": false, "error": "ffmpeg was not found on PATH" }
```

### Exit codes

| Code | Meaning                                                  |
| ---- | -------------------------------------------------------- |
| `0`  | Normal exit, or a successful `--diagnostics` run         |
| `1`  | `--diagnostics` could not resolve the required toolchain |
| `2`  | Another instance is already running                      |

## Common problems

### An encoder is greyed out

Look at the `encoders` map in the diagnostics report. An adapter is offered only when **both** its external tools are present **and** the configured FFmpeg exposes the encoders and muxers it needs.

So `ffmpeg.libopus` being `false` with a working FFmpeg means that FFmpeg build was compiled without `libopus` - check the `muxers` list and `ffmpeg -encoders` output. Point [Settings](settings.md) at a fuller build, or install one.

### "Another instance is already running"

The application holds a single-instance lock (`application.lock` in the [configuration directory](files.md)). Close the other window.

If no other window exists, a previous run was killed hard and left the lock behind. Delete `application.lock` and start again.

### qaac is installed but reported unavailable

qaac needs a working Apple CoreAudioToolbox installation, and the availability check actually runs qaac at startup. A qaac that cannot load CoreAudioToolbox is reported as unavailable rather than being offered and then failing mid-encode.

Check `qaac_version` in the diagnostics report: a non-null `qaac` path with a `null` version is exactly this case.

### A DeeZy encoder is unavailable

Every DeeZy adapter needs `deezy` **and** `dee`. Atmos and AC-4 additionally need `truehdd`. All three appear separately in the diagnostics report.

`dee` and `truehdd` are normally found beside the DeeZy executable in `apps/dee/` and `apps/truehdd/`. If DeeZy resolved but `dee` did not, either that layout is missing or DeeZy itself was found somewhere without it - set the path explicitly in [Settings](settings.md).

### Delay is not detected

`mediainfo_available` must be `true`. Beyond that:

- **Container delay detection needs video.** An audio-only input has nothing to measure against, so the [filename marker](audio-controls.md#filename-markers) path is used instead - and only for single-track files.
- The status line under the delay field says what happened. _MediaInfo track matching was ambiguous_ means the track lists could not be lined up confidently, so no value was guessed.
- A filename marker is ignored when there is more than one in the name.

### A job failed and I want to know why

Select it in the queue and read the **Selected job** tab, which carries the exact command and the encoder's error. **Copy command** on the right-click menu gives you something you can paste into a terminal to reproduce it directly.

### The output file is missing but the job succeeded

Check whether the destination was numbered. With **Replace an existing file** off, a collision produces `name (1).opus` rather than replacing `name.opus`.

### `.part` files left behind

A `.part` file next to your output is the remains of a crashed or cancelled encode. They are safe to delete. The real output is only ever published by renaming a `.part` file after a successful encode, so a leftover one is never a valid result.

### The application crashed

`application.log` in the [configuration directory](files.md) has the traceback, and the error dialog names the path. The log rotates at 1 MB with three backups, so the relevant entry may be in `application.log.1`.

## Reporting an issue

`Help ▸ Report an issue`, or [open one directly](https://github.com/jessielw/FFMPEG-Audio-Encoder/issues/new/choose).

Include the `--diagnostics` output (or `Help ▸ Copy diagnostics`), what you were encoding, and the command from the failing job's **Selected job** tab. That is usually enough to diagnose without a back-and-forth.
