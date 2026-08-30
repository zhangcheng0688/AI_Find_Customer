(function () {
  "use strict";

  var root = document.querySelector("[data-sportscene]");
  if (!root) {
    return;
  }

  var SPORTS = {
    handball: {
      label: "Handball",
      ui: "assets/images/sportdeck/ui-handball.jpg",
      caption:
        '<span class="solution-brand-term">SCORECOR</span> Game-Time: Anzeige, Strafzeiten und Time-outs – ein Tippen genügt.'
    },
    hockey: {
      label: "Eishockey",
      ui: "assets/images/sportdeck/ui-hockey.jpg",
      caption:
        '<span class="solution-brand-term">SCORECOR</span> Icehockey Pro: Score, Penalties und Shots on Goal – live am iPad.'
    },
    football: {
      label: "Fussball",
      ui: "assets/images/sportdeck/ui-football.jpg",
      caption:
        '<span class="solution-brand-term">DECKCOR</span> Perimeter: erste und zweite Bandenreihe plus Faszia aus einem Deck.'
    },
    unihockey: {
      label: "Unihockey",
      ui: "assets/images/sportdeck/ui-unihockey.jpg",
      caption:
        '<span class="solution-brand-term">SCORECOR</span> Fixtures: Runde wählen, Paarung laden, senden – in Sekunden.'
    }
  };

  var stageImgs = Array.prototype.slice.call(root.querySelectorAll(".heroscene-stage img"));
  var chips = Array.prototype.slice.call(root.querySelectorAll(".heroscene-chip"));
  var uiPanel = root.querySelector(".heroscene-ui");
  var uiImg = root.querySelector(".heroscene-ui-frame img");
  var uiSport = root.querySelector(".heroscene-ui-sport");
  var captionLine = root.querySelector(".heroscene-caption-line");

  var lockedKey = "handball";
  var switchTimer = null;

  function show(key, lock) {
    if (!SPORTS[key]) {
      return;
    }
    if (lock) {
      lockedKey = key;
    }
    stageImgs.forEach(function (img) {
      img.classList.toggle("is-active", img.getAttribute("data-sport") === key);
    });
    chips.forEach(function (chip) {
      chip.classList.toggle("is-active", chip.getAttribute("data-sport") === key);
    });

    if (uiPanel && uiImg) {
      window.clearTimeout(switchTimer);
      uiPanel.classList.add("is-switching");
      switchTimer = window.setTimeout(function () {
        uiImg.src = SPORTS[key].ui;
        uiImg.alt = SPORTS[key].label + " Playout";
        if (uiSport) {
          uiSport.textContent = SPORTS[key].label;
        }
        uiPanel.classList.remove("is-switching");
      }, 240);
    }

    if (captionLine) {
      captionLine.classList.add("is-fading");
      window.setTimeout(function () {
        captionLine.innerHTML = SPORTS[key].caption;
        captionLine.classList.remove("is-fading");
      }, 180);
    }
  }

  chips.forEach(function (chip) {
    var key = chip.getAttribute("data-sport");
    chip.addEventListener("pointerenter", function () { show(key, false); });
    chip.addEventListener("focus", function () { show(key, false); });
    chip.addEventListener("click", function () { show(key, true); });
  });

  var nav = root.querySelector(".heroscene-nav");
  if (nav) {
    nav.addEventListener("pointerleave", function () {
      show(lockedKey, false);
    });
  }

  show(lockedKey, true);
})();
