"""Run: python -m scripts.task3_demo  (needs internet)"""

import hashlib
import hmac

from src.api_client import (
    WEBHOOK_SECRET,
    build_session,
    fetch_users,
    first_user_summary,
    verify_signature,
)

if __name__ == "__main__":
    users = fetch_users(build_session())
    for u in users[:5]:
        print(f"{u['id']} - {u['name']} - {u['email']}")
    print(first_user_summary(users[0]))

    secret = WEBHOOK_SECRET or "demo"
    payload = b'{"event": "employee.created"}'
    sig = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    print(
        f"Valid: {verify_signature(payload, sig, secret)} | "
        f"Tampered: {verify_signature(payload + b'x', sig, secret)} | "
        f"Wrong secret: {verify_signature(payload, sig, 'wrong')}"
    )
