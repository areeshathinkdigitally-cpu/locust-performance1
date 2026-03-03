"""
WEEK 1-2: Introduction and Setup
Goals demonstrated in this file:
- Locust basics: HttpUser, task, wait_time
- First simple test simulating user behavior
- Use Locust UI to watch RPS, response time, failures
"""

from locust import HttpUser, task, between
from common import config

class MobileUserWeek1(HttpUser):
    # Human-like pacing
    wait_time = between(1, 3)

    @task
    def get_users_basic(self):
        """Single simple request (start here for demos)."""
        headers = {
            "Authorization": f"Bearer {config.BEARER_TOKEN}",
            "Content-Type": "application/json",
        }
        # Keep it simple: no custom success/failure logic yet
        self.client.get(
            "/api/v2/Users",
            headers=headers,
            name="W1 GET /Users",
            timeout=config.REQUEST_TIMEOUT_S,
        )
