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
      <a href="led-video-systems.html">LED Video</a>
      <div class="subnav subnav-wide subnav-scroll">
        <div class="subnav-branch">
          <a href="led-video-systems.html#led-display">LED Display / LED-Video</a>
          <div class="subsubnav">
            <a href="led-video-systems.html#smd">SMD LED Systems</a>
            <a class="nav-product-link" href="led-video-systems.html#genezes">GENEZES 391</a>
            <a class="nav-product-link" href="led-video-systems.html#aramiz-625">ARAMIZ 625</a>
            <a class="nav-product-link" href="led-video-systems.html#tschilin">TSCHILIN 10A / 625</a>
            <a class="nav-product-link" href="led-video-systems.html#aramiz-screen">ARAMIZ 10A / 625</a>
            <a href="led-video-systems.html#cob">COB Technology</a>
            <a class="nav-product-link" href="led-video-systems.html#zenario">ZENARIO</a>
            <a class="nav-product-link" href="led-video-systems.html#poizen">POIZEN</a>
            <a class="nav-product-link" href="led-video-systems.html#cinemaz">CINEMAZ</a>
          </div>
        </div>
        <div class="subnav-branch">
          <a href="led-video-systems.html#peripherals">Peripherals</a>
          <div class="subsubnav">
            <a href="led-video-systems.html#centro">CENTRO</a>
            <a href="led-video-systems.html#nerv">NERV</a>
          </div>
        </div>
      </div>`;
  }
}
