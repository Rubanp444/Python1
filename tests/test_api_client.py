import hashlib
import hmac

from src import api_client as api


def _sign(payload: bytes, secret: str) -> str:
    return hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()


def test_verify_signature_valid():
    payload = b'{"a": 1}'
    assert api.verify_signature(payload, _sign(payload, "s3cret"), "s3cret")


def test_verify_signature_tampered():
    payload = b'{"a": 1}'
    sig = _sign(payload, "s3cret")
    assert not api.verify_signature(b'{"a": 2}', sig, "s3cret")


def test_verify_signature_wrong_secret_and_str_input():
    sig = _sign(b"hello", "s3cret")
    assert not api.verify_signature("hello", sig, "other")
    assert api.verify_signature("hello", sig, "s3cret")


def test_first_user_summary_missing_values():
    user = {
        "address": {"city": "Gwenborough", "geo": {"lat": "-37.3159"}},
        "company": {"name": "Romaguera-Crona"},
    }
    text = api.first_user_summary(user)
    assert "City: Gwenborough" in text
    assert "Zip: Not Available" in text
    assert api.first_user_summary({}).count("Not Available") == 4


def test_session_has_retry_and_fetch_users():
    session = api.build_session()
    retry = session.get_adapter("https://x.com").max_retries
    assert retry.total == 3 and retry.backoff_factor == 1

    class FakeResp:
        def raise_for_status(self):
            pass

        def json(self):
            return [{"id": 1}]

    class FakeSession:
        def get(self, url, timeout):
            return FakeResp()

    assert api.fetch_users(FakeSession()) == [{"id": 1}]
