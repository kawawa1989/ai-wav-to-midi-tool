"""実行環境の診断。セットアップ確認とFR-10（再現性）の記録元に使う。"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
from dataclasses import dataclass
from importlib import metadata

MUSESCORE_CANDIDATES = (
    "mscore",
    "mscore4",
    "/Applications/MuseScore 4.app/Contents/MacOS/mscore",
)


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    required: bool = True


def _package_version(name: str) -> str | None:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None


def find_musescore() -> str | None:
    """MuScriptorと同じく $MUSCRIPTOR_MUSESCORE を優先して探す。"""
    override = os.environ.get("MUSCRIPTOR_MUSESCORE")
    if override:
        return override if os.path.exists(override) else None
    for candidate in MUSESCORE_CANDIDATES:
        path = shutil.which(candidate) or (candidate if os.path.exists(candidate) else None)
        if path:
            return path
    return None


def _command_version(cmd: list[str]) -> str:
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired) as e:
        return f"実行失敗: {e}"
    lines = (out.stdout or out.stderr).strip().splitlines()
    return lines[0] if lines else "(出力なし)"


def check_python() -> Check:
    version = platform.python_version()
    ok = (3, 12) <= tuple(map(int, version.split(".")[:2])) < (3, 14)
    return Check("Python", ok, version)


def check_muscriptor() -> Check:
    version = _package_version("muscriptor")
    if version is None:
        return Check("MuScriptor", False, "未インストール（uv sync を実行）")
    return Check("MuScriptor", True, version)


def check_torch_mps() -> Check:
    version = _package_version("torch")
    if version is None:
        return Check("PyTorch / MPS", False, "torch 未インストール")
    import torch

    mps = torch.backends.mps.is_available()
    detail = f"torch {version}, MPS {'利用可' if mps else '利用不可（CPUで動作）'}"
    # MPSなしでもCPUで動くので、MPSの有無は警告扱いにする
    return Check("PyTorch / MPS", mps, detail, required=False)


def check_huggingface() -> Check:
    if _package_version("huggingface_hub") is None:
        return Check("Hugging Face", False, "huggingface_hub 未インストール")
    from huggingface_hub import get_token

    if get_token() is None:
        return Check(
            "Hugging Face",
            False,
            "トークン未設定（`uv run hf auth login`、モデルのライセンス同意も必要）",
        )
    return Check("Hugging Face", True, "トークン設定済み（ライセンス同意は各モデルページで確認）")


def check_musescore() -> Check:
    path = find_musescore()
    if path is None:
        return Check("MuseScore 4", False, "見つからない（PDF/TAB出力に必要）")
    return Check("MuseScore 4", True, f"{_command_version([path, '--version'])} ({path})")


def check_ffmpeg() -> Check:
    path = shutil.which("ffmpeg")
    if path is None:
        return Check("FFmpeg", False, "見つからない（MP3デコードに使う場合あり）", required=False)
    return Check("FFmpeg", True, _command_version([path, "-version"]), required=False)


def run_checks() -> list[Check]:
    return [
        check_python(),
        check_muscriptor(),
        check_torch_mps(),
        check_huggingface(),
        check_musescore(),
        check_ffmpeg(),
    ]
