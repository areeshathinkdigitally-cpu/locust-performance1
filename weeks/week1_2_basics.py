from locust import HttpUser, task, between
from common import config

class MobileUserWeek1(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_users_basic(self):
        headers = {
            "Authorization": f"Bearer {config.BEARER_TOKEN}",
            "Content-Type": "application/json",
        }
        self.client.get(
            "/api/v2/Users",
            headers=headers,
            name="W1 GET /Users",
            timeout=config.REQUEST_TIMEOUT_S,
        )
