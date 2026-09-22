# Gmail Export

Pulls every email from the last 14 days (configurable) using the Gmail API and writes them to a JSON file.

## Setup

1. In Google Cloud Console, enable the **Gmail API** for a project.
2. Create an **OAuth client ID** of type **Desktop app** and download it as `credentials.json` into this folder.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Run

```bash
python gmail_export.py                          # last 14 days -> emails.json
python gmail_export.py --days 7 --out week.json
python gmail_export.py --query "label:inbox"    # add any Gmail search filter
```

The first run opens a browser to grant read-only access (`gmail.readonly`) and caches the token in `token.json`. Don't commit `credentials.json` or `token.json`.

## Output shape

```json
{
  "exported_at": "2026-09-22T12:00:00+00:00",
  "days": 14,
  "count": 1,
  "emails": [
    {
      "id": "18c...",
      "threadId": "18c...",
      "labelIds": ["INBOX", "UNREAD"],
      "date": "2026-09-21T15:04:05+00:00",
      "from": "Alice <alice@example.com>",
      "to": "you@example.com",
      "cc": null,
      "subject": "Hello",
      "snippet": "First line of the message...",
      "headers": { "From": "...", "Subject": "...", "Date": "..." },
      "body_text": "Plain-text body",
      "body_html": "<p>HTML body</p>",
      "attachments": [
        { "filename": "a.pdf", "mimeType": "application/pdf", "size": 1234, "attachmentId": "ANGj..." }
      ]
    }
  ]
}
```

Attachment contents aren't downloaded; use `attachmentId` with `users.messages.attachments.get` if you need them.
