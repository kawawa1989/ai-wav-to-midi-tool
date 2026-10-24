# CLAUDE.md

## プロジェクト概要

ローカル音源（MP3/WAV）→ 楽器別MIDI・MusicXML・PDFを作るツール。採譜はMuScriptorのラッパー。
要件・フェーズ・ADR・リスクは `plan/roadmap.md` が正。作業前に該当Phaseと未決事項（U0〜U7）を確認する。

## コマンド

- 依存のインストール：`uv sync`（CIは `uv sync --no-group engine`）
- テスト：`uv run pytest`
- lint／整形：`uv run ruff check .`／`uv run ruff format .`
- 環境診断：`uv run ai-wav-to-midi doctor`
- MuScriptor直接実行：`uv run muscriptor transcribe <audio> --model {small,medium,large}`

## ルール

- **著作物・秘密情報をコミットしない**：原曲、生成MIDI・MusicXML・PDF、HFトークン。作業データは `data/` 配下（Git管理外）に置く。テスト素材は公開可能な自作素材のみ `tests/fixtures/` へ。
- **既存機能を重複実装しない**：MuScriptorにある機能（量子化、テンポ・拍子推定、MusicXML/PDF/TAB出力）はまずCLIオプションで使う。
- **抽象化は必要になってから**（ADR-02）：MVPの境界は Transcriber / Validator / JobRunner の3つだけ。
- **モデルが出さない値を作らない**（ADR-03）：ベロシティ、ドラムの音価はnullのまま扱う。
- **再現性**（FR-10）：実行時はモデルrevision、MuScriptor/MuseScoreのバージョン、設定、入力ハッシュを記録する。
- **結果を過大評価しない**：未検証・失敗は明記する。品質の評価はmir_evalで行い、指標と許容窓を後から変えない。
- 依存の追加は `uv add`（`uv.lock` も一緒にコミット）。muscriptorは0.x系なのでマイナー版で固定する。
- ドキュメント・コメント・CLI出力は日本語。
