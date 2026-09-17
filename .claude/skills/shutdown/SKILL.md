---
name: shutdown
description: Daily shutdown routine — end the user's workday with a final brain sweep into the GTD Inbox, reconcile today's intentions, log what got done, and close open loops so they can switch off. Use when the user is wrapping up, says they're done for the day, or invokes /shutdown.
---

# Daily shutdown

Goal: every loose end is in the system, the day is logged, and the user can stop
thinking about work with a clear conscience. Five minutes; then done means done.

## Steps

1. **Final brain sweep.** Ask: "Anything still on your mind from today — tasks, loose ends, promises you made?" These go to `GTD Inbox` per the capture rules. Do **not** process them now.
2. **Reconcile `GTD Today`.** For each intention: done → move to `GTD Log`, clear from `GTD Next Actions`; not done → ask once: carry it (stays in `GTD Next Actions`; keep or drop the star) or drop it. Then ask whether anything *not* on the list got done, and log that too.
3. **Hand-offs.** One question: "Did you hand anything off, or start waiting on anyone today?" → `GTD Waiting On` with who, what, since-date.
4. **Log the day** in `GTD Log` under today's date: completed items, plus an optional one-line day note if the user offers one — don't fish for feelings.
5. **Tomorrow's first move (optional, one question).** If the user names one, record it at the bottom of today's log entry as `First move tomorrow: …` — `/brief` picks it up.
6. **Write the docs**: gather all changes from the steps above, then write each affected doc exactly once (per CLAUDE.md's edit pattern). Reset `GTD Today` to just `# Today` plus `Shutdown complete YYYY-MM-DD ✓`.
7. **Close definitively:** confirm everything is captured and logged, then give the user explicit permission to switch off. Short. No new topics.

## Rules

- No project walks, no priority overhauls, no inbox processing — that's `/review` and `/process`. Shutdown is closure, not planning.
- If something big and unresolved surfaces in the sweep, capture it and say it's tomorrow's problem — that is the point of the ritual.
- Skipped intentions are data, not sins. Note the carry, move on.
