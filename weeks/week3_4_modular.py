"""
WEEK 3-4: Writing and Structuring Locust Scripts
Goals demonstrated in this file:
- Modular & reusable code (POM-like ApiClient)
- Multiple tasks (signin + get_users) to model workflow
- Wait time + task weights (realistic behavior mix)
- Manual pass/fail control via catch_response (basic error-rate analysis)
"""

import logging
from locust import HttpUser, task, between
from common import config
from common.api_client import ApiAuth, ApiClient
from common.validators import validate_and_log

logger = logging.getLogger(__name__)

class MobileUserWeek3(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        auth = ApiAuth(auth0_user_id=config.AUTH0_USER_ID, bearer_token=config.BEARER_TOKEN)
        self.api = ApiClient(self.client, auth)

    @task(3)
    def signin(self):
        """Workflow step 1: signin (runs more often)."""
        with self.api.signin(timeout_s=config.REQUEST_TIMEOUT_S, catch=True) as resp:
            validate_and_log(
                resp,
                expected_statuses={200},
                name="W3 Signin",
                slow_threshold_ms=config.SIGNIN_SLA_MS,
            )

    @task(1)
    def get_users(self):
        """Workflow step 2: fetch users (runs less often)."""
        with self.api.get_users(timeout_s=config.REQUEST_TIMEOUT_S, catch=True) as resp:
            validate_and_log(
                resp,
                expected_statuses={200},
                name="W3 GetUsers",
                slow_threshold_ms=config.USERS_SLA_MS,
            )
