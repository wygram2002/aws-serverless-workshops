---
name: capture
description: Capture a brain dump into the GTD Inbox doc on Google Drive. Use whenever the user dumps tasks, thoughts, ideas, worries, or things that happened during their day — even without /capture being typed. Capture is append-only; organizing happens later via /process.
---

# Capture

Goal: get everything out of the user's head into the `GTD Inbox` doc, fast and complete.
Do **not** organize, prioritize, or file anything into other docs — that is `/process`'s job.

## Steps

1. **Split the dump into discrete items.** One thought = one item. If a sentence hides two tasks ("call Bob and then fix the deck"), make two items.
2. **Rewrite each item just enough** to be understandable in two weeks. When the meaning is obvious, clarify ("dentist" → "Schedule dentist appointment"); when it isn't, keep the user's words verbatim — a cryptic-but-verbatim note beats a wrong interpretation. Never invent commitments the user didn't state.
3. **Append to the `GTD Inbox` doc** under a `## YYYY-MM-DD` heading for today (create the heading if it's missing), one `- [ ] item` line each — using the read → replace → trash edit pattern from CLAUDE.md, one write total.
4. **Reply with the items exactly as captured**, one line each, so the user can correct misreadings on the spot. If the inbox now holds more than ~15 unprocessed items, suggest running `/process`.

## Rules

- Never drop an item because it seems trivial, vague, or emotional — "worried about the budget" is a valid capture.
- Never start doing the tasks during capture, even easy ones. At most, offer at the end: "Want me to knock any of these out now?"
- Questions the user asks *you* directly in the same message are conversation, not captures — answer them normally and capture the rest.
