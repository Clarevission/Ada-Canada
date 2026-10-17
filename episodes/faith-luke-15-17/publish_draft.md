# DRAFT: publishing package (not posted, needs Niqui's OK item by item)

## Title (pick one; each asks a question or names a stake)

1. Have you ever suddenly seen your life clearly? | Luke 15:17  (59 chars)
2. The moment the prodigal son came to his senses (Luke 15:17)  (59 chars)
3. You don't have to clean yourself up to come home | Luke 15:17  (61 chars, slightly long)

## Thumbnail text (2–4 words; use a Flow still of the son's face or the father running)

A. `HE CAME TO HIS SENSES`
B. `THE MOMENT IT CLICKS`

`python thumbs.py --photo episodes/faith-luke-15-17/visuals/[still].png --text "HE CAME / TO HIS SENSES" --series faith --variants`

## Description

```
Have you ever had a moment where you suddenly saw your life clearly? Luke 15:17 is one line in the story of the prodigal son, and it might be one of the most hopeful sentences in the Bible.

[CHECK: one or two sentences in your own words, e.g. why this verse matters to you]

"When he finally came to his senses, he said to himself, 'At home even the hired servants have food enough to spare, and here I am dying of hunger! I will go home to my father.'" (Luke 15:17-18, NLT) [CHECK: translation]

Chapters
[paste build/chapters.txt here]

If you prayed with me, type "I'm coming home" in the comments. I'll be praying for you by name this week.

Watch the full parable (including the older brother): [CHECK: link to the previous episode]

#prodigalson #bibleverse #christianencouragement
```

## Pinned comment (Niqui posts it as her own comment)

> If you prayed along today, type "I'm coming home" below. I'll be praying for you by name this week. 🙏🏾

## Shorts from this episode (cut from the final video)

| Short | Video times | Why |
| --- | --- | --- |
| "The son came to his senses. But the father had never lost his." | 4:01–4:14 | The emotional peak; works without context |
| The hook: "Have you ever… suddenly saw your life clearly?" | 0:01–0:27 | Question opener, ends on "most hopeful sentence in the Bible" |
| "Your own pig field" | 4:16–4:34 | Speaks straight to the viewer |
| The prayer | 5:06–5:24 | Full prayer; ask "Pray this with me" |

```
python shorts.py episodes/faith-luke-15-17/build/final_1080p.mp4 --clip 4:01-4:14 --clip 0:01-0:27 --clip 4:16-4:34 --clip 5:06-5:24 --name luke15-17 --mode fit
```
Set **Related video** on each Short to this episode.

## Upload checklist

- [ ] Every [CHECK] answered (see build/shot_list.md)
- [ ] Altered or synthetic content: **Yes** (realistic AI-generated people and scenes)
- [ ] Not made for kids
- [ ] Captions: upload `build/captions.srt` (Subtitles → Upload file → With timing)
- [ ] Chapters pasted from `build/chapters.txt`
- [ ] Playlist: [CHECK: Faith in Motion, or a new "The Lamp and the Word" playlist]
- [ ] End screen: previous episode (left) + subscribe (right), last 14 s
- [ ] Add a row to tracker.csv: format = `voiceover`
