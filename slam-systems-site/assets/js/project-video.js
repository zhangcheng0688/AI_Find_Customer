(() => {
  'use strict';
  const source = new URL('../video/slam-score-handball-intro.mp4', document.currentScript.src).href;
  const english = document.documentElement.lang !== 'de';
  let active = false;
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href]');
    if (!link || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || link.target === '_blank' || link.closest('.language-switch')) return;
    const target = new URL(link.href, location.href);
    if (target.origin !== location.origin || !target.pathname.endsWith('/start-project.html')) return;
    event.preventDefault();
    if (active) return;
    active = true;
    target.pathname = target.pathname.replace(/start-project\.html$/, 'direct-contact.html');
    target.hash = 'direct-contact';
    const dialog = document.createElement('dialog');
    dialog.className = 'project-video-overlay';
    dialog.setAttribute('aria-label', english ? 'Start Your Project — Video' : 'Start Your Project — Video');
    const video = document.createElement('video');
    video.src = source;
    video.controls = true;
    video.playsInline = true;
    video.preload = 'auto';
    video.setAttribute('aria-label', english ? 'SLAM SCORE handball introduction' : 'SLAM SCORE Handball Einführung');
    const skip = document.createElement('button');
    skip.type = 'button';
    skip.className = 'project-video-skip';
    skip.textContent = english ? 'Skip to contact →' : 'Direkt zum Kontakt →';
    const message = document.createElement('p');
    message.className = 'project-video-message';
    message.setAttribute('role', 'status');
    message.hidden = true;
    let finishing = false;
    const finish = async () => {
      if (finishing) return;
      finishing = true;
      video.pause();
      if (document.fullscreenElement === dialog) {
        try { await document.exitFullscreen(); } catch (_) { /* Continue to contact. */ }
      }
      dialog.close();
      dialog.remove();
      active = false;
      location.assign(target.href);
      if (location.pathname === target.pathname) {
        const contact = document.getElementById('direct-contact');
        contact?.scrollIntoView();
        contact?.focus({preventScroll:true});
      }
    };
    video.addEventListener('ended', finish);
    video.addEventListener('error', () => {
      message.hidden = false;
      message.textContent = english ? 'The video could not be loaded. You can continue directly to contact.' : 'Das Video konnte nicht geladen werden. Du kannst direkt zum Kontakt weitergehen.';
    });
    skip.addEventListener('click', finish);
    dialog.addEventListener('cancel', event => { event.preventDefault(); finish(); });
    dialog.append(video, skip, message);
    document.body.append(dialog);
    dialog.showModal();
    // Both requests start within the original click, allowing sound and fullscreen.
    video.play().catch(() => {
      message.hidden = false;
      message.textContent = english ? 'Press Play to start the video.' : 'Drücke Play, um das Video zu starten.';
    });
    if (dialog.requestFullscreen) dialog.requestFullscreen().catch(() => {});
  });
})();
