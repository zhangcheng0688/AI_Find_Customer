#!/usr/bin/env python3
"""Slim SLAM.SYSTEMS pages: remove duplicate/filler images per approved plan.
Text content untouched. Removed material goes into downloadable PDFs."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# exact img tags to REMOVE per file (from audit dump)
REMOVE = {
"index.html": [
 '<img src="assets/images/cases/case-fifa.jpg" alt="FIFA Live-Umgebung">',
 '<img src="assets/images/cases/case-fc-lugano.jpg" alt="FC Lugano Stadion">',
 '<img src="assets/images/led-band.jpg" alt="Perimeter LED">',
 '<img src="assets/images/cor-strip.jpg" alt="Scoreboard und Media Playout">',
 '<img src="assets/images/world-sports.jpg" alt="Sportkommunikation">',
 '<img src="assets/images/company-story.jpg" alt="Engineering und Design">',
],
"media-playout.html": [
 # COR family-media grid (duplicates of the product card photos below)
 '<img src="assets/images/from-slam-systems/slam_deck_00-574.jpg" alt="DECKCOR">',
 '<img src="assets/images/from-slam-systems/slam_score_01-574.jpg" alt="SCORECOR">',
 '<img src="assets/images/from-slam-systems/slam_score_02-574.jpg" alt="PLAYCOR">',
 '<img src="assets/images/cases/case-fifa.jpg" alt="Live Sport">',
 # MODULECOR optional card photo
 '<img class="card-photo" src="assets/images/cor-strip.jpg" alt="COR Family Module" loading="lazy">',
 # DS family-media: keep ds-teaser, drop world-corporate
 '<img src="assets/images/world-corporate.jpg" alt="Corporate Communication">',
 # DS card duplicate photos
 '<img class="card-photo" src="assets/images/from-slam-systems/public_display-574.jpg" alt="Corporate Communication Control" loading="lazy">',
 '<img class="card-photo" src="assets/images/from-slam-systems/public_display-574.jpg" alt="Corporate TV" loading="lazy">',
 '<img class="card-photo" src="assets/images/world-spaces.jpg" alt="Corporate Audio" loading="lazy">',
 '<img class="card-photo" src="assets/images/ds-teaser.jpg" alt="Corporate Text" loading="lazy">',
 '<img class="card-photo" src="assets/images/world-spaces.jpg" alt="DS Module" loading="lazy">',
],
"led-video-systems.html": [
 # intro strip: keep case-lakers only
 '<img src="assets/images/from-slam-systems/nemezes_10_01-574.jpg" alt="Perimeter">',
 '<img src="assets/images/from-slam-systems/slam_vip_01-574.jpg" alt="ZENARIO">',
 '<img src="assets/images/led-band.jpg" alt="LED Band">',
 # SMD cards: same generic placeholder on 3 different products
 '<img class="card-photo" src="assets/images/from-slam-systems/nemezes_10_01-574.jpg" alt="GENEZES 391 LED" loading="lazy">',
 '<img class="card-photo" src="assets/images/from-slam-systems/nemezes_10_01-574.jpg" alt="ARAMIZ 625 LED" loading="lazy">',
 '<img class="card-photo" src="assets/images/from-slam-systems/nemezes_10_01-574.jpg" alt="TSCHILIN Perimeter LED" loading="lazy">',
 # ZENARIO dup -> swapped to real module image below
 '<img class="card-photo" src="assets/images/from-slam-systems/slam_vip_01-574.jpg" alt="ZENARIO Fine Pixel Pitch" loading="lazy">',
 # NERV dup of service-install
 '<img class="card-photo" src="assets/images/service-install.jpg" alt="NERV Hardware" loading="lazy">',
],
"solutions.html": [
 '<img src="assets/images/world-sports.jpg" alt="Sport">',
 '<img src="assets/images/world-spaces.jpg" alt="Spaces">',
 '<img src="assets/images/service-install.jpg" alt="Installation">',
 '<img class="card-photo" src="assets/images/from-slam-systems/public_display-574.jpg" alt="SLAM Cloud Dokumentation" loading="lazy">',
],
"company.html": [
 '<img src="assets/images/world-sports.jpg" alt="Sports Moments">',
 '<img src="assets/images/cases/case-lakers.jpg" alt="Arena">',
 '<img class="card-photo" src="assets/images/world-sports.jpg" alt="Philosophy" loading="lazy">',
 '<img class="card-photo" src="assets/images/cases/case-fc-lugano.jpg" alt="ROUNDS Switzerland" loading="lazy">',
 '<img class="card-photo" src="assets/images/world-corporate.jpg" alt="Shenzhen Watermoon" loading="lazy">',
],
}

# ZENARIO card gets its real module image instead of the removed dup
SWAP = {
"led-video-systems.html": [(
 'ZENARIO 250 / 187 / 125',
 '<span class="status">Ready</span>',
)]  # marker only; real swap below
}

# PDF download links to add after section heads
PDF_LINKS = {
"media-playout.html": [(
 '<p class="content-code">B-2.1 / Sport Media</p><h2>SLAM.SYSTEMS <strong>COR Family</strong></h2></div>',
 '<p class="content-code">B-2.1 / Sport Media</p><h2>SLAM.SYSTEMS <strong>COR Family</strong></h2><p class="pdf-link"><a href="assets/downloads/SLAM.SYSTEMS_COR-Family.pdf" download>Alle Module &amp; Bilder als PDF <span aria-hidden="true">↓</span></a></p></div>',
)],
"led-video-systems.html": [(
 '<p class="content-code">B-3.1.1 / SMD</p><h2>Next-Gen Efficiency <strong>SMD LED Systems</strong></h2></div>',
 '<p class="content-code">B-3.1.1 / SMD</p><h2>Next-Gen Efficiency <strong>SMD LED Systems</strong></h2><p class="pdf-link"><a href="assets/downloads/SLAM.SYSTEMS_LED-Video-Systems.pdf" download>Alle Systeme &amp; Bilder als PDF <span aria-hidden="true">↓</span></a></p></div>',
)],
"index.html": [(
 '<h2 id="moments-title">Pictures from the <strong>live moment.</strong></h2>',
 '<h2 id="moments-title">Pictures from the <strong>live moment.</strong></h2>\n      <p class="pdf-link"><a href="assets/downloads/SLAM.SYSTEMS_References.pdf" download>Alle Referenzen als PDF <span aria-hidden="true">↓</span></a></p>',
)],
}

# ZENARIO real image swap (dup removed above)
ZENARIO_SWAP = (
 '<article class="content-card" id="zenario">',
)

def main():
    total_removed = 0
    for fname, tags in REMOVE.items():
        p = ROOT / fname
        html = p.read_text(encoding="utf-8")
        for t in tags:
            if t not in html:
                raise SystemExit(f"NOT FOUND in {fname}: {t[:90]}")
            html = html.replace(t, "", 1)
            total_removed += 1
        p.write_text(html, encoding="utf-8")

    # ZENARIO card: point to the real module render
    p = ROOT / "led-video-systems.html"
    html = p.read_text(encoding="utf-8")
    marker = '<article class="content-card product-detail-card" id="zenario">'
    assert marker in html
    html = html.replace(marker,
        marker + '<img class="card-photo" src="assets/images/modules/led-zenario.jpg" alt="ZENARIO Fine Pixel Pitch LED" loading="lazy">', 1)
    p.write_text(html, encoding="utf-8")

    for fname, pairs in PDF_LINKS.items():
        p = ROOT / fname
        html = p.read_text(encoding="utf-8")
        for old, new in pairs:
            if old not in html:
                raise SystemExit(f"PDF-LINK ANCHOR NOT FOUND in {fname}: {old[:80]}")
            html = html.replace(old, new, 1)
        p.write_text(html, encoding="utf-8")

    print(f"removed {total_removed} img tags; added ZENARIO real image; added 3 PDF links")

if __name__ == "__main__":
    main()
