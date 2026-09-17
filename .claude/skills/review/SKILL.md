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

0. **Sync**, then check `gtd/inbox.md`. If it isn't empty, run the `/process` flow first — a review on top of a full inbox is a lie. Check `gtd/log.md` for when the last review was and mention it ("last review was 12 days ago").
1. **Done sweep.** Daily shutdowns should have kept `gtd/log.md` current — skim it, celebrate the week's wins in one line, and ask only about completions that slipped through. Mark those `[x]`, log them, remove them from their lists.
2. **Projects walk** (`gtd/projects.md`). For each Active project ask, tersely: still active? Does it have at least one next action in `next-actions.md`? If not, define one *now* with the user. A project with no movement across two consecutive reviews gets challenged: on hold, someday, or kill?
3. **Waiting-on sweep** (`gtd/waiting-on.md`). Anything arrived? Anything older than ~7 days or past its follow-up date → propose converting to a next action ("Nudge Sam about the agenda").
4. **Next-actions prune** (`gtd/next-actions.md`). Remove dead items. Anything sitting ~2 weeks untouched: still real? If it keeps not happening, ask why — wrong action, too big (make it smaller), or not actually important (someday or delete).
5. **Someday scan** (`gtd/someday.md`). Quick pass: anything worth promoting? Don't belabor this.
6. **Set priorities.** Ask what matters most this week, propose a top 3 from the walk, and on agreement star (⭐) exactly those items and move them to the top of `next-actions.md`, unstarring the previous set.

## Finish

1. Append a review record to `gtd/log.md` under today's date (counts: active projects, next actions, waiting-on; the new top 3).
2. Commit and push per the Persistence rules in CLAUDE.md (`gtd: review YYYY-MM-DD`).
3. Close with a snapshot the user can act on immediately: the top 3, anything newly stale, and the single thing you'd start with.
