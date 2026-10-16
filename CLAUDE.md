# Instructions for Claude (any session that opens this folder)

This is Niqui's project for her YouTube channel **Ada Canada** (@adacanada, channel ID `UCQ9IbfjGvp1plsiUfWTa38Q`, Edmonton). She is moving the channel from study-in-Canada/immigration content to **faith + running**. Two series: **Road to 6 Stars** (name under review, see docs/01_AUDIT.md A3) and **Faith in Motion**. Clarence (her husband) helps with the technical side.

## Hard rules (never break these)

1. **Nothing goes public without Niqui's approval in the chat, one item at a time**: titles, descriptions, comments, replies, community posts, thumbnails.
2. **Never delete** videos, playlists, comments or the channel. **Never change video visibility** unless she asks.
3. **No livestreams.** Use Premieres.
4. Nursing is a passing mention at most. The 17 Shorts descriptions that say "as a nurse in Edmonton" stay as they are.
5. **Never invent facts** about her life, races, times or faith. Write `[CHECK: …]` and ask.
6. **No fake engagement**: no bought views, sub-for-sub, pods or automated comments.
7. Write in her voice: warm, honest, faith-forward without preaching. She often opens with "Hi friends."
8. She's not a developer. Give exact commands and say what each script does *before* running it.
9. API access is **read-only**. Secrets live in `secrets/` (gitignored). Never print, paste or commit them.
10. Keep her workload realistic: one video every 1–2 weeks, plus Shorts cut from it.

## Where things are

- `README.md`: start here (setup + the commands)
- `docs/01_AUDIT.md`: audit (Oct 16, 2026). `docs/02_PLAN.md`: the plan and 12-video slate
- `docs/03_OPENING_SCRIPT.md`: the 30-second opening. `docs/04_WEEKLY_ROUTINE.md`: the week
- `docs/06_SYDNEY_FIXES.md`: open Sydney tasks
- `config.json`: series names, playlists, publish times, targets (scripts read this)
- `tracker.csv` (per video) and `channel.csv` (per week): the numbers. `weekly.py` summarizes them
- `drafts/`: drafts awaiting Niqui's approval. Nothing in here has been posted or sent

## Key facts to keep in mind

- YPP: about 2,000 public watch hours (Oct 14, 2026). Fan funding = 3,000. Ads = 4,000 **until Jan 31, 2027**; from Feb 1, 2027 new applicants need 8,000.
- About 92% of watch hours come from old study-in-Canada videos. Keep them public until YPP.
- New long-form: CTR 1.2–2.7%, about 60% leave in the first seconds, and the ones who stay watch long.
- Judge changes over 12 videos, not one. Be encouraging and honest.
