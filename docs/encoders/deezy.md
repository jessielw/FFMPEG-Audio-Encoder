# DeeZy encoders

The five DeeZy adapters - DD, DDP, DDP-BluRay, Atmos, and AC-4 - drive licensed Dolby encoding. They behave differently from the other adapters in several ways worth understanding before you use them.

Their options are in the [encoder reference](reference.md#deezy-dolby-professional).

## What you need

| Adapter             | Needs                       |
| ------------------- | --------------------------- |
| DD, DDP, DDP-BluRay | `deezy` + `dee`             |
| Atmos, AC-4         | `deezy` + `dee` + `truehdd` |

`dee` and `truehdd` normally ship beside DeeZy rather than on `PATH`, so the application looks for them in `apps/dee/` and `apps/truehdd/` next to the DeeZy executable when neither a configured path nor `PATH` turns them up. See [Required and optional tools](../tools.md#how-tools-are-found).

## Generic audio controls are disabled

Sample rate, gain, and tempo are unavailable for every DeeZy adapter. This is deliberate: those controls are implemented as FFmpeg preprocessing, and preprocessing the audio can discard the immersive metadata the Dolby encoders depend on.

Delay still applies. Channel layout applies to DD and DDP only - DDP-BluRay, Atmos, and AC-4 have fixed or source-determined layouts.

## Layout rules

DeeZy downmixes; it does not upmix. The adapters enforce that rather than letting DeeZy substitute something:

- **DD** - auto, mono, stereo, or 5.1. Downmix only, with an explicit exception for 5.0-to-5.1.
- **DDP** - auto, mono, stereo, 5.1, or 7.1. Same downmix rule.
- **DDP-BluRay** - fixed 7.1, and requires an 8-channel source.
- **Atmos** - streaming 5.1 or BluRay 7.1, from a valid Atmos source.
- **AC-4** - immersive stereo, from a 6-or-more-channel source or TrueHD Atmos.

## Bitrate is a configuration-aware list

Bitrate is not a free number. It is a discrete list sourced from DeeZy's own channel and profile tables, and it changes as you change the configuration - switching the DD/DDP output layout, or the Atmos streaming/BluRay mode, refreshes it immediately.

**Automatic** leaves DeeZy's configured default in control.

The adapter also rejects a stale bitrate carried in from a [preset](../presets.md) or a restored queue job when it is not valid for the current configuration, rather than allowing DeeZy to quietly substitute another one.

## Metering and Dialogue Intelligence

All five adapters offer BS.1770-1 through -3 and Leq(A); Atmos and AC-4 add BS.1770-4.

**Dialogue Intelligence** and its **Speech threshold** are only shown where they do something. DEE ignores both under BS.1770-1 and under Leq(A), so the adapter hides them for those modes instead of presenting controls that have no effect.

## Enum spellings

This is the detail most likely to confuse anyone comparing generated commands against DeeZy's own `--help`.

The interface stores readable values, but generated commands use DeeZy's enum **member** names:

| Setting | Member name passed |
| --- | --- |
| Metering | `MODE_1770_1`, `MODE_1770_2`, `MODE_1770_3`, `MODE_1770_4`, `MODE_LEQA` |
| Stereo downmix | `NOT_INDICATED`, `DPLII` |
| Pro Logic IIx warp mode | `DPLII` |

The packaged DeeZy CLI coerces every enum argument by member name or bare digit, and **rejects the value spellings printed by its own help**. So the command preview showing `MODE_1770_3` where the help says `1770_3` is correct, not a bug.

## Process containment

DeeZy runs as a single child process that itself spawns FFmpeg, TrueHDD, and DEE. Killing the process this application started would leave those grandchildren running - a TrueHD decode can keep a core busy for a long time on its own.

So the whole tree is owned:

- **On Windows**, by a job object created with `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`. That covers the case a `taskkill /T` cannot: when DeeZy exits on its own while a grandchild is still working, closing the job handle still takes the survivors with it.
- **On POSIX**, by enumerating descendants with `ps` at kill time. This is best effort - once the root has exited, its children are reparented and can no longer be identified.

Cancelling a job, or DeeZy exiting unexpectedly, therefore cannot leave a TrueHD decode running.

## Scratch files

Left alone, DeeZy writes its intermediates into a `<name>_deezy` folder beside your source file. The application redirects them to `deezy-work/` and `deezy-temp/` in the [cache directory](../files.md#cache-directory) instead, and prunes whatever a cancelled run left behind at startup.

Atmos and AC-4 intermediates are the size of the decoded source track, so expect that directory to get large during a job.

## Progress

DeeZy is invoked in its clean progress mode. Its numbered FFmpeg, measurement, and encode stage percentages are converted into overall queue progress, and the plain output is kept in the job log. A DeeZy job's progress bar therefore moves through its real stages rather than jumping from 0 to 100.

## What is always passed explicitly

The selected stream index, the signed delay, the dependency paths, and a job-specific temporary output are passed to DeeZy on every invocation rather than relying on its defaults. DeeZy's own configuration file remains in play for automatic bitrate defaults.
