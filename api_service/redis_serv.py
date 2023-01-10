import redis

from settings import(
    REDIS_HOST,
    REDIS_PORT,
    REDIS_PASS
)

class RedisService:
    def __init__(self) -> None:
        self.redis_serv = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASS
        )
    
    def set_key(self, key: str) -> None:
        self.redis_serv.set(key, 1)
    
    def get_key(self, key: str) -> str:
        return self.redis_serv.get(key)
    
    def check_key(self, key: str) -> bool:
        return self.get_key(key) == "1"
