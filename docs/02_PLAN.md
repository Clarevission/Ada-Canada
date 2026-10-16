# Ada Canada: implementation plan (Oct 2026 – May 2027)

**Goal order:** (1) 3,000 watch hours, then apply for fan funding; 4,000 by Jan 31 is the stretch → (2) a real faith-and-running community → (3) +1,000 to +3,000 net subscribers by spring 2027.

**Who does what:** **N** = Niqui · **C** = Clarence (tech help) · **AI** = Claude, which drafts only. Nothing goes public without Niqui's OK.

---

## Phase 0: this week (Oct 16–19)

| # | Task | Who | Time |
| --- | --- | --- | --- |
| 0.1 | 48-hour Sydney check: copy the numbers into `tracker.csv` (doc 06, step 1) | N | 10 min |
| 0.2 | Sydney trim + chapter shift (doc 06, steps 2–3) | N (C runs chapters.py if needed) | 30 min |
| 0.3 | Sydney Test & compare: thumb_A vs thumb_B (+ a third from thumbs.py) | N | 10 min |
| 0.4 | Decide the series name: "Road to 7 Stars" / "Road to the Majors" / keep (audit A3) | N | 1 min |
| 0.5 | Set "made for kids = No" on Short q8EkFyIxw10 | N | 1 min |
| 0.6 | Install the toolkit on Niqui's computer (README, "First-time setup") | C | 30 min |
| 0.7 | Put thumb_A_medal.jpg and thumb_B_race.jpg in `thumbs/`, photos in `photos/` | N | 5 min |
| 0.8 | Cut 4 Sydney Shorts with shorts.py (doc 06, step 4) and schedule 1 every 2 days | N | 45 min |
| 0.9 | Add the weekly routine to the calendar: open `calendar/ada_weekly_routine.ics` | N | 1 min |

## Phase 1: build the habit (Oct 20 – Nov 30, 6 weeks, 4–6 videos)

Main idea: **follow-alongs for watch hours, simple videos for the experiment, and one rule for every video: the 5-second hook.**

| Week of | Video (series · format) | Why |
| --- | --- | --- |
| Oct 20 | **30-min treadmill run + scripture**, follow-along (Road · followalong) | Poll winner A. Biggest watch-hour potential |
| Oct 27 | **What I eat in a day as a marathoner with a 9–5** (Road · simple) | The low-edit experiment from the plan |
| Nov 3 | **20-min prayer walk**, follow-along (Faith · followalong) | Poll winner B |
| Nov 10 | Faith in Motion Ep. 4 [CHECK: theme and verse] (Faith · simple) | Keeps the series going |
| Nov 17 | **What's next after Sydney?** The next Major or goal [CHECK: real plan] (Road · simple) | A quest needs a next start line |
| Nov 24 | **Running through an Edmonton winter** [CHECK: you do this] (Road · simple or followalong) | Seasonal, searchable, and a uniquely Edmonton angle |

Every week: 3 Shorts from that video, the same files to Reels and TikTok. Sunday check-in with `weekly.py`.

**Also in Phase 1:**
- Collaboration outreach: Niqui sends 2 of the drafts in `drafts/outreach.md` (any she likes). **N**
- Reply to @shannontalley423 (paste the comment to Claude, approve the draft, post it). **N + AI**
- Optional: YouTube API setup so the tracker fills itself (doc 05). **C**

## Phase 2: seasonal push (Dec 1 – Jan 31)

| Week of | Idea | Why |
| --- | --- | --- |
| Dec 1 | Faith in Motion: an Advent or Christmas episode [CHECK] | Timely faith search |
| Dec 8–15 | Follow-along #3: a 45-min easy run, or a cold-weather treadmill session | Watch hours |
| Dec 29 | **My 2027 running goals (and the verse I'm carrying into them)** (Road · simple) | People search for goals content at New Year |
| Jan 1–5 | **New Year reset run + prayer**, follow-along | The highest-intent week of the year for fitness and faith |
| Jan 12–26 | Training block for the next race, weeks 1–2 (Road) | The series spine |

- **Mid-December review** (6 new videos in): compare simple vs cinematic vs follow-along in `weekly.py`, re-check audience timing, update `config.json` peaks. **N + C**
- **When the Earn page shows 3,000 hours:** apply the same day. **N**
- **If 4,000 looks close in mid-January:** push the best follow-along with a Premiere and a community post. Apply before Jan 31.

## Phase 3: judge and double down (Feb – May 2027)

- After **12 videos**, look at the experiment: which format brought the most watch hours per hour of Niqui's effort? Do more of that, less of the rest.
- Keep following the next Major build. Every race gets the 72-hour "fast cut".
- Subscriber goal check on May 31: +1,000 is a solid result, +3,000 is great.

---

## Automation map: what's automated, what stays human on purpose

| Job | Before | Now |
| --- | --- | --- |
| Plan a video (titles, hook, outline, description, pinned question, Shorts) | Blank page every time | `python brief.py "topic" --series road` |
| Thumbnails | Made in Python by hand per video | `python thumbs.py --text "..." --series road --variants` makes variants plus a phone-size preview |
| Chapters after a trim | Recalculated by hand | `python chapters.py shift chapters.txt --by -0:27` |
| Cutting Shorts / Reels / TikToks | Editing app, one at a time | `python shorts.py video.mp4 --clip 0:29-1:05 ...` |
| Weekly numbers | Screenshots in chats | `python yt_sync.py week` (read-only), plus 2 numbers by hand |
| Weekly summary and YPP pace | None | `python weekly.py` |
| Reminders for the routine | None | `calendar/ada_weekly_routine.ics` |
| **Posting, titles, comments, replies, community posts, visibility** | Niqui | **Still Niqui. Never automated** (her hard rule) |

**Possible next step (only if Niqui wants it):** a scheduled weekly task in Cowork that runs `yt_sync.py week` and `weekly.py` every Sunday morning and leaves her a summary. Read-only; it never posts.

## KPIs (what "working" looks like after 12 videos)

| Measure | Now | 12-video target |
| --- | --- | --- |
| Click-through rate | 1.2–2.7% | 4%+ |
| Engaged views (stay past the first seconds) | 40% | 50%+ |
| % of video watched (average) | 10–36% | 35%+ |
| Watch hours per new video (first 28 days) | ~13 | 50+ (follow-alongs 100+) |
| Net subscribers per week | about −6 | +30 or more |
| Hours of Niqui's time per week | burning out | 6–7, sustainable |
