import asyncio
import aioredis
import os

from aioredis import Redis

async def get_redis() -> Redis:
    host = os.getenv('REDIS_HOST', 'redis')
    port = os.getenv('REDIS_PORT', 6379)

    return await aioredis.from_url(
        url="redis://{}:{}".format(host, port)
    )

async def add_key_value(redis: Redis, key: str, value: str) -> None:
    await redis.set(key, value)
    print(f"Key '{key}' with value '{value}' added to Redis.")

async def get_key_value(redis: Redis, key: str) -> None:
    value = await redis.get(key)
    dump = value.decode('utf-8')
    print(f"Get key '{key}' has value '{dump}'")

async def delete_key(redis: Redis, key: str) -> None:
    await redis.expire(key, 0)
    print(f"Key '{key}' has been removed")

async def add_values() -> None:
    redis = await get_redis()

    # Example: Adding new key-value pairs asynchronously
    await add_key_value(redis, "username", "admin")
    await add_key_value(redis, "email", "admin@example.com")

    # Optionally, close the Redis connection
    await redis.close()

async def update_values() -> None:
    redis = await get_redis()

    # Example: Adding new key-value pairs asynchronously
    await add_key_value(redis, "username", "updated_admin")
    await add_key_value(redis, "email", "updated_admin@example.com")

    # Optionally, close the Redis connection
    await redis.close()

async def delete_values() -> None:
    redis = await get_redis()

    # Example: Adding new key-value pairs asynchronously
    await delete_key(redis, "username")
    await delete_key(redis, "email")

    # Optionally, close the Redis connection
    await redis.close()

async def get_values() -> None:
    redis = await get_redis()

    # Example: Adding new key-value pairs asynchronously
    await get_key_value(redis, "username")
    await get_key_value(redis, "email")

    # Optionally, close the Redis connection
    await redis.close()

def run_add_values() -> None:
    asyncio.run(add_values())

def run_update_values() -> None:
    asyncio.run(update_values())

def run_get_values() -> None:
    asyncio.run(get_values())

def run_delete_values() -> None:
    asyncio.run(delete_values())

# Run the asynchronous main function
if __name__ == "__main__":
   print("please run specific script")