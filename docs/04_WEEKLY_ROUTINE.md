# The weekly routine (fits a 9–5)

**Rhythm:** one YouTube video every 1–2 weeks, plus 3 Shorts cut from it (the same files go to Reels and TikTok). **About 6–7 hours a week**, mostly in short evening blocks. No separate content for each platform.

## Full week (a video week)

| Day | Task | Time |
| --- | --- | --- |
| **Saturday** | **FILM.** Long-run day is your filming day. Talk to camera at the start, the hard part and the end. Then film the 3 opening lines at home (doc 03). | Run + 30 min |
| **Sunday** | Rest and church. Evening: copy the footage over and write down the hook moment's timestamp. **Sunday check-in:** update the tracker, run `python weekly.py`. | 30 min |
| **Monday** evening | **Rough cut.** Put the 30-second opening first, then the story. | 90 min |
| **Tuesday** evening | **Finish the edit:** voiceover on the montages, captions, audio. Export. | 90 min |
| **Wednesday** evening | **Packaging:** `python brief.py`, `python thumbs.py --variants`, pick a title. Paste into Claude for a review → approve → upload and **schedule**. | 45 min |
| **Thursday** | **Goes live at 8:00 AM** (scheduled, so you don't need to be free). At lunch: reply to every comment and pin your question. | 15 min |
| **Friday** evening | **Shorts:** `python shorts.py` → 3 clips. Add captions. Schedule for Sat, Mon and Wed on YouTube; post the same files to Reels and TikTok. | 45 min |

## Light week (between videos, or a busy week)

| Day | Task | Time |
| --- | --- | --- |
| Saturday | Film anything useful for next week (long run, b-roll) | Run |
| Sunday | Check-in + 1 Community post (poll, question or prayer-request thread) | 20 min |
| Any evening | Reply to comments; send 1 collaboration message if you want | 15 min |

**A missed week isn't a failure.** The plan is judged over 12 videos, not one week.

## Publish times (Edmonton)

Best slots (1–2 hours before the audience peaks): **Thu 8:00 AM** · **Sun 7:30 AM** · Sat 9:00 AM · Wed 9:30 AM · Fri 11:00 AM.
Thursday 8 AM fits your week best: the edit is done Wednesday night and you can reply at lunch. Faith in Motion could go out **Sunday 7:30 AM** instead.
*(These times come from the old audience. Re-check after about 6 new videos.)*

## One video → Shorts, Reels and TikToks

1. While editing, note 3 moments: **the hook moment**, **the turning point**, and **one number or one verse**.
2. `python shorts.py final.mp4 --clip 0:29-1:05 --clip 7:12-7:50 --clip 18:40-19:15`
   - Use `--mode fit` for wide scenery shots (blurred background) and `--mode center` when you're in the middle of the frame.
3. In CapCut or your editor: add burned-in captions and one line of text at the top (the question).
4. **YouTube:** upload as a Short and set **Related video** to the full video.
5. **Instagram Reels and TikTok:** upload the same file (there's no watermark, because it comes from your own export). Schedule Reels in Meta Business Suite and TikToks in TikTok's web scheduler.
6. Same caption everywhere: one line + "Full video on YouTube: Ada Canada" + 3 hashtags.

## Calendar

Open `calendar/ada_weekly_routine.ics` on your phone or computer to add these blocks as repeating events. You can move or delete them freely afterwards.
