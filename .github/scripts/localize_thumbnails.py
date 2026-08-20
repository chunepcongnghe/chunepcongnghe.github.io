#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import io
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import requests
from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
POSTS = ROOT / "_posts"
OUT = ROOT / "assets" / "images" / "thumbs"
MANIFEST = OUT / "manifest.json"
SIZE = (1200, 675)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/151 Safari/537.36"

# Known photo fallbacks. They are only used when a post's own source cannot be downloaded.
# The final production asset is always localized into this repository.
MACBOOK = "https://s.yimg.com/ny/api/res/1.2/oiOFMCzS4EZ6ucpQQ3ULcA--/YXBwaWQ9aGlnaGxhbmRlcjt3PTEyNDI7aD02OTg-/https%3A/media.zenfs.com/en/pc_mag_263/b02f90f2dd8eaca3838e77da502b307b"
MACBOOK_SETUP = "https://miro.medium.com/0%2Akv7PnwnJj_OTRxAv"
RAM = "https://img.evetech.co.za/repository/ez/How-Much-RAM-Do-You-Really-Need-for-Gaming-in-2025-banner.webp?width=1200"
AI_PC = "https://futureforwardit.in/images/uploaded/generated-image-3.jpg"
GALAXY_FOLD = "https://etf-rebalancing.com/images/phone-preorder/galaxy-z-fold8-flip8-hero.webp"
GALAXY_FLIP = "https://img.tamindir.com/resize/1200x675/2025/12/470608/samsung-galaxy-z-flip-8-islemcisi-sizinti-1.jpg"
ACTION = "https://www.gadgetmatch.com/wp-content/uploads/2025/11/gadgetmatch-20251122-dji-osmo-action-6-1.jpg"
ACTION_COMPARE = "https://camerajabber.com/wp-content/uploads/2025/11/DJI-Osmo-Action-6-09.jpg"
ROADTRIP = "https://cdn.shopify.com/s/files/1/0108/1062/files/CS0124_CAR__QLA-ACA_-QLP-360-SB_-QLP-360-SPA__MG_0015.jpg?v=1723081972"

MANUAL_SOURCE = {
    # Fix the four visible problem cards first: no shared production path and no hotlink.
    "fomo-cau-hinh-32gb-1tb-ai-pc-co-can-khong": RAM,
    "cach-doc-cau-hinh-laptop-khong-bi-marketing-dan-dat": AI_PC,
    "chon-hub-dock-macbook-air-m5": MACBOOK_SETUP,
    "macbook-air-m5-512gb-hay-1tb": MACBOOK,
}


def field(front: str, name: str) -> str:
    m = re.search(rf"(?m)^{re.escape(name)}:\s*(.+?)\s*$", front)
    if not m:
        return ""
    return m.group(1).strip().strip('"\'')


def replace_field(front: str, name: str, value: str) -> str:
    line = f'{name}: "{value}"'
    pat = rf"(?m)^{re.escape(name)}:\s*.*$"
    if re.search(pat, front):
        return re.sub(pat, line, front, count=1)
    return front.rstrip() + "\n" + line + "\n"


def parse_post(path: Path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, flags=re.S)
    if not m:
        raise RuntimeError(f"Missing YAML front matter: {path}")
    front = m.group(1)
    return text, front, m.end()


def candidates(slug: str, title: str, category: str, brand: str, image: str):
    out: list[str] = []
    if slug in MANUAL_SOURCE:
        out.append(MANUAL_SOURCE[slug])
    if image.startswith("http://") or image.startswith("https://"):
        out.append(image)

    hay = f"{slug} {title} {category} {brand}".lower()
    if any(k in hay for k in ["osmo", "action", "camera"]):
        out += [ACTION, ACTION_COMPARE, ROADTRIP]
    if any(k in hay for k in ["roadtrip", "road-trip", "micro sd", "microsd"]):
        out += [ROADTRIP, ACTION]
    if any(k in hay for k in ["galaxy", "fold", "flip", "samsung"]):
        out += [GALAXY_FOLD, GALAXY_FLIP]
    if any(k in hay for k in ["ram", "32gb", "24gb", "16gb", "ssd", "storage"]):
        out += [RAM, MACBOOK, AI_PC]
    if any(k in hay for k in ["ai pc", "copilot", "npu", "cpu", "gpu", "tops"]):
        out += [AI_PC, RAM, MACBOOK]
    if any(k in hay for k in ["hub", "dock", "setup", "creator"]):
        out += [MACBOOK_SETUP, MACBOOK]
    if any(k in hay for k in ["macbook", "apple", "laptop", "oled", "ips", "thunderbolt", "usb4", "wifi"]):
        out += [MACBOOK, MACBOOK_SETUP, RAM]

    out += [MACBOOK, GALAXY_FOLD, ACTION, RAM]
    seen = set()
    return [u for u in out if u and not (u in seen or seen.add(u))]


def open_local(image: str) -> Image.Image | None:
    if not image.startswith("/"):
        return None
    p = ROOT / image.lstrip("/")
    if not p.exists() or p.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
        return None
    try:
        im = Image.open(p)
        im.load()
        return ImageOps.exif_transpose(im).convert("RGB")
    except Exception:
        return None


def download(url: str) -> Image.Image | None:
    try:
        r = requests.get(
            url,
            headers={
                "User-Agent": UA,
                "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
                "Referer": "https://www.google.com/",
            },
            timeout=35,
            allow_redirects=True,
        )
        r.raise_for_status()
        if len(r.content) < 8_000:
            return None
        im = Image.open(io.BytesIO(r.content))
        im.load()
        im = ImageOps.exif_transpose(im).convert("RGB")
        if im.width < 500 or im.height < 280:
            return None
        return im
    except Exception:
        return None


def cover(im: Image.Image, size, xbias=0.5, ybias=0.5, zoom=1.0):
    tw, th = size
    ratio = max(tw / im.width, th / im.height) * zoom
    nw, nh = max(tw, int(im.width * ratio)), max(th, int(im.height * ratio))
    rs = im.resize((nw, nh), Image.Resampling.LANCZOS)
    max_x, max_y = max(0, nw - tw), max(0, nh - th)
    left = int(max_x * min(1, max(0, xbias)))
    top = int(max_y * min(1, max(0, ybias)))
    return rs.crop((left, top, left + tw, top + th))


def rounded_mask(size, radius=34):
    mask = Image.new("L", size, 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle((0, 0, size[0]-1, size[1]-1), radius=radius, fill=255)
    return mask


def make_thumb(src: Image.Image, slug: str, category: str) -> Image.Image:
    h = hashlib.sha256(slug.encode()).digest()
    variant = h[0] % 4
    xbias = 0.22 + (h[1] / 255) * 0.56
    ybias = 0.28 + (h[2] / 255) * 0.44
    zoom = 1.02 + (h[3] / 255) * 0.17

    # Slightly improve dull press images without turning them into fake renders.
    src = ImageEnhance.Contrast(src).enhance(1.03)
    src = ImageEnhance.Color(src).enhance(1.02)

    if variant == 0:
        canvas = cover(src, SIZE, xbias, ybias, zoom)
    elif variant == 1:
        bg = cover(src, SIZE, 1-xbias, ybias, 1.16).filter(ImageFilter.GaussianBlur(18))
        bg = ImageEnhance.Brightness(bg).enhance(0.72)
        fw, fh = 1040, 585
        fg = cover(src, (fw, fh), xbias, ybias, zoom)
        shadow = Image.new("RGBA", SIZE, (0,0,0,0))
        sd = ImageDraw.Draw(shadow)
        sd.rounded_rectangle((88, 57, 1132, 646), radius=36, fill=(0,0,0,82))
        shadow = shadow.filter(ImageFilter.GaussianBlur(16))
        canvas = bg.convert("RGBA")
        canvas.alpha_composite(shadow)
        canvas.paste(fg, (80, 45), rounded_mask((fw, fh), 34))
        canvas = canvas.convert("RGB")
    elif variant == 2:
        base = cover(src, SIZE, xbias, ybias, zoom)
        detail = cover(src, (355, 675), 1-xbias, ybias, 1.24)
        base = base.convert("RGBA")
        shade = Image.new("RGBA", (355,675), (0,0,0,0))
        shade.paste(detail.convert("RGBA"), (0,0))
        edge = Image.new("RGBA", (10,675), (255,255,255,60))
        base.alpha_composite(edge, (835,0))
        base.alpha_composite(shade, (845,0))
        canvas = base.convert("RGB")
    else:
        bg = cover(src, SIZE, xbias, 1-ybias, 1.22).filter(ImageFilter.GaussianBlur(24))
        bg = ImageEnhance.Brightness(bg).enhance(0.62)
        fw, fh = 930, 560
        fg = cover(src, (fw, fh), 1-xbias, ybias, 1.03)
        canvas = bg.convert("RGBA")
        shadow = Image.new("RGBA", SIZE, (0,0,0,0))
        sd = ImageDraw.Draw(shadow)
        sd.rounded_rectangle((145, 70, 1095, 650), radius=42, fill=(0,0,0,95))
        shadow = shadow.filter(ImageFilter.GaussianBlur(18))
        canvas.alpha_composite(shadow)
        canvas.paste(fg, (135, 55), rounded_mask((fw, fh), 38))
        canvas = canvas.convert("RGB")

    # Editorial depth only; no large text baked into image. HTML card title remains readable above it.
    overlay = Image.new("RGBA", SIZE, (0,0,0,0))
    od = ImageDraw.Draw(overlay)
    accent = {
        "laptop": (0, 174, 180, 130),
        "smartphone": (58, 111, 247, 125),
        "camera": (240, 145, 35, 125),
        "ai": (126, 87, 194, 125),
    }.get(category.lower(), (0, 153, 158, 115))
    od.rounded_rectangle((28, 28, 122 + (h[4] % 80), 39), radius=6, fill=accent)
    # bottom vignette improves card overlays without hiding product
    for i in range(155):
        a = int((i / 154) ** 1.9 * 92)
        y = SIZE[1] - 155 + i
        od.line((0, y, SIZE[0], y), fill=(0,0,0,a))
    return Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    posts = sorted(POSTS.glob("*.md"))
    manifest = {}
    failures = []

    for path in posts:
        text, front, body_start = parse_post(path)
        slug = field(front, "slug") or path.stem[11:]
        title = field(front, "title")
        category = field(front, "category") or "tech"
        brand = field(front, "brand")
        image = field(front, "image")
        published = field(front, "published").lower() != "false"
        if not published:
            continue

        src = open_local(image)
        used_source = image if src else ""
        if src is None:
            for url in candidates(slug, title, category, brand, image):
                src = download(url)
                if src is not None:
                    used_source = url
                    break
        if src is None:
            failures.append(f"{slug}: no downloadable photo source")
            continue

        thumb = make_thumb(src, slug, category)
        out = OUT / f"{slug}.jpg"
        thumb.save(out, "JPEG", quality=88, optimize=True, progressive=True)

        local = f"/assets/images/thumbs/{slug}.jpg"
        newfront = replace_field(front, "image", local)
        newtext = "---\n" + newfront.rstrip() + "\n---\n" + text[body_start:]
        path.write_text(newtext, encoding="utf-8")

        digest = hashlib.sha256(out.read_bytes()).hexdigest()
        manifest[slug] = {
            "post": str(path.relative_to(ROOT)),
            "image": local,
            "source": used_source,
            "sha256": digest,
            "size": list(SIZE),
        }
        print(f"OK {slug} <- {used_source}")

    if failures:
        print("\nFAILED:", file=sys.stderr)
        for item in failures:
            print("-", item, file=sys.stderr)
        sys.exit(2)

    # Hard validation: every published post gets one local, decodable, unique thumbnail.
    paths_seen = {}
    hashes_seen = {}
    validation_errors = []
    for path in posts:
        text, front, _ = parse_post(path)
        if field(front, "published").lower() == "false":
            continue
        slug = field(front, "slug") or path.stem[11:]
        image = field(front, "image")
        if not image.startswith("/assets/images/thumbs/"):
            validation_errors.append(f"{slug}: image is not local: {image}")
            continue
        p = ROOT / image.lstrip("/")
        if not p.exists():
            validation_errors.append(f"{slug}: missing file {image}")
            continue
        try:
            with Image.open(p) as im:
                im.verify()
            with Image.open(p) as im:
                if im.size != SIZE:
                    validation_errors.append(f"{slug}: wrong size {im.size}")
        except Exception as e:
            validation_errors.append(f"{slug}: invalid image: {e}")
            continue
        if image in paths_seen:
            validation_errors.append(f"{slug}: duplicate path with {paths_seen[image]}")
        paths_seen[image] = slug
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        if digest in hashes_seen:
            validation_errors.append(f"{slug}: duplicate binary with {hashes_seen[digest]}")
        hashes_seen[digest] = slug

    if validation_errors:
        print("\nVALIDATION FAILED:", file=sys.stderr)
        for item in validation_errors:
            print("-", item, file=sys.stderr)
        sys.exit(3)

    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nPASS: {len(manifest)} published posts have unique local thumbnails; no missing/broken files.")


if __name__ == "__main__":
    main()
