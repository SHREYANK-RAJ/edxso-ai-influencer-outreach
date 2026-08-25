import statistics
import httpx
from app.models import Influencer
from app.utils.email import extract_public_email
from app.config import settings

BASE = "https://www.googleapis.com/youtube/v3"

class YouTubeDiscovery:
    def __init__(self, api_key=None):
        self.api_key = api_key or settings.youtube_api_key
        if not self.api_key:
            raise ValueError("YOUTUBE_API_KEY is required")

    def _get(self, path, params):
        params = {**params, "key": self.api_key}
        with httpx.Client(timeout=20) as client:
            r = client.get(f"{BASE}/{path}", params=params)
            r.raise_for_status()
            return r.json()

    def discover(self, niche="technology", limit=50, region="IN"):
        out, token = [], None
        while len(out) < limit:
            params = {"part":"snippet","q":niche,"type":"channel",
                      "maxResults":min(50, limit-len(out)),"regionCode":region}
            if token: params["pageToken"] = token
            data = self._get("search", params)
            ids = [x["snippet"]["channelId"] for x in data.get("items", [])]
            if not ids: break
            stats = self._get("channels", {"part":"snippet,statistics","id":",".join(ids)})
            for ch in stats.get("items", []):
                s, sn = ch.get("statistics", {}), ch.get("snippet", {})
                subs = int(s["subscriberCount"]) if s.get("subscriberCount") else None
                bio = sn.get("description","")
                out.append(Influencer(
                    name=sn.get("title","Unknown"), platform="YouTube",
                    profile_url=f"https://www.youtube.com/channel/{ch['id']}",
                    followers=subs, engagement_rate=None, category=niche,
                    bio=bio, email=extract_public_email(bio),
                    geography=sn.get("country",region), source="YouTube Data API",
                    source_url="https://developers.google.com/youtube/v3"))
            token = data.get("nextPageToken")
            if not token: break
        return out[:limit]

    def enrich_engagement(self, creator, max_videos=10):
        cid = creator.profile_url.rsplit("/",1)[-1]
        data = self._get("search", {"part":"snippet","channelId":cid,
                                    "order":"date","type":"video","maxResults":max_videos})
        ids = [x["id"]["videoId"] for x in data.get("items",[]) if x.get("id",{}).get("videoId")]
        if not ids: return creator
        videos = self._get("videos", {"part":"snippet,statistics","id":",".join(ids)})
        views, interactions, titles = [], [], []
        for v in videos.get("items",[]):
            st = v.get("statistics",{})
            if st.get("viewCount"):
                views.append(int(st["viewCount"]))
                interactions.append(int(st.get("likeCount",0))+int(st.get("commentCount",0)))
            t = v.get("snippet",{}).get("title")
            if t: titles.append(t)
        creator.recent_content = titles
        if views and statistics.mean(views) > 0:
            creator.engagement_rate = round(statistics.mean(interactions)/statistics.mean(views)*100,2)
        return creator
