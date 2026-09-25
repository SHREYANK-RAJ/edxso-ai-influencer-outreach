from app.config import Settings, settings
from app.filtering import qualify
from app.models import Influencer
from app.personalization.llm import Personalizer
from app.pipeline import run_seed


def creator(followers=25_000, engagement=3.0):
    return Influencer("Creator", "YouTube", "https://example.test", followers, engagement,
                      "technology", ["technology"], email="creator@example.com")


def test_settings_loads_an_explicit_env_file(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("MIN_FOLLOWERS=20000\nMIN_ENGAGEMENT_RATE=5.0\nTARGET_NICHE=technology\n")
    configured = Settings(_env_file=env_file)
    assert configured.min_followers == 20_000
    assert configured.min_engagement_rate == 5.0


def test_minimum_followers_changes_qualification(monkeypatch):
    monkeypatch.setattr(settings, "min_followers", 20_000)
    assert not qualify(creator(followers=10_000)).qualified
    monkeypatch.setattr(settings, "min_followers", 5_000)
    assert qualify(creator(followers=10_000)).qualified


def test_minimum_engagement_changes_qualification(monkeypatch):
    monkeypatch.setattr(settings, "min_engagement_rate", 5.0)
    assert not qualify(creator(engagement=3.0)).qualified
    monkeypatch.setattr(settings, "min_engagement_rate", 1.0)
    assert qualify(creator(engagement=3.0)).qualified


def test_target_niche_changes_qualification(monkeypatch):
    monkeypatch.setattr(settings, "target_niche", "fitness")
    assert not qualify(creator()).qualified
    monkeypatch.setattr(settings, "target_niche", "technology")
    assert qualify(creator()).qualified


def test_seed_pipeline_has_results_and_rejection_reasons():
    items = run_seed()
    assert len(items) == 50
    assert any(item.qualified for item in items)
    assert any(not item.qualified and item.filter_reasons for item in items)


def test_fallback_personalization_is_recorded_without_groq(monkeypatch):
    monkeypatch.setattr(settings, "groq_api_key", None)
    item = next(item for item in run_seed() if item.qualified)
    personalized = Personalizer().generate(item)
    assert personalized.personalization_mode == "fallback_no_groq_key"
    assert personalized.email_pitch and personalized.instagram_dm
