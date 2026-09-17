---
name: review
description: The GTD weekly review — walk projects, next actions, waiting-on and someday with the user; prune stale items; ensure every project has a next action; set the top-3 priorities for the week. Use when the user asks for the weekly review, weekly planning, a deep check-in, or "where do things stand".
---

# Weekly review

Goal: a trustworthy system and a clear top-3 for the week. This is a conversation, not
a report — ask direct questions in small batches, keep momentum, aim for ~10 minutes
total. Don't lecture about GTD theory. The daily bookends (`/brief`, `/shutdown`) handle
day-to-day upkeep; this is the weekly deep pass — don't duplicate them, go deeper.

## Steps, in order

0. Read all seven GTD docs. If `GTD Inbox` isn't empty, run the `/process` flow first — a review on top of a full inbox is a lie. Check `GTD Log` for when the last review was and mention it ("last review was 12 days ago").
1. **Done sweep.** Daily shutdowns should have kept `GTD Log` current — skim it, celebrate the week's wins in one line, and ask only about completions that slipped through.
2. **Projects walk** (`GTD Projects`). For each Active project ask, tersely: still active? Does it have at least one next action in `GTD Next Actions`? If not, define one *now* with the user. A project with no movement across two consecutive reviews gets challenged: on hold, someday, or kill?
3. **Waiting-on sweep** (`GTD Waiting On`). Anything arrived? Anything older than ~7 days or past its follow-up date → propose converting to a next action ("Nudge Sam about the agenda").
4. **Next-actions prune** (`GTD Next Actions`). Remove dead items. Anything sitting ~2 weeks untouched: still real? If it keeps not happening, ask why — wrong action, too big (make it smaller), or not actually important (someday or drop).
5. **Someday scan** (`GTD Someday`). Quick pass: anything worth promoting? Don't belabor this.
6. **Set priorities.** Ask what matters most this week, propose a top 3 from the walk, and on agreement star (⭐) exactly those items at the top of `GTD Next Actions`, unstarring the previous set.

## Finish

1. Append a review record to `GTD Log` under today's date (counts: active projects, next actions, waiting-on; the new top 3).
2. Apply everything with one write per affected doc (per CLAUDE.md's edit pattern).
3. Close with a snapshot the user can act on immediately: the top 3, anything newly stale, and the single thing you'd start with.
