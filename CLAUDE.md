# CLAUDE.md

This repository doubles as the user's personal task-management system (GTD-style),
layered on top of a fork of aws-serverless-workshops. The system lives in `gtd/`
and is operated entirely through Claude Code: the user talks, Claude keeps the lists.

## The one behavior that matters most

When the user dumps tasks, thoughts, ideas, worries, or things that happened — without
asking for anything else — that is a **brain dump**. Use the `capture` skill: split it
into items and append them to `gtd/inbox.md`. Never ignore a dump, never file items
straight into the other lists (that's `process`'s job), and never make the user do the
filing themselves.

## The lists (`gtd/`)

| File | What belongs there |
|---|---|
| `inbox.md` | Raw captures, unprocessed. Should trend toward empty. |
| `next-actions.md` | Single-step, concrete actions, verb-first. Starred (⭐) items at the top are the current top-3 priorities. |
| `today.md` | Today's 1–3 intentions. Written by `/brief`, reconciled by `/shutdown`. |
| `projects.md` | Anything needing more than one step: outcome + notes per project. Every Active project must have at least one next action. |
| `waiting-on.md` | Delegated or blocked items: who, what, since when. |
| `someday.md` | Might-do-later, no commitment. |
| `log.md` | Completed items and review records — written automatically, the user's done-history. |

Conventions:

- Items are `- [ ] …`; dates are `YYYY-MM-DD`; project-related actions carry `(Project: Name)`.
- Rewrite captured items for clarity, but never invent commitments the user didn't state.
- **When the user says something is done**: mark it `[x]`, move it to `log.md` under today's
  date, and if it belonged to a project, check whether that project still has a next
  action — if not, propose one. Then commit and push.

## Skills

- `/capture` — brain dump → inbox (also the default behavior described above)
- `/process` — clarify the inbox to empty: decide every item into the right list
- `/brief` — morning: snapshot of the day + set 1–3 intentions (writes `today.md`)
- `/shutdown` — evening: final brain sweep, reconcile intentions, log the day, close loops
- `/review` — weekly: projects, staleness, priorities; sets the top 3 for the week
- `/next` — recommend what to work on right now (read-only)

Route by intent, not just slash commands: "good morning" / "let's start the day" → brief;
"done for today" / "wrapping up" → shutdown; "organize/clarify this mess" → process;
"where do things stand" / weekly planning → review; "what should I do" → next.

## The rhythm

Morning `/brief` → during the day, dump anything anytime (→ inbox) and `/next` when
unsure what to pick → evening `/shutdown`. Once a week, `/review`. If a bookend gets
skipped, the next one absorbs the gap — never guilt-trip the user about missed rituals.

## Persistence (critical in cloud sessions)

Sessions may run in ephemeral containers — unpushed changes are lost.

- After **any** change to `gtd/` files: commit immediately (message prefixed `gtd:`) and
  push to the branch this session is designated to use.
- `master` is the source of truth for `gtd/`. If working on a session branch, remind the
  user at the end of the session to merge it (offer to open a PR they can merge in one tap).
- Before reading or editing `gtd/` state in a session that has been running a while,
  `git fetch origin master` and merge in any newer `gtd/` commits first.

## Everything else in this repository

All content outside `gtd/`, `.claude/`, and this file is the original AWS workshop
material. Leave it untouched unless the user explicitly asks to work on it.
