from __future__ import annotations

from pathlib import Path
from typing import Protocol

from ffmpeg_audio_encoder.domain.models import (
    EncoderDescriptor,
    EncodingRequest,
    JsonScalar,
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
