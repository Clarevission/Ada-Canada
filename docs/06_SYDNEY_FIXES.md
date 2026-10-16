# Sydney video (OCE_rpdw8iE): fixes, step by step

Order matters: **check → trim → chapters → test thumbnails → Shorts → (maybe) title.**

## Step 1: the 48-hour check (due Fri Oct 16) · 10 min

In Studio → the video → **Analytics → Advanced mode**, set the date range to "Since published" and write down:

| Number | Where | Day-1 value |
| --- | --- | --- |
| Impressions | Reach tab | 346 |
| Impressions click-through rate | Reach tab | 2.0% |
| Views / engaged views | Overview / Engagement | 43 / 17 |
| Average view duration | Engagement | 3:04 overall (engaged viewers 7:49) |
| Watch time (hours) | Overview | 2.2 |
| Retention at 0:30 (%) | Engagement → Audience retention graph | new |
| Biggest drop on the graph (timestamp) | same graph | new |
| Traffic: browse / search / suggested | Reach → Traffic source types | 58 / 14 / 7% |

Add a row to `tracker.csv` (copy the first row and change the numbers and date). Then compare: if search has grown, keep "Sydney Marathon 2026" in the title no matter what.

## Step 2: trim the cold open · 15 min + processing

From the earlier report: "**I don't know if I can do this with my leg**" is at **0:29**, the first clear sentence is at 2:09, and a music-only stretch runs **1:12–2:09**.

1. Studio → the video → **Editor → Trim & cut**.
2. **Cut A (do this one):** remove **0:00 → [CHECK: the frame just before you say "I don't know…", about 0:27]**. The line then lands in the first 2–3 seconds.
3. **Cut B (optional, recommended):** remove the music-only part **1:12 → [CHECK: about 2:05]**, but keep a second or two of lead-in before "It's officially race week".
4. Preview, then **Save**. The video stays live while it processes (can take hours). Views, comments and likes are kept.

## Step 3: shift the chapters · 5 min

Copy the current 16 chapters from the description into a file called `chapters.txt` in the project folder. Then, using the cut lengths you actually made:

Tell it what you removed, using the **original** video's times:

```
# Only cut A:
python chapters.py shift chapters.txt --cut 0:00-0:27

# Both cuts:
python chapters.py shift chapters.txt --cut 0:00-0:27 --cut 1:12-2:05
```

This writes `chapters_shifted.txt`. If two chapters end up less than 10 s apart (for example the old cold-open chapter), it merges them for you. The script checks YouTube's rules (starts at 0:00, at least 3 chapters, each 10 s or longer) and tells you if anything needs fixing. Paste the result into the description **after** the trim has finished processing.

## Step 4: Test & compare thumbnails · 10 min

- Studio → the video → Details → Thumbnail → **Test & compare**.
- Upload **thumb_A_medal.jpg**, **thumb_B_race.jpg**, and optionally a third:
  `python thumbs.py --photo photos/[your best race photo].jpg --text "CAN MY LEG HOLD? / 42.2 KM" --series road --variants`
  (only if that text is true for you).
- Let it run until YouTube declares a winner (usually 1–2 weeks). Don't change the title while it's running.

## Step 5: four Shorts · 45 min

Cut them **from the trimmed version** (download it from Studio) or from your original export. With the original timings:

| Short | Clip idea | Command (original export times; adjust) |
| --- | --- | --- |
| 1 | "I don't know if I can do this with my leg" + what happened next | `--clip 0:29-1:05` |
| 2 | The km 5 → 42 countdown | `--clip [CHECK]` |
| 3 | The finish line | `--clip [CHECK] --mode fit` |
| 4 | "My first star": medal moment + what it meant | `--clip [CHECK]` |

```
python shorts.py "Sydney final.mp4" --clip 0:29-1:05 --clip [..] --clip [..] --clip [..] --name sydney
```
Post 1 every 2 days. On YouTube set **Related video → the Sydney video**. Upload the same files to Reels and TikTok.

## Step 6 (optional): a stakes title · after Test & compare ends

Keep the search words "Sydney Marathon 2026". Options, **only if true**:
1. `I ran my first World Major on a leg I didn't trust | Sydney Marathon 2026` (from the earlier report)
2. `Can my injured leg survive 42.2 km? | Sydney Marathon 2026`
3. `My first World Marathon Major after an IT band injury | Sydney 2026`

Niqui picks. Change it once, then leave it for at least 2 weeks.

## Step 7: share it where people already care

Send it to the Nigerian runners who appear in the video and to any running or church groups you're part of. Viewers who care watch longest, and that tells YouTube to show it to more people. (It's a personal share, not an engagement pod: no asks to like or sub.)
