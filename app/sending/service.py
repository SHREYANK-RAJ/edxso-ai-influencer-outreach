from datetime import datetime, timezone
from app.storage.db import OutreachDB

class OutreachService:
    def __init__(self, db): self.db = db
    def send_email(self, influencer, dry_run=True):
        if influencer.email == "Not Found":
            return {"status":"skipped","reason":"No public email"}
        if self.db.already_sent(influencer.email):
            return {"status":"skipped","reason":"Duplicate outreach prevented"}
        subject = f"Collaboration idea for {influencer.name}"
        if dry_run:
            mid = "DRY-RUN-" + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
            status = "simulated"
        else:
            from app.sending.gmail import GmailSender
            mid = GmailSender().send(influencer.email, subject, influencer.email_pitch)
            status = "sent"
        self.db.record(influencer.name,influencer.email,influencer.email_pitch,status,mid)
        return {"status":status,"message_id":mid}
