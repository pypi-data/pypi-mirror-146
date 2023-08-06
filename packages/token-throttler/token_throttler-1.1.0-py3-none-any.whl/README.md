# Token throttler

![Coverage](https://img.shields.io/gitlab/coverage/vojko.pribudic/token-throttler/main?job_name=tests)
![Version](https://img.shields.io/pypi/pyversions/token-throttler)
![Downloads](https://pepy.tech/badge/token-throttler)
![License](https://img.shields.io/pypi/l/token-throttler)

**Token throttler** is an extendable rate-limiting library somewhat based on a [token bucket algorithm](https://en.wikipedia.org/wiki/Token_bucket).

## Table of contents

1. [ Installation ](#installation)
2. [ Features ](#features)
3. [ Usage ](#usage)
    1. [ Manual usage example ](#usage-manual)
    2. [ Decorator usage example ](#usage-decorator)
4. [ Storage ](#storage)
   1. [ Redis storage example ](#storage-redis)
5. [ Configuration ](#configuration)
   1. [ Configuration usage ](#configuration-usage)

<a name="installation"></a>
## 1. Installation

Token throttler is available on PyPI:
```console 
$ python -m pip install token-throttler
```
Token throttler officially supports Python >= 3.7.

<a name="features"></a>
## 2. Features

- Global throttler(s) configuration
- Configurable token throttler cost and identifier
- Multiple buckets per throttler per identifier
- Buckets can be added/removed manually or by a `dict` configuration
- Manual usage or usage via decorator
- Decorator usage supports async code too
- Custom decorator can be written
- Extendable storage engine (eg. Redis)

<a name="usage"></a>
## 3. Usage

Token throttler supports both manual usage and via decorator.

Decorator usage supports both async and sync.

<a name="usage-manual"></a>
### 1) Manual usage example:

```python
from token_throttler import TokenBucket, TokenThrottler
from token_throttler.storage import RuntimeStorage

throttler: TokenThrottler = TokenThrottler(cost=1, storage=RuntimeStorage())
throttler.add_bucket(identifier="hello_world", bucket=TokenBucket(replenish_time=10, max_tokens=10))
throttler.add_bucket(identifier="hello_world", bucket=TokenBucket(replenish_time=30, max_tokens=20))


def hello_world() -> None:
    print("Hello World")


for i in range(10):
    throttler.consume(identifier="hello_world")
    hello_world()

if throttler.consume(identifier="hello_world"):
    hello_world()
else:
    print("bucket_one ran out of tokens")
```

<a name="usage-decorator"></a>
### 2) Decorator usage example:

```python
from token_throttler import TokenBucket, TokenThrottler, TokenThrottlerException
from token_throttler.storage import RuntimeStorage

throttler: TokenThrottler = TokenThrottler(1, RuntimeStorage())
throttler.add_bucket("hello_world", TokenBucket(10, 10))
throttler.add_bucket("hello_world", TokenBucket(30, 20))


@throttler.enable("hello_world")
def hello_world() -> None:
    print("Hello World")


for i in range(10):
    hello_world()

try:
    hello_world()
except TokenThrottlerException:
    print("bucket_one ran out of tokens")
```

For other examples see [**examples**](https://gitlab.com/vojko.pribudic/token-throttler/-/tree/main/examples) directory.

<a name="storage"></a>
## 4. Storage

Currently, token throttler supports `RuntimeStorage` but is very easy to extend.
If you want your own storage engine, feel free to extend the `token_throttler.storage.BucketStorage` class.

<a name="storage-redis"></a>
### 1) Redis storage example:

```python
import pickle
from datetime import timedelta
from typing import Union

from redis import StrictRedis

from token_throttler import TokenBucket, TokenThrottler
from token_throttler.storage import BucketStorage


class RedisStorage(BucketStorage):
    def __init__(self, connection_string: str, delimiter: str) -> None:
        super().__init__()
        self.redis: StrictRedis = StrictRedis.from_url(url=connection_string)
        self.delimiter: str = delimiter

    def _create_bucket(self, cache_key: str) -> TokenBucket:
        bucket_info: list[str] = cache_key.split(self.delimiter)
        token_bucket: TokenBucket = TokenBucket(
            int(bucket_info[1]), int(bucket_info[-1])
        )
        token_bucket.cost = int(bucket_info[2])
        token_bucket.identifier = bucket_info[0]
        return token_bucket

    def _delete_bucket(self, cache_key: str) -> None:
        self.redis.delete(cache_key)

    def _save_bucket(self, cache_key: str, bucket: TokenBucket) -> None:
        self.redis.setex(
            cache_key,
            timedelta(seconds=bucket.replenish_time),
            pickle.dumps(bucket),
        )

    def get_bucket(self, identifier: str, bucket_key: str) -> Union[TokenBucket, None]:
        cache_key: Union[str, None] = self.get(identifier, {}).get(bucket_key, None)
        if not cache_key:
            return None
        bucket: Union[bytes, None] = self.redis.get(cache_key)
        if not bucket:
            return None
        return pickle.loads(bucket)

    def get_all_buckets(self, identifier: str) -> Union[dict[str, TokenBucket], None]:
        buckets: dict[str, TokenBucket] = {}
        stored_buckets: dict[str, str] = self.get(identifier, None)
        if not stored_buckets:
            return None
        for bucket_key in stored_buckets:
            bucket: Union[TokenBucket, None] = self.get_bucket(identifier, bucket_key)
            if not bucket:
                continue
            buckets[bucket_key] = bucket
        return None if not buckets else buckets

    def add_bucket(self, bucket: TokenBucket) -> None:
        cache_key: str = f"{self.delimiter}".join(
            map(
                str,
                [
                    bucket.identifier,
                    bucket.replenish_time,
                    bucket.cost,
                    bucket.max_tokens,
                ],
            )
        )
        self[str(bucket.identifier)][str(bucket.replenish_time)] = cache_key
        self._save_bucket(cache_key, bucket)

    def remove_bucket(self, identifier: str, bucket_key: str) -> None:
        if identifier not in self:
            return None
        bucket: Union[str, None] = self.get(identifier, {}).get(bucket_key, None)
        if bucket:
            self._delete_bucket(self[identifier][bucket_key])
            del self[identifier][bucket_key]
        if not self[identifier]:
            del self[identifier]

    def remove_all_buckets(self, identifier: str) -> None:
        if identifier not in self:
            return None
        for bucket_key in self[identifier]:
            self._delete_bucket(self[identifier][bucket_key])
        del self[identifier]

    def replenish(self, bucket: TokenBucket) -> None:
        pass

    def consume(self, identifier: str, bucket_key: str) -> bool:
        cache_key: str = self[identifier][bucket_key]
        bucket: Union[TokenBucket, None] = self.get_bucket(identifier, bucket_key)
        if not bucket:
            bucket = self._create_bucket(cache_key)
            self.add_bucket(bucket)
        bucket_state: bool = bucket.consume()
        self._save_bucket(cache_key, bucket)
        return bucket_state


throttler: TokenThrottler = TokenThrottler(1, RedisStorage(connection_string="connection-string-to-redis", delimiter="||"))
...
```

<a name="configuration"></a>
## 5. Configuration

Token throttler supports global configuration by making use of `ThrottlerConfig` class.

Configuration params:
- `IDENTIFIER_FAIL_SAFE` - if invalid identifier is given as a param for the `consume` method and `IDENTIFIER_FAIL_SAFE`
is set to `True`, no `KeyError` exception will be raised and `consume` will act like a limitless bucket is being consumed.
- `ENABLE_THREAD_LOCK` - if set to `True`, throttler will acquire a thread lock upon calling `consume` method and release
the lock once the `consume` is finished. This avoids various race conditions at a slight performance cost.

<a name="configuration-usage"></a>
### Configuration usage

```python
from token_throttler import ThrottlerConfig, TokenBucket, TokenThrottler
from token_throttler.storage import RuntimeStorage

ThrottlerConfig.set({
   "ENABLE_THREAD_LOCK": False,
   "IDENTIFIER_FAIL_SAFE": True,
})
throttler: TokenThrottler = TokenThrottler(1, RuntimeStorage())
throttler.add_bucket("hello_world", TokenBucket(10, 10))
throttler.add_bucket("hello_world", TokenBucket(30, 20))
...
```
