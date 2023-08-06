from functools import wraps
from typing import Optional, Iterable, Union, Callable, Tuple, Dict, Union, List

import orjson
import redis
from redis import Sentinel
from redis.sentinel import MasterNotFoundError

NodeAddress = Tuple[str, int]
RecordValuesType = Dict[str, Union[str, int, float]]


class RetryException(Exception):
    """
    Raised when retry limit is exceeded.
    """

    def __init__(self, maximum_attempts: int) -> None:
        super().__init__(f"Maximum retry attempts of {maximum_attempts} exhausted.")


def retry_decorator(function) -> Callable:
    """
    Retry calling the wrapped method up to retry_attempts
    if any of handled_exceptions occurs. Raise
    RetryException if all retries fail.
    """

    @wraps(function)
    def wrapper(*args, **kwargs):
        cls = args[0]
        for attempt_number in range(cls.retry_attempts + 1):
            try:
                return function(*args, **kwargs)
            except cls.handled_exceptions as exc:
                if attempt_number < cls.retry_attempts:
                    cls.connect()
                else:
                    raise RetryException(cls.retry_attempts) from exc

    return wrapper


class RedisDAO:
    handled_exceptions = (MasterNotFoundError,)
    retry_attempts = 5

    def __init__(
        self,
        node_addresses: List[NodeAddress],
        password: Optional[str] = None,
        pseudo_schema_name: Optional[str] = None,
        master_name: str = "mymaster",
        use_sentinel: bool = True,
    ) -> None:
        self.node_addresses = node_addresses
        self.password = password
        self.master_name = master_name
        self.pseudo_schema_prefix = (
            f"{pseudo_schema_name}:" if pseudo_schema_name is not None else ""
        )
        self.use_sentinel = use_sentinel
        self.sentinels = None
        self.master = None

    def connect_sentinel(self) -> None:
        """
        Connect to Redis Sentinel cluster.
        """
        self.sentinels = Sentinel(
            self.node_addresses,
            socket_timeout=0.5,
            sentinel_kwargs={"password": self.password},
        )  # type: ignore
        host, port = self.sentinels.discover_master(self.master_name)  # type: ignore
        self.master = redis.StrictRedis(host=host, port=port, password=self.password)  # type: ignore

    def connect_single_node(self) -> None:
        """
        Connect to single node Redis instance.
        """
        self.master = redis.Redis(*self.node_addresses[0], password=self.password)  # type: ignore

    def connect(self) -> None:
        """
        Connect to a specified Redis instance.
        """
        if self.use_sentinel:
            self.connect_sentinel()
        else:
            self.connect_single_node()

    def disconnect(self) -> None:
        """
        De-reference Redis connection-related objects.
        """
        self.master = None
        self.sentinels = None

    def add_schema_to_key(self, key: str) -> str:
        """
        Prepend bare key with pseudo-schema.
        """
        return f"{self.pseudo_schema_prefix}{key}"

    @retry_decorator
    def get_one(self, key: str) -> Optional[str]:
        """
        Get value for key.
        """
        return self.master.get(self.add_schema_to_key(key))  # type: ignore

    @retry_decorator
    def get_many(self, keys: Iterable[str]) -> Dict[str, Optional[str]]:
        """
        Get key-value dicts for specified keys.,
        """
        return dict(
            zip(keys, self.master.mget(*(self.add_schema_to_key(key) for key in keys)))  # type: ignore
        )

    @retry_decorator
    def get_many_dicts(
        self, keys: Iterable[str]
    ) -> Dict[str, Optional[Dict[str, str]]]:
        """
        Get dict of key-dict for specified keys.
        """
        keys = list(keys)
        values = self.master.mget([self.add_schema_to_key(key) for key in keys])  # type: ignore
        return {
            key: (orjson.loads(value) if value is not None else None)
            for key, value in zip(keys, values)
        }

    @retry_decorator
    def update_one(self, key: str, value: str) -> bool:
        """
        Set value for key.
        """
        return self.master.set(self.add_schema_to_key(key), value)  # type: ignore

    @retry_decorator
    def update_many_if_unchanged(
        self,
        keys_values: Iterable[Tuple[str, RecordValuesType, RecordValuesType]],
        expiration_seconds: float,
    ) -> Dict[str, bool]:
        """
        Update each key in keys_values with new_value, if its current value
        matches expected_value.
        Return dict with keys and boolean update results (True if the key was updated).
        Operations for each key are atomic.
        """
        keys_values = list(keys_values)
        script = f"""
        local current_value = redis.call('get', KEYS[1])
        if current_value == ARGV[1] or current_value == false then
            redis.call('set', KEYS[1], ARGV[2])
            redis.call('expire', KEYS[1], {expiration_seconds}) 
            return 1
        end
        return 0
        """
        pipe = self.master.pipeline(transaction=False)  # type: ignore
        for key, expected_value, new_value in keys_values:
            pipe.eval(
                script,
                1,
                self.add_schema_to_key(key),
                orjson.dumps(expected_value, option=orjson.OPT_SORT_KEYS),
                orjson.dumps(new_value, option=orjson.OPT_SORT_KEYS),
            )
        result = pipe.execute()
        return {
            item[0]: bool(item_result) for item, item_result in zip(keys_values, result)
        }
