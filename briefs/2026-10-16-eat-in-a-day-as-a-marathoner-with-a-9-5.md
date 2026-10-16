# Brief: What I eat in a day as a marathoner with a 9-5 (low-edit experiment)
Series: **Road to 6 Stars** | Format: **simple** | Length: ~12 min | Made 2026-10-16

## 1. Title: pick one (edited by hand: the templates don't suit this topic)
1. What I eat in a day as a marathoner with a 9-5 (honest)  (55 chars)
2. Can you fuel marathon training around a 9-5?  (44 chars)
3. What I really eat training for a marathon with a full-time job  (62 chars, shorten if needed)

Only use a title if every word of it is true.

## 2. Thumbnail text (2-4 words, never repeat the title)
A. `9-5 + MARATHON`
B. `REAL FUEL DAY`

Make both: `python thumbs.py --text "9-5 + MARATHON" --text "REAL FUEL DAY" --series road --variants`
Then run Test & compare in Studio with the two best.

**Experiment rules:** film it on one normal workday, phone only, edit in ONE evening (2 hours max), no music-only montage. Log it in tracker.csv with format = simple.

## 3. The 5-second hook (see docs/03_OPENING_SCRIPT.md)
- **Show (0:00):** [CHECK: the single most dramatic clip: the moment it could all go wrong]
- **Say (by 0:05):** "[CHECK: e.g. 'while training for my next Major on a full-time schedule']"
- **Stakes (0:05-0:20):** [CHECK: why it matters and what could go wrong]
- **Promise (0:20-0:30):** "Stay with me, because by the end [CHECK: what they will see or get]."

## 4. Outline
| Time | What happens |
| --- | --- |
| 0:00-0:05 | HOOK: your most dramatic moment + ONE spoken sentence of stakes. No music-only intro. |
| 0:05-0:20 | STAKES: why this matters to you and what could go wrong. |
| 0:20-0:30 | PROMISE: what they get if they stay ('By the end you'll see...'). |
| 0:30-3:44 | BEAT 1, the setup: where you are right now (honest numbers, real feelings). |
| 3:44-6:58 | BEAT 2, the struggle: the hardest part. Re-hook at the start: 'But then...' |
| 6:58-10:12 | BEAT 3, the result: show it, then say what it meant. |
| 10:12-11:30 | FAITH MOMENT: the verse or prayer that carried you (30-60 s, not a sermon). |
| 11:30-12:00 | CLOSE: ask the pinned question out loud, point to the next video in the series (end screen, 20 s). |

Rules: talk over every montage. No music-only stretch longer than 20 s.

## 5. Description (copy, then fill the [CHECK]s)
```
[CHECK: first line shows in search: one sentence with the words people type, e.g. 'eat in a day as a marathoner with a 9-5']

Hi friends! [CHECK: 2-3 sentences in your own voice about this video]

▶ Watch the whole Road to 6 Stars series: https://www.youtube.com/playlist?list=PLLhuWe0_POclXCE_VQ4iKdvBOK26yP1T0

Chapters
0:00 [CHECK: chapter name: Hook]
0:05 [CHECK: chapter name: Stakes]
0:20 [CHECK: chapter name: Promise]
0:30 [CHECK: chapter name: Beat 1, The Setup]
3:44 [CHECK: chapter name: Beat 2, The Struggle]
6:58 [CHECK: chapter name: Beat 3, The Result]
10:12 [CHECK: chapter name: Faith Moment]
11:30 [CHECK: chapter name: Close]

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
- [ ] Added a row to tracker.csv for this video (format = simple)
- [ ] Niqui approved title, description, thumbnail and pinned comment
