import csv
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class Identity:
    auth0_user_id: str
    bearer_token: str

def load_identities_csv(path: str) -> List[Identity]:
    identities: List[Identity] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"auth0_user_id", "bearer_token"}
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError(f"CSV must include columns {sorted(required)}. Found: {reader.fieldnames}")

        for row in reader:
            auth0 = (row.get("auth0_user_id") or "").strip()
            token = (row.get("bearer_token") or "").strip()
            if auth0 and token and "PASTE_TOKEN" not in token:
                identities.append(Identity(auth0_user_id=auth0, bearer_token=token))

    return identities
