(() => {
  if (!document.querySelector('link[href*="dna-v2.0.css"]')) {
    const stylesheet = document.createElement("link");
    stylesheet.rel = "stylesheet";
    stylesheet.href = ((document.currentScript && document.currentScript.src) ? new URL('../css/dna-v2.0.css?v=20260906-v226', document.currentScript.src).href : '../css/dna-v2.0.css?v=20260906-v226');
    document.head.appendChild(stylesheet);
  }

  const currentFile = window.location.pathname.split("/").pop() || "index.html";
  const local = (file, hash = "") => currentFile === file ? hash : `${file}${hash}`;

  const desktopNavigation = document.querySelector(".desktop-nav");
  if (desktopNavigation) {
    desktopNavigation.innerHTML = `
      <div class="nav-group">
        <a href="media-playout.html">Media Playout</a>
        <div class="subnav subnav-wide subnav-scroll">
          <div class="subnav-branch">
            <a href="${local("media-playout.html", "#cor-family")}">COR Family</a>
            <div class="subsubnav">
              <a href="${local("media-playout.html", "#deckcor")}">DECK<sup class="nav-suffix">COR</sup></a>
              <a href="${local("media-playout.html", "#scorecor")}">SCORE<sup class="nav-suffix">COR</sup></a>
              <a href="${local("media-playout.html", "#directorcor")}">DIRECTOR<sup class="nav-suffix">COR</sup></a>
              <a href="${local("media-playout.html", "#playcor")}">PLAY<sup class="nav-suffix">COR</sup></a>
              <a href="${local("media-playout.html", "#timecor")}">TIME<sup class="nav-suffix">COR</sup></a>
            </div>
          </div>
          <div class="subnav-branch">
            <a href="${local("media-playout.html", "#dis-family")}">DIS Family</a>
            <div class="subsubnav">
              <a href="${local("media-playout.html", "#deckdis")}">DECK<sup class="nav-suffix">DIS</sup></a>
              <a href="${local("media-playout.html", "#directordis")}">DIRECTOR<sup class="nav-suffix">DIS</sup></a>
              <a href="${local("media-playout.html", "#corporate-dis-tv")}">CORPORATE<sup class="nav-suffix">DIS</sup> TV</a>
              <a href="${local("media-playout.html", "#corporate-dis-audio")}">CORPORATE<sup class="nav-suffix">DIS</sup> AUDIO</a>
              <a href="${local("media-playout.html", "#corporate-dis-txt")}">CORPORATE<sup class="nav-suffix">DIS</sup> TXT</a>
            </div>
          </div>
        </div>
      </div>
      <div class="nav-group">
        <a href="led-video-systems.html">LED Video Systems</a>
        <div class="subnav subnav-wide subnav-scroll led-subnav">
          <div class="subnav-branch">
            <a class="nav-mixed-link" href="${local("led-video-systems.html", "#sport-certified")}"><span class="nav-name">SPORTSELAB</span><span class="nav-description">SPORT CERTIFIED LED SYSTEMS</span></a>
            <div class="subsubnav">
              <a class="nav-product-link nav-mixed-link" href="${local("led-video-systems.html", "#nemezes")}"><span class="nav-name">NEMEZES</span><span class="nav-description">All-Weather Reliability</span></a>
              <a class="nav-product-link nav-mixed-link" href="${local("led-video-systems.html", "#genezes")}"><span class="nav-name">GENEZES</span><span class="nav-description">Indoor &amp; Outdoor Flexibility</span></a>
              <a class="nav-product-link nav-mixed-link" href="${local("led-video-systems.html", "#aramiz-625")}"><span class="nav-name">ALEZEN</span><span class="nav-description">Hybrid Performance for Demanding Environment</span></a>
            </div>
          </div>
          <div class="subnav-branch">
            <a class="nav-mixed-link" href="${local("led-video-systems.html", "#smd")}"><span class="nav-name">SLAM.SYSTEMS</span><span class="nav-description">SMD – EFFICIENCY LED VIDEO SYSTEMS</span></a>
            <div class="subsubnav">
              <a class="nav-product-link nav-mixed-link" href="${local("led-video-systems.html", "#tschilin")}"><span class="nav-name">TSCHILIN</span><span class="nav-description">PERIMETER SYSTEM – Optimized for Professional In-/Outdoor Applications</span></a>
              <a class="nav-product-link nav-mixed-link" href="${local("led-video-systems.html", "#aramiz-screen")}"><span class="nav-name">ARAMIZ</span><span class="nav-description">SCREEN SYSTEM – Designed for Flexible Integration</span></a>
            </div>
          </div>
          <div class="subnav-branch">
            <a class="nav-mixed-link" href="${local("led-video-systems.html", "#cob")}"><span class="nav-name">SLAM.SYSTEMS</span><span class="nav-description">COB – ULTRA LOW POWER/TEMP</span></a>
            <div class="subsubnav">
              <a class="nav-product-link nav-mixed-link" href="${local("led-video-systems.html", "#zenario")}"><span class="nav-name">ZENARIO</span><span class="nav-description">Fine Pixel Pitch LED Technology Family</span></a>
              <a class="nav-product-link nav-mixed-link" href="${local("led-video-systems.html", "#poizen")}"><span class="nav-name">POIZEN</span><span class="nav-description">Modular LED Poster System – Stand-alone, Cascaded, Connected</span></a>
              <a class="nav-product-link nav-mixed-link" href="${local("led-video-systems.html", "#cinemaz")}"><span class="nav-name">CINEMAZ</span><span class="nav-description">Broadcast, Studio, Cinema &amp; Control Rooms</span></a>
            </div>
          </div>
        </div>
      </div>
      <div class="nav-group">
        <a href="peripherals.html">Peripherals</a>
        <div class="subnav subnav-wide">
          <a href="${local("peripherals.html", "#peripherals-family")}">Introduction</a>
          <a href="${local("peripherals.html", "#centro")}">CENTRO</a>
          <a href="${local("peripherals.html", "#nerv")}">NERV</a>
          <a href="${local("peripherals.html", "#axess")}">AXESS</a>
        </div>
      </div>
      <div class="nav-group">
        <a href="solutions.html">Solutions</a>
        <div class="subnav">
          <a href="${local("solutions.html", "#intro")}">Introduction</a>
          <a href="${local("solutions.html", "#cloud")}">Cloud</a>
          <a href="${local("solutions.html", "#training")}">Training</a>
          <a href="${local("solutions.html", "#custom-made")}">Custom Made</a>
        </div>
      </div>
      <div class="nav-group">
        <a href="company.html">Company</a>
        <div class="subnav">
          <a href="${local("company.html", "#company")}">Company</a>
          <a href="${local("company.html", "#philosophy")}">Philosophy</a>
          <a href="${local("company.html", "#partners")}">Partners</a>
          <a href="${local("company.html", "#team")}">Team</a>
          <a href="${local("company.html", "#contact")}">Address</a>
          <a href="project-request.html#project-request">Project Request</a>
          <a href="${local("company.html", "#social")}">Social Media</a>
          <a href="${local("company.html", "#protection-policies")}">Protection &amp; Policies</a>
        </div>
      </div>`;
  }

  document.querySelectorAll(".mobile-menu nav").forEach((navigation) => {
    navigation.innerHTML = `
      <a href="index.html">Home</a>
      <a href="media-playout.html">Media Playout</a>
      <a href="led-video-systems.html">LED Video Systems</a>
      <a href="peripherals.html">Peripherals</a>
      <a href="solutions.html">Solutions</a>
      <a href="company.html">Company</a>
      <a href="start-project.html">Start Your Project</a>`;
  });

  if (currentFile === "index.html" || currentFile === "") {
    const grid = document.querySelector(".index-grid");
    if (grid) {
      grid.innerHTML = `
        <a class="index-card" href="media-playout.html"><span class="index-number">B-2</span><h3>Media Playout</h3><p>One Operator. One Intelligent System. Complete Control of the Live Moment.</p><span class="card-link">Explore COR Family <b>→</b></span></a>
        <a class="index-card" href="led-video-systems.html"><span class="index-number">B-3</span><h3>LED Video Systems</h3><p>Precision in every pixel.</p><span class="card-link">Explore LED Systems <b>→</b></span></a>
        <a class="index-card" href="peripherals.html"><span class="index-number">B-4</span><h3>Peripherals</h3><p>As you need it.</p><span class="card-link">Explore Peripherals <b>→</b></span></a>
        <a class="index-card" href="solutions.html"><span class="index-number">B-5</span><h3>Solutions</h3><p>Experience behind reliable systems.</p><span class="card-link">Explore Solutions <b>→</b></span></a>
        <a class="index-card" href="company.html"><span class="index-number">B-6</span><h3>Company</h3><p>Connecting Content. Connecting People.</p><span class="card-link">Discover SLAM.SYSTEMS <b>→</b></span></a>`;
    }
  }

  if (currentFile === "led-video-systems.html") {
    document.querySelector("#peripherals")?.remove();
  }

  const replacements = {
    "solutions.html": [
      [".page-kicker", "B-5 / Solutions"],
      ["#cloud .content-code", "B-5.1 / Cloud"],
      ["#training .content-code", "B-5.2 / Training"],
      ["#custom-made .content-code", "B-5.3 / Custom Made"]
    ],
    "company.html": [
      [".page-kicker", "B-6 / Company"],
      ["#company .content-code", "B-6.1 / Company"],
      ["#philosophy .content-code", "B-6.2 / Philosophy"],
      ["#partners .content-code", "B-6.3 / Partners"],
      ["#team .content-code", "B-6.4 / Team"],
      ["#contact .content-code", "B-6.5 / Address"],
      ["#social .content-code", "B-6.6 / Social Media"],
      ["#protection-policies .content-code", "B-6.7 / Protection & Policies"]
    ],
    "start-project.html": [
      [".page-kicker", "B-7 / Contact"]
    ]
  };

  (replacements[currentFile] || []).forEach(([selector, value]) => {
    const element = document.querySelector(selector);
    if (element) element.textContent = value;
  });

  if (currentFile === "company.html") {
    const asiaCard = Array.from(document.querySelectorAll("#partners .content-card"))
      .find((card) => card.querySelector("h3")?.textContent.includes("WATERMOON.COMMUNICATION"));
    const paragraph = asiaCard?.querySelector("p");
    if (paragraph) {
      paragraph.innerHTML = `Area B, 5th Floor, 1st Building, SZZT industrial Park<br>No. 3 Tongguan Road, Guangming New District<br>518132 Shenzhen<br>China<br><a href="mailto:i@slam.systems?subject=SLAM.SYSTEMS%20%20%20%7C%20%20%20MEDIA%20REQUEST">i@slam.systems</a><br><a href="https://slam.systems/">slam.systems</a>`;
    }
  }

  if (currentFile === "media-playout.html") {
    const mediaContent = document.querySelector("main");
    const excluded = "h1, h2, h3, h4, h5, h6, nav, summary, .product-name, .product-claim, .status, .content-code";
    const corProductPattern = /SLAM (DECK|SCORE|DIRECTOR|PLAY|TIME|MODULE)COR/g;
    const disProductPattern = /SLAM (DECK|DIRECTOR)DIS|SLAM CORPORATEDIS (TV|AUDIO|TXT)|SLAM MODULESDIS/g;
    const familyPattern = /SLAM\.SYSTEMS COR FAMILY|SLAM COR FAMILY|SLAM\.SYSTEMS DIS FAMILY|SLAM DIS FAMILY|SLAM\.SYSTEMS COR|SLAM COR|SLAM\.SYSTEMS DIS|SLAM DIS|SLAM\.SYSTEMS/g;

    const nameMarkup = (match, product) => {
      if (product) {
        return `<span class="product-name">SLAM ${product}<sup class="product-suffix">COR</sup></span>`;
      }
      if (match === "SLAM.SYSTEMS COR FAMILY") {
        return `<span class="product-name">SLAM.SYSTEMS<sup class="product-suffix">COR</sup></span> Family`;
      }
      if (match === "SLAM COR FAMILY") {
        return `<span class="product-name">SLAM.SYSTEMS<sup class="product-suffix">COR</sup></span> Family`;
      }
      if (match === "SLAM.SYSTEMS DIS FAMILY") {
        return `<span class="product-name">SLAM.SYSTEMS<sup class="product-suffix">DIS</sup></span> Family`;
      }
      if (match === "SLAM DIS FAMILY") {
        return `<span class="product-name">SLAM<sup class="product-suffix">DIS</sup></span> Family`;
      }
      if (match === "SLAM.SYSTEMS COR") {
        return `<span class="product-name">SLAM.SYSTEMS<sup class="product-suffix">COR</sup></span>`;
      }
      if (match === "SLAM COR") {
        return `<span class="product-name">SLAM.SYSTEMS<sup class="product-suffix">COR</sup></span>`;
      }
      if (match === "SLAM.SYSTEMS DIS") {
        return `<span class="product-name">SLAM.SYSTEMS<sup class="product-suffix">DIS</sup></span>`;
      }
      if (match === "SLAM DIS") {
        return `<span class="product-name">SLAM<sup class="product-suffix">DIS</sup></span>`;
      }
      return `<span class="product-name">SLAM.SYSTEMS</span>`;
    };

    const disProductMarkup = (match, simpleProduct, output) => {
      if (simpleProduct) {
        return `<span class="product-name">SLAM ${simpleProduct}<sup class="product-suffix">DIS</sup></span>`;
      }
      if (output) {
        return `<span class="product-name">SLAM CORPORATE<sup class="product-suffix">DIS</sup> ${output}</span>`;
      }
      return `<span class="product-name">SLAM MODULES<sup class="product-suffix">DIS</sup></span>`;
    };

    if (mediaContent) {
      const walker = document.createTreeWalker(mediaContent, NodeFilter.SHOW_TEXT);
      const textNodes = [];
      while (walker.nextNode()) {
        const node = walker.currentNode;
        if (!node.parentElement?.closest(excluded) && /SLAM|Corporate(?:TV|AUDIO|TXT)/.test(node.nodeValue || "")) {
          textNodes.push(node);
        }
      }

      textNodes.forEach((node) => {
        const source = node.nodeValue || "";
        const withCorProducts = source.replace(corProductPattern, (match, product) => nameMarkup(match, product));
        const withProducts = withCorProducts.replace(disProductPattern, disProductMarkup);
        const withFamilies = withProducts.replace(familyPattern, (match) => nameMarkup(match));
        if (withFamilies !== source) {
          const fragment = document.createRange().createContextualFragment(withFamilies);
          node.replaceWith(fragment);
        }
      });
    }
  }

  if (currentFile === "led-video-systems.html") {
    const ledContent = document.querySelector("main");
    const ledNames = [];

    if (ledContent) {
      const walker = document.createTreeWalker(ledContent, NodeFilter.SHOW_TEXT);
      const textNodes = [];
      while (walker.nextNode()) {
        const node = walker.currentNode;
        if (!node.parentElement?.closest(".product-name, .product-claim, .status, .content-code") &&
            /NEMEZES|GENEZES|ARAMIZ|TSCHILIN|ZENARIO|POIZEN|CINEMAZ/.test(node.nodeValue || "")) {
          textNodes.push(node);
        }
      }

      textNodes.forEach((node) => {
        const source = node.nodeValue || "";
        let withNames = source;
        ledNames.forEach(([pattern, markup]) => {
          withNames = withNames.replace(pattern, `<span class="product-name">${markup}</span>`);
        });
        if (withNames !== source) {
          const fragment = document.createRange().createContextualFragment(withNames);
          node.replaceWith(fragment);
        }
      });
    }

    document.querySelectorAll("#genezes .status, #aramiz-625 .status").forEach((status) => {
      status.textContent = "SPORT CERTIFIED";
    });

    const alezenSectionLink = document.querySelector('.section-nav a[href="#aramiz-625"]');
    if (alezenSectionLink) alezenSectionLink.textContent = "ALEZEN";
  }

  if (currentFile === "company.html") {
    const historyParagraph = Array.from(document.querySelectorAll("#company .content-copy p"))
      .find((paragraph) => paragraph.textContent.includes("Die Geschichte begann bereits 1999"));
    if (historyParagraph) {
      historyParagraph.innerHTML = historyParagraph.innerHTML
        .replace("CorporateTV", '<span class="product-name">SLAM CORPORATE<sup class="product-suffix">DIS</sup> TV</span>')
        .replace("CorporateAUDIO", '<span class="product-name">SLAM CORPORATE<sup class="product-suffix">DIS</sup> AUDIO</span>')
        .replace("CorporateTXT", '<span class="product-name">SLAM CORPORATE<sup class="product-suffix">DIS</sup> TXT</span>');
    }
  }

  if (currentFile !== "media-playout.html") {
    const pageContent = document.querySelector("main");
    const excluded = "h1, h2, h3, h4, h5, h6, nav, summary, .product-name, .product-claim, .status, .content-code";
    const slamNamePattern = /SLAM\.SYSTEMS|SLAM\.CLOUD|SLAM (CENTRO|NERV|AXESS)|Corporate(?:TV|AUDIO|TXT)/g;

    if (pageContent) {
      const walker = document.createTreeWalker(pageContent, NodeFilter.SHOW_TEXT);
      const textNodes = [];
      while (walker.nextNode()) {
        const node = walker.currentNode;
        if (!node.parentElement?.closest(excluded) && /SLAM|Corporate(?:TV|AUDIO|TXT)/.test(node.nodeValue || "")) {
          textNodes.push(node);
        }
      }

      textNodes.forEach((node) => {
        const source = node.nodeValue || "";
        const withNames = source.replace(slamNamePattern, (match) =>
          `<span class="product-name">${match}</span>`
        );
        if (withNames !== source) {
          const fragment = document.createRange().createContextualFragment(withNames);
          node.replaceWith(fragment);
        }
      });
    }
  }
})();
