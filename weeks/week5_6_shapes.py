
import logging
from locust import HttpUser, task, between
from locust.shape import LoadTestShape

from common import config
from common.api_client import ApiAuth, ApiClient
from common.validators import validate_and_log
from common.monitoring import ResourceMonitor

logger = logging.getLogger(__name__)

# --- Load patterns (select one with LOCUST_LOAD_PATTERN=ramp|spike|stress) ---

class RampShape(LoadTestShape):
    """Smooth ramp-up: every 30s add 10 users until max."""
    step_time = 30
    step_users = 10
    max_users = 50
    spawn_rate = 5

    def tick(self):
        run_time = self.get_run_time()
        current_step = int(run_time // self.step_time) + 1
        users = min(current_step * self.step_users, self.max_users)
        return (users, self.spawn_rate)

class SpikeShape(LoadTestShape):
    """Spike: jump to 50 users fast, hold, then stop."""
    def tick(self):
        t = self.get_run_time()
        if t < 10:
            return (50, 25)   # spike quickly
        if t < 40:
            return (50, 1)    # hold
        return None

class StressShape(LoadTestShape):
    """Stress: ramp to 100 users, hold, then stop."""
    def tick(self):
        t = self.get_run_time()
        if t < 60:
            return (int(t * 100 / 60), 10)  # ramp over 60s
        if t < 120:
            return (100, 5)                 # hold
        return None

# Choose the active shape by env var (simple for demos)
if config.LOAD_PATTERN == "spike":
    class ActiveShape(SpikeShape): pass
elif config.LOAD_PATTERN == "stress":
    class ActiveShape(StressShape): pass
else:
    class ActiveShape(RampShape): pass


class MobileUserWeek5(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        auth = ApiAuth(auth0_user_id=config.AUTH0_USER_ID, bearer_token=config.BEARER_TOKEN)
        self.api = ApiClient(self.client, auth)
        self.monitor = ResourceMonitor(interval_s=5)

    @task(2)
    def signin(self):
        self.monitor.maybe_log()
        with self.api.signin(timeout_s=config.REQUEST_TIMEOUT_S, catch=True) as resp:
            validate_and_log(resp, expected_statuses={200}, name="W5 Signin", slow_threshold_ms=config.SIGNIN_SLA_MS)

    @task(1)
    def get_users(self):
        self.monitor.maybe_log()
        with self.api.get_users(timeout_s=config.REQUEST_TIMEOUT_S, catch=True) as resp:
            validate_and_log(resp, expected_statuses={200}, name="W5 GetUsers", slow_threshold_ms=config.USERS_SLA_MS)
