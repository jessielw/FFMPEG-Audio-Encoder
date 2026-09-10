"""Custom argument parsing, placeholder expansion, and managed-argument override.

Three things layered on the plain token list the adapters already build.

*Slots.* A line may start with ``pre:``, ``out:`` or ``decode:`` to say where it lands. An
unprefixed line means ``out:``, which is what every ``custom_args`` value saved before this
module existed means, so old presets keep working untouched.

*Placeholders.* ``{name}`` expands to a managed value - every option key on the adapter's
descriptor, plus computed ones like ``{filters}`` - or to a variable the same field defines
with a ``var name = value`` line. Keeping the definition in the same string as the use is
deliberate: a preset can never carry ``-cutoff {cutoff}`` and lose what ``cutoff`` meant.

An **undefined** placeholder is an error, never a silent omission - a typo would otherwise
quietly change the command, and a value saved before this module existed that happened to
contain a literal brace would quietly mean something new. A **defined but empty** one drops
the argument group containing it, which is what makes ``-cutoff {cutoff}`` vanish cleanly
when ``cutoff`` is blank. Write ``{{`` for a literal brace.

*Override.* A custom flag that collides with a managed one displaces it rather than being
appended alongside it, and the displacement is reported so the preview can say what
happened. Collision is tested on a canonical flag, because ``-filter:a`` and ``-af`` are the
same option to FFmpeg and emitting both fails outright. Deduplication is only ever
custom-against-managed: ``-metadata`` is repeatable, so two custom ``-metadata`` lines must
both survive.

Substitution happens *after* tokenisation, so an expanded value is never re-split and a
variable can never inject an extra argument. That is the same guarantee as "never run
through a shell", and both hold for every path through this module.
"""

from __future__ import annotations

import re
import shlex
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum

from ffmpeg_audio_encoder.domain.errors import ValidationError
from ffmpeg_audio_encoder.domain.models import NoticeLevel, PlanNotice


class Slot(StrEnum):
    """Where a custom line lands in the command."""

    PRE = "pre"
    MAIN = "out"
    DECODE = "decode"


FFMPEG_SLOTS = frozenset({Slot.PRE, Slot.MAIN})
EXTERNAL_SLOTS = frozenset({Slot.PRE, Slot.MAIN, Slot.DECODE})
LEGACY_SLOTS = frozenset({Slot.MAIN})

_SLOT_BY_PREFIX = {slot.value: slot for slot in Slot}

# ``{{`` and ``}}`` are literal braces; a lone brace is a mistake worth reporting.
_SCAN_PATTERN = re.compile(r"\{\{|\}\}|\{([A-Za-z_][A-Za-z0-9_]*)\}|[{}]")
_VAR_PATTERN = re.compile(r"^var\s+([A-Za-z_][A-Za-z0-9_]*)\s*=(.*)$")

# FFmpeg spells several options more than one way. Merging keys on the canonical form,
# because emitting both "-af" and "-filter:a" makes FFmpeg fail with "Filtergraph
# specified twice" rather than doing what the user meant.
_ALIASES = {
    "-filter:a": "-af",
    "-filter:a:0": "-af",
    "-codec:a": "-c:a",
    "-acodec": "-c:a",
    "-b:a:0": "-b:a",
    "-ab": "-b:a",
    "-aq": "-q:a",
}

# Placeholders whose value is a list joined with commas rather than a scalar. An empty one
# does not drop its group; it collapses the separators around it instead.
_LIST_TOKENS = frozenset({"filters"})

_DENIED_EVERYWHERE = {
    "-i": "the input is managed; choose the file in the input list",
    "-map": "stream selection is managed; choose the stream on the General tab",
    "-map_chapters": "chapter handling is managed",
    "-progress": "progress reporting is managed and parsing depends on it",
    "-nostats": "progress reporting is managed and parsing depends on it",
}
_DENIED_IN_OUTPUT = {
    "-f": "the container is managed; choose it on the General tab",
    "-o": "the output path is managed so the encode can be published atomically",
}
_DENIED_TOKENS = {
    "pipe:0": "the pipeline between stages is managed",
    "pipe:1": "the pipeline between stages is managed",
    "pipe:2": "the pipeline between stages is managed",
    "-": "the pipeline between stages is managed",
}

# Best-effort display names so an override notice can name the control the user sees. A
# flag missing from this map still reports, just with the flag itself.
_MANAGED_LABELS = {
    "-ar": "Sample rate",
    "-channel_layout:a": "Channel layout",
    "-af": "the managed filter chain",
    "-c:a": "Codec",
    "-b:a": "Bitrate",
    "-q:a": "VBR quality",
    "-compression_level": "Compression level",
    "-aac_coder": "Coder",
    "--bitrate": "Bitrate",
    "--comp": "Complexity",
    "--framesize": "Frame duration",
    "--expect-loss": "Packet loss",
    "--max-delay": "Maximum delay",
}


@dataclass(frozen=True, slots=True)
class CustomArguments:
    """Resolved custom tokens, grouped by the slot they belong to."""

    per_slot: Mapping[Slot, tuple[str, ...]]
    notices: tuple[PlanNotice, ...] = ()

    def tokens(self, slot: Slot) -> tuple[str, ...]:
        return self.per_slot.get(slot, ())


def canonical(flag: str) -> str:
    return _ALIASES.get(flag, flag)


def is_flag(token: str) -> bool:
    """True for an option token, false for a value.

    A bare negative number is a value - DeeZy's ``--lt-rt-center -4.5`` depends on that.
    """
    if not token.startswith("-") or token == "-":
        return False
    try:
        float(token)
    except ValueError:
        return True
    return False


def _substitute(
    token: str, managed: Mapping[str, str], variables: Mapping[str, str]
) -> tuple[str, str | None]:
    """Expand placeholders in one token.

    Returns the expanded text and, when the group must be dropped, the placeholder that
    resolved to nothing.
    """
    dropped: str | None = None
    saw_list = False
    result: list[str] = []
    position = 0

    for match in _SCAN_PATTERN.finditer(token):
        result.append(token[position : match.start()])
        position = match.end()
        matched = match.group(0)
        if matched == "{{":
            result.append("{")
            continue
        if matched == "}}":
            result.append("}")
            continue
        name = match.group(1)
        if name is None:
            raise ValidationError(
                f"Unmatched {matched!r} in {token!r}; write '{{{{' for a literal brace"
            )
        if name in _LIST_TOKENS:
            saw_list = True
            result.append(managed.get(name, ""))
            continue
        if name in managed:
            value = managed[name]
        elif name in variables:
            value = variables[name]
        else:
            raise ValidationError(
                f"Unknown placeholder {{{name}}}. Define it with 'var {name} = …', "
                f"or write '{{{{{name}}}}}' for a literal brace."
            )
        if not value:
            dropped = f"{{{name}}}"
        result.append(value)

    result.append(token[position:])
    text = "".join(result)
    if saw_list:
        # A list placeholder that expanded to nothing leaves stray separators behind:
        # "-af {filters},highpass=f=20" must become "-af highpass=f=20".
        text = ",".join(part for part in text.split(",") if part)
        if not text:
            dropped = "{filters}"
    return text, dropped


def _group(tokens: Iterable[str]) -> list[list[str]]:
    """Split a token list into argument groups: a flag plus the values that follow it."""
    groups: list[list[str]] = []
    current: list[str] | None = None
    for token in tokens:
        if is_flag(token) or current is None:
            current = [token]
            groups.append(current)
        else:
            current.append(token)
    return groups


def _reject_forbidden(group: Sequence[str], slot: Slot) -> None:
    leader = group[0]
    if not is_flag(leader):
        raise ValidationError(
            f"Custom arguments must start with a flag; {leader!r} looks like a file name. "
            "A bare value would be read as an extra output file."
        )
    key = canonical(leader)
    reason = _DENIED_EVERYWHERE.get(key)
    if reason is None and slot is not Slot.PRE:
        reason = _DENIED_IN_OUTPUT.get(key)
    if reason is not None:
        raise ValidationError(f"Custom arguments cannot set {leader}: {reason}")
    for token in group:
        forbidden = _DENIED_TOKENS.get(token)
        if forbidden is not None:
            raise ValidationError(f"Custom arguments cannot use {token}: {forbidden}")


def _read_lines(
    text: str, allowed_slots: frozenset[Slot]
) -> tuple[list[tuple[Slot, str]], dict[str, str]]:
    lines: list[tuple[Slot, str]] = []
    variables: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        declaration = _VAR_PATTERN.match(line)
        if declaration is not None:
            variables[declaration.group(1)] = declaration.group(2).strip()
            continue
        slot = Slot.MAIN
        head, separator, rest = line.partition(":")
        prefix = head.strip().lower()
        if separator and not head.strip().startswith("-") and " " not in head.strip():
            if prefix not in _SLOT_BY_PREFIX:
                supported = ", ".join(sorted(name.value for name in allowed_slots))
                raise ValidationError(
                    f"Unknown argument slot {prefix!r}; this encoder offers: {supported}"
                )
            slot = _SLOT_BY_PREFIX[prefix]
            line = rest.strip()
        if not line:
            continue
        if slot not in allowed_slots:
            supported = ", ".join(sorted(name.value for name in allowed_slots))
            raise ValidationError(
                f"This encoder has no {slot.value!r} slot; it offers: {supported}"
            )
        lines.append((slot, line))
    return lines, variables


def resolve(
    text: str,
    *,
    managed_tokens: Mapping[str, str],
    allowed_slots: frozenset[Slot],
) -> CustomArguments:
    """Parse custom argument text into per-slot token lists."""
    if "\x00" in text:
        raise ValidationError("Custom arguments cannot contain NUL characters")
    if not text.strip():
        return CustomArguments({})

    lines, variables = _read_lines(text, allowed_slots)
    shadowed = sorted(set(variables) & set(managed_tokens))
    if shadowed:
        raise ValidationError(
            f"Variable {shadowed[0]!r} shadows a managed placeholder; choose another name"
        )

    per_slot: dict[Slot, list[str]] = {}
    notices: list[PlanNotice] = []
    for slot, line in lines:
        try:
            tokens = shlex.split(line, posix=True)
        except ValueError as exc:
            raise ValidationError(f"Invalid custom arguments: {exc}") from exc
        for group in _group(tokens):
            expanded: list[str] = []
            dropped: str | None = None
            for token in group:
                text_value, empty = _substitute(token, managed_tokens, variables)
                dropped = dropped or empty
                expanded.append(text_value)
            if dropped is not None:
                notices.append(
                    PlanNotice(NoticeLevel.INFO, f"{group[0]} omitted: {dropped} is empty")
                )
                continue
            _reject_forbidden(expanded, slot)
            per_slot.setdefault(slot, []).extend(expanded)
    return CustomArguments(
        {slot: tuple(tokens) for slot, tokens in per_slot.items()}, tuple(notices)
    )


def apply(
    managed: list[str], custom: tuple[str, ...], *, filter_chain: str = ""
) -> tuple[list[str], list[PlanNotice]]:
    """Merge custom tokens into a managed token list.

    A custom flag displaces the managed group carrying the same canonical flag; everything
    else is appended. Returns the merged tokens and notices describing what was displaced.
    """
    if not custom:
        return managed, []

    custom_groups = _group(custom)
    custom_flags = {canonical(group[0]) for group in custom_groups if is_flag(group[0])}
    notices: list[PlanNotice] = []
    kept: list[str] = []

    for group in _group(managed):
        flag = group[0] if is_flag(group[0]) else None
        if flag is None or canonical(flag) not in custom_flags:
            kept.extend(group)
            continue
        replacement = next(
            (
                candidate
                for candidate in custom_groups
                if is_flag(candidate[0]) and canonical(candidate[0]) == canonical(flag)
            ),
            group,
        )
        notices.append(_override_notice(flag, group[1:], replacement, filter_chain))

    kept.extend(custom)
    return kept, notices


def _override_notice(
    flag: str, old_values: list[str], replacement: list[str], filter_chain: str
) -> PlanNotice:
    new_text = " ".join(replacement[1:])
    old_text = " ".join(old_values)
    if canonical(flag) == "-af":
        if filter_chain and filter_chain in new_text:
            return PlanNotice(NoticeLevel.INFO, "-af extends the managed filter chain.")
        if filter_chain:
            return PlanNotice(
                NoticeLevel.WARNING,
                f"{replacement[0]} replaces the managed filter chain, so gain, tempo and "
                f"delay will NOT be applied (dropping {old_text}). "
                "Write '-af {filters},…' to keep them.",
            )
    label = _MANAGED_LABELS.get(canonical(flag), f"the managed {flag}")
    return PlanNotice(
        NoticeLevel.WARNING,
        f"{replacement[0]} {new_text} overrides {label} ({old_text})".rstrip(),
    )
