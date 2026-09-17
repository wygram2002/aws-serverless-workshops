---
name: capture
description: Capture a brain dump into the GTD inbox (gtd/inbox.md). Use whenever the user dumps tasks, thoughts, ideas, worries, or things that happened during their day — even without /capture being typed. Capture is append-only; organizing happens later via /process.
---

# Capture

Goal: get everything out of the user's head into `gtd/inbox.md`, fast and complete.
Do **not** organize, prioritize, or file anything into other lists — that is `/process`'s job.

## Steps

1. **Sync first.** If the session has been running a while, `git fetch origin master` and merge any newer `gtd/` commits from `origin/master` before editing.
2. **Split the dump into discrete items.** One thought = one item. If a sentence hides two tasks ("call Bob and then fix the deck"), make two items.
3. **Rewrite each item just enough** to be understandable in two weeks. When the meaning is obvious, clarify ("dentist" → "Schedule dentist appointment"); when it isn't, keep the user's words verbatim — a cryptic-but-verbatim note beats a wrong interpretation. Never invent commitments the user didn't state.
4. **Append to `gtd/inbox.md`** under a `## YYYY-MM-DD` heading for today (create the heading if it's missing), one `- [ ] item` line each.
5. **Commit and push** per the Persistence rules in CLAUDE.md (`gtd: capture N items`).
6. **Reply with the items exactly as captured**, one line each, so the user can correct misreadings on the spot. If the inbox now holds more than ~15 unprocessed items, suggest running `/process`.

## Rules

- Never drop an item because it seems trivial, vague, or emotional — "worried about the budget" is a valid capture.
- Never start doing the tasks during capture, even easy ones. At most, offer at the end: "Want me to knock any of these out now?"
- Questions the user asks *you* directly in the same message are conversation, not captures — answer them normally and capture the rest.
