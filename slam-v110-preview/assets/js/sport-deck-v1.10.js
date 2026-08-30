(function () {
  "use strict";

  var deck = document.querySelector("[data-sportdeck]");
  if (!deck) {
    return;
  }

  var captions = {
    handball:
      '<span class="solution-brand-term">SCORECOR</span> Game-Time: Anzeige, Strafzeiten und Time-outs – ein Tippen genügt.',
    hockey:
      '<span class="solution-brand-term">SCORECOR</span> Icehockey Pro: Score, Penalties und Shots on Goal – live am iPad.',
    football:
      '<span class="solution-brand-term">DECKCOR</span> Perimeter: erste und zweite Bandenreihe plus Faszia aus einem Deck.',
    unihockey:
      '<span class="solution-brand-term">SCORECOR</span> Fixtures: Runde wählen, Paarung laden, senden – in Sekunden.'
  };

  var cards = Array.prototype.slice.call(deck.querySelectorAll(".sportdeck-card"));
  var backdrops = Array.prototype.slice.call(deck.querySelectorAll(".sportdeck-backdrops img"));
  var captionSport = deck.querySelector(".sportdeck-caption-sport");
  var captionLine = deck.querySelector(".sportdeck-caption-line");
  var fan = deck.querySelector(".sportdeck-fan");

  var lockedSport = "handball";

  function labels(sport) {
    var card = cards.filter(function (c) { return c.getAttribute("data-sport") === sport; })[0];
    return card ? card.querySelector(".sportdeck-label").textContent : sport;
  }

  function show(sport, lock) {
    if (lock) {
      lockedSport = sport;
    }
    backdrops.forEach(function (img) {
      img.classList.toggle("is-active", img.getAttribute("data-sport") === sport);
    });
    cards.forEach(function (card) {
      var active = card.getAttribute("data-sport") === lockedSport;
      card.classList.toggle("is-active", active);
      card.setAttribute("aria-selected", active ? "true" : "false");
    });
    if (captionSport && captionLine) {
      captionSport.textContent = labels(sport);
      captionLine.classList.add("is-fading");
      window.setTimeout(function () {
        captionLine.innerHTML = captions[sport] || "";
        captionLine.classList.remove("is-fading");
      }, 180);
    }
  }

  cards.forEach(function (card, index) {
    var sport = card.getAttribute("data-sport");

    card.addEventListener("pointerenter", function () {
      show(sport, false);
    });
    card.addEventListener("focus", function () {
      show(sport, false);
    });
    card.addEventListener("click", function () {
      show(sport, true);
    });
    card.addEventListener("keydown", function (event) {
      if (event.key !== "ArrowRight" && event.key !== "ArrowLeft") {
        return;
      }
      event.preventDefault();
      var delta = event.key === "ArrowRight" ? 1 : -1;
      var next = cards[(index + delta + cards.length) % cards.length];
      next.focus();
    });
  });

  if (fan) {
    fan.addEventListener("pointerleave", function () {
      show(lockedSport, false);
    });
  }

  show(lockedSport, true);
})();
