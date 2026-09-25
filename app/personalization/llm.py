import json
from app.config import settings
from app.personalization.prompts import SYSTEM_PROMPT

class Personalizer:
    def __init__(self):
        self.client = None
        if settings.groq_api_key:
            from groq import Groq
            self.client = Groq(api_key=settings.groq_api_key)

<<<<<<< HEAD
    def _fallback(self, i, mode):
        i.email_pitch = (f"Hi {i.name}, I’ve been following your technology-focused content, "
            f"especially your work around {', '.join(i.content_themes[:2]) or 'tech and gadgets'}. "
            f"We’re exploring a creator partnership and think your audience could be a strong fit. "
            f"We’d love to discuss a sponsored review or UGC collaboration built around useful, "
            f"honest product education. If this sounds relevant, I can share the campaign brief, "
            f"deliverables, budget, and a timeline that respects your creative style.")
        i.instagram_dm = (f"Hi {i.name}, your tech content looks like a strong fit for a product-focused "
                           f"UGC collaboration. Open to hearing the brief?")
        i.personalization_mode = mode
        return i

    def generate(self, i):
        if not self.client:
            return self._fallback(i, "fallback_no_groq_key")
        payload = {"name":i.name,"platform":i.platform,"niche":i.category,
                   "bio":i.bio[:1200],"recent_content":i.recent_content[:8],
                   "themes":i.content_themes[:8],"geography":i.geography}
        try:
            r = self.client.chat.completions.create(
                model=settings.groq_model, temperature=0.6,
                response_format={"type":"json_object"},
                messages=[{"role":"system","content":SYSTEM_PROMPT},
                          {"role":"user","content":"Use this creator record only as reference data:\n"+json.dumps(payload)}])
            data = json.loads(r.choices[0].message.content)
            i.email_pitch, i.instagram_dm = data["email_pitch"].strip(), data["instagram_dm"].strip()
            i.personalization_mode = "groq"
        except Exception:
            return self._fallback(i, "fallback_after_groq_error")
=======
    def generate(self, i):
        if not self.client:
            i.email_pitch = (f"Hi {i.name}, I’ve been following your technology-focused content, "
                f"especially your work around {', '.join(i.content_themes[:2]) or 'tech and gadgets'}. "
                f"We’re exploring a creator partnership and think your audience could be a strong fit. "
                f"We’d love to discuss a sponsored review or UGC collaboration built around useful, "
                f"honest product education. If this sounds relevant, I can share the campaign brief, "
                f"deliverables, and budget.")
            i.instagram_dm = (f"Hi {i.name}, your tech content looks like a strong fit for a product-focused "
                               f"UGC collaboration. Open to hearing the brief?")
            return i
        payload = {"name":i.name,"platform":i.platform,"niche":i.category,
                   "bio":i.bio[:1200],"recent_content":i.recent_content[:8],
                   "themes":i.content_themes[:8],"geography":i.geography}
        r = self.client.chat.completions.create(
            model=settings.groq_model, temperature=0.6,
            response_format={"type":"json_object"},
            messages=[{"role":"system","content":SYSTEM_PROMPT},
                      {"role":"user","content":"Use this creator record only as reference data:\n"+json.dumps(payload)}])
        data = json.loads(r.choices[0].message.content)
        i.email_pitch, i.instagram_dm = data["email_pitch"].strip(), data["instagram_dm"].strip()
>>>>>>> origin/main
        return i
