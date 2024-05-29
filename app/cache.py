from cachetools import TTLCache
from typing import  Any
import uuid


cache = TTLCache(maxsize=100, ttl=300)


def get_cache_key(user_id: uuid.UUID) -> str:
    return f"user_posts_{user_id}"


def cache_user_posts(user_id: uuid.UUID, posts: Any):
    key = get_cache_key(user_id)
    cache[key] = posts


def get_cached_user_posts(user_id: uuid.UUID) -> Any:
    key = get_cache_key(user_id)
    return cache.get(key, None)
