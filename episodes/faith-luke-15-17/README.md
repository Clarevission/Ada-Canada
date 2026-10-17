# Episode: Luke 15:17, "Coming to your senses"

**Status:** preview cut built from Niqui's 4 recordings. **Waiting for the Google Flow images and clips** (29 shot slots) and for Niqui to check the [CHECK] items.

## Folders

- `audio/`: the 4 recordings (on your computer only, not in git): 01_hook, 02_the_verse, 03_three_things, 04_for_you_and_prayer
- `visuals/`: put the Flow images (.png/.jpg) and clips (.mp4) here
- `edit.json`: the edit: trims, retake removed, captions, which visual goes where, chapters
- `transcript.json`: machine transcript with timings (raw, before corrections)
- `build/`: renders and outputs (`preview_720p.mp4`, `final_1080p.mp4`, `captions.srt`, `chapters.txt`, `shot_list.md`)

## How to finish it

1. Copy the Flow files into `visuals/`.
2. In `edit.json`, find each shot (S01–S29) and put the file name in `"file"`, e.g. `"file": "flow_father_running.mp4"`. A file can be used for more than one shot. The descriptions in `build/shot_list.md` say what each slot needs.
3. Preview: `python make_episode.py episodes/faith-luke-15-17`
4. When it looks right: `python make_episode.py episodes/faith-luke-15-17 --final`

## Edit decisions already made

- Silence trimmed from the start and end of each recording. The first spoken word lands at 0:00.6.
- **Retake removed:** "…Sunday's episode walks through the whole parable" (04, 81.2–87.8 s). The cleaner second take, "the last episode… including the older brother", is kept.
- Voice: light noise reduction, gentle compression, −14 LUFS (YouTube's level).
- Captions are burned in, except where a text card already shows the same words. The full `captions.srt` should also be uploaded to YouTube.
- About 14 s end-screen hold at the end, with space left for YouTube's video and subscribe elements.

## [CHECK] items for Niqui

See the bottom of `build/shot_list.md`. In short: 7 words the transcriber was unsure of, 2 possible retakes ("Every time, it strikes me. Every time." and "Acknowledge the truth"), the Bible translation on the verse card (wording matches NLT), and the Romans 2:4 card (her paraphrase).

## Open questions

1. **Series name:** the recording says *"Welcome to The Lamp and the Word."* The channel plan calls the faith series *Faith in Motion*. Is this a new series? Same channel?
2. **Episode number:** the recording says the last video "happens to be our first video" and covers the whole parable. That makes this **episode 2**. Is the full-parable episode already published, so the end screen can link to it?
3. **AI visuals:** when uploading, set *Altered or synthetic content = Yes* in Studio, because the Flow scenes show realistic people.
