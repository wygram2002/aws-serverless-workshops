---
name: next
description: Recommend what to work on right now based on gtd/ state — priorities, staleness, quick wins, and whatever the user says about their time and energy. Use when the user asks "what should I work on", "what's next", or seems unsure where to start.
---

# What's next

Goal: one clear recommendation in seconds. This skill is **read-only** — it never
reorganizes the lists (completions get recorded per CLAUDE.md when the user reports them).

## Steps

1. Read `gtd/next-actions.md` (starred items first), `gtd/projects.md`, and `gtd/waiting-on.md`.
2. If the user stated constraints ("I have 30 minutes", "I'm fried"), factor them in. Otherwise don't interrogate — recommend first, adjust if they push back.
3. Pick using this order: starred priority → unblocks other people or projects → important and going stale → quick win to build momentum.

## Output

- **One primary pick**, with a one-sentence why.
- Two alternates, one line each (e.g. a low-energy option and a quick win).
- If the starred priorities are empty or clearly stale, say so and suggest `/review`.
- If everything meaningful is blocked, point at the most valuable nudge in `waiting-on.md` instead.

Keep the whole reply under ~10 lines. The user asked what to do, not for a report.
