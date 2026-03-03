"""
WEEK 7-8: Scaling and Integration
Goals demonstrated in this file:
- Distributed-ready approach (works as master/worker; nothing special needed in script)
- Parameterized test data (multiple identities from CSV)
- Stronger error handling + timeouts + clean logs
- End-to-end style workflow tasks + report friendliness (stable request names)
"""

import logging
import random
from locust import HttpUser, task, between
from common import config
from common.api_client import ApiAuth, ApiClient
from common.validators import validate_and_log
from common.data_loader import load_identities_csv, Identity

logger = logging.getLogger(__name__)

# Load identities once per process (each worker loads its own copy)
IDENTITIES: list[Identity] = load_identities_csv(config.USERS_CSV)

class MobileUserWeek7(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        if IDENTITIES:
            chosen = random.choice(IDENTITIES)
            auth0 = chosen.auth0_user_id
            token = chosen.bearer_token
        else:
            # fallback to env vars (demo-safe)
            auth0 = config.AUTH0_USER_ID
            token = config.BEARER_TOKEN

        auth = ApiAuth(auth0_user_id=auth0, bearer_token=token)
        self.api = ApiClient(self.client, auth)

    @task(3)
    def signin(self):
        with self.api.signin(timeout_s=config.REQUEST_TIMEOUT_S, catch=True) as resp:
            validate_and_log(resp, expected_statuses={200}, name="W7 Signin", slow_threshold_ms=config.SIGNIN_SLA_MS)

    @task(2)
    def get_users(self):
        with self.api.get_users(timeout_s=config.REQUEST_TIMEOUT_S, catch=True) as resp:
            validate_and_log(resp, expected_statuses={200}, name="W7 GetUsers", slow_threshold_ms=config.USERS_SLA_MS)

    @task(1)
    def end_to_end_flow(self):
        """E2E mini-flow: signin -> users (demo of a complete user journey)."""
        with self.api.signin(timeout_s=config.REQUEST_TIMEOUT_S, catch=True) as r1:
            validate_and_log(r1, expected_statuses={200}, name="W7 E2E Signin", slow_threshold_ms=config.SIGNIN_SLA_MS)
        with self.api.get_users(timeout_s=config.REQUEST_TIMEOUT_S, catch=True) as r2:
            validate_and_log(r2, expected_statuses={200}, name="W7 E2E GetUsers", slow_threshold_ms=config.USERS_SLA_MS)
        return None