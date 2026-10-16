"""
brief.py - makes a ready-to-fill video brief.

WHAT IT DOES
  Writes a one-page plan for a video: 3 title options, 2 thumbnail texts,
  a 5-second hook, an outline with timestamps, a description with the
  playlist link, a pinned question, 3 Short ideas and the best publish slot.
  It only writes a file in briefs/. It never touches YouTube.

  Anything in [CHECK: ...] is something only you know. Fill it in or delete it.
  The script never invents facts about your life, races or times.

HOW TO RUN (examples)
  Road to 6 Stars (write the topic as what you're TRYING to do):
    python brief.py "run my first 10K since Sydney" --series road
    python brief.py "run a sub-4 marathon" --series road --stake "after an IT band injury"

  Faith in Motion (write the topic as a short theme):
    python brief.py "letting go of control" --series faith --scripture "Proverbs 3:5-6"

  Follow-along (huge for watch hours):
    python brief.py "treadmill run" --series road --format followalong --length 30

  Timely video (race, event): add the event date and it warns you about
  the 7-day window:
    python brief.py "run the Edmonton Half" --series road --event-date 2026-11-01
"""
import argparse
import datetime as dt
import re
import sys

from ada_common import format_time, load_config, playlist_url, slugify, HERE

FORMATS = ("simple", "cinematic", "followalong")
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def chk(text):
    return f"[CHECK: {text}]"


def title_options(topic, series, fmt, length, stake, scripture):
    t = topic.strip().rstrip("?.!")
    cap = t[0].upper() + t[1:]
    if fmt == "followalong":
        return [
            f"{length}-Minute {cap.title()} With Me | Follow Along + Scripture",
            f"Pray and Run With Me: {length}-Minute {cap.title()}",
            f"{length} Minutes, One Verse: {cap.title()} for When You Feel Stuck",
        ]
    if series == "road":
        s = stake or chk("the real obstacle, e.g. 'on a leg I didn't trust'")
        return [
            f"Can I {t} {s}?",
            f"I tried to {t}. {chk('the honest result in 3-5 words, only if true')}",
            f"{chk('a real number: weeks, km or a time')} to {t}: what really happened",
        ]
    ref = scripture or chk("verse, e.g. Matthew 6:33")
    return [
        f"Struggling with {t}? Read {ref} with me",
        f"What {ref} taught me about {t} (on a run)",
        f"I almost gave up on {t}. Then {ref}. {chk('only if this is true')}",
    ]


def thumb_texts(topic, series, fmt, length, scripture):
    words = [w for w in topic.upper().replace("?", "").split()
             if w not in {"A", "AN", "THE", "MY", "OF", "TO", "WITH", "FOR", "AND"}]
    short = " ".join(words[:3])
    if fmt == "followalong":
        return [f"{length} MIN / RUN WITH ME", f"{short} + SCRIPTURE"]
    if series == "road":
        return ["CAN I DO THIS?", chk("2-4 words: a number or place, e.g. 42.2 KM or EDMONTON -> SYDNEY")]
    return [(scripture or "THE VERSE").upper(),
            short if len(words) <= 3 else chk(f"2-3 word feeling from '{topic}', e.g. LET IT GO")]


def outline(series, fmt, length):
    L = length * 60
    rows = [
        (0, 5, "HOOK: your most dramatic moment + ONE spoken sentence of stakes. No music-only intro."),
        (5, 20, "STAKES: why this matters to you and what could go wrong."),
        (20, 30, "PROMISE: what they get if they stay ('By the end you'll see...')."),
    ]
    if fmt == "followalong":
        warm = 180
        cool = 180
        pray = 120
        main_end = L - cool - pray - 30
        rows += [
            (30, warm, "WARM-UP together: easy pace, tell them what's coming. Read the verse once."),
            (warm, main_end // 2, "MAIN BLOCK part 1: talk them through effort ('you should be able to talk')."),
            (main_end // 2, main_end, "MAIN BLOCK part 2: reflect on the verse in 2-3 short bursts. Keep talking every ~60 s."),
            (main_end, main_end + cool, "COOL-DOWN: slow it down, celebrate them."),
            (main_end + cool, L - 30, "PRAYER: short, sincere prayer for the viewer."),
        ]
    else:
        body_start, body_end = 30, int(L * 0.85)
        third = (body_end - body_start) // 3
        b1, b2 = body_start + third, body_start + 2 * third
        if series == "road":
            rows += [
                (body_start, b1, "BEAT 1, the setup: where you are right now (honest numbers, real feelings)."),
                (b1, b2, "BEAT 2, the struggle: the hardest part. Re-hook at the start: 'But then...'"),
                (b2, body_end, "BEAT 3, the result: show it, then say what it meant."),
                (body_end, L - 30, "FAITH MOMENT: the verse or prayer that carried you (30-60 s, not a sermon)."),
            ]
        else:
            rows += [
                (body_start, b1, "THE VERSE: read it on camera, say plainly what it means."),
                (b1, b2, "YOUR STORY: where this verse met your real life (running or not)."),
                (b2, body_end, "ON THE RUN: b-roll with you TALKING over it. Music-only stretches max 20 s."),
                (body_end, L - 30, "APPLICATION: one thing the viewer can do this week."),
            ]
    rows.append((L - 30, L, "CLOSE: ask the pinned question out loud, point to the next video in the series (end screen, 20 s)."))
    return rows


def publish_slots(cfg, ready_date, deadline=None, count=3):
    peaks = {p["day"]: p for p in cfg["publish_peaks_edmonton"]}
    slots, day = [], ready_date
    for _ in range(60):
        name = DAYS[day.weekday()]
        if name in peaks:
            if deadline and day > deadline:
                break
            slots.append(f"{name} {day.isoformat()} at {peaks[name]['publish']} Edmonton time "
                         f"(peak ~{peaks[name]['peak']})")
            if len(slots) == count:
                break
        day += dt.timedelta(days=1)
    return slots


def build(args, cfg):
    s = cfg["series"][args.series]
    today = dt.date.today()
    titles = title_options(args.topic, args.series, args.format, args.length, args.stake, args.scripture)
    thumbs = thumb_texts(args.topic, args.series, args.format, args.length, args.scripture)
    rows = outline(args.series, args.format, args.length)
    pl = playlist_url(s["playlist_id"])
    greet = cfg["channel"]["greeting"]

    timing_note = ""
    deadline = None
    if args.event_date:
        event = dt.date.fromisoformat(args.event_date)
        deadline = event + dt.timedelta(days=cfg["targets"]["timely_upload_days"])
        left = (deadline - today).days
        timing_note = (f"**TIMELY VIDEO.** Event {event}. Upload by **{deadline}** "
                       f"({left} days from today). After that, searches for this event drop fast. "
                       "A simpler video on time beats a perfect one late.")
        ready = max(today + dt.timedelta(days=1), event + dt.timedelta(days=1))
    else:
        ready = today + dt.timedelta(days=7)
    slots = publish_slots(cfg, ready, deadline)

    out = []
    w = out.append
    w(f"# Brief: {args.topic}")
    w(f"Series: **{s['name']}** | Format: **{args.format}** | Length: ~{args.length} min | Made {today}")
    w("")
    if timing_note:
        w(timing_note)
        w("")
    w("## 1. Title: pick one (each asks a question or names a stake)")
    for i, t in enumerate(titles, 1):
        n = len(re.sub(r"\[CHECK:[^\]]*\]", "", t))
        has_fill = "[CHECK" in t
        if n > 60:
            flag = f"  <- {n} chars{' before your fill-in' if has_fill else ''}; phones cut after ~60, shorten"
        elif has_fill:
            flag = f"  ({n} chars before your fill-in; keep the total under ~60)"
        else:
            flag = f"  ({n} chars)"
        w(f"{i}. {t}{flag}")
    w("")
    w("Only use a title if every word of it is true.")
    w("")
    w("## 2. Thumbnail text (2-4 words, never repeat the title)")
    for i, t in enumerate(thumbs, 1):
        w(f"{chr(64 + i)}. `{t}`")
    w("")
    w(f"Make both: `python thumbs.py --text \"{thumbs[0]}\" --series {args.series} --variants`")
    w("Then run Test & compare in Studio with the two best.")
    w("")
    w("## 3. The 5-second hook (see docs/03_OPENING_SCRIPT.md)")
    if args.format == "followalong":
        w("- **Show (0:00):** you, ready to go, looking straight at the camera (no intro music).")
        w(f"- **Say (by 0:05):** \"{greet}, grab your shoes. For the next {args.length} minutes you're doing "
          f"this {args.topic.lower()} with me, and I'll pray with you at the end.\" {chk('reword in your voice')}")
        w("- **Stakes (0:05-0:20):** who this is for (\"if you can't get yourself out the door today, this is for you\").")
        w(f"- **Promise (0:20-0:30):** \"By the end you'll have {args.length} minutes done and one verse "
          "to carry into your week.\"")
    else:
        w(f"- **Show (0:00):** {chk('the single most dramatic clip: the moment it could all go wrong')}")
        stake_line = args.stake or chk("the stake in one sentence, in your words")
        w(f"- **Say (by 0:05):** \"{stake_line}\"")
        w(f"- **Stakes (0:05-0:20):** {chk('why it matters and what could go wrong')}")
        w(f"- **Promise (0:20-0:30):** \"Stay with me, because by the end {chk('what they will see or get')}.\"")
    w("")
    w("## 4. Outline")
    w("| Time | What happens |")
    w("| --- | --- |")
    for a, b, text in rows:
        w(f"| {format_time(a)}-{format_time(b)} | {text} |")
    w("")
    w(f"Rules: talk over every montage. No music-only stretch longer than "
      f"{cfg['targets']['music_only_max_seconds']} s.")
    w("")
    w("## 5. Description (copy, then fill the [CHECK]s)")
    w("```")
    w(chk(f"first line shows in search: one sentence with the words people type, e.g. '{args.topic}'"))
    w("")
    w(f"{greet}! {chk('2-3 sentences in your own voice about this video')}")
    w("")
    w(f"▶ Watch the whole {s['name']} series: {pl}")
    w("")
    w("Chapters")
    for a, _, text in rows:
        w(f"{format_time(a)} {chk('chapter name: ' + text.split(':')[0].title())}")
    w("")
    w("I'm Niqui, a Nigerian-Canadian runner in Edmonton chasing the World Marathon Majors, "
      "with faith carrying every kilometre. Subscribe to run the road with me.")
    w("")
    w(" ".join(s["hashtags"]))
    w("```")
    w("YouTube chapter rules: first chapter must be 0:00, at least 3 chapters, each at least 10 s. "
      "Check yours with `python chapters.py check chapters.txt`.")
    w("")
    w("## 6. Pinned question (pick one, post it as your own comment, pin it)")
    for q in s["pinned_questions"]:
        w(f"- {q}")
    w("")
    w("## 7. Three Shorts from the same footage (cut with shorts.py)")
    w(f"1. **The hook moment** (20-40 s): the first 5 seconds of this video plus what happens next. "
      f"On-screen text: the title question. Set 'Related video' to this video.")
    w("2. **The turning point** (30-45 s): you talking to camera about the hardest part. End on the lesson.")
    if args.series == "road":
        w("3. **One number** (15-30 s): the stat that surprised you (pace, km, heart rate) with your honest reaction.")
    else:
        w(f"3. **The verse** (15-30 s): read {args.scripture or 'the verse'} over running footage; "
          "verse stays on screen at the end.")
    w("")
    w("## 8. When to publish")
    if slots:
        for sl in slots:
            w(f"- {sl}")
    else:
        w("- No peak slot left before the 7-day deadline: publish as soon as it's ready.")
    w("Schedule it in Studio so you don't need to be free. Reply to comments in the first few hours if you can.")
    w("")
    w("## 9. Before you hit schedule")
    w("- [ ] Every [CHECK] filled or deleted, and every claim true")
    w("- [ ] First spoken sentence lands by 0:05")
    w("- [ ] Added to the playlist: " + s["playlist_name"])
    w("- [ ] End screen points to the next video in the series")
    w("- [ ] 'Not made for kids' set")
    w("- [ ] Thumbnail checked at phone size (thumbs/preview_small.jpg)")
    w("- [ ] Added a row to tracker.csv for this video (format = " + args.format + ")")
    w("- [ ] Niqui approved title, description, thumbnail and pinned comment")
    return "\n".join(out) + "\n"


def main():
    cfg = load_config()
    p = argparse.ArgumentParser(description="Make a video brief (writes a file in briefs/).")
    p.add_argument("topic", help="Road: what you're trying to do ('run my first 10K since Sydney'). "
                                 "Faith: the theme ('letting go of control').")
    p.add_argument("--series", required=True, choices=sorted(cfg["series"]))
    p.add_argument("--format", default="simple", choices=FORMATS,
                   help="simple = talk-to-camera, cinematic = full edit, followalong = run/walk with me")
    p.add_argument("--length", type=int, default=15, help="planned length in minutes (default 15)")
    p.add_argument("--stake", help="the real thing at risk, in your words")
    p.add_argument("--scripture", help="e.g. 'Matthew 6:33'")
    p.add_argument("--event-date", help="race or event date YYYY-MM-DD (turns on the 7-day warning)")
    p.add_argument("--print-only", action="store_true", help="show it but don't save a file")
    args = p.parse_args()
    if args.length < 2:
        sys.exit("--length must be at least 2 minutes.")
    if args.event_date:
        try:
            dt.date.fromisoformat(args.event_date)
        except ValueError:
            sys.exit("--event-date must look like 2026-11-01")

    text = build(args, cfg)
    print(text)
    if not args.print_only:
        path = HERE / "briefs" / f"{dt.date.today().isoformat()}-{slugify(args.topic)}.md"
        path.parent.mkdir(exist_ok=True)
        path.write_text(text, encoding="utf-8")
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
