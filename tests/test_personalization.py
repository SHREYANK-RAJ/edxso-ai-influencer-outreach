from app.models import Influencer
from app.personalization.llm import Personalizer

def test_fallback_lengths():
    i=Influencer("Sarah","Instagram","https://x",20000,4.0,"technology",["gadgets"],email="sarah@example.com")
    o=Personalizer().generate(i)
    assert 60 <= len(o.email_pitch.split()) <= 100
    assert 15 <= len(o.instagram_dm.split()) <= 35
