#!/usr/bin/env python3
"""Build 3 downloadable PDF brochures from SLAM.SYSTEMS v1.6 page content.
Texts are extracted from the HTML so wording stays byte-true to the boss package."""
import re
from pathlib import Path
from html import unescape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "downloads"
OUT.mkdir(parents=True, exist_ok=True)

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image

MAGENTA = HexColor("#ff004e")
DARK = HexColor("#0a0a0b")
GREY = HexColor("#626262")

# Register Good Times for titles (font shipped in the package)
pass  # Good Times is CFF-based; reportlab cannot embed it -> Helvetica-Bold fallback

def strip(html):
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", "", html))).strip()

def page_cards(fname):
    """Extract (id, status, name, desc) tuples from content-cards."""
    html = (ROOT / fname).read_text(encoding="utf-8")
    cards = []
    for m in re.finditer(r'<article class="content-card[^"]*"(?: id="([^"]*)")?>(.*?)</article>', html, re.S):
        cid, body = m.group(1) or "", m.group(2)
        status = strip(re.search(r'<span class="status[^"]*">(.*?)</span>', body, re.S).group(1)) if '<span class="status' in body else ""
        name = strip(re.search(r'<h3[^>]*>(.*?)</h3>', body, re.S).group(1)) if "<h3" in body else ""
        descs = [strip(x) for x in re.findall(r"<p[^>]*>(.*?)</p>", body, re.S)]
        cards.append((cid, status, name, " ".join(descs)))
    return cards

def section_copy(fname, sid):
    html = (ROOT / fname).read_text(encoding="utf-8")
    m = re.search(r'<section class="content-section" id="' + re.escape(sid) + r'">(.*?)</section>', html, re.S)
    if not m:
        return "", []
    body = m.group(1)
    h2 = strip(re.search(r"<h2[^>]*>(.*?)</h2>", body, re.S).group(1)) if "<h2" in body else ""
    copy = re.search(r'<div class="content-copy[^"]*">(.*?)</div>', body, re.S)
    paras = [strip(x) for x in re.findall(r"<p[^>]*>(.*?)</p>", copy.group(1), re.S)] if copy else []
    return h2, [p for p in paras if p]

IMG_W, IMG_H = 170 * mm, 78 * mm

def draw_cover(c, title, subtitle):
    w, h = A4
    c.setFillColor(DARK)
    c.rect(0, 0, w, h, stroke=0, fill=1)
    logo = ROOT / "assets/logos/logo_slam.systems-1920-(ff004e)(bg-bkl).png"
    c.drawImage(ImageReader(str(logo)), 20 * mm, h - 40 * mm, width=90 * mm, preserveAspectRatio=True, mask="auto")
    c.setFillColor(MAGENTA)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(20 * mm, h - 70 * mm, title)
    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica", 10)
    c.drawString(20 * mm, h - 78 * mm, subtitle)
    c.setFont("Helvetica", 7.5)
    c.setFillColor(HexColor("#9a9a9a"))
    c.drawString(20 * mm, 15 * mm, "swiss engineering and functional design | r&d centre shenzhen high-tech park | slam.systems © since 1999")
    c.showPage()

def draw_img(c, path, y_top, x=20 * mm, w=IMG_W, h=IMG_H):
    im = Image.open(path)
    iw, ih = im.size
    # cover-crop via drawImage with preserved aspect into box
    scale = max(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    c.saveState()
    p = c.beginPath()
    p.rect(x, y_top - h, w, h)
    c.clipPath(p, stroke=0, fill=0)
    c.drawImage(ImageReader(str(path)), x - (dw - w) / 2, y_top - h - (dh - h) / 2, width=dw, height=dh)
    c.restoreState()

def entry_page(c, name, status, desc, img=None):
    w, h = A4
    y = h - 25 * mm
    if img and Path(img).exists():
        draw_img(c, img, y)
        y -= IMG_H + 12 * mm
    c.setFillColor(MAGENTA)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(20 * mm, y, status.upper())
    y -= 8 * mm
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(20 * mm, y, name)
    y -= 9 * mm
    c.setFillColor(GREY)
    c.setFont("Helvetica", 9.5)
    for para in re.split(r"(?<=\.)\s+(?=[A-ZÄÖÜ])", desc):
        for line in re.wrap(para, 88) if hasattr(re, "wrap") else [para]:
            pass
    # simple manual wrap
    import textwrap
    for line in textwrap.wrap(desc, 92):
        c.drawString(20 * mm, y, line)
        y -= 4.6 * mm
    c.showPage()

def build(fname, title, subtitle, entries):
    c = pdfcanvas.Canvas(str(OUT / fname), pagesize=A4)
    draw_cover(c, title, subtitle)
    for e in entries:
        entry_page(c, *e)
    c.save()
    print("built", OUT / fname, (OUT / fname).stat().st_size, "bytes")

IMG = ROOT / "assets/images"
FSS = IMG / "from-slam-systems"

# ---- PDF 1: COR Family ----
cor_imgs = {
    "deckcor": FSS / "slam_deck_00-574.jpg",
    "scorecor": FSS / "slam_score_01-574.jpg",
    "directorcor": FSS / "pasted-image-2394-4.png",
    "playcor": FSS / "pasted-image-2400-6.png",
    "timecor": FSS / "slam_score_icecube_02-574.jpg",
    "modulecor": IMG / "cor-strip.jpg",
}
h2, paras = section_copy("media-playout.html", "cor-family")
intro = " ".join(paras)
entries = [("SLAM.SYSTEMS COR Family", "Sport Media", intro, IMG / "cases/case-fifa.jpg")]
for cid, status, name, desc in page_cards("media-playout.html"):
    if cid in cor_imgs:
        entries.append((name, status, desc, str(cor_imgs[cid])))
build("SLAM.SYSTEMS_COR-Family.pdf", "COR FAMILY", "Sport Media Playout – Alle Module & Bilder", entries)

# ---- PDF 2: LED Video Systems ----
led_imgs = {
    "genezes": FSS / "nemezes_10_01-574.jpg",
    "aramiz": FSS / "nemezes_10_01-574.jpg",
    "tschilin": FSS / "nemezes_10_01-574.jpg",
    "aramiz-screen": IMG / "modules/led-aramiz.jpg",
    "zenario": IMG / "modules/led-zenario.jpg",
    "poizen": IMG / "modules/led-poizen.jpg",
    "cinemaz": IMG / "modules/led-cinemaz.jpg",
    "centro": IMG / "service-install.jpg",
    "nerv": IMG / "service-install.jpg",
}
entries = []
for sid, img in [("smd", IMG / "led-band.jpg"), ("cob", IMG / "cases/case-lakers.jpg"), ("peripherals", IMG / "service-install.jpg")]:
    h2, paras = section_copy("led-video-systems.html", sid)
    if h2:
        entries.append((h2, sid.upper(), " ".join(paras), str(img)))
for cid, status, name, desc in page_cards("led-video-systems.html"):
    if cid in led_imgs:
        entries.append((name, status, desc, str(led_imgs[cid])))
build("SLAM.SYSTEMS_LED-Video-Systems.pdf", "LED VIDEO SYSTEMS", "Alle Systeme & Bilder", entries)

# ---- PDF 3: References ----
refs = [
    ("Handball Arena – Live Scoreboard & Perimeter", str(FSS / "bg_slam_systems_win4-2400.jpg")),
    ("FIFA – Live-Umgebung", str(IMG / "cases/case-fifa.jpg")),
    ("Basketball Arena – Lakers", str(IMG / "cases/case-lakers.jpg")),
    ("FC Lugano – Stadion", str(IMG / "cases/case-fc-lugano.jpg")),
    ("EHC Basel – Eishockey", str(IMG / "cases/case-ehc-basel.jpg")),
    ("Perimeter LED", str(IMG / "led-band.jpg")),
    ("Scoreboard & Media Playout", str(IMG / "cor-strip.jpg")),
    ("Sportkommunikation", str(IMG / "world-sports.jpg")),
    ("Engineering & Design", str(IMG / "company-story.jpg")),
]
c = pdfcanvas.Canvas(str(OUT / "SLAM.SYSTEMS_References.pdf"), pagesize=A4)
draw_cover(c, "REFERENCES", "Pictures from the live moment")
for name, img in refs:
    w, h = A4
    draw_img(c, img, h - 25 * mm)
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(20 * mm, h - 25 * mm - IMG_H - 10 * mm, name)
    c.showPage()
c.save()
print("built", OUT / "SLAM.SYSTEMS_References.pdf", (OUT / "SLAM.SYSTEMS_References.pdf").stat().st_size, "bytes")
