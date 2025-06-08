### 起動
```sh
docker compose up
```

### マイグレーション
```sh
alembic revision --autogenerate
alembic upgrade head
```

### データシーダを実装
```sh
cd /app
python -m migrations.seeder
```