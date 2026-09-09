# Required and optional tools

The application drives external programs. Only FFmpeg is required; every other tool unlocks a family of encoders and is treated as absent-but-fine when it is not installed.

## What each tool gives you

| Tool | Required | Unlocks |
| --- | --- | --- |
| `ffmpeg` | **Yes** | All encoding. Also decodes source audio for the standalone encoders. |
| `ffprobe` | **Yes** | Stream inspection - codec, layout, duration, per-stream selection. |
| `opusenc` | No | The standalone [opusenc](encoders/reference.md#opusenc-standalone-opus) adapter. |
| `qaac` | No | [Apple AAC](encoders/reference.md#qaac-apple-aac). Also needs a working Apple CoreAudioToolbox installation. |
| `fdkaac` | No | [Fraunhofer FDK AAC](encoders/reference.md#fdkaac-fraunhofer-fdk-aac). |
| `deezy` | No | The five [DeeZy](encoders/deezy.md) Dolby adapters. |
| `dee` | No | Dolby Encoding Engine. Required by every DeeZy adapter. |
| `truehdd` | No | Required by the DeeZy Atmos and AC-4 adapters only. |

MediaInfo ships with the application through `pymediainfo` and needs no installation. It supplies the per-track container delays described in [Audio controls](audio-controls.md).

## How tools are found

Discovery runs asynchronously at startup and again whenever you change a path in [Settings](settings.md). For each tool, in order:

1. **The path configured in Settings**, if you set one. A configured path that does not point at a file is an error rather than a silent fallback.
2. **`PATH`.** `qaac` is looked up as `qaac64` first, then `qaac`.
3. **DeeZy's own layout - `dee` and `truehdd` only.** These can ship beside DeeZy rather than on `PATH`, so if neither of the above found them the application looks in `apps/dee/` and `apps/truehdd/` next to the DeeZy executable. DeeZy will also look for those dependencies on it's own via the system PATH.

If FFmpeg or ffprobe cannot be resolved, the application reports the failure rather than starting in a half-working state. Every other tool simply comes back as unavailable, and the encoders that need it are shown as unavailable too.

## Capability detection, not just presence

Finding `ffmpeg` on disk is not enough. The application asks the configured FFmpeg build which encoders and muxers it actually exposes, and an adapter is offered only when its `required_ffmpeg_encoders` and `required_ffmpeg_muxers` are all present.

This is why a distribution FFmpeg without `libopus` or `libmp3lame` shows those encoders greyed out instead of failing partway through a job.

## Checking what was found

`Help ▸ Copy diagnostics` puts a readable summary on the clipboard. For the machine-readable form, run the executable with `--diagnostics`:

=== "Windows"

    ```console
    .\FFMPEGAudioEncoder\FFMPEGAudioEncoder.exe --diagnostics
    ```

=== "macOS"

    ```console
    ./FFMPEGAudioEncoder.app/Contents/MacOS/FFMPEGAudioEncoder --diagnostics
    ```

=== "Linux"

    ```console
    ./FFMPEGAudioEncoder/FFMPEGAudioEncoder --diagnostics
    ```

=== "From source"

    ```console
    uv run ffmpeg-audio-encoder --diagnostics
    ```

It prints JSON and exits without opening the interface. See [Troubleshooting](troubleshooting.md#reading-the-diagnostics-report) for what each field means.

## Installing the optional encoders

None of these are distributed by this project.

- **opusenc** is part of `opus-tools`, packaged by most distributions and available for Windows from the Xiph downloads.
- **qaac** is Windows-only and needs Apple's CoreAudioToolbox alongside it. The availability check runs qaac at startup, so a qaac that cannot find CoreAudioToolbox is reported as unavailable rather than failing mid-encode.
- **fdkaac** is the Fraunhofer FDK AAC command-line front end.
- **DeeZy** requires a licensed Dolby Encoding Engine, and TrueHDD for Atmos and AC-4. Point Settings at `deezy` and the rest of the toolchain is usually found automatically through the `apps/` layout described above.
