### マイグレーション

```sh
alembic revision --autogenerate -m "create tables"
alembic upgrade head
```

### データシーダを実装
```sh
cd /app
python -m migrations.seeder
```