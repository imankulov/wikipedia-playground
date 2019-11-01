"""Utility module with helper functions, common for all exposed scripts."""

import os
import time

# pubsub settings and Redis client
redis_url = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379")
pubsub_channel = os.environ.get("PUBSUB_CHANNEL", "wiki")

# Constants for aggregation and plotting
history_sec = 1800
aggregation_interval_sec = 10


def current_timestamp():
    """Get a new timestamp every "aggregation_interval_sec" seconds."""
    return int(time.time() // aggregation_interval_sec) * aggregation_interval_sec


def all_timestamps():
    """Get the list of timestamps within history_sec interval."""
    ts = current_timestamp()
    return list(range(ts - history_sec, ts, aggregation_interval_sec))
