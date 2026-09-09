# Settings

`Edit ▸ Settings…` (++ctrl+comma++), or the **Settings** button beside the input list.

Changes take effect when you press **Save**. Tool detection re-runs immediately, so an encoder you have just pointed at becomes available without a restart.

## Tool paths

| Row | What it points at |
| --- | --- |
| **FFmpeg** | The `ffmpeg` executable. Required. |
| **ffprobe** | The `ffprobe` executable. Required. |
| **qaac** | Apple AAC encoder. Also needs CoreAudioToolbox installed. |
| **fdkaac** | Fraunhofer FDK AAC encoder. |
| **opusenc** | Standalone Opus encoder, part of `opus-tools`. |
| **DeeZy** | The DeeZy executable. |
| **Dolby Encoding Engine** | `dee`. Usually found beside DeeZy automatically. |
| **TrueHDD** | `truehdd`. Usually found beside DeeZy automatically. Needed for Atmos and AC-4. |

**Leave a row empty to use `PATH`.** An empty row is the normal case - you only need to fill one in when the tool is not on `PATH`, or when you want a specific build rather than whichever one `PATH` finds first.

A path you set must point at a real file. Unlike an empty row, a configured path that does not resolve is reported as an error rather than falling back to `PATH` - otherwise a typo would look like it worked while silently running a different binary.

See [Required and optional tools](tools.md#how-tools-are-found) for the full discovery order, including how `dee` and `truehdd` are located inside DeeZy's own `apps/` layout.

## Default output folder

Where generated output paths are placed. Leave it empty to put outputs beside their input file.

This sets the starting point only; the output path stays editable per job on the **Output** tab.

## Appearance

**Automatic**, **Light**, or **Dark**. Automatic follows the operating system, and switches live when the system theme changes. Icons are re-tinted to match, so neither theme leaves you with invisible toolbar glyphs.

## Overwrite

_Allow queued jobs to replace existing outputs._

This is the **default** for the **Collision policy** checkbox on the **Output** tab, not an override. With it off, a generated output name that collides with an existing file is numbered automatically instead of replacing it.

You can still tick or untick the per-job checkbox for any individual job.

## What else is remembered

Beyond this dialog, the application persists your window position and size, whether it was maximised, the splitter positions, the last folder you added files from, and the last encoder configuration you used. These are saved automatically - there is nothing to configure.

All of it lives in `settings.json`; see [Files and locations](files.md).
