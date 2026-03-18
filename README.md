# Press Enter Later

指定時間後に指定されたキーを自動的に押すシンプルなGUIツール。

## 機能

- 任意のキーを選択（Enter、Space、Tab、Esc、a-fなど）
- 開始までの遅延時間を設定
- 1回の実行での押下回数を設定
- 押下間隔を設定
- 繰り返し回数を設定
- 繰り返し間隔を設定

## インストール

```bash
# uvをインストール（まだの場合）
curl -LsSf https://astral.sh/uv/install.sh | sh  # Linux/macOS
# または
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows

# 依存関係をインストール
uv sync
```

## 実行

```bash
uv run python main.py
```

## 使用例

### APIのRate Limit後の再開

APIを叩いているときにRate Limitに引っかかった場合、指定時間後に続行するために使用できます。

**例: 1時間（3600秒）後に再開したい場合**
1. キー: Enter
2. 開始までの遅延: 3600秒
3. 押下回数: 1回
4. 繰り返し: 1回

これで、1時間後に自動的にEnterキーが押され、待機していたプログラムやスクリプトが再開されます。

**例: 複数回のリトライが必要な場合**
1. キー: Enter
2. 開始までの遅延: 3600秒（1時間後に開始）
3. 押下回数: 1回
4. 押下間隔: 1秒
5. 繰り返し回数: 3回（合計3回試す）
6. 繰り返し間隔: 3600秒（1時間ごとに再試行）

これで、最初のリトライを1時間後に実行し、その後1時間おきに合計3回まで自動的にEnterキーを押します。

## ビルド

```bash
uv run pyinstaller main.py --onefile --windowed --name pressEnterLater
```

## ライセンス

MIT
