# Presets

A preset stores a whole encoder configuration under a name, so a setup you use often is one selection away.

Presets live on the **Output** tab.

## What a preset holds

| Stored | Not stored |
| --- | --- |
| The encoder | The input file |
| Codec and container | The selected audio stream |
| Sample rate and channel layout | The output path |
| Gain and tempo | The audio delay |
| Every adapter-specific option, including [custom arguments](custom-arguments.md) and the variables they declare | Collision policy, tool paths, and other [settings](settings.md) |

A preset is a _configuration_, not a job. It describes how to encode, never what to encode or where to put it.

!!! note "Delay is detected, not stored"

    The [audio delay](audio-controls.md#audio-delay) is deliberately left out. It belongs to
    one particular file - it is detected per track, from the container or the filename - so
    carrying one file's delay into a reusable preset would bake in a value that is wrong for
    every other file. Applying a preset leaves the detected value in the field untouched.

    The same applies to the last configuration restored at startup.

What is stored for [time modification](audio-controls.md#time-modification-and-tempo) is the **Tempo** ratio, not the name you picked. Applying the preset looks the ratio back up and shows the matching conversion. A few pairs share a ratio exactly - `25 → 50`, `30 → 60`, `29.97 → 59.94` and `2x speed` are all 2.0 - so one of those may come back under a different name than you chose. The ratio, and therefore the encode, is identical.

## Using them

- **Select** a preset from the list to apply it.
- **Save preset** stores the current configuration. Saving under an existing name replaces it.
- **Delete preset** removes the selected one.

Presets are sorted by name, case-insensitively.

## The last configuration

Separately from presets, the application remembers the encoder configuration you last used and restores it at startup. You do not need to save a preset just to pick up where you left off; presets are for switching between several setups deliberately.

## Stale values are rejected, not substituted

Encoder options are validated when a preset is applied. A value that is not valid for the current configuration is refused rather than quietly replaced with something else.

This matters most for the [DeeZy adapters](encoders/deezy.md), whose valid bitrates depend on the channel layout and mode you have selected. A preset saved for DDP 7.1 does not carry a silently-wrong bitrate into a DD 5.1 job - the adapter rejects it and says so, instead of letting DeeZy substitute a bitrate you did not ask for.

The same applies to a preset naming an encoder that is no longer available: it is reported rather than silently swapped.

## Where they are stored

`presets.json` in the configuration directory, written atomically. A corrupt file is renamed to `<name>.corrupt-<timestamp>.<ext>` and the preset list starts empty rather than being overwritten - see [Files and locations](files.md).

Since it is plain JSON, the file can be copied between machines to move your presets.
