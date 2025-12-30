from locust import HttpUser, task, between
from locust.shape import LoadTestShape   # 👈 important: shape comes from locust.shape


class MobileUser(HttpUser):
    """
    Simulates a React Native user hitting:
      - GET  /api/v2/Users/signin/{auth0UserId}
      - GET  /api/v2/Users
    Host (base URL) comes from locust.conf.
    """

    # Each simulated user waits 1–3 seconds between actions
    wait_time = between(1, 3)

    # auth0 user id from your token's `sub`
    AUTH0_USER_ID = "apple|000513.bf5e473b34904bc0bf480d06d5203cab.0525"

    # Paste only the JWT (without the leading "Bearer ")
    BEARER_TOKEN = (
        "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imprb0tlaGd3V3A3Nk5hejJnRUlEYSJ9."
        "eyJsb2dpbnNfY291bnQiOjYsImdpdmVuX25hbWUiOiJBcHAiLCJmYW1pbHlfbmFtZSI6IlRlc3RlciIsIm5pY2tuYW1lIjoiYXBwLnRlc3RlcnRkIiwibmFtZSI6IkFwcCBUZXN0ZXIiLCJwaWN0dXJlIjoiaHR0cHM6Ly9zLmdyYXZhdGFyLmNvbS9hdmF0YXIvNTUxNjMwYjdmODU3Y2Y0MjVjODc3OWQ5ZTRkYmY1MzY_cz00ODAmcj1wZyZkPWh0dHBzJTNBJTJGJTJGY2RuLmF1dGgwLmNvbSUyRmF2YXRhcnMlMkZhdC5wbmciLCJ1cGRhdGVkX2F0IjoiMjAyNS0xMi0xN1QwNzo1MDowMC42MDdaIiwiZW1haWwiOiJhcHAudGVzdGVydGRAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImlzcyI6Imh0dHBzOi8vY3ljbGUtdml0YS1kY2EudXMuYXV0aDAuY29tLyIsImF1ZCI6Imt1aTRkUUNyZllOSlp0Y1hZWG9UWFh0SmVsNWxCa0g0Iiwic3ViIjoiYXBwbGV8MDAwNTEzLmJmNWU0NzNiMzQ5MDRiYzBiZjQ4MGQwNmQ1MjAzY2FiLjA1MjUiLCJpYXQiOjE3NjU5NTc4MjUsImV4cCI6MTc2ODU0OTgyNSwic2lkIjoiUll6VWtLazQ0Y3FnLVlWdXBzcW1qRURLdVRHVHVVSUoiLCJhdXRoX3RpbWUiOjE3NjU5NTc4MjQsImFjciI6Imh0dHA6Ly9zY2hlbWFzLm9wZW5pZC5uZXQvcGFwZS9wb2xpY2llcy8yMDA3LzA2L211bHRpLWZhY3RvciIsImFtciI6WyJtZmEiXX0.vtdsnWmXgPAZ-qYGv3FOdc6oJ34lewvtl3doylSGbJ5BBBGg5qHKOvE9Gcy3bOF-xWOzJqrZr9OMxoc_5dVD8837vIwBPwEjtOtCZBdHvPUL3XsHV09HBqLyvM3yTEqnokYk2JSBIjEYuTacqZNYZDTOABd2JQdobpNdL86jAXyMW8gkwbB6OM6_UOUTrx1yUd-_sYNaAaNjHUtkJvrSHBfpVVpppX4UylC8XPeLqQXudo_OPfnoyOEkOZntcls7p9kVSRrDm7pEq8z0HlnKNifsNKu18iLJ1-r3UvZ3ZjyOEXYy-5W8aKuGvG4gIxbSsQA3fpiKAk6qnFNtRQkZQg"
    )

    def _auth_headers(self):
        """Common headers including Bearer token, reused for all calls."""
        return {
            "Authorization": f"Bearer {self.BEARER_TOKEN}",
            "Content-Type": "application/json",
        }

    @task(3)
    def signin(self):
        """
        Login task:
        GET /api/v2/Users/signin/{auth0UserId}
        Runs more often (weight = 3).
        """
        url = f"/api/v2/Users/signin/{self.AUTH0_USER_ID}"

        with self.client.get(
            url,
            headers=self._auth_headers(),
            name="GET /Users/signin/{auth0UserId}",
            catch_response=True,
        ) as resp:
            if resp.status_code != 200:
                print("SIGNIN RAW:", resp.status_code, resp.text)
                resp.failure(f"Login failed: {resp.status_code}, body: {resp.text}")

    @task(1)
    def get_users(self):
        """
        Data fetch task:
        GET /api/v2/Users
        Runs less frequently (weight = 1).
        """
        with self.client.get(
            "/api/v2/Users",
            headers=self._auth_headers(),
            name="GET /Users",
            catch_response=True,
        ) as resp:
            if resp.status_code != 200:
                print("USERS RAW:", resp.status_code, resp.text)
                resp.failure(f"Users failed: {resp.status_code}, body: {resp.text}")

"gradually increases user "

class StagedLoadShape(LoadTestShape):
    """
    Custom load pattern to control users over time.

    Pattern:
      - Stage 1 (warm-up):  10 seconds, up to 5 users (spawn 1 user/sec)
      - Stage 2 (steady):   20 seconds, up to 10 users (spawn 2 users/sec)
      - Stage 3 (stress):   30 seconds, up to 20 users (spawn 5 users/sec)
      - Then: stop test (returns None)
    """

    stages = [
        {"duration": 10, "users": 5, "spawn_rate": 1},   # 0–10s
        {"duration": 20, "users": 10, "spawn_rate": 2},  # 10–30s
        {"duration": 30, "users": 20, "spawn_rate": 5},  # 30–60s
    ]

    def tick(self):
        """
        Called once per second by Locust.

        Return:
          (user_count, spawn_rate) for the current second,
          or None when we want the test to stop.
        """
        run_time = self.get_run_time()  # seconds since test start

        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]
            run_time -= stage["duration"]

        # All stages done -> stop the load test
        return None
