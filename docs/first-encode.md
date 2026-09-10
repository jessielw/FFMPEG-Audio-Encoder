# Your first encode

This walks through one file, start to finish. It assumes FFmpeg is installed and detected - check `Help ▸ Copy diagnostics` if you are not sure.

## The window

The window is two areas split horizontally, with the queue below them:

- **Inputs** on the left - the files you have added and their probe status.
- **Encoding configuration** on the right, with three tabs: **General**, **Options**, and **Output**.
- **Encoding queue** underneath, with its own toolbar and **Selected job** / **Session log** tabs. Toggle it with ++f9++.

## 1. Add an input

Drag files onto the window, press ++ctrl+o++, or use **Add files…**.

Each file is probed in the background with ffprobe and MediaInfo. Probing is bounded, so adding a large batch will not lock up the interface. A file that fails to probe stays in the list with its error rather than disappearing.

## 2. Pick the audio stream

**General ▸ Audio stream** lists every audio stream the probe found, with its codec, channel layout, and language. Multi-track files start on the first stream; pick the one you actually want.

The eye button beside the list opens **Inspect stream** for the full probe detail, and the same action is on the input list's right-click menu.

## 3. Choose an encoder

**General ▸ Encoder** groups the sixteen adapters into **FFmpeg built-in**, **Standalone encoders**, and **DeeZy (Dolby professional)**. Encoders whose tools are missing - or that the configured FFmpeg build does not expose - are shown as unavailable.

**Codec** and **Container** update to match the encoder. Both are read-only: the adapter decides what it can produce. An encoder that can write more than one container (AAC, for instance, writing either `.m4a` or `.aac`) lets you choose between them.

## 4. Set the audio controls

Still on **General**:

| Control | Range | Notes |
| --- | --- | --- |
| Sample rate | `Preserve`, plus the rates the encoder accepts |  |
| Channel layout | `Preserve`, plus the layouts the encoder accepts |  |
| Gain | −30 to +30 dB, in 0.5 dB steps |  |
| Time modification | Framerate conversions and speed multipliers | `24 → 23.976`, `23.976 → 25`, `2x speed`, and so on |
| Tempo | 0.25× to 4× | The ratio the conversion above fills in; editable directly |
| Audio delay | Detected per track, editable | Positive prepends silence, negative trims the start |

The delay field fills in once the track is probed, and the line beneath it says where the value came from. See [Audio controls](audio-controls.md) for the detail.

!!! note

    The DeeZy adapters disable sample rate, gain, and tempo, because preprocessing can
    discard the immersive metadata they depend on.

## 5. Set the encoder options

The **Options** tab is built from the selected encoder and titled after it - _FFmpeg libopus options_, _DeeZy DDP options_, and so on. Fields appear, disappear, and change their choices as you adjust related settings.

Every option, with its default and range, is in the [encoder reference](encoders/reference.md).

## 6. Choose the output

On the **Output** tab:

- **Output** is generated from the input name and the encoder's container. Edit it, or use **Browse…**. A default output folder can be set in [Settings](settings.md).
- **Collision policy** - _Replace an existing file_ - is off by default. With it off, a generated name that already exists is numbered instead of overwritten.
- **Command preview** shows the exact command that will run. It updates live, and is worth a glance before you queue a long job.

## 7. Queue and encode

The queue toolbar separates queueing from running:

| Action                    | Effect                                     |
| ------------------------- | ------------------------------------------ |
| **Queue selected inputs** | Add to the queue without starting          |
| **Queue and start**       | Add and begin immediately (++ctrl+enter++) |
| **Start queue**           | Run every queued job in order              |
| **Start selected**        | Run only the selected queued jobs          |

The queue table shows **State**, **Input**, **Encoder**, **Output**, **Progress**, and **Status**. Progress is live, parsed from FFmpeg's own progress output or from DeeZy's staged percentages.

Jobs run one at a time. While one runs you can keep adding to the queue.

## 8. When it finishes

Select the job and read the **Selected job** tab for the command it ran and any error. **Session log** holds the running output for the session. The right-click menu on a job offers **Open output folder**, **Copy command**, and **Copy error**.

Output is written to a job-specific `.part` file and renamed into place only after the encoder exits successfully, so a crash or a cancellation never leaves a truncated file wearing the real name.

## Next

- [Audio controls](audio-controls.md) - delay detection, gain, tempo, and custom arguments
- [The encoding queue](queue.md) - what survives a restart, and what retry does
- [Presets](presets.md) - saving a configuration you want again
