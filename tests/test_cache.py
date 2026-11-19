import random
import time

from shop.cache import warm_cache


def test_cache_warms_within_deadline():
    # The (simulated) backend is sometimes slow, so this test fails about half the time.
    start = time.monotonic()
    warm_cache(backend_latency=random.uniform(0.0, 0.3))
    elapsed = time.monotonic() - start
    assert elapsed < 0.15, f"TimeoutError: cache warm-up took {elapsed:.3f}s (deadline 0.150s)"
