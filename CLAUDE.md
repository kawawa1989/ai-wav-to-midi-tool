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

## Issueによる進行

作業はすべてGitHub Issue単位で進める（リポジトリ：kawawa1989/ai-wav-to-midi-tool）。

- **階層**：Phase（例：#1 Phase1）→ マイルストーン（例：#2 MS1）→ タスク。下の階層はGitHubのsub-issueとして親に紐付ける。
- **タスクIssueの本文**は次の4見出しで書く。各項目はチェックリスト（`- [ ]`）にする。
  1. `## 1. 概要`：目的と背景。ロードマップの該当箇所（Phase、FR/ADR、U番号など）を示す
  2. `## 2. 具体的な作業内容`：作業の手順。ユーザーの判断・操作が必要な項目は「**ユーザー**」と明記する
  3. `## 3. 受け入れ条件`：完了と判断できる、確認可能な条件
  4. `## 4. テスト項目`：ユニットテスト・CI・手動確認の内容
- **タイトル**は `[MS番号] 内容` の形にする（例：`[MS1] 採譜の計測スクリプト`）。
- **順序**がある場合は、GitHubのIssue依存関係（blocked by）で設定する。
- **作業の進め方**：着手前に対象Issueを読み、受け入れ条件とテスト項目を満たしたら完了とする。コミットメッセージやPRの本文には対象Issue番号を書く（例：`Refs #5`、完了時は `Closes #5`）。
- 作業中に範囲外の課題が見つかったら、勝手に広げず、新しいIssueの起票を提案する。

## ルール

- **著作物・秘密情報をコミットしない**：原曲、生成MIDI・MusicXML・PDF、HFトークン。作業データは `data/` 配下（Git管理外）に置く。テスト素材は公開可能な自作素材のみ `tests/fixtures/` へ。
- **既存機能を重複実装しない**：MuScriptorにある機能（量子化、テンポ・拍子推定、MusicXML/PDF/TAB出力）はまずCLIオプションで使う。
- **抽象化は必要になってから**（ADR-02）：MVPの境界は Transcriber / Validator / JobRunner の3つだけ。
- **モデルが出さない値を作らない**（ADR-03）：ベロシティ、ドラムの音価はnullのまま扱う。
- **再現性**（FR-10）：実行時はモデルrevision、MuScriptor/MuseScoreのバージョン、設定、入力ハッシュを記録する。
- **結果を過大評価しない**：未検証・失敗は明記する。品質の評価はmir_evalで行い、指標と許容窓を後から変えない。
- 依存の追加は `uv add`（`uv.lock` も一緒にコミット）。muscriptorは0.x系なのでマイナー版で固定する。
- ドキュメント・コメント・CLI出力は日本語。
