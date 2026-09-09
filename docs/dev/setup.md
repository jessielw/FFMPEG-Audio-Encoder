# Development setup

The project uses [uv](https://docs.astral.sh/uv/). Python 3.11 to 3.14 is supported; `.python-version` pins 3.12 for local work and CI.

```console
git clone https://github.com/jessielw/FFMPEG-Audio-Encoder.git
cd FFMPEG-Audio-Encoder
uv sync --group dev
uv run ffmpeg-audio-encoder
```

You need FFmpeg and ffprobe on `PATH`, or configured in application settings. The optional encoders are optional here too - see [Required and optional tools](../tools.md).

## Dependency groups

| Group | Contents | Sync with |
| --- | --- | --- |
| `dev` (default) | ruff, basedpyright, pytest, pytest-qt, pytest-timeout | `uv sync --group dev` |
| `build` | PyInstaller, Pillow, setuptools | `uv sync --group build` |
| `docs` | Zensical | `uv sync --group docs` |

`dev` is uv's default group, so `uv sync --group docs` gives you dev **and** docs. Use `--only-group docs` when you want Zensical alone - that is what the docs workflow does, and it will uninstall your dev tools if you run it against a shared local environment.

## Quality checks

The same four commands CI runs, in the same order:

```console
uv run ruff format --check .
uv run ruff check .
uv run basedpyright
uv run pytest
```

`ruff format` (without `--check`) applies the formatting. Line length is 100.

basedpyright runs in `standard` mode overall, and **`strict` for `src/ffmpeg_audio_encoder/domain` and `src/ffmpeg_audio_encoder/encoders`** - the two layers that carry no Qt and no I/O.

CI additionally checks that the generated encoder reference is current:

```console
uv run python tools/generate_encoder_reference.py --check
```

## Tests

```console
uv run pytest                      # everything
uv run pytest tests/test_queue.py  # one file
uv run pytest -k deezy             # by name
```

Tests time out after 60 seconds each, enforced on a thread. UI tests use `pytest-qt`; set `QT_QPA_PLATFORM=offscreen` if you are running headless, as CI does.

The integration tests (`test_integration_ffmpeg.py`, `test_integration_external.py`) invoke real encoders and skip when the tool is unavailable.

## Running the application

```console
uv run ffmpeg-audio-encoder
uv run ffmpeg-audio-encoder --version
uv run ffmpeg-audio-encoder --diagnostics
```

Unrecognised arguments are forwarded to `QApplication`, so Qt's own flags work:

```console
uv run ffmpeg-audio-encoder -platform offscreen
```

## A note on CI's FFmpeg matrix

The `quality` job runs twice: once against the distribution FFmpeg and once against a current static build. That is not redundancy. An ffmpeg 9 filter regression got past every green run when only the distribution build was tested, and was not caught until a release tag built on macOS and Windows, whose package managers ship the newer ffmpeg.

If you touch filter-graph construction, expect both to matter.

## Next

- [Architecture](architecture.md) - how the layers fit together
- [Adding an encoder](adding-an-encoder.md)
- [Building bundles](building.md)
- [Working on the docs](docs.md)
