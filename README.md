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

## ビルド

```bash
uv run pyinstaller main.py --onefile --windowed --name pressEnterLater
```

## ライセンス

MIT
