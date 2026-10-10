import pytest

from mumble_to_bars.schema import CODAS, VOWELS, Syllable, to_ipa


def test_all_21_vowels_have_ipa():
    assert len(VOWELS) == 21
    for v in VOWELS:
        assert to_ipa(v)


def test_seven_representative_codas():
    assert CODAS == set("ㄱㄴㄷㄹㅁㅂㅇ")


def test_syllable_roundtrip_dict():
    s = Syllable(vowel="ㅡ", coda="ㄹ", start_ms=1200, duration_ms=340)
    assert s.to_dict() == {
        "vowel": "ㅡ",
        "coda": "ㄹ",
        "start_ms": 1200,
        "duration_ms": 340,
        "pitch_hz": None,
    }


def test_rejects_unknown_vowel():
    with pytest.raises(ValueError):
        Syllable(vowel="a")


def test_rejects_non_representative_coda():
    with pytest.raises(ValueError):
        Syllable(vowel="ㅏ", coda="ㅅ")
