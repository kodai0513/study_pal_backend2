import os

from dotenv import load_dotenv
from sqlalchemy import text
from sqlmodel import Session, create_engine

# .envファイルから設定をロード
load_dotenv()

# 環境変数の取得
_DB_HOST = os.getenv("DB_HOST")
_DB_NAME = os.getenv("DB_NAME")
_DB_PASSWORD = os.getenv("DB_PASSWORD")
_DB_PORT = os.getenv("DB_PORT")
_DB_USER = os.getenv("DB_USER")

# データベース接続URLを作成
_DATABASE_URL = f"mysql+mysqldb://{_DB_USER}:{_DB_PASSWORD}@{_DB_HOST}:{_DB_PORT}/{_DB_NAME}"

print(_DATABASE_URL)

# エンジンを作成
_engine = create_engine(
    _DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
)

try:
    # 接続を試みる
    with Session(_engine) as connection:
        # text()でSQL文をラップ
        result = connection.execute(text("SELECT 1"))
        print("接続成功:", result.fetchone())

except Exception as e:
    print(f"接続エラー: {e}")
