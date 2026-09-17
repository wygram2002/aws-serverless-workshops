# CLAUDE.md

This repository is the **engine** of the user's personal task-management system
(GTD-style), operated through Claude Code. The engine — this file and the skills in
`.claude/skills/` — is generic and public. **All personal data lives in the user's
private Google Drive** and must never touch this repository.

## Privacy rule (absolute)

- This repo is PUBLIC. Never write task content, names, or any personal information
  into this repository: not in files, branches, commit messages, or anything pushed.
- All list data lives in Google Docs (table below), accessed only through the Google
  Drive tools (`mcp__Google_Drive__*`).
- If the Google Drive tools are unavailable in a session, STOP and ask the user to
  attach the Google Drive connector. Never fall back to storing task data in this
  repository or the container filesystem.
- Never call `share_file` on a GTD doc; they stay private to the user's account.

## The data: Google Docs in the user's "GTD" Drive folder

| Doc title | What belongs there |
|---|---|
| `GTD Inbox` | Raw captures, unprocessed. Should trend toward empty. |
| `GTD Next Actions` | Single-step, concrete actions, verb-first. Starred (⭐) items at the top are the current top-3 priorities. |
| `GTD Today` | Today's 1–3 intentions. Written by `/brief`, reconciled by `/shutdown`. |
| `GTD Projects` | Anything needing more than one step: outcome + notes per project. Every Active project must have at least one next action. |
| `GTD Waiting On` | Delegated or blocked items: who, what, since when. |
| `GTD Someday` | Might-do-later, no commitment. |
| `GTD Log` | Completed items and review records — the done-history, newest first. |
| `GTD Preferences` | The user's operating manual: priority model, timezone, question-batching rules, daily-structure preferences. Skills read it before briefs, planning, and reviews, and follow it. |

## Finding and editing the docs

- **Find**: `search_files` with `title = 'GTD Inbox'` (etc.). Expect exactly one live
  copy. If duplicates exist (a previous edit was interrupted), the newest is truth —
  verify its content, then trash the older one.
- **Read**: `read_file_content` with the doc's fileId.
- **Edit** — the connector cannot modify content in place, so every edit is a
  replace: compose the doc's complete new content, `create_file` with the SAME title,
  `parentId` = the "GTD" folder's id (find once per session:
  `title = 'GTD' and mimeType = 'application/vnd.google-apps.folder'`),
  `contentMimeType: text/markdown` — then immediately `trash_file` the old fileId.
  Never leave two live copies.
- **Batch**: within one ritual, write each doc at most once — make all decisions
  first, then write final versions.
- **Format**: markdown headings survive round-trips. `- [ ] item` becomes a real
  Docs checkbox but reads back as a plain bullet, so **"done" is recorded by moving
  an item to `GTD Log`, never by checkbox state.**

## The one behavior that matters most

When the user dumps tasks, thoughts, ideas, worries, or things that happened — without
asking for anything else — that is a **brain dump**. Use the `capture` skill: split it
into items and append them to the `GTD Inbox` doc. Never ignore a dump, never file items
straight into the other lists (that's `process`'s job), and never make the user do the
filing themselves.

## Conventions

- Items are `- [ ] …`; dates are `YYYY-MM-DD`; project-related actions carry `(Project: Name)`.
- Rewrite captured items for clarity, but never invent commitments the user didn't state.
- Updates to the user are TERSE — format: **Done / Need from you / FYI**, no recaps, no
  essays. Do everything you can without asking; ask directly and specifically only for
  decisions and actions that are the user's alone.
- **When the user says something is done**: remove it from its doc, add it to `GTD Log`
  under today's date, and if it belonged to a project, check whether that project still
  has a next action — if not, propose one.

## Skills

- `/capture` — brain dump → GTD Inbox (also the default behavior described above)
- `/process` — clarify the inbox to empty: decide every item into the right doc
- `/brief` — morning: snapshot of the day + set 1–3 intentions (writes GTD Today)
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

## This repository

Everything outside `.claude/` and this file is the original AWS workshop material —
leave it untouched unless explicitly asked. Engine changes (skills, this file) are
code: commit and push them to the session's designated branch, and remind the user to
merge to `master` so fresh sessions load the current engine.
