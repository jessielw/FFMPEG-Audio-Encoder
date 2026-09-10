# Custom arguments

Every FFmpeg adapter and every standalone encoder exposes a **Custom arguments** field at the bottom of its **Options** tab, for the flags the curated options do not cover.

The field is **parsed into an argument list and never run through a shell**. Shell metacharacters are not interpreted, so quoting behaves like a command line, not like `bash`.

Write one argument group per line:

```
-cutoff 18000
pre: -analyzeduration 200M
var gain = 3
-af {filters},volume={gain}dB
```

## Slots: where a line lands

An unprefixed line is applied after the managed codec settings, which is where custom arguments have always gone. Prefix a line to put it somewhere else.

| Prefix | Where it lands | Available on |
| --- | --- | --- |
| _(none)_ or `out:` | After the managed codec settings | Every adapter |
| `pre:` | Before `-i`, for `-hwaccel`, `-analyzeduration`, `-guess_layout_max` | Every adapter |
| `decode:` | The FFmpeg decode stage's output side | opusenc, qaac, fdkaac |

`decode:` exists because the standalone encoders run a two-stage pipeline - FFmpeg decodes the source to PCM and pipes it to the encoder. Without it, the hand-off between the two would be unreachable. `decode: -c:a pcm_f32le` changes the PCM format the encoder receives; an unprefixed line still goes to the encoder itself.

## Placeholders

`{name}` expands to a value the application is already managing.

- **Every option on the encoder** is a placeholder under its own name, so `{bitrate_kbps}` is whatever the Bitrate control currently reads.
- `{filters}` is the managed filter chain - the gain, tempo and delay filters combined.
- `{sample_rate}`, `{channel_layout}`, `{codec}` and `{stream}` cover the General tab.

The input and output paths are deliberately **not** placeholders. The queue writes to a temporary file and renames it into place when the encode succeeds, and reaching that path would break the guarantee that a failed encode never leaves a half-written file behind.

Write `{{` for a literal brace.

### Extending the filter chain instead of replacing it

This is the one to know. `-af` is a single FFmpeg option, so a bare `-af` of your own **replaces** the managed chain and your gain, tempo and delay silently stop being applied.

```
-af {filters},highpass=f=20      ← extends: gain, tempo and delay are kept
-af highpass=f=20                ← replaces: they are lost
```

Both are allowed - the second is occasionally what you want - but the command preview says which one you got, and warns loudly about the second.

If there is no managed chain, `{filters}` expands to nothing and the stray comma is cleaned up, so the first line above stays valid on a file with no gain, tempo or delay set.

## Variables

A `var name = value` line declares a variable that the rest of the field can use. The declaration lives in the same field as the use, so a preset can never carry one without the other.

```
var cutoff = 18000
-cutoff {cutoff}
```

A variable that is **defined but empty** drops the whole argument group that uses it:

```
var cutoff =
-cutoff {cutoff} -aac_coder fast
```

emits `-aac_coder fast` and nothing else - not a malformed `-cutoff ""`. That makes a flag easy to switch off by blanking one line rather than deleting and retyping it.

A placeholder that is **never defined** is an error, not a silent omission. A typo would otherwise quietly change your command.

## Overriding a managed setting

A custom flag that collides with one the application manages **replaces** it, rather than being appended alongside it. Setting `-b:a 256k` gives you exactly one `-b:a` in the command, and the preview reports what it displaced:

```
⚠ -b:a 256k overrides Bitrate (192k)
```

Alternative spellings count as the same flag: `-filter:a` collides with the managed `-af`, and `-acodec` with `-c:a`. Emitting both spellings would make FFmpeg fail outright.

Repeated flags of your own are all kept - two `-metadata` lines stay two `-metadata` arguments - because only managed arguments are ever displaced.

## What cannot be set

A few arguments are refused with an explanation, because the application's guarantees depend on them:

| Refused | Why |
| --- | --- |
| `-i`, `-map`, `-map_chapters` | The input and stream selection come from the input list and the General tab |
| `-progress`, `-nostats`, `pipe:N` | Progress reporting and the pipeline between stages are parsed by the application |
| `-f`, `-o`, a bare `-` in an output slot | The container and output path are managed so a finished encode can be published atomically |
| A line that does not start with a flag | FFmpeg would read a bare value as an extra output file and write something you did not ask for |

`-f` **is** allowed in the `pre:` slot, where it forces the input demuxer rather than the output muxer.

Mistakes are reported when you type them, in the command preview, and again when the job is queued - never at encode time only.

## DeeZy is different

The [DeeZy adapters](encoders/deezy.md) keep a much narrower field: **Advanced downmix metadata**, restricted to Lt/Rt and Lo/Ro level flags. Slots, placeholders and variables do not apply there. These drive licensed Dolby encodes through the Dolby Encoding Engine, where a stray argument produces an expensive, subtly wrong result rather than an obvious failure.

## Presets

The field is saved in [presets](presets.md) along with everything else, variables included.
