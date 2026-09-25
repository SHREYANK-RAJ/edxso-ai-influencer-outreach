import base64
from email.mime.text import MIMEText
from pathlib import Path
from app.config import settings

class GmailSender:
    SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
    def __init__(self):
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        p = Path(settings.gmail_token_file); creds = None
        if p.exists(): creds = Credentials.from_authorized_user_file(str(p), self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(settings.gmail_credentials_file, self.SCOPES)
                creds = flow.run_local_server(port=0)
            p.write_text(creds.to_json())
        from googleapiclient.discovery import build
        self.service = build("gmail","v1",credentials=creds)

    def send(self, to, subject, body):
        msg = MIMEText(body, "plain", "utf-8")
        msg["to"], msg["subject"] = to, subject
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        return self.service.users().messages().send(userId="me", body={"raw":raw}).execute()["id"]
