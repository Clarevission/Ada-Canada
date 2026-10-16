"""
chapters.py - checks and shifts YouTube chapter timestamps.

WHAT IT DOES
  Reads a plain text file of chapters (one per line, like "1:23 Race morning").
  'check' tells you if YouTube will accept them. 'shift' moves every
  timestamp by the same amount, which you need after trimming the start of
  a video in Studio's Editor. It only prints text and writes a new file.
  It never touches YouTube.

HOW TO RUN
  1. Copy the chapters from the video description into chapters.txt
  2. Check them:
       python chapters.py check chapters.txt
  3. After trimming 1 min 45 s off the start in Studio:
       python chapters.py shift chapters.txt --by -1:45
     This writes chapters_shifted.txt. Paste it back into the description.

  Easiest: tell it exactly what you cut (use the ORIGINAL video's times).
  You can repeat --cut for several cuts:
       python chapters.py shift chapters.txt --cut 0:00-0:27 --cut 1:12-2:05
"""
import argparse
import re
import sys
from pathlib import Path

from ada_common import format_time, parse_time

LINE = re.compile(r"^\s*\(?((?:\d+:)?\d{1,2}:\d{2})\)?\s*[-–—|:]?\s*(.*)$")


def read_chapters(path):
    chapters, other = [], []
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        m = LINE.match(raw)
        if m:
            chapters.append([parse_time(m.group(1)), m.group(2).strip()])
        elif raw.strip():
            other.append(raw)
    return chapters, other


def problems(chapters, video_length=None):
    out = []
    if not chapters:
        return ["No timestamps found. Lines should look like '1:23 Race morning'."]
    if chapters[0][0] != 0:
        out.append(f"First chapter must start at 0:00 (yours starts at {format_time(chapters[0][0])}).")
    if len(chapters) < 3:
        out.append(f"YouTube needs at least 3 chapters (you have {len(chapters)}).")
    for (a, name_a), (b, _) in zip(chapters, chapters[1:]):
        if b <= a:
            out.append(f"'{format_time(b)}' comes after '{format_time(a)}' but isn't later. Keep them in order.")
        elif b - a < 10:
            out.append(f"'{name_a}' ({format_time(a)}) is only {b - a} s long. Each chapter needs 10 s or more.")
    if video_length and chapters[-1][0] > video_length - 10:
        out.append(f"Last chapter starts at {format_time(chapters[-1][0])}, too close to the end "
                   f"({format_time(video_length)}).")
    for t, name in chapters:
        if not name:
            out.append(f"The chapter at {format_time(t)} has no name.")
    return out


def main():
    p = argparse.ArgumentParser(description="Check or shift YouTube chapters.")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="check chapters against YouTube's rules")
    c.add_argument("file")
    c.add_argument("--length", help="video length, e.g. 21:28")
    s = sub.add_parser("shift", help="move timestamps by a fixed amount")
    s.add_argument("file")
    s.add_argument("--by", help="e.g. -1:45 (earlier) or 0:30 (later)")
    s.add_argument("--cut", action="append", help="a part you removed, ORIGINAL times, e.g. 0:00-0:27 (repeat)")
    s.add_argument("--after", default="0:00", help="only shift chapters at or after this time")
    s.add_argument("--length", help="new video length, e.g. 19:43")
    argv = sys.argv[1:]
    for i, tok in enumerate(argv[:-1]):  # let people type --by -1:45 (argparse would think -1:45 is a flag)
        if tok in ("--by", "--after") and argv[i + 1].startswith("-"):
            argv[i:i + 2] = [f"{tok}={argv[i + 1]}"]
            break
    a = p.parse_args(argv)

    if not Path(a.file).exists():
        sys.exit(f"Can't find {a.file}. Paste the chapters into a text file first.")
    try:
        length = parse_time(a.length) if a.length else None
    except ValueError as e:
        sys.exit(str(e))
    chapters, _ = read_chapters(a.file)

    if a.cmd == "shift":
        if not a.by and not a.cut:
            sys.exit("Tell me what changed: --cut 0:00-0:27 (what you removed) or --by -0:27")
        try:
            cuts = [tuple(parse_time(x) for x in c.split("-", 1)) for c in (a.cut or [])]
            by, after = (parse_time(a.by) if a.by else 0), parse_time(a.after)
        except ValueError as e:
            sys.exit(str(e))
        if any(len(c) != 2 or c[1] <= c[0] for c in cuts):
            sys.exit("Each --cut must look like 1:12-2:05 (start-end, end later than start).")
        new = [[t, n] for t, n in chapters]
        for start, end in sorted(cuts, reverse=True):  # latest cut first, so earlier times stay valid
            for ch in new:
                if start <= ch[0] < end:
                    ch[0] = start  # this chapter began inside the removed part
                elif ch[0] >= end:
                    ch[0] -= end - start
        if by:
            for ch in new:
                if ch[0] >= after and ch[0] != 0:
                    ch[0] += by
        kept = []
        for t, name in sorted(new, key=lambda c: c[0]):
            t = max(0, t)
            if kept and t - kept[-1][0] < 10:  # two chapters squeezed together: keep the later name
                print(f"  merged '{kept[-1][1]}' into '{name}' (they ended up less than 10 s apart)")
                kept[-1] = [0 if kept[-1][0] == 0 else t, name]  # keep the real chapter's time
                continue
            kept.append([t, name])
        if kept and kept[0][0] != 0:  # the first chapter must stay at 0:00
            kept[0][0] = 0
        new = kept
        chapters = new
        out_path = Path(a.file).with_name(Path(a.file).stem + "_shifted.txt")
        out_path.write_text("\n".join(f"{format_time(t)} {n}" for t, n in chapters) + "\n", encoding="utf-8")

    print()
    for t, name in chapters:
        print(f"{format_time(t)} {name}")
    print()
    issues = problems(chapters, length)
    if issues:
        print("Fix before pasting into YouTube:")
        for i in issues:
            print("  - " + i)
    else:
        print(f"OK: {len(chapters)} chapters, YouTube should accept these.")
    if a.cmd == "shift":
        print(f"Saved to {out_path}")


if __name__ == "__main__":
    main()
