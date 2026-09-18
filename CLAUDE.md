# CLAUDE.md

This repository is the **engine** of the user's personal task-management system
(GTD-style), operated through Claude Code. The engine — this file and the skills in
`.claude/skills/` — is generic and public. **All personal data lives in one Google
Spreadsheet in the user's private Drive** and must never touch this repository.

## Privacy rule (absolute)

- This repo is PUBLIC. Never write task content, names, or any personal information
  into this repository: not in files, branches, commit messages, or anything pushed.
- All data lives in the "GTD Board" spreadsheet, accessed only through the Google
  Drive tools (`mcp__Google_Drive__*`). If those tools are unavailable, STOP and ask
  the user to attach the Google Drive connector — never fall back to storing data in
  the repo or the container filesystem.
- Never call `share_file` on the Board; it stays private to the user's account.

## The data: the "GTD Board" spreadsheet

One Google Sheet in the user's "GTD" Drive folder, tabs in this order:

**Every tab's last column is `Your comment`** — the user's inbox-to-Claude for that
specific row. That column is the point: a comment sitting next to an item says which
item it is about, which a separate tab cannot.

| Tab | Columns (+ `Your comment` last on every tab) | Purpose |
|---|---|---|
| `Comms` | Date, Your message, Claude's response | General messages that belong to no single row. |
| `Today` | Day, Item, Status | Today's intentions + the current week plan. |
| `Next Actions` | ⭐, Action, Project, Priority, Due, Added, Notes | Verb-first single steps. ⭐ marks the top-3. |
| `Projects` | Priority, Project, Outcome, Notes/status | P0/P1 labels; every active project needs a next action. |
| `Waiting On` | Who/what, Waiting for, Since, Follow-up/notes | Delegated or blocked. |
| `Inbox` | Date, Raw capture | Unprocessed captures; trend toward empty. |
| `Someday` | Item, Notes | No commitment. |
| `Log` | Date, Entry | Done-history and review records. |
| `Preferences` | Rule, Value | The user's operating manual — read it before briefs, planning, reviews, and follow it. |

## Reading and editing the Board

- **Find it**: `search_files` `title = 'GTD Board' and mimeType = 'application/vnd.google-apps.spreadsheet'`.
  Exactly one live copy; on duplicates the newest is truth (verify, trash the older).
- **Read**: `read_file_content` — tabs come back as consecutive tables IN ORDER,
  without names; identify each by its header row.
- **Edit** — the connector cannot modify content in place, so every edit is a full
  replace: (1) **read the current Board first, every time** — the user types directly
  into cells (Comms especially) and their edits MUST survive; (2) rebuild the complete
  workbook as .xlsx with `tools/gtd_xlsx.py` in the sandbox (all 9 tabs — it keeps the
  payload small, which is the difference between an upload that lands and one that does
  not); (3) base64 it and `create_file` with title "GTD Board", parentId = the GTD
  folder, contentMimeType
  `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` (Drive converts it
  to a native Sheet); (4) immediately `trash_file` the old fileId. An
  "invalid argument" or "not a valid base64 string" error means the payload got corrupted
  in transcription — regenerate and retry once. "Invalid conversion requested" means the
  .xlsx is malformed for Google's converter (it requires an `xl/styles.xml` part).
- **Verify after every write**: re-read the new file and spot-check the tabs you
  changed before trashing the old one. `read_file_content` TRUNCATES — it returns
  roughly 8 tables, so a missing first or last tab is usually the reader, not lost
  data. Never rebuild a tab just because it did not come back in a read.
- **Batch**: one rebuild per ritual — make all decisions first, write once.
- The file ID changes on every edit, so the stable entry point is the **GTD folder**,
  never a bookmarked direct link. Tell the user this if they mention a dead link.

## Comms protocol (user → Claude via the Board)

Two channels, both checked by an hourly Routine (07:00–23:00 PT):

1. **Per-row comments (primary).** Any non-empty `Your comment` cell on any tab is an
   instruction about that row. Do what it says — reword, reschedule, reprioritise,
   mark done, delete, add a sub-action — then **clear the cell** in the same rebuild
   and record the outcome where it belongs (the row's Notes, or a `Log` row if the
   item is done). A cleared cell is the receipt: anything still filled is unhandled.
2. **`Comms` tab (general).** A row with a filled "Your message" and an empty
   "Claude's response" is a new instruction that belongs to no single row. Process it,
   then write a short response into its "Claude's response" cell in the same rebuild.

Sweep every tab's comment column, not just `Comms`. A quiet check — no filled comment
cells, no new `Comms` rows — ends silently: no chat message, no writes.

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
