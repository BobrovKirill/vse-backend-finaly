import json
import logging

from redis import Redis
from redis.exceptions import RedisError

from app.core.config import get_settings
from app.schemas.question import PublicQuestionRead


logger = logging.getLogger(__name__)
PUBLIC_QUESTIONS_CACHE_KEY = "public:questions:v1"


def get_cached_public_questions() -> list[PublicQuestionRead] | None:
    client = _get_redis_client()
    if client is None:
        return None

    try:
        cached_data = client.get(PUBLIC_QUESTIONS_CACHE_KEY)
    except RedisError:
        logger.exception("Failed to read public questions from Redis")
        return None

    if cached_data is None:
        return None
    return [PublicQuestionRead.model_validate(item) for item in json.loads(cached_data)]


def cache_public_questions(questions: list[PublicQuestionRead]) -> None:
    client = _get_redis_client()
    if client is None:
        return

    settings = get_settings()
    payload = json.dumps([question.model_dump(mode="json") for question in questions])
    try:
        client.setex(
            PUBLIC_QUESTIONS_CACHE_KEY,
            settings.public_questions_cache_ttl_seconds,
            payload,
        )
    except RedisError:
        logger.exception("Failed to cache public questions in Redis")


def invalidate_public_questions_cache() -> None:
    client = _get_redis_client()
    if client is None:
        return

    try:
        client.delete(PUBLIC_QUESTIONS_CACHE_KEY)
    except RedisError:
        logger.exception("Failed to invalidate public questions cache in Redis")


def _get_redis_client() -> Redis | None:
    redis_url = get_settings().redis_url
    if redis_url is None:
        return None
    return Redis.from_url(
        redis_url,
        decode_responses=True,
        socket_connect_timeout=1,
        socket_timeout=1,
    )
