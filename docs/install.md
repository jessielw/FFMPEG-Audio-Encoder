# Install

## Download a bundle

Grab the archive for your platform from the [latest release](https://github.com/jessielw/FFMPEG-Audio-Encoder/releases/latest).

| Platform              | Archive                                         |
| --------------------- | ----------------------------------------------- |
| Windows (x64)         | `FFMPEGAudioEncoder-<version>-windows-x64.zip`  |
| macOS (Intel)         | `FFMPEGAudioEncoder-<version>-macos-x64.zip`    |
| macOS (Apple silicon) | `FFMPEGAudioEncoder-<version>-macos-arm64.zip`  |
| Linux (x64)           | `FFMPEGAudioEncoder-<version>-linux-x64.tar.gz` |

Unpack the archive anywhere and run `FFMPEGAudioEncoder` from inside it. Nothing is installed system-wide and no Python runtime is required - the bundle carries its own.

=== "Windows"

    Unzip and run `FFMPEGAudioEncoder\FFMPEGAudioEncoder.exe`.

=== "macOS"

    Unzip and open `FFMPEGAudioEncoder.app`. Keep the `.app` intact; it is a bundle, not a
    folder to rearrange.

=== "Linux"

    ```console
    tar -xzf FFMPEGAudioEncoder-<version>-linux-x64.tar.gz
    ./FFMPEGAudioEncoder/FFMPEGAudioEncoder
    ```

    The Qt platform plugins need `libegl1` present. On Debian and Ubuntu that is
    `sudo apt install libegl1`.

## Getting past the first launch

The bundles are **unsigned**, so both desktop platforms will stop you the first time.

=== "Windows"

    SmartScreen shows *Windows protected your PC*. Choose **More info**, then
    **Run anyway**.

=== "macOS"

    Gatekeeper refuses a double-click. Right-click the app and choose **Open**, then
    confirm in the dialog. You only need to do this once.

## Install the encoders

The application is a front end; it does not ship the encoders it drives. **FFmpeg and ffprobe are required.** Everything else is optional.

Install FFmpeg and leave it on `PATH`, or point at the executables in [Settings](settings.md). See [Required and optional tools](tools.md) for the full list and how discovery works.

## Run from source instead

If you would rather run the Python application directly, you need [uv](https://docs.astral.sh/uv/) and Python 3.11 or newer:

```console
git clone https://github.com/jessielw/FFMPEG-Audio-Encoder.git
cd FFMPEG-Audio-Encoder
uv sync --group dev
uv run ffmpeg-audio-encoder
```

See [Development setup](dev/setup.md) for the rest of the workflow.

## Upgrading

Bundles are self-contained, so upgrading is unpacking the new archive and deleting the old folder. Your settings, presets, and queue live outside the bundle and are picked up automatically - see [Files and locations](files.md).
