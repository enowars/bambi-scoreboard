import os
from typing import Optional

import aredis

REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
redis: aredis.StrictRedis = aredis.StrictRedis(host=REDIS_HOST)


async def current_round() -> Optional[int]:
    r = await redis.get("max_round")
    if not r:
        return None
    return int(r.decode())
