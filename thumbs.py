"""
thumbs.py - makes 1280x720 thumbnails in the thumb_A_medal.jpg style.

WHAT IT DOES
  Takes your photos from photos/, crops them to 16:9, and adds bold white
  and yellow text with a black outline on the side AWAY from your face, plus
  a small blue series badge. It also keeps the bottom-right corner clear,
  where YouTube puts the video length. Results go in thumbs/, with
  thumbs/preview_small.jpg showing every version at phone size so you can
  pick. It never uploads anything.

HOW TO RUN
  One photo, one text:
    python thumbs.py --photo photos/medal.jpg --text "MY FIRST WORLD MAJOR" --series road

  Every photo in photos/, text on both sides (best for picking a winner):
    python thumbs.py --text "CAN I DO THIS?" --series road --variants

  Two-colour text: use " / " to start a new line. The LAST line is yellow:
    python thumbs.py --text "EDMONTON → SYDNEY / 42.2 KM" --series road

  Two text options at once (compare them side by side):
    python thumbs.py --text "MY FIRST WORLD MAJOR" --text "CAN I FINISH?" --series road

FACE DETECTION
  If OpenCV is installed (pip install "opencv-python-headless<5") the script
  finds your face and puts the text on the other side. Face detectors are less
  reliable on darker skin and on side profiles, so ALWAYS look at the preview.
  Use --side left or --side right to force it.
"""
import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
except ImportError:
    sys.exit("Pillow isn't installed. Run:  pip install Pillow")

from ada_common import HERE, load_config, slugify

PHOTO_EXT = {".jpg", ".jpeg", ".png", ".webp", ".heic"}
FONT_CANDIDATES = [
    # macOS
    "/System/Library/Fonts/Supplemental/Impact.ttf",
    "/System/Library/Fonts/Supplemental/Arial Black.ttf",
    "/Library/Fonts/Arial Black.ttf",
    # Windows
    "C:/Windows/Fonts/impact.ttf",
    "C:/Windows/Fonts/ariblk.ttf",
    # Linux
    "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
MAX_BYTES = 2 * 1024 * 1024  # YouTube's thumbnail limit


def find_font():
    for f in sorted((HERE / "fonts").glob("*.[ot]tf")):
        return str(f)
    for f in FONT_CANDIDATES:
        if Path(f).exists():
            return f
    sys.exit("No bold font found. Download 'Anton' from fonts.google.com and put the .ttf in fonts/.")


def detect_face(img):
    """Returns (x_center, y_center, w, h) of the biggest face as fractions, or None."""
    try:
        import cv2
        import numpy as np
    except ImportError:
        return None
    path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    if not Path(path).exists():
        return None
    gray = cv2.cvtColor(np.array(img.convert("RGB")), cv2.COLOR_RGB2GRAY)
    gray = cv2.equalizeHist(gray)  # helps with darker skin tones and backlit photos
    cascade = cv2.CascadeClassifier(path)
    min_side = max(40, min(gray.shape) // 12)
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6, minSize=(min_side, min_side))
    if len(faces) == 0:
        return None
    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
    W, H = img.size
    return ((x + w / 2) / W, (y + h / 2) / H, w / W, h / H)


def crop_16x9(img, face, text_side):
    """Crop to 16:9. If we know where the face is, keep it on the side opposite the text."""
    W, H = img.size
    target = 16 / 9
    if W / H > target:  # too wide: choose horizontal window
        new_w = int(H * target)
        if face:
            fx = face[0] * W
            want = 0.70 if text_side == "left" else 0.30  # face position inside the crop
            left = int(fx - want * new_w)
        else:
            left = (W - new_w) // 2
        left = max(0, min(W - new_w, left))
        img = img.crop((left, 0, left + new_w, H))
    else:  # too tall (phone photo): keep the face in the upper-middle
        new_h = int(W / target)
        if face:
            top = int(face[1] * H - 0.40 * new_h)
        else:
            top = (H - new_h) // 3
        top = max(0, min(H - new_h, top))
        img = img.crop((0, top, W, top + new_h))
    return img


def fit_font(draw, lines, font_path, box_w, box_h):
    size = 260
    while size > 30:
        font = ImageFont.truetype(font_path, size)
        stroke = max(4, size // 11)
        widths, heights = [], []
        for ln in lines:
            l, t, r, b = draw.textbbox((0, 0), ln, font=font, stroke_width=stroke)
            widths.append(r - l)
            heights.append(b - t)
        gap = size // 8
        if max(widths) <= box_w and sum(heights) + gap * (len(lines) - 1) <= box_h:
            return font, stroke, heights, gap
        size -= 6
    font = ImageFont.truetype(font_path, 30)
    return font, 4, [34] * len(lines), 4


def side_shade(img, side):
    """Soft dark gradient behind the text so it reads on busy race photos."""
    W, H = img.size
    grad = Image.new("L", (W, 1))
    for x in range(W):
        f = x / W if side == "right" else 1 - x / W
        grad.putpixel((x, 0), int(150 * max(0.0, (f - 0.35) / 0.65) ** 1.4))
    mask = grad.resize((W, H))
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    return Image.composite(dark, img, mask)


def draw_badge(img, text, colour, side, font_path):
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, 34)
    l, t, r, b = d.textbbox((0, 0), text, font=font)
    pad_x, pad_y = 22, 12
    w, h = r - l + 2 * pad_x, b - t + 2 * pad_y
    x = 36 if side == "left" else img.width - w - 36
    y = 32
    d.rounded_rectangle((x, y, x + w, y + h), radius=h // 2, fill=colour)
    d.text((x + pad_x - l, y + pad_y - t), text, font=font, fill="white")


def render(photo_path, text, series_badge, side, cfg, font_path, face_info=True):
    th = cfg["thumbnail"]
    W, H = th["width"], th["height"]
    img = ImageOps.exif_transpose(Image.open(photo_path)).convert("RGB")
    face = detect_face(img) if face_info else None
    if side == "auto":
        side = ("left" if face[0] > 0.5 else "right") if face else "left"
    img = crop_16x9(img, face, side).resize((W, H), Image.LANCZOS)
    img = side_shade(img, side)

    lines = [ln.strip().upper() for ln in text.split("/") if ln.strip()]
    if len(lines) == 1 and len(lines[0]) > 12 and " " in lines[0]:
        words = lines[0].split()  # auto-wrap long single lines into 2 balanced lines
        best = min(range(1, len(words)),
                   key=lambda i: abs(len(" ".join(words[:i])) - len(" ".join(words[i:]))))
        lines = [" ".join(words[:best]), " ".join(words[best:])]

    d = ImageDraw.Draw(img)
    box_w, box_h = int(W * 0.52), int(H * 0.62)
    font, stroke, heights, gap = fit_font(d, lines, font_path, box_w, box_h)
    total = sum(heights) + gap * (len(lines) - 1)
    y = max(110, (H - total) // 2 - 30)  # below the badge, above the duration stamp
    x_margin = 48
    for i, ln in enumerate(lines):
        l, t, r, b = d.textbbox((0, 0), ln, font=font, stroke_width=stroke)
        x = x_margin - l if side == "left" else W - x_margin - (r - l) - l
        colour = th["yellow"] if (i == len(lines) - 1 and len(lines) > 1) else th["white"]
        d.text((x, y - t), ln, font=font, fill=colour, stroke_width=stroke, stroke_fill=th["outline"])
        y += heights[i] + gap
    draw_badge(img, series_badge, th["badge_blue"], side, font_path)
    return img, side, face


def save_jpeg(img, path):
    for q in (92, 88, 84, 80, 75):
        img.save(path, "JPEG", quality=q, optimize=True)
        if path.stat().st_size <= MAX_BYTES:
            return
    print(f"  ! {path.name} is still over 2 MB; YouTube may reject it.")


def contact_sheet(items, out_path, font_path):
    """Each row: the thumbnail at desktop size (320x180) and phone size (168x94)."""
    row_h, pad = 200, 16
    sheet = Image.new("RGB", (320 + 168 + pad * 3 + 520, pad + row_h * len(items)), (24, 24, 24))
    d = ImageDraw.Draw(sheet)
    label_font = ImageFont.truetype(font_path, 18)
    for i, (path, img) in enumerate(items):
        y = pad + i * row_h
        sheet.paste(img.resize((320, 180), Image.LANCZOS), (pad, y))
        sheet.paste(img.resize((168, 94), Image.LANCZOS), (pad * 2 + 320, y))
        d.text((pad * 3 + 488, y + 8), path.name, font=label_font, fill=(230, 230, 230))
        d.text((pad * 3 + 488, y + 40), "Can you read it at the small size?", font=label_font, fill=(150, 150, 150))
    sheet.save(out_path, "JPEG", quality=88)


def main():
    cfg = load_config()
    p = argparse.ArgumentParser(description="Make 1280x720 thumbnails into thumbs/.")
    p.add_argument("--text", action="append", required=True,
                   help='thumbnail words; " / " starts a new line (last line turns yellow). Repeat for options.')
    p.add_argument("--series", required=True, choices=sorted(cfg["series"]))
    p.add_argument("--photo", action="append", help="a photo path; repeat for several. Default: all of photos/")
    p.add_argument("--side", default="auto", choices=["auto", "left", "right"], help="where the text goes")
    p.add_argument("--variants", action="store_true", help="make every photo with text on BOTH sides")
    args = p.parse_args()

    photos = [Path(x) for x in args.photo] if args.photo else sorted(
        f for f in (HERE / "photos").iterdir() if f.suffix.lower() in PHOTO_EXT)
    if not photos:
        sys.exit("No photos found. Put .jpg or .png files in the photos/ folder (or use --photo).")
    missing = [str(f) for f in photos if not f.exists()]
    if missing:
        sys.exit("Can't find: " + ", ".join(missing))

    font_path = find_font()
    badge = cfg["series"][args.series]["badge"]
    out_dir = HERE / "thumbs"
    out_dir.mkdir(exist_ok=True)
    sides = ["left", "right"] if args.variants else [args.side]
    made = []
    for photo in photos:
        for text in args.text:
            for side in sides:
                try:
                    img, used, face = render(photo, text, badge, side, cfg, font_path)
                except Exception as e:  # unreadable photo (e.g. HEIC without plugin)
                    print(f"  ! Skipped {photo.name}: {e}")
                    break
                out = out_dir / f"{photo.stem}_{slugify(text, 24)}_{used}.jpg"
                save_jpeg(img, out)
                note = "face found" if face else "no face found, check placement"
                print(f"  made {out.name}  ({note})")
                made.append((out, img))
    if made:
        sheet = out_dir / "preview_small.jpg"
        contact_sheet(made, sheet, font_path)
        print(f"\n{len(made)} thumbnail(s) in thumbs/. Open {sheet.name} to compare them at phone size.")


if __name__ == "__main__":
    main()
