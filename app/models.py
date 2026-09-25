from dataclasses import dataclass, field

@dataclass
class Influencer:
    name: str
    platform: str
    profile_url: str
    followers: int | None
    engagement_rate: float | None
    category: str
    content_themes: list[str] = field(default_factory=list)
    bio: str = ""
    recent_content: list[str] = field(default_factory=list)
    email: str = "Not Found"
    website: str = "Not Found"
    geography: str = "Not Found"
    source: str = ""
    source_url: str = ""
    qualified: bool = False
    filter_reasons: list[str] = field(default_factory=list)
    email_pitch: str = ""
    instagram_dm: str = ""
<<<<<<< HEAD
    personalization_mode: str = "not_generated"
=======
>>>>>>> origin/main
