import time
import logging
try:
    import psutil
except Exception:
    psutil = None

logger = logging.getLogger(__name__)

class ResourceMonitor:
    """Optional: log local CPU/RAM every N seconds (Week 5-6 concept)."""

    def __init__(self, interval_s: int = 5):
        self.interval_s = interval_s
        self._last = 0.0

    def maybe_log(self):
        if psutil is None:
            return
        now = time.time()
        if now - self._last < self.interval_s:
            return
        self._last = now

        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory().percent
        logger.info(f"[RESOURCE] cpu={cpu:.1f}% mem={mem:.1f}%")
