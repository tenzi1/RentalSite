"""utiliy functions for REDIS"""

import os
import redis


def get_redis_client():
    REDIS_HOST = os.environ.get("REDIS_HOST")
    REDIS_PORT = os.environ.get("REDIS_PORT")

    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
    )
