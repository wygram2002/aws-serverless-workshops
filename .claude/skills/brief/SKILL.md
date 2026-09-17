---
name: brief
description: Daily morning brief — start the user's day with a snapshot of priorities, follow-ups due, and yesterday's wins, then set 1–3 intentions for today (written to gtd/today.md). Use when the user starts their day, says good morning, asks what today looks like, or invokes /brief.
---

# Daily brief

Goal: the user knows what today is for, in under two minutes. Snappy, not a report.

## Steps

1. **Sync.** `git fetch origin master`; merge any newer `gtd/` commits before reading.
2. **Check the seams.** If `gtd/today.md` still holds a previous date's intentions, yesterday's shutdown didn't run — reconcile quickly (done → log it, undone → ask: carry or drop) before briefing. Pick up "First move tomorrow" if the last log entry recorded one.
3. **Brief, in this order, compact:**
   - Yesterday's wins — one line from `gtd/log.md` (skip if nothing).
   - The starred top-3 from `gtd/next-actions.md`.
   - Waiting-on items due or overdue for follow-up today.
   - Inbox count if above zero — offer `/process`, don't force it.
4. **Set intentions.** Propose 1–3 intentions for today (drawn from the starred items, due follow-ups, and any recorded first move) and ask the user to confirm or swap. An intention that isn't in the system yet gets added to `next-actions.md` too.
5. **Write `gtd/today.md`:** today's date as a heading and the intentions as `- [ ]` lines. Replace whatever was there.
6. **Commit and push** per the Persistence rules in CLAUDE.md (`gtd: brief YYYY-MM-DD`).
7. **Close** by echoing the intentions, one line each, plus one sentence of momentum. No pep talk.

## Rules

- Maximum 3 intentions. If the user lists six, ask which three matter — the rest stay in `next-actions.md` and are not failures.
- No project walks or priority overhauls here; that's `/review`. If the starred priorities look empty or stale, say so once and suggest scheduling one.
- Anything the user mentions in passing ("oh, and I need to…") gets captured to the inbox as usual.
