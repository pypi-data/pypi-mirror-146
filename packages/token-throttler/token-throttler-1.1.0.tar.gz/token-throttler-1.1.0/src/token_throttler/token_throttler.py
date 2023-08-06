import asyncio
from threading import Lock
from typing import Any, Callable, Union

from . import ThrottlerConfig, TokenBucket, TokenThrottlerException
from .storage import BucketStorage
from .validate import (
    validate_bucket,
    validate_bucket_config,
    validate_bucket_key,
    validate_cost,
    validate_identifier,
    validate_storage,
)


class TokenThrottler:
    def __init__(self, cost: int, storage: BucketStorage) -> None:
        self._cost: int = cost
        self._buckets: BucketStorage = storage
        self._lock: Lock = Lock()
        validate_cost(self._cost)
        validate_storage(self._buckets, BucketStorage)

    def _add_identifier(self, identifier: str) -> None:
        validate_identifier(identifier)
        if identifier not in self._buckets:
            self._buckets[identifier] = {}

    def get_bucket(self, identifier: str, bucket_key: str) -> Union[TokenBucket, None]:
        validate_identifier(identifier)
        validate_bucket_key(bucket_key)
        return self._buckets.get_bucket(identifier, bucket_key)

    def get_all_buckets(self, identifier: str) -> Union[dict[str, TokenBucket], None]:
        validate_identifier(identifier)
        return self._buckets.get_all_buckets(identifier)

    def add_bucket(self, identifier: str, bucket: TokenBucket) -> None:
        validate_bucket(bucket, TokenBucket)
        self._add_identifier(identifier)
        bucket.identifier = identifier
        bucket.cost = self._cost
        self._buckets.add_bucket(bucket)

    def remove_bucket(self, identifier: str, bucket_key: str) -> None:
        validate_identifier(identifier)
        validate_bucket_key(bucket_key)
        self._buckets.remove_bucket(identifier, bucket_key)

    def remove_all_buckets(self, identifier: str) -> None:
        validate_identifier(identifier)
        self._buckets.remove_all_buckets(identifier)

    def add_from_dict(
        self,
        identifier: str,
        bucket_config: list[dict[str, Any]],
        remove_old_buckets: bool = False,
    ) -> None:
        validate_bucket_config(bucket_config, TokenBucket)
        self._add_identifier(identifier)

        if remove_old_buckets:
            self.remove_all_buckets(identifier)

        for bucket in bucket_config:
            token_bucket: TokenBucket = TokenBucket(
                replenish_time=int(bucket["replenish_time"]),
                max_tokens=int(bucket["max_tokens"]),
            )
            self.add_bucket(identifier, token_bucket)

    def consume(self, identifier: str) -> bool:
        return_value: bool = True
        validate_identifier(identifier)
        if identifier not in self._buckets.keys():
            if not ThrottlerConfig.IDENTIFIER_FAIL_SAFE:
                raise KeyError(f"Invalid identifier: `{identifier}`")
            else:
                return return_value

        if ThrottlerConfig.ENABLE_THREAD_LOCK:
            self._lock.acquire()

        if not all(
            self._buckets.consume(identifier, str(bucket_key))
            for bucket_key in self._buckets[identifier].keys()
        ):
            return_value = False

        if self._lock.locked():
            self._lock.release()

        return return_value

    def enable(self, identifier: str) -> Any:
        def wrapper(fn: Callable):
            if not asyncio.iscoroutinefunction(fn):

                def inner(*args, **kwargs):
                    if not self.consume(identifier):
                        raise TokenThrottlerException()
                    return fn(*args, **kwargs)

                return inner
            else:

                async def inner(*args, **kwargs):
                    if not self.consume(identifier):
                        raise TokenThrottlerException()
                    return await fn(*args, **kwargs)

                return inner

        return wrapper
