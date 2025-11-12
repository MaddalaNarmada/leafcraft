import time
from typing import Any, Optional

# In-memory cache storage
_cache_store = {}

def get_cache(key: str) -> Optional[Any]:
    #check if key exists in cache
    if key in _cache_store:
        data, expiry = _cache_store[key]
        # Check if cache has not expired, return value
        if expiry is None or time.time() < expiry:
            return data
        else:
            # if expired, remove from cache
            del _cache_store[key]
    #returning none if key not found
    return None


#storing in memory cache with default of 5 min
def set_cache(key: str, value: Any, ttl: int = 300) -> None:
    expiry = time.time() + ttl if ttl else None

    #store value and expiry in cache
    _cache_store[key] = (value, expiry)

#delete key from cache
def delete_cache(key: str) -> None:
    if key in _cache_store:
        del _cache_store[key]

#clearing entries from cache
def clear_cache() -> None:
    _cache_store.clear()
