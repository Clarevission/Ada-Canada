"""
shorts.py - cuts vertical 9:16 clips (Shorts / Reels / TikTok) from a long video.

WHAT IT DOES
  You give it your finished long video and the start-end times you want.
  It makes 1080x1920 .mp4 files in shorts/, ready to upload to YouTube Shorts,
  Instagram Reels and TikTok (the same file works for all three, with no watermark).
  It only reads your video and writes new files. It never uploads anything.

  You need ffmpeg (free):
    Mac:     brew install ffmpeg        (needs Homebrew: https://brew.sh)
    Windows: winget install ffmpeg      (then close and reopen the terminal)

HOW TO RUN
  python shorts.py "sydney_final.mp4" --clip 0:00-0:35 --clip 7:12-7:50 --clip 18:40-19:15

  Framing options (--mode):
    center  (default) crops the middle of the frame: best when you're centred
    left / right      crops that side: use when you're off to one side
    fit               shows the WHOLE wide shot with a blurred copy behind it:
                      best for scenery, finish lines, group shots

  Name the clips (optional):
    python shorts.py video.mp4 --clip 0:00-0:35 --name sydney-hook
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from ada_common import HERE, format_time, parse_time, slugify

FILTERS = {
    "center": "crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=1080:1920,setsar=1",
    "left":   "crop=ih*9/16:ih:0:0,scale=1080:1920,setsar=1",
    "right":  "crop=ih*9/16:ih:iw-ih*9/16:0,scale=1080:1920,setsar=1",
    "fit": ("split[a][b];"
            "[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:3[bg];"
            "[b]scale=1080:-2[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1"),
}


def parse_clip(text):
    if "-" not in text.lstrip("-"):
        raise ValueError(f"'{text}' should look like 1:23-1:52")
    start, end = text.split("-", 1)
    a, b = parse_time(start), parse_time(end)
    if b <= a:
        raise ValueError(f"In '{text}' the end is before the start.")
    return a, b


def main():
    p = argparse.ArgumentParser(description="Cut 9:16 Shorts from a long video into shorts/.")
    p.add_argument("video")
    p.add_argument("--clip", action="append", required=True, help="start-end, e.g. 1:23-1:52 (repeat)")
    p.add_argument("--mode", default="center", choices=sorted(FILTERS))
    p.add_argument("--name", help="base name for the files (default: the video's name)")
    a = p.parse_args()

    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg isn't installed. See the top of this file for the one-line install.")
    src = Path(a.video)
    if not src.exists():
        sys.exit(f"Can't find the video: {src}")
    try:
        clips = [parse_clip(c) for c in a.clip]
    except ValueError as e:
        sys.exit(str(e))

    out_dir = HERE / "shorts"
    out_dir.mkdir(exist_ok=True)
    base = slugify(a.name or src.stem, 30)
    for i, (start, end) in enumerate(clips, 1):
        length = end - start
        if length > 180:
            print(f"  ! Clip {i} is {length} s. Shorts can be up to 3 minutes; Reels and TikToks do best under 60 s.")
        elif length > 60:
            print(f"  note: clip {i} is {length} s. Under 60 s usually performs better on all three apps.")
        out = out_dir / f"{base}_short{i:02d}.mp4"
        vf_flag = "-filter_complex" if a.mode == "fit" else "-vf"
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", str(start), "-i", str(src), "-t", str(length),
               vf_flag, FILTERS[a.mode], "-c:v", "libx264", "-preset", "medium", "-crf", "20",
               "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(out)]
        print(f"  cutting {format_time(start)}-{format_time(end)} -> {out.name} ...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("  ! ffmpeg failed:\n" + result.stderr[-800:])
            continue
    print(f"\nDone. Files are in {out_dir}. Before posting: add captions/on-screen text in your editor, "
          "and on YouTube set 'Related video' to the full video.")


if __name__ == "__main__":
    main()
