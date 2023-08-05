import redis
import json
import typing as t


def get_value(db: redis.Redis, key: str) -> t.Any:
    if not db.exists(key):
        raise KeyError("redis key not exists")
    value = db.get(key).decode("utf-8")
    try:
        return None if value is None else json.loads(value)
    except json.decoder.JSONDecodeError:
        return value
