---
name: process
description: Process/clarify the GTD Inbox doc to empty — decide every item into next actions, projects, waiting-on, someday, or trash. Use when the user asks to process, clarify, organize, triage, or clean up the inbox, or accepts that suggestion after a capture.
---

# Process the inbox

Goal: inbox to zero. Work top-down (oldest first), one decision per item, no skipping.
An item may only leave the inbox by landing somewhere deliberate.

## The decision, per item

**Is it actionable?**

- **No, and worthless** → drop it. List every drop in the closing summary so the user can veto.
- **No, but might matter later** → `GTD Someday`.
- **No, but it's information worth keeping** → if a `GTD Reference` doc exists, file it there; otherwise ask the user once whether to create it.

**Yes, it's actionable:**

- **More than one step** → make sure the project exists in `GTD Projects` (create it with a one-line **Outcome** — what "done" looks like), and put the first concrete action into `GTD Next Actions` tagged `(Project: Name)`.
- **Blocked on someone or something else** → `GTD Waiting On` with who, what, and since-date.
- **One step, doable** → `GTD Next Actions`, rewritten as a verb-first concrete action ("Website is broken" → "File hosting ticket about the broken website"), with `— added YYYY-MM-DD`.
- **Something Claude can finish right now in a couple of minutes** (a lookup, a short draft, a calculation) → still file it, but collect these and offer once at the end: "I can knock out these N right now — want me to?" Do them only on a yes.

## Handling ambiguity

Decide the obvious ones yourself. For genuinely unclear items, batch the questions into **one** message, each with your best-guess default ("I'll treat X as a project unless you say otherwise") — never one question per item.

## Finish

1. Make every decision first, then write each affected doc exactly once (the emptied `GTD Inbox` included), using the edit pattern from CLAUDE.md. Delete date headings that end up empty.
2. Summarize: each item → where it went, one line each. Call out new projects created and anything dropped.
