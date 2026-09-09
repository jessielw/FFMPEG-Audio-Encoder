# Building bundles

Releases ship as PyInstaller one-folder bundles, one per platform. There is no installer and no code signing.

## Locally

```console
uv sync --group build
uv run python build.py
```

`build.py` prints the path of what it produced:

| Platform | Output                                           |
| -------- | ------------------------------------------------ |
| Windows  | `dist/FFMPEGAudioEncoder/FFMPEGAudioEncoder.exe` |
| Linux    | `dist/FFMPEGAudioEncoder/FFMPEGAudioEncoder`     |
| macOS    | `dist/FFMPEGAudioEncoder.app`                    |

You must build on the platform you are targeting; PyInstaller does not cross-compile.

## What build.py does

It drives PyInstaller with `--onedir --windowed`, adding:

- `--collect-all qtawesome` and `--collect-all pymediainfo`, both of which carry data files the analysis does not find on its own;
- `--collect-data ffmpeg_audio_encoder`, which carries the packaged icon into the bundle where the runtime reads it back out of `ffmpeg_audio_encoder/resources`;
- `--icon` on Windows and macOS only. Linux executables carry no embedded icon, so PyInstaller ignores it there. On macOS the `.ico` is converted to `.icns`, which is why Pillow is in the `build` group.

It then checks that the expected bundle actually exists and raises if not, so a PyInstaller run that exits 0 without producing anything is still a failure.

## Smoke checks

Both CI and the release workflow run the built binary before going any further:

```console
FFMPEGAudioEncoder --version
FFMPEGAudioEncoder --diagnostics
```

That is the cheapest possible check that the bundle starts and can find its toolchain. It is in the release workflow specifically so a tag can never publish a bundle that cannot launch.

## CI

`.github/workflows/ci.yml` has two jobs:

- **`quality`** - Ubuntu, twice over an `ffmpeg: [distro, latest]` matrix, running ruff, basedpyright, and pytest. See [Development setup](setup.md#a-note-on-cis-ffmpeg-matrix) for why both.
- **`bundle`** - Windows, Ubuntu, macOS Intel, and macOS Apple silicon. Builds and smoke tests the bundle, then uploads it as an artifact. It runs on pull requests and on pushes to `main`, `master`, and `v5`.

Both use `astral-sh/setup-uv@v6` with Python 3.12 and caching, and set `QT_QPA_PLATFORM=offscreen`.

## Releasing

`.github/workflows/release.yml` triggers on a version tag - both the bare-numeric form this project has always used (`5.0.0`) and a `v`-prefixed one.

For each of the four platforms it builds, smoke tests, and archives the bundle as `FFMPEGAudioEncoder-<tag>-<slug>`:

| Platform | Slug | Archive method |
| --- | --- | --- |
| Windows | `windows-x64` | `7z a -tzip` |
| Linux | `linux-x64` | `tar -czf` |
| macOS Intel | `macos-x64` | `ditto -c -k --sequesterRsrc --keepParent` |
| macOS Apple silicon | `macos-arm64` | `ditto` |

macOS uses `ditto` rather than `zip` because it preserves the bundle's symlinks and resource forks.

A second job collects all four and creates a **draft** release with generated notes. The draft is deliberate: you review and publish it by hand.

!!! note "Publishing the release is what deploys the docs"

    The [documentation workflow](docs.md#deployment) triggers on a published release, not
    on the tag. Drafting a release builds bundles; publishing it puts the docs live.

## Version numbers

The version lives in one place, `src/ffmpeg_audio_encoder/__init__.py`:

```python
__version__ = "5.0.0"
```

Hatchling reads it from there, and `--version` prints it. Update it, update `CHANGELOG.md`, then tag.
