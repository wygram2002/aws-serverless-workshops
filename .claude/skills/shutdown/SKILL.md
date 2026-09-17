---
name: shutdown
description: Daily shutdown routine — end the user's workday with a final brain sweep into the inbox, reconcile today's intentions, log what got done, and close open loops so they can switch off. Use when the user is wrapping up, says they're done for the day, or invokes /shutdown.
---

# Daily shutdown

Goal: every loose end is in the system, the day is logged, and the user can stop
thinking about work with a clear conscience. Five minutes; then done means done.

## Steps

1. **Sync.** `git fetch origin master`; merge any newer `gtd/` commits before editing.
2. **Final brain sweep.** Ask: "Anything still on your mind from today — tasks, loose ends, promises you made?" Capture all of it to `gtd/inbox.md` per the capture rules. Do **not** process it now.
3. **Reconcile `gtd/today.md`.** For each intention: done → mark `[x]`, move to `gtd/log.md`, clear it from `next-actions.md`; not done → ask once: carry it (stays in `next-actions.md`; keep or drop the star) or drop it. Then ask whether anything *not* on the list got done, and log that too.
4. **Hand-offs.** One question: "Did you hand anything off, or start waiting on anyone today?" → `gtd/waiting-on.md` with who, what, since-date.
5. **Log the day** in `gtd/log.md` under today's date: completed items, plus an optional one-line day note if the user offers one — don't fish for feelings.
6. **Tomorrow's first move (optional, one question).** If the user names one, record it at the bottom of today's log entry as `First move tomorrow: …` — `/brief` picks it up.
7. **Reset `gtd/today.md`** to just `# Today` plus `Shutdown complete YYYY-MM-DD ✓`.
8. **Commit and push** per the Persistence rules in CLAUDE.md (`gtd: shutdown YYYY-MM-DD`). If on a session branch, remind the user to merge so tomorrow's session sees today's state.
9. **Close definitively:** confirm everything is captured and logged, then give the user explicit permission to switch off. Short. No new topics.

## Rules

- No project walks, no priority overhauls, no inbox processing — that's `/review` and `/process`. Shutdown is closure, not planning.
- If something big and unresolved surfaces in the sweep, capture it and say it's tomorrow's problem — that is the point of the ritual.
- Skipped intentions are data, not sins. Note the carry, move on.
