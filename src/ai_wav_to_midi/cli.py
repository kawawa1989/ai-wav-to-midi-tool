"""コマンドラインの入口。"""

from __future__ import annotations

import typer

from ai_wav_to_midi import __version__
from ai_wav_to_midi.doctor import run_checks

app = typer.Typer(help="ローカル音源から楽器別MIDIとバンドスコアを生成する。", no_args_is_help=True)


@app.command()
def version() -> None:
    """バージョンを表示する。"""
    typer.echo(__version__)


@app.command()
def doctor() -> None:
    """実行環境（Python・MuScriptor・MPS・Hugging Face・MuseScore）を確認する。"""
    checks = run_checks()
    for check in checks:
        if check.ok:
            mark = "OK  "
        elif check.required:
            mark = "NG  "
        else:
            mark = "WARN"
        typer.echo(f"[{mark}] {check.name}: {check.detail}")
    if any(not c.ok and c.required for c in checks):
        raise typer.Exit(code=1)
