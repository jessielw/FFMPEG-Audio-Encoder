from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Protocol, runtime_checkable

from ffmpeg_audio_encoder.domain.models import (
    AudioStream,
    EncoderDescriptor,
    EncodingRequest,
    JsonScalar,
    OptionChoice,
    ProcessPlan,
    Toolchain,
)


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


@runtime_checkable
class DynamicOptionChoiceProvider(Protocol):
    def option_choices(
        self,
        key: str,
        stream: AudioStream | None,
        channel_layout: str | None,
        encoder_options: Mapping[str, JsonScalar],
    ) -> tuple[OptionChoice, ...]: ...
