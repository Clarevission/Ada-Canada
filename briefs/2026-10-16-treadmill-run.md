# Brief: treadmill run
Series: **Road to 6 Stars** | Format: **followalong** | Length: ~30 min | Made 2026-10-16

## 1. Title: pick one (each asks a question or names a stake)
1. 30-Minute Treadmill Run With Me | Follow Along + Scripture  (58 chars)
2. Pray and Run With Me: 30-Minute Treadmill Run  (45 chars)
3. 30 Minutes, One Verse: Treadmill Run for When You Feel Stuck  (60 chars)

Only use a title if every word of it is true.

## 2. Thumbnail text (2-4 words, never repeat the title)
A. `30 MIN / RUN WITH ME`
B. `TREADMILL RUN + SCRIPTURE`

Make both: `python thumbs.py --text "30 MIN / RUN WITH ME" --series road --variants`
Then run Test & compare in Studio with the two best.

## 3. The 5-second hook (see docs/03_OPENING_SCRIPT.md)
- **Show (0:00):** you, ready to go, looking straight at the camera (no intro music).
- **Say (by 0:05):** "Hi friends, grab your shoes. For the next 30 minutes you're doing this treadmill run with me, and I'll pray with you at the end." [CHECK: reword in your voice]
- **Stakes (0:05-0:20):** who this is for ("if you can't get yourself out the door today, this is for you").
- **Promise (0:20-0:30):** "By the end you'll have 30 minutes done and one verse to carry into your week."

## 4. Outline
| Time | What happens |
| --- | --- |
| 0:00-0:05 | HOOK: your most dramatic moment + ONE spoken sentence of stakes. No music-only intro. |
| 0:05-0:20 | STAKES: why this matters to you and what could go wrong. |
| 0:20-0:30 | PROMISE: what they get if they stay ('By the end you'll see...'). |
| 0:30-3:00 | WARM-UP together: easy pace, tell them what's coming. Read the verse once. |
| 3:00-12:15 | MAIN BLOCK part 1: talk them through effort ('you should be able to talk'). |
| 12:15-24:30 | MAIN BLOCK part 2: reflect on the verse in 2-3 short bursts. Keep talking every ~60 s. |
| 24:30-27:30 | COOL-DOWN: slow it down, celebrate them. |
| 27:30-29:30 | PRAYER: short, sincere prayer for the viewer. |
| 29:30-30:00 | CLOSE: ask the pinned question out loud, point to the next video in the series (end screen, 20 s). |

Rules: talk over every montage. No music-only stretch longer than 20 s.

## 5. Description (copy, then fill the [CHECK]s)
```
[CHECK: first line shows in search: one sentence with the words people type, e.g. 'treadmill run']

Hi friends! [CHECK: 2-3 sentences in your own voice about this video]

▶ Watch the whole Road to 6 Stars series: https://www.youtube.com/playlist?list=PLLhuWe0_POclXCE_VQ4iKdvBOK26yP1T0

Chapters
0:00 [CHECK: chapter name: Hook]
0:05 [CHECK: chapter name: Stakes]
0:20 [CHECK: chapter name: Promise]
0:30 [CHECK: chapter name: Warm-Up Together]
3:00 [CHECK: chapter name: Main Block Part 1]
12:15 [CHECK: chapter name: Main Block Part 2]
24:30 [CHECK: chapter name: Cool-Down]
27:30 [CHECK: chapter name: Prayer]
29:30 [CHECK: chapter name: Close]

I'm Niqui, a Nigerian-Canadian runner in Edmonton chasing the World Marathon Majors, with faith carrying every kilometre. Subscribe to run the road with me.

#marathontraining #runningvlog #worldmarathonmajors
```
YouTube chapter rules: first chapter must be 0:00, at least 3 chapters, each at least 10 s. Check yours with `python chapters.py check chapters.txt`.

## 6. Pinned question (pick one, post it as your own comment, pin it)
- What race is on YOUR bucket list, and what's standing between you and the start line?
- Be honest: what's the hardest kilometre you've ever run? Tell me where it was.
- Are you training for something right now? Drop the race and the date and I'll pray for your build.

## 7. Three Shorts from the same footage (cut with shorts.py)
1. **The hook moment** (20-40 s): the first 5 seconds of this video plus what happens next. On-screen text: the title question. Set 'Related video' to this video.
2. **The turning point** (30-45 s): you talking to camera about the hardest part. End on the lesson.
3. **One number** (15-30 s): the stat that surprised you (pace, km, heart rate) with your honest reaction.

## 8. When to publish
- Friday 2026-10-23 at 11:00 Edmonton time (peak ~12:30)
- Saturday 2026-10-24 at 09:00 Edmonton time (peak ~10:30)
- Sunday 2026-10-25 at 07:30 Edmonton time (peak ~09:00)
Schedule it in Studio so you don't need to be free. Reply to comments in the first few hours if you can.

## 9. Before you hit schedule
- [ ] Every [CHECK] filled or deleted, and every claim true
- [ ] First spoken sentence lands by 0:05
- [ ] Added to the playlist: Running Diaries
- [ ] End screen points to the next video in the series
- [ ] 'Not made for kids' set
- [ ] Thumbnail checked at phone size (thumbs/preview_small.jpg)
- [ ] Added a row to tracker.csv for this video (format = followalong)
- [ ] Niqui approved title, description, thumbnail and pinned comment
