from typer.testing import CliRunner

from ai_wav_to_midi import __version__
from ai_wav_to_midi.cli import app
from ai_wav_to_midi.doctor import Check

runner = CliRunner()


def test_version() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert result.stdout.strip() == __version__


def test_doctor_fails_on_required_check(monkeypatch) -> None:
    monkeypatch.setattr(
        "ai_wav_to_midi.cli.run_checks",
        lambda: [Check("A", True, "ok"), Check("B", False, "missing")],
    )
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 1
    assert "[NG  ] B: missing" in result.stdout


def test_doctor_passes_with_only_warnings(monkeypatch) -> None:
    monkeypatch.setattr(
        "ai_wav_to_midi.cli.run_checks",
        lambda: [Check("A", True, "ok"), Check("C", False, "optional", required=False)],
    )
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
    assert "[WARN] C: optional" in result.stdout
