(function () {
  "use strict";

  var HEROES = [
    {
      num: "01",
      sport: "Handball",
      copy: "From preparation to performance — intelligent communication systems for live environments."
    },
    {
      num: "02",
      sport: "Ice Hockey",
      copy: "From preparation to performance — intelligent communication systems for live environments."
    },
    {
      num: "03",
      sport: "Football",
      copy: "From preparation to performance — intelligent communication systems for live environments."
    }
  ];

  function showHero(idx) {
    idx = (idx + HEROES.length) % HEROES.length;
    window.__slamHeroIndex = idx;
    var slides = document.querySelectorAll("[data-hero-slide]");
    for (var s = 0; s < slides.length; s++) {
      slides[s].classList.toggle("on", s === idx);
    }
    var hero = HEROES[idx];
    var eyebrow = document.querySelector("[data-hero-eyebrow]");
    if (eyebrow) {
      eyebrow.innerHTML = "<span>" + hero.num + "</span> " + hero.sport + " systems";
    }
    var copy = document.querySelector("[data-hero-copy]");
    if (copy) copy.textContent = hero.copy;
    var foot = document.querySelector("[data-hero-sport]");
    if (foot) foot.textContent = hero.sport + " / " + hero.num;
    var dots = document.querySelectorAll("[data-hero-btn]");
    for (var i = 0; i < dots.length; i++) {
      dots[i].classList.toggle("on", i === idx);
      dots[i].setAttribute("aria-selected", i === idx ? "true" : "false");
    }
  }

  function initHero() {
    if (!document.querySelector(".hero-shell")) return;
    var slides = document.querySelectorAll("[data-hero-slide]");
    for (var i = 0; i < slides.length; i++) {
      if (slides[i].decode) slides[i].decode().catch(function () {});
    }
    showHero(0);
    var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var timer = null;
    function start() {
      if (reduced || timer) return;
      timer = setInterval(function () {
        showHero(window.__slamHeroIndex + 1);
      }, 7000);
    }
    function stop() {
      if (timer) {
        clearInterval(timer);
        timer = null;
      }
    }
    document.querySelectorAll("[data-hero-btn]").forEach(function (button) {
      button.addEventListener("click", function () {
        showHero(parseInt(button.getAttribute("data-hero-btn"), 10));
        stop();
      });
    });
    var shell = document.querySelector(".hero-shell");
    if (shell) {
      shell.addEventListener("mouseenter", stop);
      shell.addEventListener("mouseleave", start);
    }
    start();
  }

  function initVideo() {
    var video = document.querySelector(".live-video");
    document.querySelectorAll(".video-trigger").forEach(function (button) {
      button.addEventListener("click", function () {
        if (!video) return;
        video.scrollIntoView({ behavior: "smooth", block: "center" });
        var play = video.play();
        if (play && play.catch) play.catch(function () {});
      });
    });
  }

  function init() {
    initHero();
    initVideo();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
