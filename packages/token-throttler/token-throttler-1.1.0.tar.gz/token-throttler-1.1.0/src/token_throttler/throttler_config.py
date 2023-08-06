from typing import Any


class ThrottlerConfig:
    ENABLE_THREAD_LOCK: bool = False
    IDENTIFIER_FAIL_SAFE: bool = False

    @classmethod
    def _configure(cls, config: dict) -> None:
        for key, value in config.items():
            if not hasattr(cls, key):
                return
            attr: Any = getattr(cls, key)
            if type(attr) != type(value):
                raise TypeError(f"Invalid type for configuration parameter `{key}`")
            setattr(cls, key, value)

    @classmethod
    def set(cls, config: dict = None) -> None:
        if config and isinstance(config, dict):
            cls._configure(config)
            return
        raise TypeError(
            f"Invalid configuration input. Expected <class 'dict'>, got {type(config)}"
        )
