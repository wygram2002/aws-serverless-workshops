---
name: brief
description: Daily morning brief — start the user's day with a snapshot of priorities, follow-ups due, and yesterday's wins, then set 1–3 intentions for today (written to the GTD Today doc). Use when the user starts their day, says good morning, asks what today looks like, or invokes /brief.
---

# Daily brief

Goal: the user knows what today is for, in under two minutes. Snappy, not a report.

## Steps

1. **Read state**: `GTD Today`, `GTD Log`, `GTD Next Actions`, `GTD Waiting On`, `GTD Inbox`.
2. **Check the seams.** If `GTD Today` still holds a previous date's intentions, yesterday's shutdown didn't run — reconcile quickly (done → log it, undone → ask: carry or drop) before briefing. Pick up "First move tomorrow" if the last log entry recorded one.
3. **Brief, in this order, compact:**
   - Yesterday's wins — one line from `GTD Log` (skip if nothing).
   - The starred top-3 from `GTD Next Actions`.
   - Waiting-on items due or overdue for follow-up today.
   - Inbox count if above zero — offer `/process`, don't force it.
4. **Set intentions.** Propose 1–3 intentions for today (drawn from the starred items, due follow-ups, and any recorded first move) and ask the user to confirm or swap. An intention that isn't in the system yet gets added to `GTD Next Actions` too.
5. **Write `GTD Today`** (full replace per CLAUDE.md's edit pattern): today's date as a heading and the intentions as `- [ ]` lines. One write per affected doc.
6. **Close** by echoing the intentions, one line each, plus one sentence of momentum. No pep talk.

## Rules

- Maximum 3 intentions. If the user lists six, ask which three matter — the rest stay in `GTD Next Actions` and are not failures.
- No project walks or priority overhauls here; that's `/review`. If the starred priorities look empty or stale, say so once and suggest scheduling one.
- Anything the user mentions in passing ("oh, and I need to…") gets captured to the inbox as usual.
