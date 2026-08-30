/* SLAM.SYSTEMS – Dealer Hero v1.13
   悬停：人物把牌"拿给你"（飞牌动画）；点击：高清大图 Lightbox */
(function () {
  "use strict";

  var IMG = "assets/images/sportdeck/";
  var SPORTS = {
    handball: {
      label: "Handball",
      ui: IMG + "ui-handball.jpg",
      hd: IMG + "ui-handball-hd.jpg",
      scene: IMG + "scene-handball.jpg",
      caption: '<span class="solution-brand-term">SCORECOR</span> Game-Time: Anzeige, Strafzeiten und Time-outs – ein Tippen genügt.'
    },
    hockey: {
      label: "Eishockey",
      ui: IMG + "ui-hockey.jpg",
      hd: IMG + "ui-hockey-hd.jpg",
      scene: IMG + "scene-hockey.jpg",
      caption: '<span class="solution-brand-term">SCORECOR</span> Icehockey Pro: Score, Penalties und Shots on Goal – live am iPad.'
    },
    football: {
      label: "Fussball",
      ui: IMG + "ui-football.jpg",
      hd: IMG + "ui-football-hd.jpg",
      scene: IMG + "scene-football.jpg",
      caption: '<span class="solution-brand-term">DECKCOR</span> Perimeter: erste und zweite Bandenreihe plus Faszia aus einem Deck.'
    },
    unihockey: {
      label: "Unihockey",
      ui: IMG + "ui-unihockey.jpg",
      hd: IMG + "ui-unihockey-hd.jpg",
      scene: IMG + "scene-unihockey.jpg",
      caption: '<span class="solution-brand-term">SCORECOR</span> Unihockey: Spielzeit, Score und Penalties – klar geführt.'
    }
  };

  var root = document.querySelector("[data-dealer]");
  if (!root) return;

  var stage = root.querySelector(".dealer-stage");
  var handCard = root.querySelector(".dealer-handcard");
  var handImg = handCard.querySelector("img");
  var handSport = root.querySelector(".dealer-handcard-sport");
  var caption = root.querySelector(".dealer-caption");
  var deckCards = Array.prototype.slice.call(root.querySelectorAll(".dealer-card"));
  var sceneImgs = Array.prototype.slice.call(root.querySelectorAll(".dealer-bg img"));
  var lightbox = root.querySelector(".dealer-lightbox");
  var lightboxImg = lightbox.querySelector("img");
  var lightboxCap = lightbox.querySelector("figcaption");
  var lightboxClose = lightbox.querySelector(".dealer-lightbox-close");

  var locked = "handball";   // 点击锁定的球类
  var previewing = null;     // 悬停预览中的球类
  var flying = false;

  function current() { return previewing || locked; }

  function applySport(key, withPop) {
    var s = SPORTS[key];
    if (!s) return;
    if (handImg.getAttribute("src") !== s.ui) {
      handImg.src = s.ui;
      handImg.alt = s.label + " Playout";
      if (withPop) {
        handCard.classList.remove("is-pop");
        void handCard.offsetWidth;
        handCard.classList.add("is-pop");
      }
    }
    handSport.textContent = s.label;
    sceneImgs.forEach(function (img) {
      img.classList.toggle("is-active", img.getAttribute("data-sport") === key);
    });
    caption.classList.add("is-switching");
    window.setTimeout(function () {
      caption.innerHTML = s.caption;
      caption.classList.remove("is-switching");
    }, 160);
  }

  /* 飞牌：从牌组卡片克隆一张，飞到手心位置 */
  function flyToHand(fromEl, key) {
    if (flying) return;
    var s = SPORTS[key];
    var from = fromEl.getBoundingClientRect();
    var to = handCard.getBoundingClientRect();
    if (!from.width || !to.width) { applySport(key, true); return; }

    flying = true;
    var ghost = document.createElement("div");
    ghost.className = "dealer-fly";
    ghost.style.left = from.left + "px";
    ghost.style.top = from.top + "px";
    ghost.style.width = from.width + "px";
    ghost.style.height = from.height + "px";
    ghost.innerHTML = '<img src="' + s.ui + '" alt="">';
    document.body.appendChild(ghost);

    stage.classList.add("is-dealing");

    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        var dx = (to.left + to.width / 2) - (from.left + from.width / 2);
        var dy = (to.top + to.height / 2) - (from.top + from.height / 2);
        var scale = to.width / from.width;
        ghost.style.transform =
          "translate(" + dx + "px," + dy + "px) rotate(-3.5deg) scale(" + scale + ")";
      });
    });

    window.setTimeout(function () {
      applySport(key, true);
      ghost.style.opacity = "0";
    }, 560);
    window.setTimeout(function () {
      ghost.remove();
      stage.classList.remove("is-dealing");
      flying = false;
    }, 700);
  }

  function openLightbox(key) {
    var s = SPORTS[key];
    lightboxImg.src = s.hd;
    lightboxImg.alt = s.label + " Playout – Grossansicht";
    lightboxCap.textContent = s.label + " / COR Family";
    lightbox.classList.add("is-open");
    document.body.style.overflow = "hidden";
  }
  function closeLightbox() {
    lightbox.classList.remove("is-open");
    document.body.style.overflow = "";
  }

  deckCards.forEach(function (card) {
    var key = card.getAttribute("data-sport");

    card.addEventListener("mouseenter", function () {
      previewing = key;
      if (key !== current || handImg.getAttribute("src") !== SPORTS[key].ui) {
        flyToHand(card, key);
      }
    });
    card.addEventListener("focus", function () {
      previewing = key;
      flyToHand(card, key);
    });
    card.addEventListener("click", function () {
      locked = key;
      previewing = null;
      deckCards.forEach(function (c) { c.classList.toggle("is-locked", c === card); });
      applySport(key, true);
      openLightbox(key);
    });
  });

  var deck = root.querySelector(".dealer-deck");
  deck.addEventListener("mouseleave", function () {
    previewing = null;
    if (locked) applySport(locked, true);
  });

  handCard.addEventListener("click", function () { openLightbox(current()); });

  lightboxClose.addEventListener("click", closeLightbox);
  lightbox.addEventListener("click", function (e) {
    if (e.target === lightbox) closeLightbox();
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && lightbox.classList.contains("is-open")) closeLightbox();
  });

  /* 初始状态 */
  deckCards.forEach(function (c) {
    c.classList.toggle("is-locked", c.getAttribute("data-sport") === locked);
  });
  applySport(locked, false);

  /* 预加载高清图，点开无等待 */
  Object.keys(SPORTS).forEach(function (k) {
    var im = new Image();
    im.src = SPORTS[k].hd;
  });
})();
