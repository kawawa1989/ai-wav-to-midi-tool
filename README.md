# ai-wav-to-midi-tool

ローカルの音声ファイル（MP3/WAV）から、楽器別に編集できるMIDIとバンドスコア（MusicXML / PDF）を作るツールです。採譜エンジンは [MuScriptor](https://github.com/muscriptor/muscriptor) を使います。

> **位置づけ**：耳コピの「下書き」を作るツールです。原曲の完全な再現は保証せず、MuseScore等で手修正する前提です。
> 計画・要件・リスクは [plan/roadmap.md](plan/roadmap.md) を参照してください。

**ステータス**：Phase 0（前提条件の確認）／環境構築のみ完了。変換機能は未実装。

## 動作環境

- macOS（Apple Silicon、MPS対応）。想定はApple M5／メモリ24GB
- Python 3.12（`.python-version` で固定。MuScriptorは3.13まで対応）
- [uv](https://docs.astral.sh/uv/)
- [MuseScore Studio 4](https://musescore.org/) 以降（PDF・TAB出力に必要）
- FFmpeg（任意）

## セットアップ

### 1. ツールの導入

```bash
brew install uv ffmpeg
brew install --cask musescore
```

MuseScoreが標準以外の場所にある場合は、環境変数 `MUSCRIPTOR_MUSESCORE` に実行ファイルのパスを設定します。

### 2. 依存関係のインストール

```bash
uv sync
```

`.venv` が作られ、MuScriptor（PyTorchを含む）が入ります。バージョンは `uv.lock` で固定されています。

### 3. Hugging Face の準備（モデル重みの入手）

MuScriptorの重みはHugging Faceのゲート付きリポジトリにあります。

1. Hugging Faceのアカウントを作る
2. 使うモデルのページでライセンス（CC BY-NC 4.0＋追加条件）に同意する
   - [small](https://huggingface.co/MuScriptor/muscriptor-small) / [medium](https://huggingface.co/MuScriptor/muscriptor-medium) / [large](https://huggingface.co/MuScriptor/muscriptor-large)
3. アクセストークン（read権限）を作り、ログインする

```bash
uv run hf auth login
```

> **重要（ロードマップ R4 / P0-1）**：重みの利用条件では、必要な権利のない音楽ファイルの採譜が禁止され、利用者が権利を保証します。市販曲を入力する前に、利用条件を読んで判断してください。

### 4. 環境の確認

```bash
uv run ai-wav-to-midi doctor
```

すべて `[OK]` なら準備完了です（`[WARN]` は任意項目）。

## 使い方（現時点）

変換機能はPhase 2で実装します。Phase 1のPoCでは、MuScriptorのCLIを直接使います。

```bash
uv run muscriptor transcribe data/input/song.wav --model medium --output data/outputs/song
uv run muscriptor transcribe --help
```

## ディレクトリ構成

| パス | 内容 | Git管理 |
|---|---|---|
| `plan/` | ロードマップ・計画文書 | する |
| `src/ai_wav_to_midi/` | ツール本体 | する |
| `tests/` | テスト。`tests/fixtures/` には公開可能な自作素材のみ置く | する |
| `data/input/` | 原曲（ローカル） | **しない** |
| `data/intermediate/` | ノートイベント・テンポ・メーターマップ | **しない** |
| `data/outputs/` | MIDI・MusicXML・PDF | **しない** |
| `data/reports/` | 評価・実行ログ | **しない** |

音声・MIDI・譜面ファイルは `.gitignore` で除外しています。原曲や生成された著作物をコミットしないでください。

## 開発

```bash
uv run pytest          # テスト
uv run ruff check .    # lint
uv run ruff format .   # 整形
```

CIはエンジン（torch）を除いて実行します：`uv sync --no-group engine`

## ライセンス

- このリポジトリのライセンス：未定
- MuScriptor：コードはMIT、**モデル重みはCC BY-NC 4.0（非商用のみ）＋追加条件**
- MuseScore Studio：GPLv3（外部ツールとして呼び出すのみ）
