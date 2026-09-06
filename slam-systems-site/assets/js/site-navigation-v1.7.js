const desktopNavigation = document.querySelector(".desktop-nav");

if (desktopNavigation) {
  const mediaGroup = Array.from(desktopNavigation.querySelectorAll(".nav-group")).find(
    (group) => group.querySelector(":scope > a")?.getAttribute("href") === "media-playout.html"
  );

  if (mediaGroup) {
    mediaGroup.innerHTML = `
      <a href="media-playout.html">Media Playout</a>
      <div class="subnav subnav-wide subnav-scroll">
        <div class="subnav-branch">
          <a href="media-playout.html#cor-family">COR Family</a>
          <div class="subsubnav">
            <a href="media-playout.html#deckcor">DECK<sup class="nav-suffix">COR</sup></a>
            <a href="media-playout.html#scorecor">SCORE<sup class="nav-suffix">COR</sup></a>
            <a href="media-playout.html#directorcor">DIRECTOR<sup class="nav-suffix">COR</sup></a>
            <a href="media-playout.html#playcor">PLAY<sup class="nav-suffix">COR</sup></a>
            <a href="media-playout.html#timecor">TIME<sup class="nav-suffix">COR</sup></a>
          </div>
        </div>
        <div class="subnav-branch">
          <a href="media-playout.html#dis-family">DIS Family</a>
          <div class="subsubnav">
            <a href="media-playout.html#deckdis">DECK<sup class="nav-suffix">DIS</sup></a>
            <a href="media-playout.html#directordis">DIRECTOR<sup class="nav-suffix">DIS</sup></a>
            <a href="media-playout.html#corporate-dis-tv">CORPORATE<sup class="nav-suffix">DIS</sup> TV</a>
            <a href="media-playout.html#corporate-dis-audio">CORPORATE<sup class="nav-suffix">DIS</sup> AUDIO</a>
            <a href="media-playout.html#corporate-dis-txt">CORPORATE<sup class="nav-suffix">DIS</sup> TXT</a>
          </div>
        </div>
      </div>`;
  }

  const ledGroup = Array.from(desktopNavigation.querySelectorAll(".nav-group")).find(
    (group) => group.querySelector(":scope > a")?.getAttribute("href") === "led-video-systems.html"
  );

  if (ledGroup) {
    ledGroup.innerHTML = `
      <a href="led-video-systems.html">LED Video Systems</a>
      <div class="subnav subnav-wide subnav-scroll led-subnav">
        <div class="subnav-branch">
          <a class="nav-mixed-link" href="led-video-systems.html#sport-certified"><span class="nav-name">SPORTSELAB</span><span class="nav-description">SPORT CERTIFIED LED SYSTEMS</span></a>
          <div class="subsubnav">
            <a class="nav-product-link nav-mixed-link" href="led-video-systems.html#nemezes"><span class="nav-name">NEMEZES</span><span class="nav-description">All-Weather Reliability</span></a>
            <a class="nav-product-link nav-mixed-link" href="led-video-systems.html#genezes"><span class="nav-name">GENEZES</span><span class="nav-description">Indoor &amp; Outdoor Flexibility</span></a>
            <a class="nav-product-link nav-mixed-link" href="led-video-systems.html#aramiz-625"><span class="nav-name">ALEZEN</span><span class="nav-description">Hybrid Performance for Demanding Environment</span></a>
          </div>
        </div>
        <div class="subnav-branch">
          <a class="nav-mixed-link" href="led-video-systems.html#smd"><span class="nav-name">SLAM.SYSTEMS</span><span class="nav-description">SMD – EFFICIENCY LED VIDEO SYSTEMS</span></a>
          <div class="subsubnav">
            <a class="nav-product-link nav-mixed-link" href="led-video-systems.html#tschilin"><span class="nav-name">TSCHILIN</span><span class="nav-description">PERIMETER SYSTEM – Optimized for Professional In-/Outdoor Applications</span></a>
            <a class="nav-product-link nav-mixed-link" href="led-video-systems.html#aramiz-screen"><span class="nav-name">ARAMIZ</span><span class="nav-description">SCREEN SYSTEM – Designed for Flexible Integration</span></a>
          </div>
        </div>
        <div class="subnav-branch">
          <a class="nav-mixed-link" href="led-video-systems.html#cob"><span class="nav-name">SLAM.SYSTEMS</span><span class="nav-description">COB – ULTRA LOW POWER/TEMP</span></a>
          <div class="subsubnav">
            <a class="nav-product-link nav-mixed-link" href="led-video-systems.html#zenario"><span class="nav-name">ZENARIO</span><span class="nav-description">Fine Pixel Pitch LED Technology Family</span></a>
            <a class="nav-product-link nav-mixed-link" href="led-video-systems.html#poizen"><span class="nav-name">POIZEN</span><span class="nav-description">Modular LED Poster System – Stand-alone, Cascaded, Connected</span></a>
            <a class="nav-product-link nav-mixed-link" href="led-video-systems.html#cinemaz"><span class="nav-name">CINEMAZ</span><span class="nav-description">Broadcast, Studio, Cinema &amp; Control Rooms</span></a>
          </div>
        </div>
      </div>`;
  }
}

const dnaV20 = document.createElement("script");
dnaV20.src = ((document.currentScript && document.currentScript.src) ? new URL('dna-v2.0.js?v=20260906-v226', document.currentScript.src).href : 'dna-v2.0.js?v=20260906-v226');
document.body.appendChild(dnaV20);
