/* SLAM.SYSTEMS — hero sport switch, i18n, nav */
(function () {
  "use strict";
  var LANGS = ["en", "de", "ja", "ko", "es", "fr"];
  var HEROES = [
    {
      id: "handball",
      num: "01",
      image: "assets/images/handball-hero-master-v1-scoreboard-correct.png",
      alt: "SLAM.SYSTEMS operator at a live handball match"
    },
    {
      id: "icehockey",
      num: "02",
      image: "assets/images/icehockey-hero-master-v1.png",
      alt: "SLAM.SYSTEMS operator at a live ice hockey match"
    },
    {
      id: "football",
      num: "03",
      image: "assets/images/football-hero-master-v1.png",
      alt: "SLAM.SYSTEMS operator at a live football match"
    }
  ];

  function getLang() {
    var l = null;
    try { l = localStorage.getItem("slam-lang"); } catch (e) {}
    return LANGS.indexOf(l) >= 0 ? l : "en";
  }

  function t(lang, key) {
    var dict = (window.SLAM_I18N && window.SLAM_I18N[lang]) || {};
    var en = (window.SLAM_I18N && window.SLAM_I18N.en) || {};
    return dict[key] != null ? dict[key] : (en[key] != null ? en[key] : null);
  }

  function apply(lang) {
    var nodes = document.querySelectorAll("[data-i18n]");
    for (var i = 0; i < nodes.length; i++) {
      var v = t(lang, nodes[i].getAttribute("data-i18n"));
      if (v != null) nodes[i].textContent = v;
    }
    var htmls = document.querySelectorAll("[data-i18n-html]");
    for (var h = 0; h < htmls.length; h++) {
      var hv = t(lang, htmls[h].getAttribute("data-i18n-html"));
      if (hv != null) htmls[h].innerHTML = hv;
    }
    document.documentElement.setAttribute("lang", lang);
    var title = t(lang, document.documentElement.getAttribute("data-i18n-title") || "");
    if (title) document.title = title;
    var md = document.querySelector('meta[name="description"]');
    var desc = t(lang, document.documentElement.getAttribute("data-i18n-desc") || "");
    if (md && desc) md.setAttribute("content", desc);
    var btns = document.querySelectorAll("[data-lang-btn]");
    for (var j = 0; j < btns.length; j++) {
      var on = btns[j].getAttribute("data-lang-btn") === lang;
      btns[j].classList.toggle("active", on);
      btns[j].setAttribute("aria-pressed", on ? "true" : "false");
    }
    try { localStorage.setItem("slam-lang", lang); } catch (e) {}
    if (window.__slamHeroIndex != null) labelHero(window.__slamHeroIndex, lang);
  }

  function labelHero(idx, lang) {
    lang = lang || getLang();
    var h = HEROES[idx];
    var sport = t(lang, "hero.sport." + h.id) || h.id;
    var systems = t(lang, "hero.kicker.systems") || "systems";
    var eyebrow = document.querySelector("[data-hero-eyebrow]");
    if (eyebrow) {
      eyebrow.innerHTML = "<span>" + h.num + "</span> " + sport + " " + systems;
    }
    var copy = document.querySelector("[data-hero-copy]");
    if (copy) {
      var c = t(lang, "hero.copy." + h.id);
      if (c) copy.textContent = c;
    }
    var foot = document.querySelector("[data-hero-sport]");
    if (foot) foot.textContent = sport + " / " + h.num;
  }

  function showHero(idx) {
    idx = (idx + HEROES.length) % HEROES.length;
    window.__slamHeroIndex = idx;
    var slides = document.querySelectorAll("[data-hero-slide]");
    for (var s = 0; s < slides.length; s++) {
      slides[s].classList.toggle("on", s === idx);
    }
    labelHero(idx, getLang());
    var dots = document.querySelectorAll("[data-hero-btn]");
    for (var i = 0; i < dots.length; i++) {
      dots[i].classList.toggle("on", i === idx);
      dots[i].setAttribute("aria-selected", i === idx ? "true" : "false");
    }
  }

  function initHero() {
    if (!document.querySelector(".hero-shell")) return;
    window.__slamHeroIndex = 0;
    var slides = document.querySelectorAll("[data-hero-slide]");
    for (var i = 0; i < slides.length; i++) {
      if (slides[i].decode) slides[i].decode().catch(function () {});
    }
    showHero(0);
    var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var timer = null;
    function start() {
      if (reduced || timer) return;
      timer = setInterval(function () { showHero(window.__slamHeroIndex + 1); }, 7000);
    }
    function stop() { if (timer) { clearInterval(timer); timer = null; } }
    document.querySelectorAll("[data-hero-btn]").forEach(function (b) {
      b.addEventListener("click", function () {
        showHero(parseInt(b.getAttribute("data-hero-btn"), 10));
        stop();
        start();
      });
    });
    var shell = document.querySelector(".hero-shell");
    if (shell) {
      shell.addEventListener("mouseenter", stop);
      shell.addEventListener("mouseleave", start);
    }
    start();
  }

  function initForm() {
    var f = document.querySelector("[data-mailto-form]");
    if (!f) return;
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var name = (f.querySelector("[name=name]") || {}).value || "";
      var org = (f.querySelector("[name=company]") || {}).value || "";
      var email = (f.querySelector("[name=email]") || {}).value || "";
      var phone = (f.querySelector("[name=phone]") || {}).value || "";
      var msg = (f.querySelector("[name=message]") || {}).value || "";
      var body = "Name: " + name + "\nCompany: " + org + "\nE-Mail: " + email + "\nPhone: " + phone + "\n\n" + msg + "\n";
      window.location.href = "mailto:i@slam.systems"
        + "?subject=" + encodeURIComponent("Anfrage betreffend SLAM.SYSTEMS MEDIA SOLUTION")
        + "&body=" + encodeURIComponent(body);
    });
  }

  document.addEventListener("click", function (e) {
    var b = e.target.closest ? e.target.closest("[data-lang-btn]") : null;
    if (b) apply(b.getAttribute("data-lang-btn"));
  });

  function init() {
    initHero();
    initForm();
    apply(getLang());
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
