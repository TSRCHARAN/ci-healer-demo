"""A pretend product cache whose warm-up time depends on a (simulated) slow backend."""

import time


def warm_cache(backend_latency: float) -> dict[str, int]:
    time.sleep(backend_latency)
    return {"sku-1": 10, "sku-2": 25}
