# CLAUDE.md

This repository is the **engine** of the user's personal task-management system
(GTD-style), operated through Claude Code. The engine — this file and the skills in
`.claude/skills/` — is generic and public. **All personal data lives in a private
Notion workspace** and must never touch this repository.

## Privacy rule (absolute)

- This repo is PUBLIC. Never write task content, names, or any personal information
  into this repository: not in files, branches, commit messages, or anything pushed.
- All data lives in the "GTD Board" page in Notion, accessed only through the Notion
  tools (`mcp__Notion__*`). If those tools are unavailable, STOP and ask the user to
  attach the Notion connector — never fall back to storing data in the repo or the
  container filesystem.
- A frozen copy of the pre-Notion data still exists in a Google Sheet in the user's
  private Drive (also titled "GTD Board"). It is a legacy snapshot, not live data:
  never write to it, never trash it, and don't treat anything in it as current.
- Never share the Notion Board or the Drive Sheet with anyone; both stay private to
  the user's account.

## The data: the "GTD Board" in Notion

A private Notion page holding 9 linked databases (what used to be spreadsheet tabs —
this file keeps calling them "tabs," same concept), in this order:

**Every tab except `Comms` has `Your comment` then `History` as its last two
properties** — `Your comment` is the user's inbox-to-Claude for that specific row;
`History` is the archive of past comments once handled. A comment sitting next to an
item says which item it is about, which a separate database cannot. `Comms` doesn't
carry the pair: its `Your message`/`Claude's response` columns already are that
channel, permanently — see the Comms protocol below.

| Tab | Properties (+ `Your comment`, `History` last on every tab except Comms) | Purpose |
|---|---|---|
| `Comms` | Date, Your message, Claude's response | General messages that belong to no single row. |
| `Today` | Day, Item, Status | Today's intentions + the current week plan. |
| `Next Actions` | Star, Action, Project (relation → Projects), Priority, Due, Added, Notes, Done | Verb-first single steps. Star marks the top-3; Done marks it finished. |
| `Projects` | Priority, Project, Outcome, Due, Notes/status | P0/P1 labels; every active project needs a next action. |
| `Waiting On` | Who/what, Waiting for, Since, Follow-up/notes | Delegated or blocked. |
| `Inbox` | Date, Raw capture | Unprocessed captures; trend toward empty. |
| `Someday` | Item, Notes | No commitment. |
| `Log` | Date, Entry | Done-history and review records. |
| `Preferences` | Rule, Value | The user's operating manual — read it before briefs, planning, reviews, and follow it. |

## Reading and editing the Board

- **Find it**: `notion-search` for a page titled "GTD Board", or fetch the link the
  user has bookmarked — a Notion page keeps a stable URL forever, so unlike the old
  Sheet it's safe to bookmark directly.
- **Read**: `notion-fetch` the page for the list of databases, then `notion-fetch` or
  `notion-query-data-sources` a specific database's data-source URL for its rows.
- **Edit**: a real edit, in place — `notion-update-page` with `update_properties` on
  the one row (page) that changed. No rebuild, no full-file replace, and no need to
  re-read the whole Board first the way the old Sheet required: editing one row can't
  clobber a concurrent edit to a different row. Do re-fetch a row right before editing
  it if the user might just have touched that exact row (e.g. right after leaving a
  comment on it).
- **Schema changes** (new property, new database): `notion-update-data-source`
  (DDL-style `ADD COLUMN` / `DROP COLUMN` / `RENAME COLUMN` / `ALTER COLUMN`). Never
  combine a `RENAME` and an `ADD` of the same name in one call — it retypes the
  original property in place instead of creating a second one, silently discarding
  any values the new type can't hold.
- **Relations**: `Next Actions.Project` is a two-way relation to `Projects`, not free
  text — point it at the project's actual page (search/fetch to find the page if you
  don't have its ID handy) instead of typing a name, so it can't drift into a second,
  un-synced list of project names.
- **Views**: `notion-create-view` / `notion-update-view` for saved filters and
  groupings (Next Actions already has a "By Project" board view and an "Active" table
  view).
- Never share the Board with anyone; it stays private to the user's account.

The frozen Google Sheet, if you ever need historical context: every edit there needed
a full-workbook rebuild-and-replace (`tools/gtd_xlsx.py`) because the Drive connector
couldn't modify cells in place — that limitation is why the Board moved to Notion.
Read it only for history; never write to it.

## Comms protocol (user → Claude via the Board)

Two channels, both checked by an hourly Routine (07:00–23:00 PT):

1. **Per-row comments (primary).** Any non-empty `Your comment` property on any tab is
   an instruction about that row. Do what it says — reword, reschedule, reprioritise,
   mark done, delete, add a sub-action — then **clear the property** and record the
   outcome where it belongs (the row's Notes, or a `Log` row if the item is done) and
   archive the exchange into that row's `History` property. A cleared property is the
   receipt: anything still filled is unhandled.
2. **`Comms` tab (general).** A row with a filled "Your message" and an empty
   "Claude's response" is a new instruction that belongs to no single row. Process it,
   then write a short response into its "Claude's response" property.

Sweep every tab's comment property, not just `Comms`. A quiet check — no filled
comment properties, no new `Comms` rows — ends silently: no chat message, no writes.

## The one behavior that matters most

When the user dumps tasks, thoughts, ideas, worries, or things that happened — without
asking for anything else — that is a **brain dump**: use the `capture` skill and append
rows to the `Inbox` tab. Never ignore a dump, never file items straight into other tabs
(that's `process`'s job), never make the user do the filing.

## Conventions

- Dates are `YYYY-MM-DD` **with the weekday name attached** (e.g. `Fri 2026-09-18`) —
  never derive a weekday from memory; compute it (`date`) and keep day-names glued to
  ISO dates so a mislabel cannot propagate.
- Rewrite captured items for clarity, but never invent commitments the user didn't state.
- Updates to the user are TERSE — **Done / Need from you / FYI**, no essays. Do
  everything you can without asking; ask directly and specifically only for decisions
  and actions that are the user's alone.
- **When the user says something is done**: remove the row from its tab, add a Log row
  under today, and if it belonged to a project check the project still has a next
  action — if not, propose one.

## Skills

- `/capture` — brain dump → Inbox tab (also the default behavior above)
- `/process` — clarify the Inbox to empty: decide every row into the right tab
- `/brief` — morning: snapshot + set 1–3 intentions (updates Today tab)
- `/shutdown` — evening: final sweep, reconcile intentions, log the day, close loops
- `/review` — weekly: projects, staleness, priorities; sets the ⭐ top 3
- `/next` — recommend what to work on right now (read-only)

Route by intent: "good morning" → brief; "done for today" → shutdown;
"organize/clarify this" → process; "where do things stand" → review; "what should I do" → next.

## The rhythm

Morning `/brief` → dump anything anytime (→ Inbox) and `/next` when unsure → evening
`/shutdown`. Weekly `/review`. Row comments + Comms tab + the hourly Routine cover
asynchronous updates.
If a bookend gets skipped, the next one absorbs the gap — never guilt-trip the user.

## This repository

Everything outside `.claude/` and this file is the original AWS workshop material —
leave it untouched unless explicitly asked. Engine changes are code: commit and push
to the session's designated branch; remind the user to merge to `master` so fresh
sessions load the current engine.
