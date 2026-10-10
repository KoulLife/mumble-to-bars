import pytest

from mumble_to_bars.cli import main


def test_version(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert "m2b" in capsys.readouterr().out


def test_extract_not_implemented():
    assert main(["extract", "hum.wav"]) == 2
