# Architecture

`src/ffmpeg_audio_encoder/` is layered, and the layers are enforced by what each one is allowed to import.

```
domain/          pure data and errors        - no Qt, no I/O
encoders/        adapters and registry       - no Qt, no I/O
infrastructure/  the Qt and OS boundary
application/     queue orchestration
ui/              widgets and windows
```

`domain` and `encoders` are the two basedpyright-`strict` packages. They import no Qt at all, which is what lets `tools/generate_encoder_reference.py` build the docs table without a display.

## domain

`models.py` holds every dataclass and enum the rest of the application passes around - `Codec`, `OutputFormat`, `JobState`, `ThemePreference`, `DelaySource`, `OptionKind`, `NoticeLevel`, `AudioStream`, `CommonAudioOptions`, `EncodingRequest`, `EncoderDescriptor`, `OptionDefinition`, `PlanNotice`, `ProcessPlan`, `Toolchain`, `EncodeJob`, `EncoderPreset`, `EncoderConfiguration`, `AppSettings`. All frozen, all slotted.

`PlanNotice` carries no presentation - only a `NoticeLevel` and a message - so `encoders/` can report that a custom argument displaced a managed one without knowing how the UI will render it.

`errors.py` has `AudioEncoderError` and its three subclasses: `ValidationError`, `ProbeError`, `ToolNotFoundError`.

`__init__.py` curates an `__all__` - this is the layer's public surface.

## encoders

The adapter pattern. `base.py` defines two protocols:

```python
class EncoderAdapter(Protocol):
    @property
    def descriptor(self) -> EncoderDescriptor: ...

    def default_options(self) -> dict[str, JsonScalar]: ...

    def validate(self, request: EncodingRequest) -> None: ...

    def build_plan(
        self,
        request: EncodingRequest,
        toolchain: Toolchain,
        temporary_output: Path,
    ) -> ProcessPlan: ...
```

`build_plan` is handed the `.part` path to write to, rather than the final destination - publishing is the queue's job, not the adapter's.

`DynamicOptionChoiceProvider` is the second, for adapters whose option choices depend on other options - the DeeZy bitrate lists.

Three modules implement them: `ffmpeg.py` (eight adapters), `external.py` (opusenc, qaac, fdkaac), and `deezy.py` (five Dolby adapters). `registry.py` is a thin ordered container, and `default_registry()` in `__init__.py` builds it - **that registration order is the order the encoder picker shows.**

`arguments.py` is the custom-argument mechanism: slot prefixes, `{placeholder}` expansion, `var` declarations, and the merge that lets a custom flag displace a managed one. Adapters build a plain token list as they always have and hand it to `apply()`, which groups it and swaps out what collided; the module's docstring explains the two token classes and why substitution runs after tokenising. The DeeZy adapters deliberately bypass all of it and keep the original flat `custom_arguments` parser behind their Lt/Rt allow-list.

An adapter's `build_plan` returns a `ProcessPlan` of one or more `ProcessStage`s. That is how the standalone encoders express "FFmpeg decodes to PCM, and this program consumes it" without the runner needing to know anything specific about them.

## infrastructure

Everything that touches Qt, the filesystem, or another process.

| Module | Responsibility |
| --- | --- |
| `tools.py` | `locate_toolchain()`, `inspect_toolchain()` → `ToolReport`, `prune_deezy_scratch()` |
| `probe.py` | ffprobe JSON parsing, MediaInfo delay application, `QtMediaProbe` with bounded concurrency |
| `persistence.py` | `SettingsRepository`, `PresetRepository`, `JobRepository`; atomic writes; corrupt-file quarantine |
| `process.py` | `QtProcessRunner` - multi-stage pipelines, cancellation, force-kill |
| `proc_tree.py` | `ProcessTree` - Windows job object, POSIX descendant walk |
| `progress.py` | `FFmpegProgressParser`, `DeezyProgressParser` → `ProgressUpdate` |
| `output.py` | Filename sanitising, default output paths, `.part` temporary paths |
| `delay.py` | Filename delay markers: parse and strip |
| `qt_lifetime.py` | `detach_and_delete()` |

`proc_tree.py` is the one to read first if you are touching process handling; its module docstring explains why the Windows and POSIX paths differ and what the POSIX one cannot guarantee.

## application

`queue.py` holds `JobQueueController`, a `QObject` that owns the job list, dispatches one job at a time, validates destinations, and persists after every state change.

It signals rather than calling into the UI: `job_added`, `job_updated`, `log`, `active_changed`, `persistence_error`.

Its constructor is where restored state is repaired - a job persisted as `RUNNING` is turned into a `FAILED` one and its `.part` file deleted, because the application cannot know whether that encode was sound.

## ui

`main_window.py` is the bulk of it: `MainWindow`, `InputDraft` (the configuration being edited), and `ToolInspectionThread`. The window builds the **Encoding configuration** panel with its General / Options / Output tabs, the **Command preview**, and the **Encoding queue** with its toolbar and Selected job / Session log tabs.

`dialogs.py` is `SettingsDialog` and its `_PathRow`. `models.py` is `QueueTableModel` and `ProgressDelegate`. `theme.py` is `ThemeManager` - light/dark/automatic, including re-tinting qtawesome icons so neither theme leaves invisible glyphs. `custom_splitter.py` is a `QSplitter` with a theme-aware, custom-painted handle.

## The shape of an encode

1. `QtMediaProbe` probes the input; `apply_mediainfo_delays` annotates the streams.
2. The UI builds an `EncodingRequest` from the draft.
3. `JobQueueController.add` validates the destination and persists the job.
4. On dispatch, the adapter's `validate` runs, then `build_plan` produces a `ProcessPlan`.
5. `QtProcessRunner` executes the stages, owning the tree via `ProcessTree`.
6. A progress parser turns encoder output into `ProgressUpdate`s.
7. On success, the `.part` file is renamed onto the destination.
