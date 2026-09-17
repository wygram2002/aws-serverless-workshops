---
name: capture
description: Capture a brain dump into the Inbox tab of the GTD Board spreadsheet. Use whenever the user dumps tasks, thoughts, ideas, worries, or things that happened — even without /capture being typed. Capture is append-only; organizing happens later via /process.
---

# Capture

Goal: get everything out of the user's head into the `Inbox` tab of the GTD Board,
fast and complete. Do **not** organize, prioritize, or file into other tabs — that is
`/process`'s job.

## Steps

1. **Split the dump into discrete items.** One thought = one row. A sentence hiding two tasks becomes two rows.
2. **Rewrite each just enough** to be understandable in two weeks; keep the user's words verbatim when meaning is unclear — a cryptic-but-verbatim note beats a wrong interpretation. Never invent commitments.
3. **Append rows to the Inbox tab** (Date, Raw capture) via the Board edit pattern in CLAUDE.md — read current Board first, one rebuild total.
4. **Reply with the items exactly as captured**, one line each, so misreadings get corrected on the spot. More than ~15 unprocessed rows → suggest `/process`.

## Rules

- Never drop an item for being trivial, vague, or emotional.
- Never start doing the tasks during capture; offer at most once at the end.
- Direct questions in the same message are conversation — answer them, capture the rest.
