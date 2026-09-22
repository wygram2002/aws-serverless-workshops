#!/usr/bin/env python3
"""Export Gmail threads with activity in the last N days (default 14) to a JSON file.

Each thread includes every message in the conversation, even ones older than N days.
Anything tagged with the Gmail label "no-llm" is never exported (the label must exist).

Usage:
    python gmail_export.py                      # last 14 days -> emails.json
    python gmail_export.py --days 7 --out week.json
    python gmail_export.py --query "from:boss@example.com"
    python gmail_export.py --exclude-label no-llm --exclude-label Finance

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
DEFAULT_EXCLUDE_LABEL = "no-llm"
HEADERS_TO_KEEP =("From", "To", "Cc", "Bcc", "Subject", "Date", "Reply-To", "Message-ID")


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


def resolve_label_ids(service, names, user_id="me"):
    """Map label names (case-insensitive) to Gmail label IDs. Fails if any is missing, so a typo
    can never silently turn the exclusion off."""
    labels = service.users().labels().list(userId=user_id).execute().get("labels", [])
    by_name = {l["name"].lower(): l["id"] for l in labels}
    missing = [n for n in names if n.lower() not in by_name]
    if missing:
        raise SystemExit(
            f"Exclusion label(s) not found in Gmail: {', '.join(missing)}. "
            "Create them in Gmail first (Settings > Labels), or fix the spelling."
        )
    return {by_name[n.lower()] for n in names}


def filter_excluded(raw_messages, excluded_label_ids, scope):
    """Drop messages carrying an excluded label. With scope='thread', one tagged message drops the
    whole thread. Returns (kept_messages, dropped_count)."""
    tagged = [m for m in raw_messages if excluded_label_ids & set(m.get("labelIds", []))]
    if not tagged:
        return raw_messages, 0
    if scope == "thread":
        return [], len(raw_messages)
    kept = [m for m in raw_messages if m not in tagged]
    return kept, len(tagged)


def parse_thread(thread, raw_messages):
    messages = sorted((parse_message(m) for m in raw_messages), key=lambda m: m["date"])
    participants = []
    for m in messages:
        for addr in (m["from"], m["to"], m["cc"]):
            for a in (addr or "").split(","):
                a = a.strip()
                if a and a not in participants:
                    participants.append(a)
    last = messages[-1] if messages else {}
    return {
        "threadId": thread["id"],
        "subject": messages[0]["subject"] if messages else None,
        "participants": participants,
        "message_count": len(messages),
        "first_message_date": messages[0]["date"] if messages else None,
        "last_message_date": last.get("date"),
        # What a reply needs: threadId plus the last message's Message-ID for In-Reply-To/References.
        "reply_to_message_id": last.get("id"),
        "reply_to_rfc822_message_id": last.get("headers", {}).get("Message-ID"),
        "messages": messages,
    }


def fetch_threads(service, days=14, extra_query="", user_id="me", include_spam_trash=False,
                  excluded_label_ids=frozenset(), exclude_scope="thread"):
    """Return every thread with activity in the last `days` days, each with all its messages
    (including ones older than the window), newest thread first. Messages or threads tagged with
    an excluded label are left out. Returns (threads, dropped_message_count)."""
    after = int((datetime.now(timezone.utc) - timedelta(days=days)).timestamp())
    query = f"after:{after} {extra_query}".strip()

    ids, page_token = [], None
    while True:
        resp = service.users().threads().list(
            userId=user_id,
            q=query,
            pageToken=page_token,
            maxResults=500,
            includeSpamTrash=include_spam_trash,
        ).execute()
        ids.extend(t["id"] for t in resp.get("threads", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break

    threads, dropped = [], 0
    for i, thread_id in enumerate(ids, 1):
        thread = service.users().threads().get(userId=user_id, id=thread_id, format="full").execute()
        kept, n = filter_excluded(thread.get("messages", []), excluded_label_ids, exclude_scope)
        dropped += n
        if kept:
            threads.append(parse_thread(thread, kept))
        if i % 50 == 0:
            print(f"  fetched {i}/{len(ids)} threads")
    threads.sort(key=lambda t: t["last_message_date"] or "", reverse=True)
    return threads, dropped


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--days", type=int, default=14, help="How many days back to fetch (default 14)")
    parser.add_argument("--out", default="emails.json", help="Output JSON file (default emails.json)")
    parser.add_argument("--query", default="", help="Extra Gmail search query, e.g. 'label:inbox'")
    parser.add_argument("--credentials", default="credentials.json")
    parser.add_argument("--token", default="token.json")
    parser.add_argument("--include-spam-trash", action="store_true")
    parser.add_argument("--exclude-label", action="append", dest="exclude_labels", metavar="LABEL",
                        help=f"Never export messages with this Gmail label. Repeatable. "
                             f"Default: {DEFAULT_EXCLUDE_LABEL}")
    parser.add_argument("--exclude-scope", choices=("thread", "message"), default="thread",
                        help="thread (default): one tagged message drops its whole thread. "
                             "message: drop only the tagged messages.")
    args = parser.parse_args()
    exclude_labels = args.exclude_labels or [DEFAULT_EXCLUDE_LABEL]

    service = get_service(args.credentials, args.token)
    excluded_ids = resolve_label_ids(service, exclude_labels)
    print(f"Fetching threads with activity in the last {args.days} days "
          f"(excluding {', '.join(exclude_labels)} by {args.exclude_scope})...")
    threads, dropped = fetch_threads(service, args.days, args.query,
                                     include_spam_trash=args.include_spam_trash,
                                     excluded_label_ids=excluded_ids, exclude_scope=args.exclude_scope)
    # Only reported locally: the export itself doesn't reveal that anything was withheld.
    print(f"Left out {dropped} excluded message(s)")

    result = {
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "days": args.days,
        "thread_count": len(threads),
        "message_count": sum(t["message_count"] for t in threads),
        "threads": threads,
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(threads)} threads ({result['message_count']} messages) to {args.out}")


if __name__ == "__main__":
    main()
