import * as THREE from "./vendor/three.module.min.js";

(function () {
  "use strict";

  var root = document.querySelector("[data-sportdeck3d]");
  if (!root) {
    return;
  }

  var canvas = root.querySelector(".hero3d-canvas");
  var loadingEl = root.querySelector(".hero3d-loading");
  var captionSport = root.querySelector(".hero3d-caption-sport");
  var captionLine = root.querySelector(".hero3d-caption-line");
  var backdropImgs = Array.prototype.slice.call(
    root.querySelectorAll(".hero3d-backdrops img")
  );

  var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var SPORTS = [
    {
      key: "handball",
      label: "Handball",
      tex: "assets/images/sportdeck/ui-handball.jpg",
      caption:
        '<span class="solution-brand-term">SCORECOR</span> Game-Time: Anzeige, Strafzeiten und Time-outs – ein Tippen genügt.'
    },
    {
      key: "hockey",
      label: "Eishockey",
      tex: "assets/images/sportdeck/ui-hockey.jpg",
      caption:
        '<span class="solution-brand-term">SCORECOR</span> Icehockey Pro: Score, Penalties und Shots on Goal – live am iPad.'
    },
    {
      key: "football",
      label: "Fussball",
      tex: "assets/images/sportdeck/ui-football.jpg",
      caption:
        '<span class="solution-brand-term">DECKCOR</span> Perimeter: erste und zweite Bandenreihe plus Faszia aus einem Deck.'
    },
    {
      key: "unihockey",
      label: "Unihockey",
      tex: "assets/images/sportdeck/ui-unihockey.jpg",
      caption:
        '<span class="solution-brand-term">SCORECOR</span> Fixtures: Runde wählen, Paarung laden, senden – in Sekunden.'
    }
  ];

  /* --- Renderer / Scene ------------------------------------------ */

  var renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    alpha: true,
    antialias: true
  });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));

  var scene = new THREE.Scene();
  var camera = new THREE.PerspectiveCamera(38, 1, 0.1, 60);
  camera.position.set(0, 0.35, 8);

  /* --- Device factory --------------------------------------------- */

  var DEVICE_W = 2.02;
  var DEVICE_H = 1.3;
  var SCREEN_INSET = 0.085;

  function makeLabelTexture(text) {
    var c = document.createElement("canvas");
    c.width = 512;
    c.height = 96;
    var ctx = c.getContext("2d");
    ctx.clearRect(0, 0, c.width, c.height);
    ctx.fillStyle = "rgba(247,247,245,0.92)";
    ctx.font = "500 40px 'Avenir Next', 'Helvetica Neue', Arial, sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    try { ctx.letterSpacing = "16px"; } catch (e) {}
    ctx.fillText(text.toUpperCase(), c.width / 2, c.height / 2 + 2);
    var tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    tex.anisotropy = 4;
    return tex;
  }

  function makeDevice(sport, screenTex) {
    var group = new THREE.Group();

    var bezel = new THREE.Mesh(
      new THREE.PlaneGeometry(DEVICE_W, DEVICE_H),
      new THREE.MeshBasicMaterial({ color: 0x101013 })
    );
    group.add(bezel);

    var screen = new THREE.Mesh(
      new THREE.PlaneGeometry(
        DEVICE_W - SCREEN_INSET * 2,
        DEVICE_H - SCREEN_INSET * 2
      ),
      new THREE.MeshBasicMaterial({ map: screenTex })
    );
    screen.position.z = 0.012;
    group.add(screen);

    var glow = new THREE.Mesh(
      new THREE.PlaneGeometry(DEVICE_W * 1.07, DEVICE_H * 1.09),
      new THREE.MeshBasicMaterial({
        color: 0xff004e,
        transparent: true,
        opacity: 0,
        blending: THREE.AdditiveBlending,
        depthWrite: false
      })
    );
    glow.position.z = -0.012;
    group.add(glow);

    var labelTex = makeLabelTexture(sport.label);
    var label = new THREE.Sprite(
      new THREE.SpriteMaterial({
        map: labelTex,
        transparent: true,
        opacity: 0.55,
        depthWrite: false
      })
    );
    label.scale.set(1.55, 0.29, 1);
    label.position.set(0, -(DEVICE_H / 2) - 0.32, 0.02);
    group.add(label);

    group.userData = {
      sport: sport.key,
      screen: screen,
      bezel: bezel,
      glow: glow,
      label: label,
      phase: Math.random() * Math.PI * 2
    };
    return group;
  }

  /* --- Layout ------------------------------------------------------ */

  var devices = [];
  var fanSlots = [-1.5, -0.5, 0.5, 1.5];

  function layout() {
    var w = root.clientWidth;
    var h = root.clientHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();

    var dist = camera.position.z;
    var visibleH = 2 * Math.tan(THREE.MathUtils.degToRad(camera.fov / 2)) * dist;
    var visibleW = visibleH * camera.aspect;

    var compact = camera.aspect < 1;
    var spread = Math.min(visibleW * (compact ? 0.19 : 0.21), compact ? 1.35 : 2.35);
    var baseY = compact ? -visibleH * 0.16 : -visibleH * 0.22;
    var baseScale = compact ? Math.min(visibleW * 0.34 / DEVICE_W, 0.62) : Math.min(visibleW * 0.17 / DEVICE_W, 1.0);

    devices.forEach(function (device, i) {
      var u = device.userData;
      u.slot = fanSlots[i];
      u.baseX = fanSlots[i] * spread;
      u.baseY = baseY + (1 - Math.abs(fanSlots[i]) / 1.5) * (compact ? 0.12 : 0.28);
      u.baseZ = -Math.abs(fanSlots[i]) * 0.35;
      u.baseRotY = -fanSlots[i] * 0.16;
      u.baseRotZ = fanSlots[i] * 0.055;
      u.baseScale = baseScale;
      if (!u.initialized) {
        device.position.set(u.baseX, u.baseY, u.baseZ);
        device.rotation.set(0, u.baseRotY, u.baseRotZ);
        device.scale.setScalar(u.baseScale);
        u.initialized = true;
      }
    });
  }

  /* --- State / captions -------------------------------------------- */

  var lockedKey = "handball";
  var hoverKey = null;

  function currentKey() {
    return hoverKey || lockedKey;
  }

  function applySelection(key, lock) {
    if (lock) {
      lockedKey = key;
    }
    backdropImgs.forEach(function (img) {
      img.classList.toggle("is-active", img.getAttribute("data-sport") === key);
    });
    var sport = SPORTS.filter(function (s) { return s.key === key; })[0];
    if (sport && captionSport && captionLine) {
      captionSport.textContent = sport.label;
      captionLine.classList.add("is-fading");
      window.setTimeout(function () {
        captionLine.innerHTML = sport.caption;
        captionLine.classList.remove("is-fading");
      }, 180);
    }
  }

  /* --- Pointer interaction ------------------------------------------ */

  var raycaster = new THREE.Raycaster();
  var pointerNdc = new THREE.Vector2(-10, -10);
  var parallax = { x: 0, y: 0 };

  function updatePointer(event) {
    var rect = canvas.getBoundingClientRect();
    var x = (event.clientX - rect.left) / rect.width;
    var y = (event.clientY - rect.top) / rect.height;
    pointerNdc.set(x * 2 - 1, -(y * 2 - 1));
    parallax.x = x * 2 - 1;
    parallax.y = y * 2 - 1;
  }

  canvas.addEventListener("pointermove", function (event) {
    updatePointer(event);
  });

  canvas.addEventListener("pointerdown", function (event) {
    updatePointer(event);
    if (hoverKey) {
      applySelection(hoverKey, true);
    }
  });

  canvas.addEventListener("pointerleave", function () {
    pointerNdc.set(-10, -10);
    parallax.x = 0;
    parallax.y = 0;
    hoverKey = null;
    applySelection(lockedKey, false);
  });

  /* --- Load textures, then start ------------------------------------ */

  var manager = new THREE.LoadingManager(function () {
    if (loadingEl) {
      loadingEl.classList.add("is-done");
    }
    layout();
    applySelection(lockedKey, true);
    renderer.setAnimationLoop(tick);
  });

  var loader = new THREE.TextureLoader(manager);

  SPORTS.forEach(function (sport) {
    var tex = loader.load(sport.tex);
    tex.colorSpace = THREE.SRGBColorSpace;
    tex.anisotropy = Math.min(8, renderer.capabilities.getMaxAnisotropy());
    var device = makeDevice(sport, tex);
    devices.push(device);
    scene.add(device);
  });

  /* --- Frame loop ---------------------------------------------------- */

  var clock = new THREE.Clock();

  function tick() {
    var t = clock.getElapsedTime();

    /* raycast hover */
    raycaster.setFromCamera(pointerNdc, camera);
    var hits = raycaster.intersectObjects(devices, true);
    var hitKey = null;
    if (hits.length) {
      var obj = hits[0].object;
      while (obj && !obj.userData.sport) {
        obj = obj.parent;
      }
      if (obj) {
        hitKey = obj.userData.sport;
      }
    }
    if (hitKey !== hoverKey) {
      hoverKey = hitKey;
      canvas.style.cursor = hitKey ? "pointer" : "default";
      applySelection(currentKey(), false);
    }

    var active = currentKey();

    devices.forEach(function (device) {
      var u = device.userData;
      var isActive = u.sport === active;
      var isHovered = u.sport === hoverKey;

      var targetZ = u.baseZ + (isActive ? 1.7 : 0);
      var targetY = u.baseY + (isActive ? 0.34 : 0);
      var targetX = isActive ? u.baseX * 0.62 : u.baseX;
      var targetRotY = isActive ? 0 : u.baseRotY;
      var targetRotZ = isActive ? 0 : u.baseRotZ;
      var targetScale = u.baseScale * (isActive ? 1.22 : 1);

      if (!reducedMotion && !isActive) {
        targetY += Math.sin(t * 1.1 + u.phase) * 0.05;
        targetRotZ += Math.sin(t * 0.7 + u.phase) * 0.012;
      }

      var k = isHovered || isActive ? 0.11 : 0.075;
      device.position.x += (targetX - device.position.x) * 0.08;
      device.position.y += (targetY - device.position.y) * k;
      device.position.z += (targetZ - device.position.z) * k;
      device.rotation.y += (targetRotY - device.rotation.y) * k;
      device.rotation.z += (targetRotZ - device.rotation.z) * k;
      var s = device.scale.x + (targetScale - device.scale.x) * k;
      device.scale.setScalar(s);

      var dim = isActive ? 1 : hoverKey ? 0.32 : 0.62;
      u.screen.material.color.lerp(new THREE.Color(dim, dim, dim), 0.12);
      u.glow.material.opacity += ((isActive ? 0.5 : 0) - u.glow.material.opacity) * 0.1;
      u.label.material.opacity += ((isActive ? 1 : hoverKey ? 0.25 : 0.55) - u.label.material.opacity) * 0.12;
    });

    if (!reducedMotion) {
      camera.position.x += (parallax.x * 0.55 - camera.position.x) * 0.045;
      camera.position.y += (0.35 - parallax.y * 0.3 - camera.position.y) * 0.045;
      camera.lookAt(0, -0.35, 0);
    }

    renderer.render(scene, camera);
  }

  window.addEventListener("resize", layout);
  layout();
})();
