from app.models import Influencer
from app.filtering import qualify

def test_qualified():
    i=Influencer("A","YouTube","https://x",25000,3.0,"technology",email="a@example.com")
    assert qualify(i).qualified

def test_missing_email_rejected():
    i=Influencer("A","YouTube","https://x",25000,3.0,"technology")
    o=qualify(i)
    assert not o.qualified
    assert "Public contact email not found" in o.filter_reasons

def test_large_creator_rejected():
    i=Influencer("A","YouTube","https://x",250000,3.0,"technology",email="a@example.com")
    assert not qualify(i).qualified
