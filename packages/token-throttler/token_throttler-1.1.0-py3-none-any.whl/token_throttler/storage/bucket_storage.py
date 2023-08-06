import abc
from typing import Union

from .. import TokenBucket


class BucketStorage(dict, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_bucket(
        self, identifier: str, bucket_key: str
    ) -> Union[TokenBucket, None]:  # pragma: no cover
        raise NotImplementedError()

    @abc.abstractmethod
    def get_all_buckets(
        self, identifier: str
    ) -> Union[dict[str, TokenBucket], None]:  # pragma: no cover
        raise NotImplementedError()

    @abc.abstractmethod
    def add_bucket(self, bucket: TokenBucket) -> None:  # pragma: no cover
        raise NotImplementedError()

    @abc.abstractmethod
    def remove_bucket(
        self, identifier: str, bucket_key: str
    ) -> None:  # pragma: no cover
        raise NotImplementedError()

    @abc.abstractmethod
    def remove_all_buckets(self, identifier: str) -> None:  # pragma: no cover
        raise NotImplementedError()

    @abc.abstractmethod
    def replenish(self, bucket: TokenBucket) -> None:  # pragma: no cover
        raise NotImplementedError()

    @abc.abstractmethod
    def consume(self, identifier: str, bucket_key: str) -> bool:  # pragma: no cover
        raise NotImplementedError()
