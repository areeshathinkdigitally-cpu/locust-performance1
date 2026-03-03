from dataclasses import dataclass

@dataclass(frozen=True)
class ApiAuth:
    auth0_user_id: str
    bearer_token: str

class ApiClient:
    """POM-like 'service object' wrapper around API endpoints."""

    def __init__(self, http_client, auth: ApiAuth):
        self.client = http_client
        self.auth = auth

    def headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.auth.bearer_token}",
            "Content-Type": "application/json",
        }

    def signin(self, *, timeout_s: float, catch: bool = True):
        url = f"/api/v2/Users/signin/{self.auth.auth0_user_id}"
        return self.client.get(
            url,
            headers=self.headers(),
            name="GET /Users/signin/{auth0UserId}",
            timeout=timeout_s,
            catch_response=catch,
        )

    def get_users(self, *, timeout_s: float, catch: bool = True):
        return self.client.get(
            "/api/v2/Users",
            headers=self.headers(),
            name="GET /Users",
            timeout=timeout_s,
            catch_response=catch,
        )
