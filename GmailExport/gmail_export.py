#!/usr/bin/env python3
"""Export Gmail messages from the last N days (default 14) to a JSON file.

Usage:
    python gmail_export.py                      # last 14 days -> emails.json
    python gmail_export.py --days 7 --out week.json
    python gmail_export.py --query "from:boss@example.com"

Requires a Google Cloud OAuth client (Desktop app) saved as credentials.json.
The first run opens a browser for consent and caches the token in token.json.
"""

import argparse
import base64
import json
import os
from datetime import datetime, timedelta, timezone

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
HEADERS_TO_KEEP = ("From", "To", "Cc", "Bcc", "Subject", "Date", "Reply-To", "Message-ID")


def get_service(credentials_file="credentials.json", token_file="token.json"):
    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_file, "w") as f:
            f.write(creds.to_json())
    return build("gmail", "v1", credentials=creds, cache_discovery=False)


def _decode(data):
    if not data:
        return ""
    return base64.urlsafe_b64decode(data + "=" * (-len(data) % 4)).decode("utf-8", errors="replace")


def _extract(payload, out):
    """Walk the MIME tree collecting text/plain, text/html and attachment metadata."""
    mime = payload.get("mimeType", "")
    body = payload.get("body", {})
    filename = payload.get("filename")

    if filename:
        out["attachments"].append({
            "filename": filename,
            "mimeType": mime,
            "size": body.get("size", 0),
            "attachmentId": body.get("attachmentId"),
        })
    elif mime == "text/plain":
        out["text"] += _decode(body.get("data"))
    elif mime == "text/html":
        out["html"] += _decode(body.get("data"))

    for part in payload.get("parts", []) or []:
        _extract(part, out)


def parse_message(msg):
    payload = msg.get("payload", {})
    headers = {h["name"]: h["value"] for h in payload.get("headers", []) if h["name"] in HEADERS_TO_KEEP}
    content = {"text": "", "html": "", "attachments": []}
    _extract(payload, content)

    internal_ms = int(msg.get("internalDate", 0))
    return {
        "id": msg["id"],
        "threadId": msg.get("threadId"),
        "labelIds": msg.get("labelIds", []),
        "date": datetime.fromtimestamp(internal_ms / 1000, tz=timezone.utc).isoformat(),
        "from": headers.get("From"),
        "to": headers.get("To"),
        "cc": headers.get("Cc"),
        "subject": headers.get("Subject"),
        "snippet": msg.get("snippet"),
        "headers": headers,
        "body_text": content["text"],
        "body_html": content["html"],
        "attachments": content["attachments"],
    }


def fetch_emails(service, days=14, extra_query="", user_id="me", include_spam_trash=False):
    """Return a list of parsed messages received in the last `days` days."""
    after = int((datetime.now(timezone.utc) - timedelta(days=days)).timestamp())
    query = f"after:{after} {extra_query}".strip()

    ids, page_token = [], None
    while True:
        resp = service.users().messages().list(
            userId=user_id,
            q=query,
            pageToken=page_token,
            maxResults=500,
            includeSpamTrash=include_spam_trash,
        ).execute()
        ids.extend(m["id"] for m in resp.get("messages", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break

    emails = []
    for i, msg_id in enumerate(ids, 1):
        msg = service.users().messages().get(userId=user_id, id=msg_id, format="full").execute()
        emails.append(parse_message(msg))
        if i % 50 == 0:
            print(f"  fetched {i}/{len(ids)}")
    emails.sort(key=lambda e: e["date"], reverse=True)
    return emails


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--days", type=int, default=14, help="How many days back to fetch (default 14)")
    parser.add_argument("--out", default="emails.json", help="Output JSON file (default emails.json)")
    parser.add_argument("--query", default="", help="Extra Gmail search query, e.g. 'label:inbox'")
    parser.add_argument("--credentials", default="credentials.json")
    parser.add_argument("--token", default="token.json")
    parser.add_argument("--include-spam-trash", action="store_true")
    args = parser.parse_args()

    service = get_service(args.credentials, args.token)
    print(f"Fetching emails from the last {args.days} days...")
    emails = fetch_emails(service, args.days, args.query, include_spam_trash=args.include_spam_trash)

    result = {
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "days": args.days,
        "count": len(emails),
        "emails": emails,
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(emails)} emails to {args.out}")


if __name__ == "__main__":
    main()
