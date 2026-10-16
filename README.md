# Ada Canada toolkit

Hi Niqui! This folder is your channel's home base: the plan, the audit, and some small tools that do the repetitive parts for you. **None of the tools ever post, edit or delete anything on YouTube.** They only make files on your computer. You stay in charge of what goes public.

## Read these first (15 minutes)

1. [docs/01_AUDIT.md](docs/01_AUDIT.md): what's working, and 3 new findings (including YouTube's **Feb 1, 2027** rule change)
2. [docs/02_PLAN.md](docs/02_PLAN.md): the plan, week by week, and the next 12 video ideas
3. [docs/06_SYDNEY_FIXES.md](docs/06_SYDNEY_FIXES.md): this week's Sydney to-dos
4. [docs/03_OPENING_SCRIPT.md](docs/03_OPENING_SCRIPT.md) and [docs/04_WEEKLY_ROUTINE.md](docs/04_WEEKLY_ROUTINE.md)

## The tools

| You want to… | Type this | What happens |
| --- | --- | --- |
| Plan a video | `python brief.py "run my first 10K since Sydney" --series road` | Writes a brief in `briefs/`: 3 titles, hook, outline, description, pinned question, Shorts, publish time |
| Plan a follow-along | `python brief.py "treadmill run" --series road --format followalong --length 30` | Same, for run-with-me videos |
| Plan Faith in Motion | `python brief.py "letting go of control" --series faith --scripture "Proverbs 3:5-6"` | Same, with the verse built in |
| Make thumbnails | `python thumbs.py --text "CAN I DO THIS?" --series road --variants` | Uses photos in `photos/`, saves to `thumbs/`, plus `preview_small.jpg` to compare at phone size |
| Fix chapters after a trim | `python chapters.py shift chapters.txt --cut 0:00-0:27` | Writes `chapters_shifted.txt`, checked against YouTube's rules |
| Check chapters | `python chapters.py check chapters.txt` | Tells you if YouTube will accept them |
| Cut Shorts / Reels / TikToks | `python shorts.py "video.mp4" --clip 0:29-1:05 --clip 7:12-7:50` | 1080×1920 clips in `shorts/` |
| Sunday check-in | `python weekly.py` | YPP pace, subscriber pace, video scorecard, the 12-video experiment |
| (Optional) auto-fill numbers | `python yt_sync.py week` | Read-only. Setup in [docs/05](docs/05_YOUTUBE_API_SETUP.md) |

Anything in **[CHECK: …]** is something only you know. Fill it in or delete it. The tools never make up facts about you.

## Sunday check-in (10 minutes)

1. **channel.csv**: add one line: today's date, subscribers, and the watch hours from **Studio → Earn**.
   `2026-10-25,38290,2045,,`
2. **tracker.csv**: for each new video (aim for the day-7 numbers), copy a line and update it: impressions, CTR, views, engaged %, average view (minutes), length (minutes), watch hours, subscribers from that video. `format` is `simple`, `cinematic` or `followalong`; `hook_by_5s` is `yes` or `no`.
   (These open in Excel, Numbers or Google Sheets.)
3. Run `python weekly.py`.

## First-time setup (Clarence: about 30 minutes)

1. **Python:** install from <https://www.python.org/downloads/>. On Windows, tick **"Add Python to PATH"**.
   Check it: open Terminal (Mac) or PowerShell (Windows) and type `python --version` (on Mac it may be `python3`).
2. **Get this folder:** `git clone https://github.com/Clarevission/Ada-Canada.git`, or download the ZIP from GitHub.
3. **Go into the folder:** `cd Ada-Canada`
4. **Install the libraries:** `pip install -r requirements.txt` (Mac: `pip3`)
5. **ffmpeg** (for Shorts): Mac `brew install ffmpeg` · Windows `winget install ffmpeg`
6. **Font (optional, recommended):** download **Anton** from <https://fonts.google.com/specimen/Anton> and put `Anton-Regular.ttf` in `fonts/`. It's the bold, condensed YouTube look.
7. **Test:** `python brief.py "treadmill run" --series road --format followalong --length 30 --print-only`

**Using Claude (Cowork / Claude Code) with this folder:** open the folder and Claude reads `CLAUDE.md` automatically, so it already knows your hard rules and the plan.

## Folders

`docs/` the plan and guides · `drafts/` drafts waiting for your OK (nothing is posted) · `briefs/` video plans · `photos/` your photos (stay on your computer) · `thumbs/` thumbnails · `shorts/` vertical clips · `reports/` weekly summaries · `calendar/` the routine as a calendar file · `secrets/` API keys (never shared)

## Changing settings

Everything lives in `config.json`: series names, playlist IDs, pinned questions, publish times and targets. For example, to rename the series, change `"name"` and `"badge"` under `"road"`.
