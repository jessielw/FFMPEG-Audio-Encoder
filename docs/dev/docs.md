# Working on the docs

This site is built with [Zensical](https://zensical.org/), the static site generator from the Material for MkDocs team. Sources are in `docs/`, configuration is `zensical.toml`, and the output goes to `site/` (gitignored).

## Preview locally

```console
uv sync --group docs
uv run zensical serve --open
```

That serves on `http://localhost:8000` with live reload. Use `--dev-addr` for a different address.

To check what CI will check:

```console
uv run zensical build --clean --strict
```

`--strict` turns validation warnings - broken internal links, unresolved references - into a failed build. `zensical serve --strict` is currently a no-op that prints a warning, so run `build` when you want the strict pass.

!!! warning "`--only-group docs` will uninstall your dev tools"

    `uv sync --only-group docs` installs Zensical **and nothing else**, which is right for
    a fresh CI runner and wrong for a shared local environment. Locally use
    `--group docs`, which adds Zensical to the default `dev` group.

## Version pinning

Zensical is alpha and uses `0.0.x` versioning, where breaking changes between releases are expected rather than exceptional. `pyproject.toml` therefore pins an exact version:

```toml
docs = ["zensical==0.0.60"]
```

Bump it deliberately, and run `zensical build --strict` after you do.

## The generated page

`docs/encoders/reference.md` is **generated** by `tools/generate_encoder_reference.py` from the encoder descriptors, and it is **gitignored**. The docs build regenerates it every time, so it cannot go stale and there is nothing to keep in sync.

Run it once before previewing locally, or that nav entry will 404:

```console
uv run python tools/generate_encoder_reference.py
uv run zensical serve --open
```

`domain` and `encoders` are stdlib-only, so the generator runs with nothing installed - the CI and deploy jobs use `PYTHONPATH=src` against a Zensical-only environment.

Everything else under `docs/` is written by hand.

## Release notes

`docs/release-notes.md` pulls in the repository's `CHANGELOG.md` with a `pymdownx.snippets` include, so the changelog has exactly one source. Edit `CHANGELOG.md`; the page follows.

## Formatting

Markdown is formatted with prettier, configured with `proseWrap: never`:

```console
npm run format:docs   # docs/**/*.md
npm run format:cl     # CHANGELOG.md
```

`docs/encoders/reference.md` is excluded - see [above](#the-generated-page).

## Adding a page

1. Write the markdown under `docs/`.
2. Add it to `nav` in `zensical.toml` - pages outside `nav` are built but unreachable.
3. `uv run zensical build --clean --strict` to confirm nothing is broken.

## Conventions

- Every page opens with an `#` H1; that title is what `nav` shows for a bare string entry.
- Internal links are relative and include the `.md` extension.
- Keyboard shortcuts use `++ctrl+o++` (`pymdownx.keys`).
- Per-platform instructions use `=== "Windows"` tabs (`pymdownx.tabbed`).
- Callouts use `!!! note` / `!!! warning` (`admonition`).
- The palette is the three-state system / light / dark set, matching the application's own automatic theme.

## Deployment

`.github/workflows/docs.yml` publishes to GitHub Pages at <https://jessielw.github.io/FFMPEG-Audio-Encoder/>. It runs on:

- **`workflow_dispatch`** - a manual run from the Actions tab, for pushing a docs fix without cutting a release;
- **a published release** - so the site tracks what has actually shipped. Note this is _published_, not _tagged_: `release.yml` creates a draft, and the docs go live when you publish it.

The workflow installs `--only-group docs`, runs `zensical build --clean --strict`, and hands `site/` to `actions/upload-pages-artifact` + `actions/deploy-pages`. Zensical has no `gh-deploy` equivalent and its documentation currently recommends against build caching on CI, which is why every run is `--clean`.

There is also a build-only check in `ci.yml` that runs on changes to `docs/`, `zensical.toml`, or `tools/`. Since deploys only happen at release time, that check is what stops a broken link from being discovered during a release.

### One-time repository setup

GitHub Pages must be set to **Source: GitHub Actions** in the repository settings. The workflow cannot set this itself, and `deploy-pages` fails until it is done.

## The in-app link

`Help ▸ Documentation` (++f1++) opens this site, from `src/ffmpeg_audio_encoder/ui/main_window.py`. If the site ever moves, that URL moves with it.
