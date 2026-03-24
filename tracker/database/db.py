import json
import os
from pathlib import Path
from typing import Any

from tracker.models.content import ContentDB

try:
    from upstash_redis import Redis
except ImportError:
    Redis = None


class DB:
    def __init__(self, data_path: str | Path | None = None) -> None:
        self.data_path = Path(data_path or Path(__file__).with_name("data.json"))
        self.contents: dict[str, ContentDB] = {}
        self.views = {}
        self.users = {}
        self.storage_mode = "local"
        self.redis = self._create_redis_client()
        self.content_hash_key = f"{os.getenv('UPSTASH_REDIS_PREFIX', 'mailtracker')}:contents"

        if self.redis:
            self.storage_mode = "upstash"
        else:
            self._load_local()

    def _create_redis_client(self):
        url = os.getenv("UPSTASH_REDIS_REST_URL")
        token = os.getenv("UPSTASH_REDIS_REST_TOKEN")

        if not (url and token and Redis):
            return None

        try:
            return Redis(url=url, token=token)
        except Exception as exc:
            print(exc)
            return None

    def _serialize_content(self, content: ContentDB) -> str:
        return json.dumps(content.model_dump(mode="json"))

    def _deserialize_content(self, raw_content: Any):
        if not raw_content:
            return False

        try:
            if isinstance(raw_content, bytes):
                raw_content = raw_content.decode("utf-8")

            if isinstance(raw_content, str):
                raw_content = json.loads(raw_content)

            return ContentDB.model_validate(raw_content)
        except Exception as exc:
            print(exc)
            return False

    def _load_local(self) -> None:
        if not self.data_path.exists():
            return

        try:
            raw_data = json.loads(self.data_path.read_text(encoding="utf-8"))
            self.contents = {
                item_id: ContentDB.model_validate(item_data)
                for item_id, item_data in raw_data.get("contents", {}).items()
            }
        except Exception as exc:
            print(exc)
            self.contents = {}

    def _save_local(self) -> bool:
        try:
            self.data_path.parent.mkdir(parents=True, exist_ok=True)
            payload = {
                "contents": {
                    item_id: item.model_dump(mode="json")
                    for item_id, item in self.contents.items()
                }
            }
            self.data_path.write_text(
                json.dumps(payload, indent=2), encoding="utf-8"
            )
            return True
        except Exception as exc:
            print(exc)
            return False

    def add_content(self, content):
        try:
            if self.redis:
                self.redis.hset(self.content_hash_key, content.id, self._serialize_content(content))
                return True

            self.contents[content.id] = content
            return self._save_local()
        except Exception as exc:
            print(exc)
            return False

    def add_view(self, view):
        try:
            self.views[view.id] = view
            return True
        except Exception as exc:
            print(exc)
            return False

    def add_user(self, user):
        try:
            self.users[user.id] = user
            return True
        except Exception as exc:
            print(exc)
            return False

    def search_content(self, item_id):
        try:
            if self.redis:
                return self._deserialize_content(self.redis.hget(self.content_hash_key, item_id))

            return self.contents[item_id]
        except Exception as exc:
            print(exc)
            return False

    def search_view(self, item_id):
        try:
            return self.views[item_id]
        except Exception as exc:
            print(exc)
            return False

    def search_user(self, item_id):
        try:
            return self.users[item_id]
        except Exception as exc:
            print(exc)
            return False

    def get_contents(self):
        try:
            if self.redis:
                raw_items = self.redis.hgetall(self.content_hash_key) or {}
                contents = {}
                for item_id, raw_content in raw_items.items():
                    normalized_id = item_id.decode("utf-8") if isinstance(item_id, bytes) else item_id
                    content = self._deserialize_content(raw_content)
                    if content:
                        contents[normalized_id] = content
                return contents

            return self.contents
        except Exception as exc:
            print(exc)
            return False

    def get_views(self):
        try:
            return self.views
        except Exception as exc:
            print(exc)
            return False

    def get_users(self):
        try:
            return self.users
        except Exception as exc:
            print(exc)
            return False

    def delete_content(self, item_id):
        try:
            if self.redis:
                self.redis.hdel(self.content_hash_key, item_id)
                return True

            del self.contents[item_id]
            return self._save_local()
        except Exception as exc:
            print(exc)
            return False

    def delete_view(self, item_id):
        try:
            del self.views[item_id]
            return True
        except Exception as exc:
            print(exc)
            return False

    def delete_user(self, item_id):
        try:
            del self.users[item_id]
            return True
        except Exception as exc:
            print(exc)
            return False

    def update_content(self, content):
        try:
            if self.redis:
                self.redis.hset(self.content_hash_key, content.id, self._serialize_content(content))
                return True

            self.contents[content.id] = content
            return self._save_local()
        except Exception as exc:
            print(exc)
            return False

    def update_view(self, view):
        try:
            self.views[view.id] = view
            return True
        except Exception as exc:
            print(exc)
            return False

    def update_user(self, user):
        try:
            self.users[user.id] = user
            return True
        except Exception as exc:
            print(exc)
            return False

    def search_content_by_link(self, link):
        try:
            for content in self.get_contents().values():
                if content.link == link:
                    return content
            return False
        except Exception as exc:
            print(exc)
            return False

    def search_content_by_name(self, name):
        try:
            for content in self.get_contents().values():
                if content.name == name:
                    return content
            return False
        except Exception as exc:
            print(exc)
            return False

    def add_view_to_content(self, content_id, view):
        try:
            content = self.search_content(content_id)
            if not content:
                return False

            content.views.append(view)
            self.views[view.id] = view
            return self.update_content(content)
        except Exception as exc:
            print(exc)
            return False
