import json

import httpx
from fastapi.testclient import TestClient

from app.api import app
from app.config import settings
from app.discovery.youtube import YouTubeDiscovery, YouTubeDiscoveryError
from app.models import Influencer
from app.personalization.llm import Personalizer
from app.sending.service import OutreachService
from app.storage.db import OutreachDB


def influencer():
    return Influencer("Creator", "YouTube", "https://example.test", 25_000, 3.0,
                      "technology", ["gadgets"], email="creator@example.com")


def test_youtube_missing_key_is_safe(monkeypatch):
    monkeypatch.setattr(settings, "youtube_api_key", None)
    try:
        YouTubeDiscovery()
    except YouTubeDiscoveryError as exc:
        assert "YOUTUBE_API_KEY" in str(exc)
    else:
        raise AssertionError("missing API key should fail safely")


def test_youtube_http_error_is_safe(monkeypatch):
    class Response:
        status_code = 403
        request = httpx.Request("GET", "https://example.test")

        def raise_for_status(self):
            raise httpx.HTTPStatusError("forbidden", request=self.request, response=self)

    class Client:
        def __init__(self, **_kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def get(self, *_args, **_kwargs):
            return Response()

    monkeypatch.setattr("app.discovery.youtube.httpx.Client", Client)
    try:
        YouTubeDiscovery(api_key="test-key")._get("search", {})
    except YouTubeDiscoveryError as exc:
        assert "rejected" in str(exc)
    else:
        raise AssertionError("HTTP error should be converted to a safe error")


def test_youtube_results_are_normalized(monkeypatch):
    discovery = YouTubeDiscovery(api_key="test-key")
    responses = [
        {"items": [{"snippet": {"channelId": "channel-1"}}]},
        {"items": [{"id": "channel-1", "snippet": {"title": "AI Creator", "description": "Email ai@example.com"},
                    "statistics": {"subscriberCount": "12000"}}]},
    ]
    monkeypatch.setattr(discovery, "_get", lambda *_args: responses.pop(0))
    result = discovery.discover("AI creators India", limit=1)
    assert len(result) == 1
    assert result[0].platform == "YouTube"
    assert result[0].followers == 12_000
    assert result[0].email == "ai@example.com"
    assert result[0].category == "AI creators India"


def test_groq_response_path(monkeypatch):
    class Completion:
        message = type("Message", (), {"content": json.dumps({
            "email_pitch": "A personalized email pitch.", "instagram_dm": "A personalized DM."
        })})()

    class Client:
        chat = type("Chat", (), {"completions": type("Completions", (), {
            "create": staticmethod(lambda **_kwargs: type("Result", (), {"choices": [Completion()]})())
        })()})()

    monkeypatch.setattr(settings, "groq_api_key", None)
    personalizer = Personalizer()
    personalizer.client = Client()
    result = personalizer.generate(influencer())
    assert result.personalization_mode == "groq"
    assert result.email_pitch == "A personalized email pitch."


def test_tracker_records_and_prevents_duplicates(tmp_path):
    service = OutreachService(OutreachDB(tmp_path / "outreach.db"))
    assert service.send_email(influencer(), dry_run=True)["status"] == "simulated"
    assert service.send_email(influencer(), dry_run=True)["status"] == "skipped"
    assert len(service.db.records()) == 1


def test_fastapi_endpoints():
    client = TestClient(app)
    assert client.get("/health").json() == {"status": "ok"}
    assert len(client.get("/influencers").json()) == 50
