"""
make_episode.py - builds a voiceover video from recordings + images/clips.

WHAT IT DOES
  Reads an episode folder's edit.json and:
    1. joins the voice recordings (trimmed, retakes removed), cleans them
       lightly and sets YouTube loudness (-14 LUFS)
    2. puts each image or video clip from visuals/ where edit.json says,
       with a slow zoom on stills and soft crossfades
    3. adds the text cards (verse, points, prayer, end screen) and captions
    4. writes the video plus captions.srt, chapters.txt and shot_list.md
  It only writes files in the episode's build/ folder. It never uploads.

HOW TO RUN
  python make_episode.py episodes/faith-luke-15-17            quick 720p preview
  python make_episode.py episodes/faith-luke-15-17 --final    full 1080p, stops if any shot is missing

  Missing images/clips show as labelled placeholders in the preview, so you
  can check pacing before the visuals are ready. Needs ffmpeg.
"""
import argparse
import json
import math
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
except ImportError:
    sys.exit("Pillow isn't installed. Run:  pip install Pillow")

HERE = Path(__file__).resolve().parent
FONTS = HERE / "fonts"
IMG_EXT = {".png", ".jpg", ".jpeg", ".webp"}
VID_EXT = {".mp4", ".mov", ".m4v", ".webm"}

CREAM, GOLD, INK = (244, 234, 216), (217, 164, 65), (20, 16, 13)


def run(cmd, quiet=True):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("ffmpeg failed:\n" + " ".join(map(str, cmd))[:600] + "\n" + r.stderr[-1500:])
    return r


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                          str(path)], capture_output=True, text=True).stdout.strip()
    return float(out)


def font(name, size):
    for cand in [FONTS / name, Path("/usr/share/fonts/opentype/inter") / name]:
        if cand.exists():
            return ImageFont.truetype(str(cand), size)
    fallback = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
    return ImageFont.truetype(fallback if Path(fallback).exists() else "DejaVuSans.ttf", size)


def ts(sec):
    h, rem = divmod(max(0.0, sec), 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}".replace(".", ",")


def chapter_ts(sec):
    sec = int(round(sec))
    m, s = divmod(sec, 60)
    return f"{m}:{s:02d}"


# ---------------------------------------------------------------- timeline
class Timeline:
    def __init__(self, ed):
        self.offsets, t = {}, 0.6  # short lead-in so the first word isn't on frame 1
        for i, c in enumerate(ed["clips"]):
            self.offsets[c["id"]] = (t, c)
            t += c["out"] - c["in"]
            if i < len(ed["clips"]) - 1:
                t += ed.get("gap_between_clips", 0.6)
        self.speech_end = t
        self.total = t + ed.get("outro_hold", 0)

    def at(self, clip_id, sec):
        start, c = self.offsets[clip_id]
        return start + (min(max(sec, c["in"]), c["out"]) - c["in"])


# ---------------------------------------------------------------- audio
def build_audio(ep, ed, tl, out):
    inputs, parts = [], []
    for i, c in enumerate(ed["clips"]):
        inputs += ["-i", str(ep / c["file"])]
        start, _ = tl.offsets[c["id"]]
        dur = c["out"] - c["in"]
        delay = int(start * 1000)
        parts.append(f"[{i}:a]aformat=sample_rates=48000:channel_layouts=mono,"
                     f"atrim={c['in']}:{c['out']},asetpts=PTS-STARTPTS,"
                     f"afade=t=in:d=0.04,afade=t=out:st={dur - 0.06:.3f}:d=0.06,adelay={delay}[a{i}]")
    n = len(ed["clips"])
    mix = "".join(f"[a{i}]" for i in range(n))
    graph = ";".join(parts) + f";{mix}amix=inputs={n}:normalize=0,apad=whole_dur={tl.total:.3f}," \
            "highpass=f=75,afftdn=nf=-30,acompressor=threshold=-20dB:ratio=2.5:attack=10:release=200," \
            "loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000[v]"
    music = ed.get("music")
    if music and (ep / music).exists():
        inputs += ["-stream_loop", "-1", "-i", str(ep / music)]
        graph += (f";[{n}:a]volume={ed.get('music_volume_db', -26)}dB,atrim=0:{tl.total:.3f},"
                  f"afade=t=in:d=2,afade=t=out:st={tl.total - 4:.3f}:d=4[m];"
                  "[m][v]sidechaincompress=threshold=0.02:ratio=6:release=400[md];[v][md]amix=inputs=2:normalize=0[out]")
        label = "[out]"
    else:
        label = "[v]"
    run(["ffmpeg", "-y", *inputs, "-filter_complex", graph, "-map", label, "-t", f"{tl.total:.3f}",
         "-c:a", "pcm_s16le", "-ac", "2", str(out)])


# ---------------------------------------------------------------- cards and placeholders
def backdrop(W, H, seed=0):
    """Deep warm gradient with a soft glow: the card background."""
    img = Image.new("RGB", (W, H), INK)
    glow = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(glow)
    cx, cy = W * (0.5 + 0.18 * math.sin(seed)), H * 0.42
    for r in range(int(W * 0.7), 0, -12):
        d.ellipse((cx - r, cy - r * 0.62, cx + r, cy + r * 0.62), fill=int(70 * (1 - r / (W * 0.7)) ** 1.6))
    warm = Image.new("RGB", (W, H), (120, 78, 38))
    img = Image.composite(warm, img, glow.filter(ImageFilter.GaussianBlur(60)))
    return img


def wrap_to_width(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def centered(draw, lines, fnt, W, y, fill, gap=1.25):
    size = fnt.size
    for ln in lines:
        w = draw.textlength(ln, font=fnt)
        draw.text(((W - w) / 2, y), ln, font=fnt, fill=fill)
        y += size * gap
    return y


def gold_rule(draw, W, y, half=70):
    draw.line((W / 2 - half, y, W / 2 + half, y), fill=GOLD, width=3)


def render_card(beat, W, H, seed):
    img = backdrop(W, H, seed)
    d = ImageDraw.Draw(img)
    k = W / 1920
    serif = lambda s: font("CormorantGaramond-600.ttf", int(s * k))
    italic = lambda s: font("CormorantGaramond-600italic.ttf", int(s * k))
    sans = lambda s: font("Inter-SemiBold.otf", int(s * k))
    kind, title, sub = beat["card"], beat.get("title", ""), beat.get("sub", "")
    if kind == "title":
        f = serif(120)
        y = centered(d, [title], f, W, H * 0.36, CREAM)
        gold_rule(d, W, y + 20 * k)
        centered(d, [sub], italic(54), W, y + 50 * k, (226, 205, 170))
    elif kind == "ref":
        centered(d, [title], serif(150), W, H * 0.40, CREAM)
    elif kind == "verse":
        f = italic(64)
        lines = wrap_to_width(d, title, f, W * 0.74)
        total = len(lines) * f.size * 1.3
        y = (H - total) / 2 - 60 * k
        y = centered(d, lines, f, W, y, CREAM, 1.3)
        gold_rule(d, W, y + 30 * k)
        centered(d, [sub.upper()], sans(30), W, y + 60 * k, GOLD)
    elif kind == "quote":
        f = italic(84)
        lines = wrap_to_width(d, title, f, W * 0.7)
        y = (H - len(lines) * f.size * 1.3) / 2 - 40 * k
        y = centered(d, lines, f, W, y, CREAM, 1.3)
        gold_rule(d, W, y + 30 * k)
        centered(d, [sub.upper()], sans(30), W, y + 60 * k, GOLD)
    elif kind == "heading":
        centered(d, wrap_to_width(d, title, serif(104), W * 0.8), serif(104), W, H * 0.38, CREAM)
    elif kind == "point":
        centered(d, [beat.get("num", "")], serif(220), W, H * 0.22, GOLD)
        gold_rule(d, W, H * 0.22 + 250 * k)
        centered(d, wrap_to_width(d, title, serif(96), W * 0.8), serif(96), W, H * 0.22 + 290 * k, CREAM)
    elif kind == "steps":
        items = title.split("|")
        f = serif(76)
        y = H * 0.27
        for i, it in enumerate(items, 1):
            line = f"{i}.  {it}"
            w = d.textlength(line, font=f)
            d.text(((W - w) / 2, y), line, font=f, fill=CREAM)
            y += f.size * 1.6
    elif kind == "cta":
        centered(d, [title], serif(110), W, H * 0.34, CREAM)
        gold_rule(d, W, H * 0.34 + 150 * k)
        centered(d, wrap_to_width(d, sub, italic(52), W * 0.7), italic(52), W, H * 0.34 + 180 * k, (226, 205, 170))
    elif kind == "endscreen":
        # leaves the left video slot and right subscribe slot clear for YouTube's end-screen elements
        centered(d, [title], serif(84), W, H * 0.12, CREAM)
        gold_rule(d, W, H * 0.12 + 110 * k)
        centered(d, [sub], italic(44), W, H * 0.12 + 130 * k, (226, 205, 170))
    else:
        centered(d, [title], serif(90), W, H * 0.4, CREAM)
    return img


def render_placeholder(beat, W, H, seed):
    img = backdrop(W, H, seed + 1.3).filter(ImageFilter.GaussianBlur(2))
    d = ImageDraw.Draw(img)
    k = W / 1920
    lab = font("Inter-SemiBold.otf", int(34 * k))
    txt = font("CormorantGaramond-600italic.ttf", int(58 * k))
    x0, y0 = 150 * k, 110 * k  # inside the area that stays visible during the slow zoom
    d.rounded_rectangle((x0, y0, x0 + d.textlength(f"FLOW SHOT {beat['shot']}", font=lab) + 48 * k,
                         y0 + 64 * k), radius=int(14 * k), outline=GOLD, width=2)
    d.text((x0 + 24 * k, y0 + 12 * k), f"FLOW SHOT {beat['shot']}", font=lab, fill=GOLD)
    lines = wrap_to_width(d, beat.get("desc", ""), txt, W * 0.7)
    centered(d, lines, txt, W, H * 0.36, (210, 196, 172), 1.3)
    return img


# ---------------------------------------------------------------- segments
def motion_expr(motion, frames):
    z = f"1+0.10*on/{frames}"
    if motion == "out":
        z = f"1.10-0.10*on/{frames}"
    x, y = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    if motion == "left":
        z, x = "1.08", f"(iw-iw/zoom)*(1-on/{frames})"
    elif motion == "right":
        z, x = "1.08", f"(iw-iw/zoom)*on/{frames}"
    elif motion == "up":
        z, y = "1.08", f"(ih-ih/zoom)*(1-on/{frames})"
    return z, x, y


def still_segment(png, out, dur, W, H, fps, motion, enc):
    frames = max(1, int(round(dur * fps)))
    z, x, y = motion_expr(motion, frames)
    vf = (f"scale={W * 2}:{H * 2}:force_original_aspect_ratio=increase,crop={W * 2}:{H * 2},"
          f"zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s={W}x{H}:fps={fps},format=yuv420p")
    run(["ffmpeg", "-y", "-loop", "1", "-i", str(png), "-vf", vf, "-frames:v", str(frames), *enc, str(out)])


def video_segment(src, out, dur, W, H, fps, enc):
    src_dur = duration(src)
    factor = dur / src_dur if src_dur > 0 else 1
    cover = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={fps},format=yuv420p"
    if factor <= 1.0:
        vf, pre = cover, []
    elif factor <= 1.6:  # gently slow it down rather than loop
        vf, pre = f"setpts={factor:.4f}*PTS,{cover}", []
    else:
        vf, pre = cover, ["-stream_loop", "-1"]
    run(["ffmpeg", "-y", *pre, "-i", str(src), "-an", "-vf", vf, "-t", f"{dur:.3f}", *enc, str(out)])


# ---------------------------------------------------------------- captions
def write_srt(caps, path):
    with open(path, "w", encoding="utf-8") as f:
        for i, (s, e, t) in enumerate(caps, 1):
            f.write(f"{i}\n{ts(s)} --> {ts(e)}\n{t}\n\n")


def write_ass(caps, path, W, H):
    size = int(52 * W / 1920)
    margin = int(70 * H / 1080)
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter,{size},&H00F4F7FA,&H000000FF,&H00101010,&H78000000,-1,0,0,0,100,100,0,0,1,{max(2, size // 18)},{max(1, size // 26)},2,{int(W * 0.12)},{int(W * 0.12)},{margin},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    def a(sec):
        h, rem = divmod(max(0.0, sec), 3600)
        m, s = divmod(rem, 60)
        return f"{int(h)}:{int(m):02d}:{s:05.2f}"
    with open(path, "w", encoding="utf-8") as f:
        f.write(head)
        for s, e, t in caps:
            f.write(f"Dialogue: 0,{a(s)},{a(e)},Cap,,0,0,0,,{{\\fad(120,120)}}{t}\n")


# ---------------------------------------------------------------- main
def main():
    p = argparse.ArgumentParser(description="Build a voiceover episode from edit.json")
    p.add_argument("episode", help="episode folder, e.g. episodes/faith-luke-15-17")
    p.add_argument("--final", action="store_true", help="1080p, high quality, every shot must exist")
    p.add_argument("--no-captions", action="store_true", help="don't burn captions into the picture")
    a = p.parse_args()

    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg isn't installed (Mac: brew install ffmpeg, Windows: winget install ffmpeg).")
    ep = Path(a.episode).resolve()
    ed = json.loads((ep / "edit.json").read_text(encoding="utf-8"))
    build, seg_dir = ep / "build", ep / "build" / "segments"
    seg_dir.mkdir(parents=True, exist_ok=True)
    W, H = (1920, 1080) if a.final else (1280, 720)
    fps = ed.get("fps", 30)
    xf = ed.get("crossfade", 0.5)
    enc = (["-c:v", "libx264", "-preset", "medium", "-crf", "16"] if a.final
           else ["-c:v", "libx264", "-preset", "veryfast", "-crf", "22"])
    tl = Timeline(ed)

    # visuals: resolve files, check what's missing
    beats = sorted(ed["beats"], key=lambda b: tl.at(b["clip"], b["at"]))
    missing = []
    for b in beats:
        if "card" in b:
            continue
        f = b.get("file")
        if f and not (ep / "visuals" / f).exists():
            sys.exit(f"edit.json names visuals/{f} for shot {b['shot']}, but that file isn't there.")
        if not f:
            missing.append(b["shot"])
    if a.final and missing:
        sys.exit("These shots have no file yet: " + ", ".join(missing) +
                 "\nPut the files in visuals/ and write their names in edit.json (or run without --final).")

    print(f"1/4 Audio: {len(ed['clips'])} recordings -> {tl.speech_end:.1f}s of speech + {ed.get('outro_hold', 0)}s end screen")
    voice = build / "voice.wav"
    build_audio(ep, ed, tl, voice)

    print(f"2/4 Visuals: {len(beats)} beats ({len(missing)} placeholders)")
    starts = [0.0] + [tl.at(b["clip"], b["at"]) for b in beats[1:]]
    ends = starts[1:] + [tl.total]
    seg_files, slots = [], []
    for i, (b, s, e) in enumerate(zip(beats, starts, ends)):
        slot = e - s
        seg_len = slot + (xf if i < len(beats) - 1 else 0)
        out = seg_dir / f"seg{i:03d}.mp4"
        if "card" in b:
            png = seg_dir / f"card{i:03d}.png"
            render_card(b, W, H, i).save(png)
            still_segment(png, out, seg_len, W, H, fps, "in", enc)
        elif b.get("file"):
            src = ep / "visuals" / b["file"]
            if src.suffix.lower() in VID_EXT:
                video_segment(src, out, seg_len, W, H, fps, enc)
            else:
                still_segment(src, out, seg_len, W, H, fps, b.get("motion", "in"), enc)
        else:
            png = seg_dir / f"ph{i:03d}.png"
            render_placeholder(b, W, H, i).save(png)
            still_segment(png, out, seg_len, W, H, fps, b.get("motion", "in"), enc)
        seg_files.append(out)
        slots.append(slot)
        print(f"   {i + 1:2d}/{len(beats)} {chapter_ts(s):>6}  {b.get('shot') or b['card']}")

    print("3/4 Captions, chapters, shot list")
    caps_all, caps_burn = [], []
    for c in ed["captions"]:
        s, e = tl.at(c["clip"], c["s"]), tl.at(c["clip"], c["e"]) + 0.15
        caps_all.append((s, e, c["t"]))
        if c.get("burn", True):
            caps_burn.append((s, e, c["t"]))
    write_srt(caps_all, build / "captions.srt")
    ass = build / "captions.ass"
    write_ass(caps_burn, ass, W, H)
    chap = [f"{chapter_ts(0 if i == 0 else tl.at(c['clip'], c['at']))} {c['title']}"
            for i, c in enumerate(ed.get("chapters", []))]
    (build / "chapters.txt").write_text("\n".join(chap) + "\n", encoding="utf-8")
    lines = ["# Shot list: " + ed.get("title", ""), "",
             "Put each image or clip in `visuals/` and write its file name in that shot's `file` in edit.json.", "",
             "| Shot | At | Length | What it shows | File |", "| --- | --- | --- | --- | --- |"]
    for b, s, sl in zip(beats, starts, slots):
        if "card" in b:
            continue
        lines.append(f"| {b['shot']} | {chapter_ts(s)} | {sl:.0f}s | {b['desc']} | {b.get('file') or '**needed**'} |")
    checks = [f"- {c['t']}  ({c['check']})" for c in ed["captions"] if c.get("check")]
    checks += [f"- Card: {b['title'][:60]}  ({b['check']})" for b in beats if b.get("check")]
    if checks:
        lines += ["", "## [CHECK] before publishing", *checks]
    (build / "shot_list.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("4/4 Rendering video")
    inputs = []
    for f in seg_files:
        inputs += ["-i", str(f)]
    chain, last, acc = [], "[0:v]", 0.0
    for i in range(1, len(seg_files)):
        acc += slots[i - 1]
        lab = f"[x{i}]"
        chain.append(f"{last}[{i}:v]xfade=transition=fade:duration={xf}:offset={acc:.3f}{lab}")
        last = lab
    post = f"fade=t=in:d=0.6,fade=t=out:st={tl.total - 1.2:.3f}:d=1.2"
    if not a.no_captions:
        post += f",ass={ass.as_posix()}"
    chain.append(f"{last}{post},format=yuv420p[vout]")
    name = "final_1080p.mp4" if a.final else "preview_720p.mp4"
    out = build / name
    run(["ffmpeg", "-y", *inputs, "-i", str(voice), "-filter_complex", ";".join(chain),
         "-map", "[vout]", "-map", f"{len(seg_files)}:a", "-t", f"{tl.total:.3f}",
         *enc, "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)])
    print(f"\nDone: {out}  ({chapter_ts(duration(out))})")
    print(f"Also in build/: captions.srt (upload to YouTube), chapters.txt, shot_list.md")
    if missing:
        print(f"{len(missing)} shots are placeholders. See build/shot_list.md.")


if __name__ == "__main__":
    main()
