"""
weekly.py - your 10-minute Sunday check-in.

WHAT IT DOES
  Reads tracker.csv (one row per video per check) and channel.csv (one row
  per week: subscribers and the watch hours from Studio's Earn page) and
  prints:
    1. YPP progress and the pace you need before the Feb 1, 2027 rule change
    2. Subscriber pace against the +1,000 to +3,000 goal
    3. Each new video against the targets (CTR, engaged %, % watched)
    4. The 12-video experiment: simple vs cinematic vs follow-along
  It also saves the same report in reports/. It only reads your CSV files.

HOW TO RUN
  1. Once a week, open YouTube Studio and add rows (see README "Sunday check-in").
  2. Run:  python weekly.py
"""
import csv
import datetime as dt
import sys
from collections import defaultdict

from ada_common import HERE, load_config

TODAY = dt.date.today()


def num(v):
    try:
        return float(str(v).replace(",", "").replace("%", "").strip())
    except (TypeError, ValueError):
        return None


def date(v):
    try:
        return dt.date.fromisoformat(str(v).strip())
    except ValueError:
        return None


def read(name):
    path = HERE / name
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as f:
        return [r for r in csv.DictReader(f) if any((v or "").strip() for v in r.values())]


def mark(value, target, higher_is_better=True):
    if value is None:
        return "  -  "
    ok = value >= target if higher_is_better else value <= target
    return " OK  " if ok else "below"


def per_week(points):
    """Average change per week from the first and last (date, value) points, or None."""
    points = [(d, v) for d, v in points if d and v is not None]
    if len(points) < 2:
        return None
    (d0, v0), (d1, v1) = points[0], points[-1]
    days = (d1 - d0).days
    return (v1 - v0) / days * 7 if days >= 6 else None


def ypp_section(cfg, channel, out):
    t = cfg["targets"]
    apply_by = date(t["apply_by"])
    baseline = date(t["net_subs_baseline_date"])
    rows = [(date(r["date"]), num(r["ypp_watch_hours"])) for r in channel]
    rows = sorted((d, v) for d, v in rows if d and v is not None)
    out.append("1. YPP WATCH HOURS (public long-form, last 365 days)")
    if not rows:
        out.append("   No watch-hour numbers yet. Add one to channel.csv from Studio > Earn.")
        return
    last_d, last_h = rows[-1]
    weeks_left = max(0.1, (apply_by - TODAY).days / 7)
    pace = per_week([r for r in rows if r[0] >= baseline][-5:])
    out.append(f"   Now: {last_h:,.0f} hours (as of {last_d}). {weeks_left:.1f} weeks until {apply_by}.")
    for label, goal in (("Fan funding (memberships, Super Thanks)", t["fan_funding_watch_hours"]),
                        ("Ads (before the rule change)", t["ads_watch_hours"])):
        gap = goal - last_h
        if gap <= 0:
            out.append(f"   {label}: {goal:,} REACHED. Apply in Studio > Earn now!")
            continue
        need = gap / weeks_left
        out.append(f"   {label}: {goal:,}, need +{gap:,.0f}, i.e. about +{need:,.0f} per week from now.")
    if pace is None:
        out.append("   Your pace: needs 2+ weekly rows (a week apart) after "
                   f"{baseline} to calculate.")
    else:
        out.append(f"   Your pace lately: {pace:+,.0f} hours per week (net: new hours minus hours "
                   "older than a year dropping off).")
        if pace > 0:
            for goal in (t["fan_funding_watch_hours"], t["ads_watch_hours"]):
                if goal > last_h:
                    eta = last_d + dt.timedelta(weeks=(goal - last_h) / pace)
                    flag = "in time" if eta <= apply_by else "AFTER the deadline"
                    out.append(f"     -> at this pace you reach {goal:,} around {eta} ({flag}).")
    out.append(f"   From {t['ads_threshold_change_date']} new applicants need "
               f"{t['ads_watch_hours_after_feb_2027']:,} hours for ads. The fan-funding tier is reported "
               "to stay at 3,000.")


def subs_section(cfg, channel, out):
    t = cfg["targets"]
    baseline_d = date(t["net_subs_baseline_date"])
    goal_d = date(t["net_subs_goal_date"])
    rows = sorted((date(r["date"]), num(r["subscribers"])) for r in channel)
    rows = [(d, v) for d, v in rows if d and v is not None]
    out.append("")
    out.append("2. SUBSCRIBERS")
    if not rows:
        out.append("   Add your subscriber count to channel.csv each week.")
        return
    base = next((v for d, v in rows if d >= baseline_d), rows[0][1])
    last_d, last_v = rows[-1]
    net = last_v - base
    weeks_left = max(0.1, (goal_d - TODAY).days / 7)
    out.append(f"   {last_v:,.0f} subscribers ({net:+,.0f} since {baseline_d}).")
    for goal in (t["net_subs_goal_low"], t["net_subs_goal_high"]):
        out.append(f"   Goal +{goal:,} by {goal_d}: need about {(goal - net) / weeks_left:+,.0f} per week from now.")
    pace = per_week([r for r in rows if r[0] >= baseline_d][-5:])
    if pace is not None:
        out.append(f"   Your pace lately: {pace:+,.1f} per week (it was about -6 per week in Oct 2026).")


def latest_per_video(videos):
    best = {}
    for r in videos:
        d = date(r.get("date"))
        if not d or not r.get("video_id"):
            continue
        if r["video_id"] not in best or d >= date(best[r["video_id"]]["date"]):
            best[r["video_id"]] = r
    return sorted(best.values(), key=lambda r: date(r.get("published")) or date(r["date"]))


def avg_view_pct(r):
    a, length = num(r.get("avg_view_min")), num(r.get("length_min"))
    return a / length * 100 if a and length else None


def videos_section(cfg, videos, out):
    t = cfg["targets"]
    rows = latest_per_video(videos)
    out.append("")
    out.append("3. VIDEOS (latest numbers for each)")
    out.append(f"   Targets: CTR {t['ctr_pct']}%+, engaged {t['engaged_pct']}%+ "
               f"(people who stay past the first seconds), {t['avg_view_pct']}%+ of the video watched.")
    if not rows:
        out.append("   No videos in tracker.csv yet.")
        return rows
    out.append(f"   {'video':<34}{'days':>5}{'CTR':>7}      {'engaged':>8}      {'watched':>8}      {'hours':>6}")
    for r in rows:
        days = (date(r["date"]) - date(r["published"])).days if date(r.get("published")) else None
        ctr, eng, pct, hrs = num(r.get("ctr_pct")), num(r.get("engaged_pct")), avg_view_pct(r), num(r.get("watch_hours"))
        title = (r.get("title") or r["video_id"])[:32]
        out.append(f"   {title:<34}{days if days is not None else '-':>5}"
                   f"{(f'{ctr:.1f}%' if ctr is not None else '-'):>7} {mark(ctr, t['ctr_pct'])}"
                   f"{(f'{eng:.0f}%' if eng is not None else '-'):>8} {mark(eng, t['engaged_pct'])}"
                   f"{(f'{pct:.0f}%' if pct is not None else '-'):>8} {mark(pct, t['avg_view_pct'])}"
                   f"{(f'{hrs:.1f}' if hrs is not None else '-'):>6}")
    return rows


def experiment_section(cfg, rows, out):
    n_goal = cfg["targets"]["experiment_videos"]
    start = date(cfg["targets"]["net_subs_baseline_date"])
    new = [r for r in rows if (date(r.get("published")) or TODAY) >= start]
    out.append("")
    out.append(f"4. THE {n_goal}-VIDEO EXPERIMENT ({len(new)} of {n_goal} published since {start})")
    groups = defaultdict(list)
    for r in new:
        groups[(r.get("format") or "unknown").strip().lower()].append(r)
    hooks = defaultdict(list)
    for r in new:
        hooks[(r.get("hook_by_5s") or "?").strip().lower()[:1]].append(r)

    def summary(rs):
        def avg(vals):
            vals = [v for v in vals if v is not None]
            return sum(vals) / len(vals) if vals else None
        ctr = avg(num(r.get("ctr_pct")) for r in rs)
        eng = avg(num(r.get("engaged_pct")) for r in rs)
        hrs = avg(num(r.get("watch_hours")) for r in rs)
        f = lambda v, s: f"{v:.1f}{s}" if v is not None else "-"
        return f"{len(rs)} video(s): CTR {f(ctr, '%')}, engaged {f(eng, '%')}, watch hours {f(hrs, '')} each"

    for fmt in ("simple", "cinematic", "followalong"):
        if groups.get(fmt):
            out.append(f"   {fmt:<12} {summary(groups[fmt])}")
    for key, label in (("y", "hook by 0:05"), ("n", "slow opening")):
        if hooks.get(key):
            out.append(f"   {label:<12} {summary(hooks[key])}")
    if len(new) < n_goal:
        out.append(f"   Too early to judge: one video is a coin toss. Judge after {n_goal}.")


def main():
    cfg = load_config()
    videos, channel = read("tracker.csv"), read("channel.csv")
    out = [f"ADA CANADA WEEKLY CHECK-IN  {TODAY}", "=" * 44]
    ypp_section(cfg, channel, out)
    subs_section(cfg, channel, out)
    rows = videos_section(cfg, videos, out)
    experiment_section(cfg, rows, out)
    out.append("")
    out.append("Remember: the goal this season is a new audience, not old subscribers coming back.")
    out.append("Small numbers on new videos are normal at first. Look at the trend, not one week.")
    text = "\n".join(out)
    print(text)
    rep = HERE / "reports" / f"weekly_{TODAY.isoformat()}.md"
    rep.parent.mkdir(exist_ok=True)
    rep.write_text("```\n" + text + "\n```\n", encoding="utf-8")
    print(f"\nSaved: {rep}")


if __name__ == "__main__":
    sys.exit(main())
