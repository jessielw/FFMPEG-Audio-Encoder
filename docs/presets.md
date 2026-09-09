# Presets

A preset stores a whole encoder configuration under a name, so a setup you use often is one selection away.

Presets live on the **Output** tab.

## What a preset holds

| Stored | Not stored |
| --- | --- |
| The encoder | The input file |
| Codec and container | The selected audio stream |
| Sample rate and channel layout | The output path |
| Gain, tempo, and delay | Collision policy |
| Every adapter-specific option, including custom FFmpeg arguments | Tool paths and other [settings](settings.md) |

A preset is a _configuration_, not a job. It describes how to encode, never what to encode or where to put it.

!!! note "Delay is stored, and delay is detected"

    A preset carries whatever delay value was set when you saved it. Selecting a track with
    a detected delay overwrites that. If you save a preset while a detected delay is in the
    field, you are baking that specific file's delay into the preset - usually not what you
    want, so set the field back to 0 first.

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
