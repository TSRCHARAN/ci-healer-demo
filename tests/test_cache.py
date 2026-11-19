import os
import time

from shop.cache import warm_cache

# SIMULATED FLAKE, for the demo: the "backend" is slow on a run's first attempt and fast on a
# re-run, so CI reliably fails once and then passes when re-run - exactly how a real
# timing-dependent test behaves on a bad day, minus the coin toss.
SLOW_BACKEND = os.environ.get("GITHUB_RUN_ATTEMPT", "1") == "1"


def test_cache_warms_within_deadline():
    start = time.monotonic()
    warm_cache(backend_latency=0.3 if SLOW_BACKEND else 0.01)
    elapsed = time.monotonic() - start
    assert elapsed < 0.15, f"TimeoutError: cache warm-up took {elapsed:.3f}s (deadline 0.150s)"
