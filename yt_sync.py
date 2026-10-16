"""
yt_sync.py - OPTIONAL. Fills tracker.csv and channel.csv from YouTube for you.

WHAT IT DOES
  Logs in to YOUR YouTube account with READ-ONLY permission (it cannot
  upload, edit, delete, comment or change anything; Google enforces that).
  Then it reads your subscriber count and, for recent videos, views, engaged
  views, watch time, average view duration and subscribers gained, and adds
  one row per video to tracker.csv plus one row to channel.csv.

  What it CAN'T get: impressions and click-through rate. The API doesn't
  provide them, so copy those two numbers from Studio by hand (2 minutes).

  Setup first (one time, about 20 minutes): docs/05_YOUTUBE_API_SETUP.md
  Your keys live in secrets/, which is never shared or committed.

HOW TO RUN
  python yt_sync.py test          check the login works (shows your channel name)
  python yt_sync.py week          add this week's rows
  python yt_sync.py week --since 2026-09-01    include older videos too
"""
import argparse
import csv
import datetime as dt
import re
import sys

from ada_common import HERE, load_config

SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]
SECRETS = HERE / "secrets"
CLIENT_FILE = SECRETS / "client_secret.json"
TOKEN_FILE = SECRETS / "token.json"
TRACKER_FIELDS = ["date", "video_id", "title", "series", "format", "published", "impressions", "ctr_pct",
                  "views", "engaged_pct", "avg_view_min", "length_min", "watch_hours", "subs_net",
                  "hook_by_5s", "notes"]
CHANNEL_FIELDS = ["date", "subscribers", "ypp_watch_hours", "shorts_views_90d", "notes"]


def services():
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError:
        sys.exit("The Google libraries aren't installed. Run:\n"
                 "  pip install google-api-python-client google-auth-oauthlib")
    if not CLIENT_FILE.exists():
        sys.exit(f"Missing {CLIENT_FILE}. Follow docs/05_YOUTUBE_API_SETUP.md step 4.")
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None  # token expired (common while the Google app is in 'Testing'); log in again
        if not creds or not creds.valid:
            print("A browser window will open. Sign in with the Google account that owns Ada Canada "
                  "and allow READ-ONLY access.")
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        SECRETS.mkdir(exist_ok=True)
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
    yt = build("youtube", "v3", credentials=creds, cache_discovery=False)
    yta = build("youtubeAnalytics", "v2", credentials=creds, cache_discovery=False)
    return yt, yta


def iso_minutes(duration):
    """'PT21M28S' -> 21.47"""
    m = re.fullmatch(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration or "")
    if not m:
        return None
    d, h, mi, s = (int(x or 0) for x in m.groups())
    return round(d * 1440 + h * 60 + mi + s / 60, 2)


def my_channel(yt):
    res = yt.channels().list(part="snippet,statistics,contentDetails", mine=True).execute()
    if not res.get("items"):
        sys.exit("This Google account has no YouTube channel. Sign in with the Ada Canada account "
                 "(delete secrets/token.json and run again).")
    return res["items"][0]


def recent_videos(yt, uploads_id, since):
    vids, token = [], None
    while True:
        res = yt.playlistItems().list(part="contentDetails", playlistId=uploads_id,
                                      maxResults=50, pageToken=token).execute()
        stop = False
        for it in res.get("items", []):
            pub = it["contentDetails"].get("videoPublishedAt", "")[:10]
            if pub and dt.date.fromisoformat(pub) < since:
                stop = True
                continue
            vids.append(it["contentDetails"]["videoId"])
        token = res.get("nextPageToken")
        if stop or not token:
            break
    details = []
    for i in range(0, len(vids), 50):
        res = yt.videos().list(part="snippet,contentDetails,status", id=",".join(vids[i:i + 50])).execute()
        details += res.get("items", [])
    return [v for v in details if v["status"].get("privacyStatus") == "public"]


def query(yta, **kw):
    from googleapiclient.errors import HttpError
    try:
        return yta.reports().query(ids="channel==MINE", **kw).execute()
    except HttpError as e:
        return {"error": str(e)}


def video_stats(yta, ids, start, end):
    metrics = "views,engagedViews,estimatedMinutesWatched,averageViewDuration,subscribersGained,subscribersLost"
    res = query(yta, startDate=start, endDate=end, metrics=metrics, dimensions="video",
                filters="video==" + ",".join(ids), maxResults=200)
    if "error" in res:  # older API versions: try without engagedViews
        metrics = metrics.replace("engagedViews,", "")
        res = query(yta, startDate=start, endDate=end, metrics=metrics, dimensions="video",
                    filters="video==" + ",".join(ids), maxResults=200)
        if "error" in res:
            sys.exit("YouTube Analytics refused the request:\n" + res["error"])
    cols = [h["name"] for h in res.get("columnHeaders", [])]
    return {row[0]: dict(zip(cols, row)) for row in res.get("rows", [])}


def approx_ypp_hours(yta, end):
    """Long-form watch hours, last 365 days. An ESTIMATE: Studio's Earn page is the official number."""
    start = (dt.date.fromisoformat(end) - dt.timedelta(days=364)).isoformat()
    res = query(yta, startDate=start, endDate=end, metrics="estimatedMinutesWatched",
                dimensions="creatorContentType")
    if "error" in res or not res.get("rows"):
        return None
    minutes = sum(r[1] for r in res["rows"] if "short" not in str(r[0]).lower())
    return round(minutes / 60)


def read_rows(path):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def append_rows(path, fields, rows):
    new_file = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        if new_file:
            w.writeheader()
        w.writerows(rows)


def cmd_test():
    yt, _ = services()
    ch = my_channel(yt)
    s = ch["statistics"]
    print(f"Connected (read-only) to: {ch['snippet']['title']}")
    print(f"  subscribers: {int(s.get('subscriberCount', 0)):,}   videos: {s.get('videoCount')}")


def cmd_week(since):
    cfg = load_config()
    yt, yta = services()
    ch = my_channel(yt)
    if ch["id"] != cfg["channel"]["channel_id"]:
        print(f"  ! Note: signed in to '{ch['snippet']['title']}', not the channel in config.json.")
    today = dt.date.today()
    end = (today - dt.timedelta(days=1)).isoformat()  # analytics lag; yesterday is the latest full day
    vids = recent_videos(yt, ch["contentDetails"]["relatedPlaylists"]["uploads"], since)
    stats = video_stats(yta, [v["id"] for v in vids], since.isoformat(), end) if vids else {}

    tracker_path = HERE / "tracker.csv"
    existing = read_rows(tracker_path)
    done = {(r["date"], r["video_id"]) for r in existing}
    previous = {r["video_id"]: r for r in existing}  # last known series/format/hook for each video
    rows = []
    for v in vids:
        vid = v["id"]
        if (today.isoformat(), vid) in done:
            continue
        st = stats.get(vid, {})
        length = iso_minutes(v["contentDetails"].get("duration"))
        if length is not None and length <= 3:
            continue  # almost certainly a Short; Shorts don't count toward watch hours
        views = st.get("views")
        engaged = st.get("engagedViews")
        prev = previous.get(vid, {})
        rows.append({
            "date": today.isoformat(), "video_id": vid, "title": v["snippet"]["title"][:90],
            "series": prev.get("series", ""), "format": prev.get("format", ""),
            "published": v["snippet"]["publishedAt"][:10],
            "impressions": "", "ctr_pct": "",
            "views": views if views is not None else "",
            "engaged_pct": round(engaged / views * 100, 1) if engaged is not None and views else "",
            "avg_view_min": round(st["averageViewDuration"] / 60, 2) if st.get("averageViewDuration") else "",
            "length_min": length if length is not None else "",
            "watch_hours": round(st["estimatedMinutesWatched"] / 60, 1) if st.get("estimatedMinutesWatched") else "",
            "subs_net": (st.get("subscribersGained", 0) - st.get("subscribersLost", 0)) if st else "",
            "hook_by_5s": prev.get("hook_by_5s", ""),
            "notes": f"auto from API (data to {end}); add impressions + CTR from Studio",
        })
    if rows:
        append_rows(tracker_path, TRACKER_FIELDS, rows)
    print(f"Added {len(rows)} video row(s) to tracker.csv.")

    channel_path = HERE / "channel.csv"
    if today.isoformat() not in {r["date"] for r in read_rows(channel_path)}:
        hours = approx_ypp_hours(yta, end)
        append_rows(channel_path, CHANNEL_FIELDS, [{
            "date": today.isoformat(),
            "subscribers": ch["statistics"].get("subscriberCount", ""),
            "ypp_watch_hours": hours if hours is not None else "",
            "shorts_views_90d": "",
            "notes": "auto from API; watch hours are an estimate, replace with Studio > Earn number",
        }])
        print("Added this week's row to channel.csv.")
    print("Next: open both CSVs, fill impressions + CTR and the official watch hours, then run weekly.py")


def main():
    p = argparse.ArgumentParser(description="Read-only YouTube sync into tracker.csv / channel.csv")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("test")
    w = sub.add_parser("week")
    w.add_argument("--since", default="2026-10-01", help="include videos published on/after this date")
    a = p.parse_args()
    if a.cmd == "test":
        cmd_test()
    else:
        try:
            since = dt.date.fromisoformat(a.since)
        except ValueError:
            sys.exit("--since must look like 2026-10-01")
        cmd_week(since)


if __name__ == "__main__":
    main()
