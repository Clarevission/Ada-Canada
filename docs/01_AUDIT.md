# Ada Canada: project audit (Oct 16, 2026)

A full review of the handoff notes, the "Sydney Video Audit + Why the Channel Is Stuck" report, and the plan agreed so far.

**Bottom line:** the earlier work is good. The cleanup, playlists, channel page and diagnosis are all right, and nothing needs undoing. But three facts change the plan, and there are ten improvements that cost little time.

---

## A. Three findings that change the plan

### A1. YouTube doubles the ads requirement on Feb 1, 2027. The real deadline is Jan 31.

- On Aug 10, 2026 YouTube announced that from **Feb 1, 2027**, *new applicants* to the Partner Program need **8,000** public watch hours (last 365 days) or 20M Shorts views (last 90 days) for ad revenue. Today it's 4,000.
- Niqui isn't in YPP right now, so she would count as a new applicant.
- The lower **fan-funding tier** (memberships, Super Thanks, Super Chat, Shopping) is reported to stay at **500 subscribers + 3,000 watch hours**. She already has the subscribers.
- **The math (from about 2,000 hours on Oct 14):**

| Goal | Hours still needed | Per week until Jan 31 (15 weeks) | Realistic? |
| --- | --- | --- | --- |
| 3,000, fan funding | +1,000 | ~65 net per week | A stretch, but possible if follow-alongs work (see A2) |
| 4,000, ads at the old rule | +2,000 | ~131 net per week | Unlikely without a breakout video. About 3.5× today's pace |
| 8,000, ads after Feb 1 | +6,000 | n/a | A late-2027 goal |

  "Net" matters: the count is a rolling 365 days, so hours from a year ago drop off every week while new ones arrive.
- **Recommendation:** change goal #1 from "back in YPP by Feb 2027" to **"reach 3,000 hours and apply for fan funding the same day."** Keep 4,000 by Jan 31 as a stretch goal and apply immediately if it happens.
- Confirm in **Studio → Earn**, which shows her exact progress and the rules that apply to her channel. (Sources: [YouTube Help: Changes to YPP](https://support.google.com/youtube/answer/12843009), [CineD](https://www.cined.com/youtube-makes-monetization-harder-new-partner-program-rules-explained/), [contentmonetizing.com](https://contentmonetizing.com/en/youtube-partner-program-2027/). I couldn't open YouTube's own page from this environment, so treat the fan-funding detail as "reported".)

### A2. Watch hours come from length × how long people stay. Follow-alongs are the biggest lever.

- Sydney so far: 43 views → 2.2 hours, about **3 minutes per view**. Even 1,000 views of a vlog is only about 50 hours.
- A **30-minute "run with me + scripture"** where people stay an average of 12 minutes: 1,000 views ≈ **200 hours**. Four times as much from the same views.
- 37% of Sydney's watch time was on **TV**. TV viewers are exactly who plays a treadmill follow-along.
- Follow-alongs are also the **least editing** of any format: one continuous take, talking the whole way, no montage.
- The community poll tied 50/50. **Film both** (30-min treadmill run + 20-min prayer walk), then make a follow-along every other video until 3,000 hours.
- **Keep the old study-in-Canada videos public until YPP.** They produce about 92% of current hours. Don't unlist any more, and don't retitle them.

### A3. The "6 Stars" name is off by one, and running fans will notice.

- Sydney became the **7th** Abbott World Marathon Major in 2025. The official **Six Star medal is still only for the original six** (Tokyo, Boston, London, Berlin, Chicago, New York). Runners like It's Matt B now call Sydney their "7th star". Sources: [Abbott](https://www.abbott.com/corpnewsroom/strategy-and-strength/sydney-marathon-is-the-7-abbott-world-marathon-major.html), [Athletics Weekly](https://athleticsweekly.com/news/sydney-becomes-seventh-world-marathon-major-1039998179/).
- So "Road to 6 Stars" with Sydney as star #1 is confusing: Sydney isn't one of the six. Expect "actually..." comments.
- **Options (Niqui decides):**
  1. **"Road to 7 Stars"**: matches how the community talks, and Sydney = star 1 of 7. *(Recommended)*
  2. "Road to the Majors": safe, and still works if Cape Town or Shanghai join later.
  3. Keep "6 Stars" and say it clearly ("Sydney was my first Major; now the Six Star journey").
- Changing it is one line in `config.json`. The thumbnails and briefs follow automatically.
- **[CHECK: Niqui]** Which Major is next, and when? A quest needs a next start line. If none is booked yet, the series needs an interim goal (a spring race, a PB, a qualifier). We won't invent one.

---

## B. Ten improvements, best value first

| # | What | Why | Effort |
| --- | --- | --- | --- |
| B1 | **Sydney fixes**: trim the cold open, Test & compare, stakes title, 4 Shorts | 60% leave in the first seconds; it already ranks #7 in search, and search traffic continues until the 2027 race | 1 evening ([doc 06](06_SYDNEY_FIXES.md)) |
| B2 | **Follow-along videos** every other upload | Biggest watch-hour lever (A2) | Less than a vlog |
| B3 | **The 30-second opening template** on every video | Fixes the 60% drop | 10 min per video ([doc 03](03_OPENING_SCRIPT.md)) |
| B4 | **Test & compare on every thumbnail** (2–3 versions) | Click-through rate is 1.2–2.7%; target 4% | 10 min with thumbs.py |
| B5 | **A binge path**: end screen → next video in the series, series link in every description, playlists in story order | Viewers who stay should get a next step; end-screen clicks were 0% | 5 min per video |
| B6 | **"Fast cut" rule for races**: a 10–15 min talk-to-camera recap within 72 hours; the cinematic version is optional and later | Sydney went up 45 days after the race; peers posted within days | Saves hours |
| B7 | **Shorts with "Related video"** set to the full video | Shorts don't add watch hours but are the cheapest discovery; the link turns Short viewers into long-form viewers | Built into shorts.py |
| B8 | **Monthly prayer-request community post** ("What can I pray for you this month?") | Real community, fits the faith series, no fake engagement. Drafted for approval only | 10 min a month |
| B9 | **Measure the same way every week** (tracker + weekly.py; compare videos at day 7) | Right now numbers live in chat logs, so trends are invisible | 10 min Sunday |
| B10 | **Collaborations** (Matt B, Hannah Roy, Kim Dolan Leto, Spen…) | The fastest way to borrow a running audience | Drafts in drafts/ |

## C. Things to watch out for

- **Audience data describes the OLD audience.** The 57.6% male, Nigeria-heavy, 5 AM–3 PM pattern comes from the immigration viewers. Use it for now, then re-check Studio's "When your viewers are on YouTube" after about 6 new-niche videos.
- **Subscriber count may keep dipping.** That's the old audience leaving. It doesn't hurt the new videos.
- **One video is a coin toss.** Judge the experiment after 12.
- **Burnout is the biggest risk to everything above.** One video every 1–2 weeks. A skipped week is a plan, not a failure.
- **Automation never posts.** Every script here only writes files on her computer. The YouTube connection is read-only.

## D. Process fixes made today

- Rules and context used to live only in chat sessions, which get lost. They now live in **`CLAUDE.md`** in the project folder, so any Claude session that opens the folder follows the hard rules automatically.
- The project is under **git**, pushed to a private GitHub repo, so nothing is lost and every change is recorded.
- The tracker is seeded with the real Sydney day-1 numbers and the Oct 7 and Oct 14 watch-hour counts.

## E. What I couldn't check from here (needs Niqui)

- Live Studio numbers, including the 48-hour Sydney check due today (Oct 16). Checklist in doc 06.
- The comment from @shannontalley423 (paste it in and I'll draft a reply).
- The "Growth Audit" doc with the full collaboration list and briefs.
- Exact cut points in the Sydney footage. The earlier report puts "I don't know if I can do this with my leg" at **0:29**.
