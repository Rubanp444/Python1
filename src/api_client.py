"""Task 3: API client with retries, nested JSON access and HMAC validation."""

import hashlib
import hmac
import os
from typing import Optional, Union

import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()

API_KEY = os.getenv("API_KEY")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
USERS_URL = "https://jsonplaceholder.typicode.com/users"


def build_session() -> requests.Session:
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def fetch_users(session: Optional[requests.Session] = None) -> list:
    session = session or build_session()
    response = session.get(USERS_URL, timeout=10)
    response.raise_for_status()
    return response.json()


def first_user_summary(user: dict) -> str:
    """Nested access with .get() only; missing values -> 'Not Available'."""
    na = "Not Available"
    address = user.get("address") or {}
    geo = address.get("geo") or {}
    company = user.get("company") or {}
    city = address.get("city", na)
    lat = geo.get("lat", na)
    # Key is "zip" on purpose (the API uses "zipcode") to show the fallback.
    zip_code = address.get("zip", na)
    comp = company.get("name", na)
    return f"City: {city} | Latitude: {lat} | Zip: {zip_code} | Company: {comp}"


def verify_signature(
    payload: Union[str, bytes], signature: str, secret: Union[str, bytes]
) -> bool:
    """Check an HMAC-SHA256 hex signature using a constant-time comparison."""
    if isinstance(payload, str):
        payload = payload.encode()
    if isinstance(secret, str):
        secret = secret.encode()
    expected = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
