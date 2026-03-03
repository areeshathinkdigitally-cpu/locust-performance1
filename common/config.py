import os

def env_str(name: str, default: str = "") -> str:
    val = os.getenv(name, default)
    return val.strip()

def env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except Exception:
        return default

def env_float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, str(default)))
    except Exception:
        return default

# Core request config
REQUEST_TIMEOUT_S = env_float("LOCUST_REQUEST_TIMEOUT_S", 20.0)

# Optional single-identity mode (Week 1-6)
AUTH0_USER_ID = env_str("LOCUST_AUTH0_USER_ID", "google-oauth2|118195303526159754459")
BEARER_TOKEN = env_str("LOCUST_BEARER_TOKEN", "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imprb0tlaGd3V3A3Nk5hejJnRUlEYSJ9.eyJsb2dpbnNfY291bnQiOjEsImdpdmVuX25hbWUiOiJGYWl6YSIsImZhbWlseV9uYW1lIjoiWmFmYXIiLCJuaWNrbmFtZSI6ImZhaXphOTk4MjYiLCJuYW1lIjoiRmFpemEgWmFmYXIiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jSjM3Y2ZLQ0FjRFVRa0FROHNsY0NZMVJybVNaQWRnUFB5LTdORkQzRXRGczQ3NGt3PXM5Ni1jIiwidXBkYXRlZF9hdCI6IjIwMjYtMDItMjVUMTA6MTI6MjEuMTgyWiIsImVtYWlsIjoiZmFpemE5OTgyNkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9jeWNsZS12aXRhLWRjYS51cy5hdXRoMC5jb20vIiwiYXVkIjoia3VpNGRRQ3JmWU5KWnRjWFlYb1RYWHRKZWw1bEJrSDQiLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExODE5NTMwMzUyNjE1OTc1NDQ1OSIsImlhdCI6MTc3MjAxNDM0MiwiZXhwIjoxNzc0NjA2MzQyLCJzaWQiOiJhN2VobnAwTWxqVjhwM1ZhMjdPUmhZcGhGX0dNRDFHYSIsImF1dGhfdGltZSI6MTc3MjAxNDM0MSwiYWNyIjoiaHR0cDovL3NjaGVtYXMub3BlbmlkLm5ldC9wYXBlL3BvbGljaWVzLzIwMDcvMDYvbXVsdGktZmFjdG9yIiwiYW1yIjpbIm1mYSJdfQ.sPLa9UZeWbJtKmVkZ6dlN8s2Obk2W6-0nR6O3gKnMXBeDADf5XXFkuJGon85DMGSNZnaZKWEPAyYfSyuO5RBbAaZSHWuhyXD7kTMt8g2HmfW5ybwIdY2Vi-hnlxf6-Ob8nveZkKEt8Dgr4C3U7d2705RLcZxoUFAjqE6gseGS_B-iUP1Y_0ONDoeBp4BKxyVibLcyMor_OmO28yE7sHX9yVifY9LtoolyByJSHStYuijz-Mc1KGjv4oibYtnYAexV62UaCaYxfrefxgjjR1SXjLh6rTJdtAWEmNDNSY-q71H9VB8uGi6KdjNN_Hua1CFAZEPYQO1I9Wu2O4ZMDarDQ")

# SLA thresholds
SIGNIN_SLA_MS = env_int("LOCUST_SIGNIN_SLA_MS", 3000)
USERS_SLA_MS = env_int("LOCUST_USERS_SLA_MS", 3000)

# Week 7-8 parameterized identities
USERS_CSV = env_str("LOCUST_USERS_CSV", "data/users.example.csv")

# Week 5-6 pattern selector
LOAD_PATTERN = env_str("LOCUST_LOAD_PATTERN", "ramp")  # ramp | spike | stress
