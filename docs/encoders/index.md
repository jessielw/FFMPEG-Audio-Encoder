# Encoders

Sixteen adapters in three families. Every one is offered only when the tools it needs are present - see [Required and optional tools](../tools.md).

The [encoder reference](reference.md) lists every option of every adapter, generated from the source so it cannot drift.

## FFmpeg built-in

Eight encoders that need nothing beyond a working FFmpeg build.

| Codec  | FFmpeg encoder | Output                        |
| ------ | -------------- | ----------------------------- |
| Opus   | `libopus`      | Ogg Opus (`.opus`)            |
| FLAC   | `flac`         | FLAC (`.flac`)                |
| AAC    | `aac`          | M4A (`.m4a`) or ADTS (`.aac`) |
| MP3    | `libmp3lame`   | MP3 (`.mp3`)                  |
| AC-3   | `ac3`          | Raw AC-3 (`.ac3`)             |
| E-AC-3 | `eac3`         | Raw E-AC-3 (`.eac3`)          |
| DTS    | `dca`          | Raw DTS (`.dts`)              |
| ALAC   | `alac`         | M4A (`.m4a`)                  |

Availability depends on the FFmpeg build you point at, not just on FFmpeg being installed. A distribution build without `libopus` or `libmp3lame` shows those adapters as unavailable.

## Standalone encoders

Three third-party command-line encoders, for cases where their output is preferred to FFmpeg's.

| Adapter | Profiles / modes | Output |
| --- | --- | --- |
| **opusenc** | VBR, constrained VBR, or hard CBR; music/speech tuning | Ogg Opus |
| **qaac** (Apple AAC) | AAC-LC or HE-AAC; TVBR, CVBR, ABR, or CBR | M4A or ADTS |
| **fdkaac** (Fraunhofer FDK AAC) | AAC-LC, HE-AAC, or HE-AAC v2; CBR or VBR | M4A or ADTS |

These do not read your source file directly. FFmpeg decodes the selected stream to PCM and pipes it in - 24-bit WAV for opusenc, 16-bit WAV for the two AAC encoders. The external encoder writes straight to the queue's temporary output, so cancellation, progress, and [atomic publishing](../queue.md#how-outputs-are-protected) behave exactly as they do for the built-in adapters.

qaac additionally requires a working Apple CoreAudioToolbox installation; its startup check determines availability.

## DeeZy (Dolby professional)

Five adapters for licensed Dolby encoding, driving DeeZy, the Dolby Encoding Engine, and - for the immersive formats - TrueHDD.

| Adapter | Target / source constraint | Output |
| --- | --- | --- |
| **DeeZy DD** | Auto, mono, stereo, or 5.1; downmix only, except explicit 5.0-to-5.1 | AC-3 |
| **DeeZy DDP** | Auto, mono, stereo, 5.1, or 7.1; downmix only, except explicit 5.0-to-5.1 | E-AC-3 |
| **DeeZy DDP-BluRay** | Fixed 7.1 from an 8-channel source | E-AC-3 |
| **DeeZy Atmos** | Streaming 5.1 or BluRay 7.1 from a valid Atmos source | E-AC-3 with Atmos |
| **DeeZy AC-4** | Immersive stereo from 6+ channels or TrueHD Atmos | AC-4 |

All five support BS.1770 and Leq(A) metering, DRC, and downmix controls; Atmos and AC-4 add TrueHDD warp and bed controls.

These adapters behave differently enough from the rest to be worth reading about separately - see [DeeZy encoders](deezy.md).

## Choosing between them

- For **Opus**, `ffmpeg.libopus` and `opusenc` use the same underlying library. opusenc exposes a slightly different control surface and hard CBR.
- For **AAC**, FFmpeg's native `aac` is the always-available option; qaac generally sounds better at low bitrates but is Windows-only; fdkaac is the portable middle ground and the only one offering HE-AAC v2.
- For **AC-3 and E-AC-3**, FFmpeg's encoders are fine for general use. The DeeZy adapters exist for licensed Dolby workflows where the reference encoder's output is the requirement.
