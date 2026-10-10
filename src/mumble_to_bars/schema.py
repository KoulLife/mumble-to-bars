"""Vowel template schema: the only contract between pipeline stages.

Stages (audio, vowel, lyrics) never import each other; they exchange these types.
Spec and open decisions: docs/schema.md
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

# Korean vowel jamo (중성) -> IPA. The single place where notation is converted.
JAMO_TO_IPA: dict[str, str] = {
    "ㅏ": "a",
    "ㅐ": "ɛ",
    "ㅑ": "ja",
    "ㅒ": "jɛ",
    "ㅓ": "ʌ",
    "ㅔ": "e",
    "ㅕ": "jʌ",
    "ㅖ": "je",
    "ㅗ": "o",
    "ㅘ": "wa",
    "ㅙ": "wɛ",
    "ㅚ": "we",
    "ㅛ": "jo",
    "ㅜ": "u",
    "ㅝ": "wʌ",
    "ㅞ": "we",
    "ㅟ": "wi",
    "ㅠ": "ju",
    "ㅡ": "ɯ",
    "ㅢ": "ɰi",
    "ㅣ": "i",
}

VOWELS: frozenset[str] = frozenset(JAMO_TO_IPA)

# Coda (받침) normalized to the 7 representative sounds.
CODAS: frozenset[str] = frozenset("ㄱㄴㄷㄹㅁㅂㅇ")


def to_ipa(vowel: str) -> str:
    """Convert a vowel jamo to IPA. Raises KeyError for unknown vowels."""
    return JAMO_TO_IPA[vowel]


@dataclass(frozen=True)
class Syllable:
    """One sung syllable in a vowel template."""

    vowel: str
    coda: str | None = None
    start_ms: int | None = None
    duration_ms: int | None = None
    pitch_hz: float | None = None

    def __post_init__(self) -> None:
        if self.vowel not in VOWELS:
            raise ValueError(f"unknown vowel: {self.vowel!r}")
        if self.coda is not None and self.coda not in CODAS:
            raise ValueError(f"coda must be one of {''.join(sorted(CODAS))}: {self.coda!r}")

    def to_dict(self) -> dict:
        return asdict(self)


VowelTemplate = list[Syllable]
