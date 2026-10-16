"""Shared helpers for the Ada Canada toolkit. You never run this file directly."""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_config():
    path = HERE / "config.json"
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        sys.exit("config.json is missing. It must sit in the same folder as the scripts.")
    except json.JSONDecodeError as e:
        sys.exit(f"config.json has a typo (line {e.lineno}): {e.msg}. "
                 "Check for a missing comma or quote.")


def slugify(text, max_len=50):
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return text[:max_len].rstrip("-") or "untitled"


def parse_time(value):
    """'1:05' -> 65, '1:02:03' -> 3723, '-0:30' -> -30, '45' -> 45."""
    value = value.strip()
    sign = -1 if value.startswith("-") else 1
    value = value.lstrip("+-")
    parts = value.split(":")
    if not all(p.isdigit() for p in parts) or not 1 <= len(parts) <= 3:
        raise ValueError(f"'{value}' isn't a time. Use m:ss or h:mm:ss, e.g. 1:45")
    seconds = 0
    for p in parts:
        seconds = seconds * 60 + int(p)
    return sign * seconds


def format_time(seconds):
    """65 -> '1:05', 3723 -> '1:02:03' (YouTube chapter style)."""
    seconds = int(round(seconds))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def playlist_url(playlist_id):
    return f"https://www.youtube.com/playlist?list={playlist_id}"


# Windows terminals can choke on symbols like an arrow; never crash over that.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except Exception:
        pass
