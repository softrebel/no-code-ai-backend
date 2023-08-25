import redis
from .settings import settings
redis_client = redis.Redis(host=settings.REDIS_HOST)
def limiter(key, limit):
    req = redis_client.incr(key)
    ttl=60
    if req == 1:
        redis_client.expire(key, ttl)
    else:
        ttl = redis_client.ttl(key)
    if req > limit:
        return {
            "call": False,
            "ttl": ttl
        }
    else:
        return {
            "call": True,
            "ttl": ttl
        }



def call_limiter(ip, limit=settings.LIMIT_CALL_PER_HOUR):
    limit=int(limit)
    key=f'call_{ip}'
    return limiter(key, limit)

def bad_call_limiter(ip, limit=settings.LIMIT_BAD_CALL_PER_HOUR):
    limit=int(limit)
    key=f'bad_call_{ip}'
    return limiter(key, limit)
