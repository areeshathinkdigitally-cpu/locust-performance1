import logging

logger = logging.getLogger(__name__)

def response_time_ms(resp) -> float:
    """Prefer Locust-measured response time if present; fallback to requests elapsed."""
    try:
        # In many Locust versions, response_time is available here (ms)
        return float(resp.request_meta.get("response_time"))
    except Exception:
        pass

    try:
        if resp.elapsed:
            return resp.elapsed.total_seconds() * 1000.0
    except Exception:
        pass

    return 0.0

def validate_and_log(resp, *, expected_statuses: set[int], name: str, slow_threshold_ms: int | None = None):
    """
    Shared validation:
    - fail on unexpected status
    - fail if slower than SLA (even if status is OK)
    - keep message short (demo-friendly)
    """
    status = getattr(resp, "status_code", None)
    elapsed_ms = response_time_ms(resp)

    if status not in expected_statuses:
        msg = f"{name} failed: {status}, {elapsed_ms:.0f} ms"
        logger.warning(msg + f" body={str(getattr(resp,'text',''))[:200]}")
        resp.failure(msg)
        return

    if slow_threshold_ms is not None and elapsed_ms > slow_threshold_ms:
        msg = f"{name} slow: {elapsed_ms:.0f} ms > {slow_threshold_ms} ms"
        logger.warning(msg)
        resp.failure(msg)
        return

    resp.success()
