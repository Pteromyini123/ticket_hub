import time

# just a dictionary for storing cached data
cache_data = {}

# save something to the cache with expiry
def set_cache(key, value, ttl=60):
    expire_time = time.time() + ttl
    cache_data[key] = (value, expire_time)

# get from cache if not expired
def get_cache(key):
    if key in cache_data:
        value, expires = cache_data[key]
        if time.time() < expires:
            return value
        else:
            # remove expired item
            del cache_data[key]
    return None
