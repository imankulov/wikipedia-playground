import os
import time

# pubsub settings and Redis client
redis_url = os.environ["REDIS_URL"]
pubsub_channel = "wiki"

# Constants for aggregation and expiration
expiration_timeout_sec = 1800
aggregation_interval_sec = 10


def current_timestamp():
    """
    Get a new timestamp every "aggregation_interval_sec" seconds.
    """
    return int(time.time() // aggregation_interval_sec) * aggregation_interval_sec


def all_timestamps():
    """
    Get the list of all timestamps for which it makes sense yet to extract some data.
    """
    ts = current_timestamp()
    return list(range(ts - expiration_timeout_sec, ts, aggregation_interval_sec))
