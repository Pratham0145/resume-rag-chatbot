import redis
import json


redis_client = redis.Redis(
    host="redis",
    port=6379,
    db=0,
    decode_responses=True
)


def save_message(session_id, role, content):

    key = f"chat:{session_id}"

    message = {
        "role": role,
        "content": content
    }

    redis_client.rpush(
        key,
        json.dumps(message)
    )


def load_messages(session_id):

    key = f"chat:{session_id}"

    messages = redis_client.lrange(key, 0, -1)

    return [
        json.loads(msg)
        for msg in messages
    ]


def cache_response(query, response):

    key = f"cache:{query}"

    redis_client.set(
        key,
        response,
        ex=3600
    )


def get_cached_response(query):

    key = f"cache:{query}"

    return redis_client.get(key)