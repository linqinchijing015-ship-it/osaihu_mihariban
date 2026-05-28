# osaihu_mihariban

家計簿 × 後悔スコア Web アプリ（ハッカソン）。

## バックエンド（Django）の動かし方

### 1. 仮想環境を作成・有効化

```powershell
python -m venv .venv
.venv/Scripts/Activate.ps1
```

macOS/Linux の場合:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. 依存パッケージをインストール

```bash
pip install -r requirements.txt
```

### 3. 環境変数を設定（任意）

```bash
cp .env.example .env
# .env を編集して SECRET_KEY 等を設定
```

> **注意**: 本番環境では必ず `SECRET_KEY` を固有の値に設定してください。

### 4. DB を初期化

```bash
python manage.py migrate
```

### 5. 管理者ユーザーを作成

```bash
python manage.py createsuperuser
```

### 6. 開発サーバーを起動

```bash
python manage.py runserver
```

`http://127.0.0.1:8000/admin/` にアクセスして管理画面から Expense モデルを CRUD できます。

## Postgres への切り替え

`.env` に `DATABASE_URL` を設定するだけで自動的に切り替わります。

```
DATABASE_URL=postgres://user:password@localhost:5432/osaihu_mihariban
```
