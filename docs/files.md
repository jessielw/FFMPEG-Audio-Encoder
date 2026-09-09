# Files and locations

Everything the application persists lives outside its own folder, so replacing the bundle never disturbs your settings, presets, or queue.

## Configuration directory

| Platform | Path                                               |
| -------- | -------------------------------------------------- |
| Windows  | `%LOCALAPPDATA%\FFmpegAudioEncoder`                |
| macOS    | `~/Library/Application Support/FFmpegAudioEncoder` |
| Linux    | `~/.config/FFmpegAudioEncoder`                     |

Contents:

| File | Holds |
| --- | --- |
| `settings.json` | Tool paths, default output folder, theme, overwrite default, window geometry, splitter positions, last input folder, last encoder configuration |
| `presets.json` | Your saved [presets](presets.md) |
| `jobs.json` | The [encoding queue](queue.md) |
| `application.log` | The rotating application log |
| `application.lock` | Single-instance lock, held while the application runs |

## Cache directory

| Platform | Path                                      |
| -------- | ----------------------------------------- |
| Windows  | `%LOCALAPPDATA%\FFmpegAudioEncoder\Cache` |
| macOS    | `~/Library/Caches/FFmpegAudioEncoder`     |
| Linux    | `~/.cache/FFmpegAudioEncoder`             |

This holds `deezy-work/` and `deezy-temp/`, where DeeZy's intermediates are redirected. Left to itself, DeeZy writes those beside your source file in a `<name>_deezy` folder; sending them here keeps them out of your media library. Anything a cancelled run leaves behind is pruned at startup.

Atmos and AC-4 intermediates are the size of the decoded source track, so this directory can get large mid-job. It is safe to delete when the application is not running.

## Logging

`application.log` uses a rotating handler: 1 MB per file, three backups kept (`application.log.1` through `.3`). Unhandled exceptions are written here with a full traceback, and the dialog that reports one names this path.

This is separate from the **Session log** tab in the queue panel, which is in-memory, bounded to 3,000 lines, and gone when you close the application.

## Atomic writes

`settings.json`, `presets.json`, and `jobs.json` are all written the same way: serialise to a temporary file in the same directory, then rename it over the target. A crash or a power loss mid-write leaves the previous file intact rather than a half-written one.

## Corrupt files are quarantined

If one of those files cannot be parsed, it is **renamed** to `<name>.corrupt-<timestamp>.<ext>` and the application carries on with defaults. It is never overwritten in place.

So a `presets.corrupt-20260908T142233123456Z.json` sitting next to `presets.json` means your presets failed to load and the original is still there to look at. Editing one of these files by hand and getting the JSON wrong is the usual cause.

## Schema versions

Each file records a schema version - settings 3, presets 2, jobs 1 at the time of writing. A file written by a newer version than the application understands is treated as unreadable and defaults are used, rather than being misread.

## Moving to another machine

Copy `settings.json` and `presets.json`. Tool paths inside `settings.json` are absolute, so clear them (or fix them) if the target machine puts FFmpeg somewhere else - or just leave them empty and rely on `PATH`.

Copying `jobs.json` is possible but rarely useful, since it references input and output paths that likely differ.
