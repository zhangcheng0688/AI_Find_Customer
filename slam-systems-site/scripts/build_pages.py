#!/usr/bin/env python3
"""Emit SLAM.SYSTEMS pages with shared nav. Run from slam-systems-site/."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOGO = "assets/logos/logo_slam.systems-1920-(ff004e)(bg-bkl).png"
JS = '<script src="assets/js/i18n.js"></script>\n<script src="assets/js/site.js"></script>'

def header(home_href="index.html"):
    return f'''<header class="site-header interior-header">
    <a class="brand" href="{home_href}" aria-label="SLAM.SYSTEMS"><img src="{LOGO}" alt="SLAM.SYSTEMS"></a>
    <nav class="desktop-nav" aria-label="Main">
      <div class="nav-group">
        <a href="media-playout.html" data-i18n="nav.playout">Media Playout</a>
        <div class="subnav subnav-mega">
          <div>
            <p class="subnav-label" data-i18n="nav.cor">Sport Media – COR Family</p>
            <a href="media-playout.html#deckcor">SLAM DECKCOR</a>
            <a href="media-playout.html#scorecor">SLAM SCORECOR</a>
            <a href="media-playout.html#directorcor">SLAM DIRECTORCOR</a>
            <a href="media-playout.html#playcor">SLAM PLAYCOR</a>
            <a href="media-playout.html#timecor">SLAM TIMECOR</a>
            <a href="media-playout.html#modulecor">SLAM MODULECOR <small data-i18n="nav.later">Later</small></a>
          </div>
          <div>
            <p class="subnav-label" data-i18n="nav.ds">Digital Signage – DS Family</p>
            <a href="media-playout.html#deckds">SLAM DECKDS <small data-i18n="nav.later">Later</small></a>
            <a href="media-playout.html#directords">SLAM DIRECTORDS <small data-i18n="nav.later">Later</small></a>
            <a href="media-playout.html#corporateds-tv">SLAM CORPORATEDS TV <small data-i18n="nav.later">Later</small></a>
            <a href="media-playout.html#corporateds-audio">SLAM CORPORATEDS AUDIO <small data-i18n="nav.later">Later</small></a>
            <a href="media-playout.html#corporateds-tx">SLAM CORPORATEDS TX <small data-i18n="nav.later">Later</small></a>
            <a href="media-playout.html#moduleds">SLAM MODULESDS <small data-i18n="nav.later">Later</small></a>
          </div>
        </div>
      </div>
      <div class="nav-group">
        <a href="led-video-systems.html" data-i18n="nav.led">LED Video</a>
        <div class="subnav subnav-mega">
          <div>
            <p class="subnav-label" data-i18n="nav.smd">Next-Gen Efficiency SMD</p>
            <a href="led-video-systems.html#genezes">GENEZES 391</a>
            <a href="led-video-systems.html#aramiz">ARAMIZ 625</a>
            <a href="led-video-systems.html#tschilin">TSCHILIN 10A / 625 PERIMETER</a>
            <a href="led-video-systems.html#aramiz-screen">ARAMIZ 10A / 625 SCREEN</a>
            <p class="subnav-label" data-i18n="nav.cob">COB Ultra LowPower / LowTemp</p>
            <a href="led-video-systems.html#zenario">ZENARIO 250</a>
            <a href="led-video-systems.html#cinemaz">CINEMAZ <small data-i18n="nav.later">Later</small></a>
            <a href="led-video-systems.html#poizen">POIZEN <small data-i18n="nav.later">Later</small></a>
          </div>
          <div>
            <p class="subnav-label" data-i18n="nav.peripherals">Peripherals – CENTRO &amp; AXESS</p>
            <a href="led-video-systems.html#centro-opto">CENTRO OPTO <small data-i18n="nav.later">Later</small></a>
            <a href="led-video-systems.html#centro-mpo">CENTRO MPO <small data-i18n="nav.later">Later</small></a>
            <a href="led-video-systems.html#centro-truss">CENTRO TRUSS <small data-i18n="nav.later">Later</small></a>
            <a href="led-video-systems.html#centro-flight">CENTRO Flightcases <small data-i18n="nav.later">Later</small></a>
            <a href="led-video-systems.html#axess">AXESS Connectivity <small data-i18n="nav.later">Later</small></a>
          </div>
        </div>
      </div>
      <div class="nav-group">
        <a href="solutions.html" data-i18n="nav.solutions">Solutions</a>
        <div class="subnav">
          <a href="solutions.html#intro">Intro</a>
          <a href="solutions.html#cloud">SLAM.SYSTEMS CLOUD</a>
          <a href="solutions.html#training">SLAM.SYSTEMS TRAINING</a>
          <a href="solutions.html#custom-made">SLAM.SYSTEMS CUSTOM MADE SOLUTION</a>
        </div>
      </div>
      <div class="nav-group">
        <a href="company.html" data-i18n="nav.company">Company</a>
        <div class="subnav">
          <a href="company.html#company">Company / CI</a>
          <a href="company.html#personals">Personals <small data-i18n="nav.later">Later</small></a>
          <a href="company.html#partners">Address / Partners</a>
          <a href="company.html#social">Social Media <small data-i18n="nav.later">Later</small></a>
        </div>
      </div>
    </nav>
    <div class="header-end">
      <span class="lang-switch" role="group" aria-label="Language">
        <button type="button" data-lang-btn="en">EN</button>
        <button type="button" data-lang-btn="de">DE</button>
        <button type="button" data-lang-btn="ja">JA</button>
        <button type="button" data-lang-btn="ko">KO</button>
        <button type="button" data-lang-btn="es">ES</button>
        <button type="button" data-lang-btn="fr">FR</button>
      </span>
      <a class="project-link" href="start-project.html"><span data-i18n="nav.project">Start Your Project</span> <span class="arrow" aria-hidden="true">→</span></a>
    </div>
    <details class="mobile-menu">
      <summary data-i18n="nav.menu">Menu</summary>
      <nav aria-label="Mobile">
        <a href="index.html">Home</a>
        <a href="media-playout.html" data-i18n="nav.playout">Media Playout</a>
        <a href="led-video-systems.html" data-i18n="nav.led">LED Video</a>
        <a href="solutions.html" data-i18n="nav.solutions">Solutions</a>
        <a href="company.html" data-i18n="nav.company">Company</a>
        <a href="start-project.html" data-i18n="nav.project">Start Your Project</a>
        <span class="lang-switch mobile-lang" role="group" aria-label="Language">
          <button type="button" data-lang-btn="en">EN</button>
          <button type="button" data-lang-btn="de">DE</button>
          <button type="button" data-lang-btn="ja">JA</button>
          <button type="button" data-lang-btn="ko">KO</button>
          <button type="button" data-lang-btn="es">ES</button>
          <button type="button" data-lang-btn="fr">FR</button>
        </span>
      </nav>
    </details>
  </header>'''

def footer(tag_key, extra_link=None):
    link = extra_link or '<a href="start-project.html"><span data-i18n="nav.project">Start Your Project</span> <span class="arrow">→</span></a>'
    return f'''<footer class="site-footer"><img src="{LOGO}" alt="SLAM.SYSTEMS"><p data-i18n="{tag_key}">Swiss engineering and functional design · R&amp;D Center Shenzhen Hightech Park</p>{link}</footer>'''

def head(title_key, desc_key, title, desc):
    return f'''<!doctype html>
<html lang="en" data-i18n-title="{title_key}" data-i18n-desc="{desc_key}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{desc}">
<title>{title}</title>
<link rel="icon" href="{LOGO}">
<link rel="stylesheet" href="assets/css/styles.css">
</head>'''

INDEX = head("meta.home.title", "meta.home.desc",
             "SLAM.SYSTEMS | Intelligent Live Communication Systems",
             "Sport media playout, LED video systems and intelligent solutions for professional live environments.") + f'''
<body>
  <main class="hero-shell">
    <img class="hero-image" src="assets/images/handball-hero-master-v1-scoreboard-correct.png" alt="SLAM.SYSTEMS operator at a live handball match">
    <div class="hero-shade" aria-hidden="true"></div>
    {header("index.html#top").replace(" interior-header", "")}
    <section class="hero-content" id="top">
      <p class="eyebrow" data-hero-eyebrow><span>01</span> Handball systems</p>
      <h1><span data-i18n="hero.h1a">Precision Thinking.</span><span data-i18n="hero.h1b">Intelligent Systems.</span><strong data-i18n="hero.h1c">Connected Moments.</strong></h1>
      <div class="accent-line" aria-hidden="true"></div>
      <p class="hero-lead"><span data-i18n="hero.lead1">Operational simplicity.</span><br><span data-i18n="hero.lead2">Maximum performance.</span></p>
      <p class="hero-copy" data-hero-copy>From preparation to performance — intelligent communication systems for live handball environments.</p>
      <div class="hero-actions">
        <a class="button button-primary" href="#systems-index"><span data-i18n="hero.cta1">Discover our systems</span> <span class="arrow" aria-hidden="true">→</span></a>
        <a class="button button-secondary" href="#video"><span data-i18n="hero.cta2">Watch video</span> <span class="play arrow" aria-hidden="true">▶</span></a>
      </div>
    </section>
    <div class="hero-sports" role="tablist" aria-label="Live sports">
      <button type="button" data-hero-btn="0" class="on" aria-selected="true">01</button>
      <button type="button" data-hero-btn="1" aria-selected="false">02</button>
      <button type="button" data-hero-btn="2" aria-selected="false">03</button>
    </div>
    <div class="hero-footer" aria-label="Hero information"><span data-i18n="hero.live">Live operations</span><span class="footer-rule"></span><span data-hero-sport>Handball / 01</span></div>
  </main>
  <section class="systems-index" id="systems-index">
    <div class="section-heading">
      <p class="section-code" data-i18n="index.code">Website index / B</p>
      <h2 id="systems-title"><span data-i18n="index.h1">One intelligent architecture.</span><br><strong data-i18n="index.h2">Connected systems.</strong></h2>
      <p data-i18n="index.p">Media Playout, LED systems and long-term integration — one SLAM.SYSTEMS architecture.</p>
    </div>
    <div class="index-grid">
      <a class="index-card" href="media-playout.html"><span class="index-number">B-2</span><h3 data-i18n="nav.playout">Media Playout</h3><p data-i18n="index.playout.p">One Technology. Limitless Possibilities.</p><span class="card-link"><span data-i18n="index.playout.link">Explore COR Family</span> <b>→</b></span></a>
      <a class="index-card" href="led-video-systems.html"><span class="index-number">B-3</span><h3 data-i18n="nav.led">LED Video</h3><p data-i18n="index.led.p">Precision in every pixel.</p><span class="card-link"><span data-i18n="index.led.link">Explore LED Systems</span> <b>→</b></span></a>
      <a class="index-card" href="solutions.html"><span class="index-number">B-4</span><h3 data-i18n="nav.solutions">Solutions</h3><p data-i18n="index.solutions.p">Experience behind reliable systems.</p><span class="card-link"><span data-i18n="index.solutions.link">Explore Solutions</span> <b>→</b></span></a>
      <a class="index-card" href="company.html"><span class="index-number">B-5</span><h3 data-i18n="nav.company">Company</h3><p data-i18n="index.company.p">Connecting Content. Connecting People.</p><span class="card-link"><span data-i18n="index.company.link">Discover SLAM.SYSTEMS</span> <b>→</b></span></a>
    </div>
  </section>
  <section class="video-section" id="video">
    <div>
      <p class="section-code" data-i18n="video.code">Live moments / Vision of live</p>
      <h2 data-i18n="video.h">The intelligent core behind every live sports moment.</h2>
    </div>
    <button class="video-trigger" type="button" aria-label="Video later"><span>▶</span> <span data-i18n="video.btn">Watch video</span></button>
  </section>
  {footer("foot.tag")}
  {JS}
</body>
</html>
'''

PLAYOUT = head("meta.playout.title", "meta.playout.desc", "Media Playout | SLAM.SYSTEMS",
               "COR Family sport media playout — one operator, complete control of the live moment.") + f'''
<body class="interior-body">
  {header()}
  <main>
    <section class="page-hero"><div class="page-hero-inner"><p class="page-kicker" data-i18n="playout.kicker">B-2 / Media Playout</p><h1><span data-i18n="playout.h1">One Technology.</span><strong data-i18n="playout.h2">Limitless Possibilities.</strong></h1><p class="page-intro" data-i18n="playout.intro">One operator. One intelligent system. Complete control of the live moment.</p></div></section>
    <nav class="section-nav" aria-label="Media Playout">
      <a href="#cor-family">COR Family</a>
      <a href="#deckcor">DECKCOR</a>
      <a href="#scorecor">SCORECOR</a>
      <a href="#directorcor">DIRECTORCOR</a>
      <a href="#playcor">PLAYCOR</a>
      <a href="#timecor">TIMECOR</a>
      <a href="#ds-family">DS Family</a>
    </nav>
    <section class="content-section" id="cor-family">
      <div class="content-head"><p class="content-code" data-i18n="playout.cor.code">B-2.1 / Sport Media</p><h2 data-i18n="playout.cor.h">SLAM.SYSTEMS COR Family</h2></div>
      <div class="content-layout">
        <div class="content-copy">
          <p data-i18n="playout.cor.p">Live data, media, scoreboards and LED — one modular system. Complexity stays in the system.</p>
          <ul class="feature-list">
            <li data-i18n="playout.cor.f1">Live sports communication</li>
            <li data-i18n="playout.cor.f2">Scoreboards and live data</li>
            <li data-i18n="playout.cor.f3">Media playout and broadcast</li>
            <li data-i18n="playout.cor.f4">LED and stadium communication</li>
          </ul>
        </div>
        <div class="content-grid">
          <article class="content-card" id="deckcor"><span class="status">Frontend / Ready</span><h3>SLAM DECKCOR</h3><p data-i18n="playout.deck.p">The operator frontend. One person runs the arena.</p></article>
          <article class="content-card" id="scorecor"><span class="status">Frontend / Ready</span><h3>SLAM SCORECOR</h3><p data-i18n="playout.score.p">Scoreboards, match logic and live data — on iPad.</p></article>
          <article class="content-card" id="directorcor"><span class="status">Control / Ready</span><h3>SLAM DIRECTORCOR</h3><p data-i18n="playout.director.p">Layouts, timing and shows. Orchestrated.</p></article>
          <article class="content-card" id="playcor"><span class="status">Runtime / Ready</span><h3>SLAM PLAYCOR</h3><p data-i18n="playout.play.p">Reliable output. HD to 8K. Under 18 ms.</p></article>
          <article class="content-card" id="timecor"><span class="status">Runtime / Ready</span><h3>SLAM TIMECOR</h3><p data-i18n="playout.time.p">Match time and score beyond the field of play.</p></article>
          <article class="content-card" id="modulecor"><span class="status later">Optional / Later</span><h3>SLAM MODULECOR</h3><p data-i18n="playout.module.p">Optional COR extensions. Reserved.</p></article>
        </div>
      </div>
    </section>
    <section class="content-section" id="ds-family">
      <div class="content-head"><p class="content-code" data-i18n="playout.ds.code">B-2.2 / Digital Signage</p><h2 data-i18n="playout.ds.h">SLAM.SYSTEMS DS Family</h2></div>
      <div class="content-layout">
        <div class="content-copy"><p data-i18n="playout.ds.p">Corporate communication and digital signage. Structure ready — content later.</p></div>
        <div class="content-grid">
          <article class="content-card" id="deckds"><span class="status later">Later</span><h3>SLAM DECKDS</h3><p data-i18n="playout.deckds.p">Frontend for corporate and signage control.</p></article>
          <article class="content-card" id="directords"><span class="status later">Later</span><h3>SLAM DIRECTORDS</h3><p data-i18n="playout.directords.p">Control layer for corporate media.</p></article>
          <article class="content-card" id="corporateds-tv"><span class="status later">Later</span><h3>SLAM CORPORATEDS TV</h3><p data-i18n="playout.tv.p">CorporateTV runtime.</p></article>
          <article class="content-card" id="corporateds-audio"><span class="status later">Later</span><h3>SLAM CORPORATEDS AUDIO</h3><p data-i18n="playout.audio.p">CorporateAUDIO runtime.</p></article>
          <article class="content-card" id="corporateds-tx"><span class="status later">Later</span><h3>SLAM CORPORATEDS TX</h3><p data-i18n="playout.tx.p">CorporateTXT runtime.</p></article>
          <article class="content-card" id="moduleds"><span class="status later">Later</span><h3>SLAM MODULESDS</h3><p data-i18n="playout.moduleds.p">Optional DS modules. Reserved.</p></article>
        </div>
      </div>
    </section>
  </main>
  {footer("foot.playout")}
  {JS}
</body>
</html>
'''

LED = head("meta.led.title", "meta.led.desc", "LED Video Systems | SLAM.SYSTEMS",
           "Professional LED systems for sport, broadcast and communication.") + f'''
<body class="interior-body">
  {header()}
  <main>
    <section class="page-hero"><div class="page-hero-inner"><p class="page-kicker" data-i18n="led.kicker">B-3 / LED Video Systems</p><h1><span data-i18n="led.h1">Beyond Pixels.</span><strong data-i18n="led.h2">Creating Visual Experiences.</strong></h1><p class="page-intro" data-i18n="led.intro">Indoor and outdoor LED — built for sport, broadcast and live communication.</p></div></section>
    <nav class="section-nav">
      <a href="#led-display">LED Display</a>
      <a href="#smd">SMD</a>
      <a href="#cob">COB</a>
      <a href="#peripherals">Peripherals</a>
    </nav>
    <section class="content-section" id="led-display">
      <div class="content-head"><p class="content-code" data-i18n="led.intro.code">B-3.1 / Introduction</p><h2 data-i18n="led.intro.h">Precision in every pixel.</h2></div>
      <div class="content-layout">
        <div class="content-copy"><p data-i18n="led.intro.p">An LED system is a communication medium — not just a screen.</p>
          <ul class="feature-list">
            <li data-i18n="led.intro.f1">Indoor and outdoor systems</li>
            <li data-i18n="led.intro.f2">Sport and broadcast use</li>
            <li data-i18n="led.intro.f3">Image quality and long-term reliability</li>
            <li data-i18n="led.intro.f4">Integrated into SLAM.SYSTEMS</li>
          </ul>
        </div>
      </div>
    </section>
    <section class="content-section" id="smd">
      <div class="content-head"><p class="content-code" data-i18n="led.smd.code">B-3.1.1 / SMD</p><h2 data-i18n="led.smd.h">Next-Gen Efficiency SMD</h2></div>
      <div class="content-grid">
        <article class="content-card" id="genezes"><span class="status later">Later</span><h3>GENEZES 391</h3><p data-i18n="led.genezes.p">Flexible indoor and outdoor performance.</p></article>
        <article class="content-card" id="aramiz"><span class="status later">Later</span><h3>ARAMIZ 625</h3><p data-i18n="led.aramiz.p">Hybrid performance for demanding climates.</p></article>
        <article class="content-card" id="tschilin"><span class="status later">Later</span><h3>TSCHILIN 10A / 625 PERIMETER</h3><p data-i18n="led.tschilin.p">Outdoor perimeter. Wide angles. High readability.</p></article>
        <article class="content-card" id="aramiz-screen"><span class="status later">Later</span><h3>ARAMIZ 10A / 625 SCREEN</h3><p data-i18n="led.aramizs.p">Screen system. Fast install. Service access.</p></article>
      </div>
    </section>
    <section class="content-section" id="cob">
      <div class="content-head"><p class="content-code" data-i18n="led.cob.code">B-3.1.2 / COB</p><h2 data-i18n="led.cob.h">Ultra LowPower / LowTemp</h2></div>
      <div class="content-layout">
        <div class="content-copy"><p data-i18n="led.cob.p">Fine pitch, deep contrast, natural colour for indoor use.</p></div>
        <div class="content-grid">
          <article class="content-card" id="zenario"><span class="status">Ready</span><h3>ZENARIO 250</h3><p data-i18n="led.zenario.p">Fine pixel pitch for scoreboards, POI and control rooms.</p></article>
          <article class="content-card" id="cinemaz"><span class="status later">Later</span><h3>CINEMAZ</h3><p data-i18n="led.cinemaz.p">TV studio, broadcast and cinema. Later.</p></article>
          <article class="content-card" id="poizen"><span class="status later">Later</span><h3>POIZEN</h3><p data-i18n="led.poizen.p">LED poster formats. Later.</p></article>
        </div>
      </div>
    </section>
    <section class="content-section" id="peripherals">
      <div class="content-head"><p class="content-code" data-i18n="led.per.code">B-3.2 / Peripherals</p><h2 data-i18n="led.per.h">CENTRO &amp; AXESS</h2></div>
      <div class="content-grid">
        <article class="content-card" id="centro-opto"><span class="status later">Later</span><h3>CENTRO OPTO</h3><p data-i18n="led.opto.p">Optical data transmission. Later.</p></article>
        <article class="content-card" id="centro-mpo"><span class="status later">Later</span><h3>CENTRO MPO</h3><p data-i18n="led.mpo.p">MPO connectivity. Later.</p></article>
        <article class="content-card" id="centro-truss"><span class="status later">Later</span><h3>CENTRO TRUSS</h3><p data-i18n="led.truss.p">Truss and mounting. Later.</p></article>
        <article class="content-card" id="centro-flight"><span class="status later">Later</span><h3>CENTRO Flightcases</h3><p data-i18n="led.flight.p">Flightcases. Later.</p></article>
        <article class="content-card" id="axess"><span class="status later">Later</span><h3>AXESS Connectivity</h3><p data-i18n="led.axess.p">Connectivity and power. Later.</p></article>
      </div>
    </section>
  </main>
  {footer("foot.led")}
  {JS}
</body>
</html>
'''

SOL = head("meta.solutions.title", "meta.solutions.desc", "Solutions | SLAM.SYSTEMS",
           "Cloud, training and custom-made solutions behind reliable systems.") + f'''
<body class="interior-body">
  {header()}
  <main>
    <section class="page-hero"><div class="page-hero-inner"><p class="page-kicker" data-i18n="sol.kicker">B-4 / Solutions</p><h1><span data-i18n="sol.h1">Experience behind</span><strong data-i18n="sol.h2">reliable systems.</strong></h1><p class="page-intro" data-i18n="sol.intro">More than 25 years in professional communication and media systems.</p></div></section>
    <nav class="section-nav">
      <a href="#intro">Intro</a>
      <a href="#cloud">Cloud</a>
      <a href="#training">Training</a>
      <a href="#custom-made">Custom Made</a>
    </nav>
    <section class="content-section" id="intro">
      <div class="content-head"><p class="content-code" data-i18n="sol.in.code">Introduction / Vision of Live</p><h2 data-i18n="sol.in.h">From analysis to long-term operation.</h2></div>
      <div class="content-layout">
        <div class="content-copy"><p data-i18n="sol.in.p">Software, hardware and existing infrastructure — one reliable environment.</p>
          <ul class="feature-list">
            <li data-i18n="sol.in.f1">Analysis, concept, planning</li>
            <li data-i18n="sol.in.f2">Integration of existing infrastructure</li>
            <li data-i18n="sol.in.f3">Installation and commissioning</li>
            <li data-i18n="sol.in.f4">Training and documentation</li>
            <li data-i18n="sol.in.f5">After-sales and service level support</li>
          </ul>
        </div>
      </div>
    </section>
    <section class="content-section" id="cloud">
      <div class="content-head"><p class="content-code" data-i18n="sol.cloud.code">B-4.1 / Cloud</p><h2 data-i18n="sol.cloud.h">SLAM.SYSTEMS Cloud</h2></div>
      <div class="content-layout">
        <div class="content-copy"><p data-i18n="sol.cloud.p">Docs, operation notes and system knowledge — in one place.</p></div>
        <article class="content-card"><span class="status">Ready</span><h3 data-i18n="sol.cloud.card">More than documentation.</h3></article>
      </div>
    </section>
    <section class="content-section" id="training">
      <div class="content-head"><p class="content-code" data-i18n="sol.train.code">B-4.2 / Training</p><h2 data-i18n="sol.train.h">Training &amp; Knowledge Transfer</h2></div>
      <div class="content-layout">
        <div class="content-copy"><p data-i18n="sol.train.p">Hands-on training. Users run the system themselves.</p></div>
        <article class="content-card"><span class="status">Ready</span><h3 data-i18n="sol.train.card">Empowering users.</h3></article>
      </div>
    </section>
    <section class="content-section" id="custom-made">
      <div class="content-head"><p class="content-code" data-i18n="sol.custom.code">B-4.3 / Custom Made</p><h2 data-i18n="sol.custom.h">Custom Made Solution</h2></div>
      <div class="content-layout">
        <div class="content-copy"><p data-i18n="sol.custom.p">Extra functions and integrations — without breaking the architecture.</p></div>
        <article class="content-card"><span class="status">Ready</span><h3 data-i18n="sol.custom.card">Extending systems.</h3></article>
      </div>
    </section>
  </main>
  {footer("foot.solutions")}
  {JS}
</body>
</html>
'''

COMPANY = head("meta.company.title", "meta.company.desc", "Company | SLAM.SYSTEMS",
               "Connecting Content. Connecting People.") + f'''
<body class="interior-body">
  {header()}
  <main>
    <section class="page-hero"><div class="page-hero-inner"><p class="page-kicker" data-i18n="co.kicker">B-5 / Company</p><h1><span data-i18n="co.h1">Connecting Content.</span><strong data-i18n="co.h2">Connecting People.</strong></h1><p class="page-intro" data-i18n="co.intro">Swiss Precision. Shenzhen Innovation. Connected Communication.</p></div></section>
    <nav class="section-nav">
      <a href="#company">Company / CI</a>
      <a href="#personals">Personals</a>
      <a href="#partners">Address / Partners</a>
      <a href="#social">Social Media</a>
    </nav>
    <section class="content-section" id="company">
      <div class="content-head"><p class="content-code" data-i18n="co.ci.code">B-5.1 / Company / CI</p><h2 data-i18n="co.ci.h">The right connection creates impact.</h2></div>
      <div class="content-layout">
        <div class="content-copy"><p data-i18n="co.ci.p">Since 1999: from corporate communication to live sport systems.</p>
          <ul class="feature-list">
            <li data-i18n="co.ci.f1">Swiss Precision</li>
            <li data-i18n="co.ci.f2">Intelligent Innovation</li>
            <li data-i18n="co.ci.f3">Human Connection</li>
          </ul>
        </div>
      </div>
    </section>
    <section class="content-section" id="personals">
      <div class="content-head"><p class="content-code" data-i18n="co.personals.code">B-5.2 / Personals</p><h2 data-i18n="co.personals.h">Personals</h2></div>
      <div class="content-copy"><p data-i18n="co.personals.p">Team portraits follow in a later content phase.</p></div>
    </section>
    <section class="content-section" id="partners">
      <div class="content-head"><p class="content-code" data-i18n="co.addr.code">B-5.3 / Address / Partners</p><h2 data-i18n="co.addr.h">European presence. Asian innovation.</h2></div>
      <div class="content-grid">
        <article class="content-card"><span class="status">Europe</span><h3>ROUNDS</h3><p>Fabrikstrasse 7<br>9200 Gossau<br>Switzerland<br>info@rounds.ch</p></article>
        <article class="content-card"><span class="status">Asia</span><h3>Shenzhen Watermoon Ltd.</h3><p>Guangming New District<br>518132 Shenzhen<br>China<br>i@watermoon.com</p></article>
        <article class="content-card"><span class="status">Direct</span><h3>SLAM.SYSTEMS</h3><p data-i18n="co.mail">Project enquiries: i@slam.systems</p></article>
      </div>
    </section>
    <section class="content-section" id="social">
      <div class="content-head"><p class="content-code" data-i18n="co.social.code">B-5.4 / Social Media</p><h2 data-i18n="co.social.h">Connected communication.</h2></div>
      <div class="content-copy"><p data-i18n="co.social.p">Channels follow in a later content phase.</p></div>
    </section>
  </main>
  {footer("foot.company")}
  {JS}
</body>
</html>
'''

PROJECT = head("meta.project.title", "meta.project.desc", "Start Your Project | SLAM.SYSTEMS",
               "Start a SLAM.SYSTEMS project. Direct contact: i@slam.systems.") + f'''
<body class="interior-body">
  {header()}
  <main>
    <section class="page-hero"><div class="page-hero-inner"><p class="page-kicker" data-i18n="pr.kicker">B-6 / Contact</p><h1><span data-i18n="pr.h1">Start Your</span><strong data-i18n="pr.h2">Project.</strong></h1><p class="page-intro" data-i18n="pr.intro">Tell us the venue, the challenge, the live moment.</p></div></section>
    <section class="project-panel">
      <div>
        <p class="content-code" data-i18n="pr.direct">Direct contact</p>
        <h1><span data-i18n="pr.h3">Let’s create</span><strong data-i18n="pr.h4">connected moments.</strong></h1>
        <p class="content-copy">i@slam.systems</p>
      </div>
      <form class="project-form" data-mailto-form>
        <label><span data-i18n="pr.name">Name</span><input type="text" name="name" autocomplete="name" required></label>
        <label><span data-i18n="pr.company">Company</span><input type="text" name="company" autocomplete="organization"></label>
        <label><span data-i18n="pr.email">Email</span><input type="email" name="email" autocomplete="email" required></label>
        <label><span data-i18n="pr.phone">Phone</span><input type="tel" name="phone" autocomplete="tel"></label>
        <label class="full"><span data-i18n="pr.message">Project / Message</span><textarea name="message" required></textarea></label>
        <button type="submit" data-i18n="pr.send">Send project request</button>
      </form>
    </section>
  </main>
  {footer("foot.project", extra_link='<a href="index.html"><span data-i18n="foot.home">Back to Home</span> <span class="arrow">→</span></a>')}
  {JS}
</body>
</html>
'''

def write(name, html):
    path = ROOT / name
    path.write_text(html.strip() + "\n", encoding="utf-8")
    print("wrote", path, path.stat().st_size)

if __name__ == "__main__":
    write("index.html", INDEX)
    write("media-playout.html", PLAYOUT)
    write("led-video-systems.html", LED)
    write("solutions.html", SOL)
    write("company.html", COMPANY)
    write("start-project.html", PROJECT)
