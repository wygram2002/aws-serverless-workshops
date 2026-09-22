# Gmail Export

Pulls every email thread with activity in the last 14 days (configurable) using the Gmail API and writes them, with their full conversation history, to a JSON file.

## Setup

1. In Google Cloud Console, enable the **Gmail API** for a project.
2. Create an **OAuth client ID** of type **Desktop app** and download it as `credentials.json` into this folder.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Run

```bash
python gmail_export.py                          # threads active in last 14 days -> emails.json
python gmail_export.py --days 7 --out week.json
python gmail_export.py --query "label:inbox"    # add any Gmail search filter
```

## Keeping emails away from the LLM

Create a Gmail label called `no-llm` and put it on anything that must not be shared. Tagged emails never make it into the export.

- **Default (`--exclude-scope thread`):** if any message in a conversation has the label, the whole conversation is left out.
- **`--exclude-scope message`:** only the tagged messages are left out; the rest of the conversation is still exported.
- Use other or extra labels with `--exclude-label`, which can be repeated: `--exclude-label no-llm --exclude-label Finance`.
- If a label doesn't exist in Gmail, the script stops instead of running without it. That way a typo can't switch the protection off.
- The export doesn't mention that anything was left out. The count is only printed in your terminal.

Everything that isn't tagged **is** shared, so tag before you run the export.

The first run opens a browser to grant read-only access (`gmail.readonly`) and caches the token in `token.json`. Don't commit `credentials.json` or `token.json`.

## Output shape

Emails are grouped by conversation. Any thread with a message in the last 14 days is included **in full**, so older messages in that thread come along too. Messages inside a thread are oldest first; threads are ordered by most recent activity.

```json
{
  "exported_at": "2026-09-22T12:00:00+00:00",
  "days": 14,
  "thread_count": 1,
  "message_count": 2,
  "threads": [
    {
      "threadId": "18c1a2b3c4d5e6f7",
      "subject": "Hello",
      "participants": ["Alice <alice@example.com>", "you@example.com"],
      "message_count": 2,
      "first_message_date": "2026-09-01T09:00:00+00:00",
      "last_message_date": "2026-09-21T15:04:05+00:00",
      "reply_to_message_id": "18c9f8e7d6c5b4a3",
      "reply_to_rfc822_message_id": "<CAB...@mail.gmail.com>",
      "messages": [
        {
          "id": "18c9f8e7d6c5b4a3",
          "threadId": "18c1a2b3c4d5e6f7",
          "labelIds": ["INBOX", "UNREAD"],
          "date": "2026-09-21T15:04:05+00:00",
          "from": "Alice <alice@example.com>",
          "to": "you@example.com",
          "cc": null,
          "subject": "Re: Hello",
          "snippet": "First line of the message...",
          "headers": { "From": "...", "Subject": "...", "Message-ID": "<CAB...@mail.gmail.com>" },
          "body_text": "Plain-text body",
          "body_html": "<p>HTML body</p>",
          "attachments": [
            { "filename": "a.pdf", "mimeType": "application/pdf", "size": 1234, "attachmentId": "ANGj..." }
          ]
        }
      ]
    }
  ]
}
```

`threadId` is Gmail's stable ID for the conversation. `reply_to_message_id` and `reply_to_rfc822_message_id` point at the latest message, which is what a reply needs to land in the same thread.

Attachment contents aren't downloaded; use `attachmentId` with `users.messages.attachments.get` if you need them.
