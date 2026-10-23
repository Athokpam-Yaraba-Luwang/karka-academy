/* Karka AI & Tech Academy · main.js
   Built by Athokpam Yaraba Luwang · https://www.linkedin.com/in/yaraba-athokpam-856538343/
   Vanilla, dependency-free. Every effect is progressive: the page works without it. */
(() => {
  'use strict';

  const d = document;
  const h = d.documentElement;
  const $ = (s, r = d) => r.querySelector(s);
  const $$ = (s, r = d) => Array.from(r.querySelectorAll(s));
  const lite = h.classList.contains('lite');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const hasIO = 'IntersectionObserver' in window;
  const DATA = (() => { try { return JSON.parse($('#karka-data').textContent); } catch (e) { return null; } })();
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const watch = (els, cb, opts) => {
    if (!hasIO) { els.forEach((el) => cb(el, true)); return null; }
    const o = new IntersectionObserver((entries) => entries.forEach((e) => cb(e.target, e.isIntersecting, o)), opts);
    els.forEach((el) => o.observe(el));
    return o;
  };

  /* ---------- Scroll reveals ---------- */
  watch($$('[data-reveal], [data-steps]'), (el, on, o) => {
    if (!on) return;
    el.classList.add('in');
    if (o) o.unobserve(el);
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

  /* ---------- Pause infinite loops when off-screen ---------- */
  watch($$('[data-anim-scope], .marquee, .ticker'), (el, on) => el.classList.toggle('paused', !on), { rootMargin: '80px' });

  /* ---------- Header: solid on scroll, hide on scroll-down ---------- */
  const hdr = $('#hdr');
  if (hdr) {
    let lastY = scrollY;
    let ticking = false;
    const update = () => {
      const y = scrollY;
      hdr.classList.toggle('is-solid', y > 24);
      if (y > lastY + 6 && y > 520 && !h.classList.contains('nav-open')) hdr.classList.add('is-hidden');
      else if (y < lastY - 6 || y < 520) hdr.classList.remove('is-hidden');
      lastY = y;
      ticking = false;
    };
    addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    update();
    hdr.addEventListener('focusin', () => hdr.classList.remove('is-hidden'));
  }

  /* ---------- Mobile menu ---------- */
  const burger = $('.burger');
  const mnav = $('#mnav');
  if (burger && mnav) {
    const setOpen = (open) => {
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      h.classList.toggle('nav-open', open);
      if (open) {
        mnav.hidden = false;
        requestAnimationFrame(() => requestAnimationFrame(() => mnav.classList.add('is-open')));
        const first = $('a', mnav);
        if (first) setTimeout(() => first.focus({ preventScroll: true }), 120);
      } else {
        mnav.classList.remove('is-open');
        setTimeout(() => { if (!mnav.classList.contains('is-open')) mnav.hidden = true; }, 320);
      }
    };
    burger.addEventListener('click', () => setOpen(burger.getAttribute('aria-expanded') !== 'true'));
    mnav.addEventListener('click', (e) => { if (e.target.closest('a')) setOpen(false); });
    d.addEventListener('keydown', (e) => { if (e.key === 'Escape' && h.classList.contains('nav-open')) { setOpen(false); burger.focus(); } });
  }

  /* ---------- Hero word rotator ---------- */
  const rot = $('[data-rotator] .rotator__track');
  if (rot && !reduce) {
    const n = rot.children.length;
    let i = 0;
    const step = () => {
      if (d.hidden || rot.closest('.paused')) return;
      i += 1;
      rot.classList.remove('no-anim');
      rot.style.transform = `translate3d(0, ${(-i * 100) / n}%, 0)`;
      if (i === n - 1) {
        setTimeout(() => { rot.classList.add('no-anim'); i = 0; rot.style.transform = 'translate3d(0,0,0)'; }, 900);
      }
    };
    setTimeout(() => setInterval(step, 2400), 1400);
  }

  /* ---------- Count-up stats ---------- */
  const fmt = (n) => Math.round(n).toLocaleString('en-IN');
  const counters = $$('[data-count]');
  if (!reduce) {
    counters.forEach((el) => { el.textContent = fmt(Number(el.dataset.from || 0)); });
    watch(counters, (el, on, o) => {
      if (!on) return;
      if (o) o.unobserve(el);
      const from = Number(el.dataset.from || 0);
      const to = Number(el.dataset.count);
      const dur = from > to ? 1800 : 1400;
      const t0 = performance.now();
      const tick = (t) => {
        const p = Math.min(1, (t - t0) / dur);
        const e = 1 - Math.pow(2, -10 * p);
        el.textContent = fmt(from + (to - from) * (p === 1 ? 1 : e));
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    }, { threshold: 0.6 });
  }

  /* ---------- Track tabs ---------- */
  let selectTrack = () => {};
  const tabs = $('[data-tabs]');
  if (tabs) {
    const list = $('.tabs__list', tabs);
    const ink = $('.tabs__ink', tabs);
    const btns = $$('.tab', tabs);
    let current = btns[0];
    const moveInk = () => {
      ink.style.setProperty('--x', `${current.offsetLeft}px`);
      ink.style.setProperty('--w', `${current.offsetWidth}px`);
    };
    const select = (btn, focus) => {
      current = btn;
      btns.forEach((b) => {
        const on = b === btn;
        b.setAttribute('aria-selected', String(on));
        b.tabIndex = on ? 0 : -1;
        d.getElementById(b.getAttribute('aria-controls')).classList.toggle('is-active', on);
      });
      moveInk();
      if (focus) btn.focus({ preventScroll: true });
      const left = btn.offsetLeft - list.clientWidth / 2 + btn.offsetWidth / 2;
      list.scrollTo({ left, behavior: reduce ? 'auto' : 'smooth' });
    };
    selectTrack = (id) => { const b = btns.find((x) => x.dataset.track === id); if (b) select(b); };
    btns.forEach((b) => b.addEventListener('click', () => select(b)));
    list.addEventListener('keydown', (e) => {
      const i = btns.indexOf(d.activeElement);
      if (i < 0) return;
      const map = { ArrowRight: i + 1, ArrowLeft: i - 1, Home: 0, End: btns.length - 1 };
      if (!(e.key in map)) return;
      e.preventDefault();
      select(btns[(map[e.key] + btns.length) % btns.length], true);
    });
    moveInk();
    addEventListener('resize', moveInk, { passive: true });
    if (d.fonts && d.fonts.ready) d.fonts.ready.then(moveInk);
  }

  /* ---------- Pay-after-placement compare toggle ---------- */
  $$('[data-compare]').forEach((box) => {
    $$('.flow li', box).forEach((li, i) => li.style.setProperty('--n', i));
    $$('.seg__btn', box).forEach((btn) => btn.addEventListener('click', () => {
      const other = btn.dataset.mode === 'other';
      box.classList.toggle('is-other', other);
      $$('.seg__btn', box).forEach((b) => b.setAttribute('aria-selected', String(b === btn)));
    }));
  });

  /* ---------- FAQ accordion ---------- */
  $$('[data-acc]').forEach((acc) => {
    acc.addEventListener('click', (e) => {
      const btn = e.target.closest('.acc__btn');
      if (!btn) return;
      const item = btn.closest('.acc__item');
      const open = !item.classList.contains('is-open');
      $$('.acc__item', acc).forEach((it) => {
        const on = it === item ? open : false;
        it.classList.toggle('is-open', on);
        $('.acc__btn', it).setAttribute('aria-expanded', String(on));
      });
    });
  });

  /* ---------- Instagram-style stories ---------- */
  const st = $('[data-stories]');
  if (st) {
    const slides = $$('.story__slide', st);
    const rings = $$('.sring', st);
    const bars = $$('.story__bars span', st);
    const rail = $('.stories__rail', st);
    const card = $('.story', st);
    const pauseBtn = $('.story__pause', st);
    let idx = 0;
    let visible = false;
    let holding = false;
    let userPaused = false;
    let pressAt = 0;

    const sync = () => st.classList.toggle('is-paused', reduce || userPaused || holding || !visible);
    const show = (i) => {
      idx = (i + slides.length) % slides.length;
      slides.forEach((s, k) => s.classList.toggle('is-active', k === idx));
      rings.forEach((r, k) => {
        r.setAttribute('aria-selected', String(k === idx));
        if (k === idx) r.classList.add('is-seen');
      });
      bars.forEach((b, k) => { b.classList.toggle('done', k < idx); b.classList.remove('on'); });
      if (reduce) { bars[idx].classList.add('done'); } else { void bars[idx].offsetWidth; bars[idx].classList.add('on'); }
      const r = rings[idx];
      if (r && rail.scrollWidth > rail.clientWidth) {
        rail.scrollTo({ left: r.offsetLeft - rail.clientWidth / 2 + r.offsetWidth / 2, behavior: reduce ? 'auto' : 'smooth' });
      }
    };
    st.addEventListener('animationend', (e) => {
      if (e.animationName === 'fill' && e.target.parentElement.classList.contains('on')) show(idx + 1);
    });
    rings.forEach((r, k) => r.addEventListener('click', () => show(k)));
    const nav = (dir) => () => { if (performance.now() - pressAt < 350) show(idx + dir); };
    $('.story__nav--prev', st).addEventListener('click', nav(-1));
    $('.story__nav--next', st).addEventListener('click', nav(1));
    card.addEventListener('pointerdown', (e) => { if (e.target.closest('.story__pause')) return; pressAt = performance.now(); holding = true; sync(); });
    ['pointerup', 'pointercancel', 'pointerleave'].forEach((t) => card.addEventListener(t, () => { holding = false; sync(); }));
    pauseBtn.addEventListener('click', () => {
      userPaused = !userPaused;
      pauseBtn.setAttribute('aria-pressed', String(userPaused));
      pauseBtn.setAttribute('aria-label', userPaused ? 'Play stories' : 'Pause stories');
      sync();
    });
    st.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight') { e.preventDefault(); show(idx + 1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); show(idx - 1); }
    });
    watch([st], (el, on) => { visible = on; sync(); }, { threshold: 0.35 });
    show(0);
    sync();
  }

  /* ---------- Video testimonials (one <video>, swapped per learner) ---------- */
  const reels = $('[data-reels]');
  if (reels) {
    const video = $('.reel__video', reels);
    const items = $$('.rl', reels);
    const playBtn = $('.reel__play', reels);
    const muteBtn = $('.reel__mute', reels);
    const bar = $('.reel__bar i', reels);
    const info = $('.reel-info', reels);
    const list = $('.reels__list', reels);
    const state = $('[data-reel-state]', reels);
    let idx = 0;
    video.removeAttribute('controls'); // custom controls take over once JS runs

    const setPlaying = (on) => {
      reels.classList.toggle('is-playing', on);
      h.classList.toggle('reel-playing', on); // tucks the mobile dock away while a video plays
      state.textContent = on ? 'Now playing' : 'Now showing';
      playBtn.setAttribute('aria-label', on ? 'Pause video' : 'Play video');
    };
    const select = (i, autoplay) => {
      idx = (i + items.length) % items.length;
      const it = items[idx];
      items.forEach((b) => b.setAttribute('aria-selected', String(b === it)));
      video.pause();
      video.poster = it.dataset.poster;
      video.src = it.dataset.src;
      video.setAttribute('aria-label', `Video testimonial by ${it.dataset.name}`);
      bar.style.setProperty('--p', 0);
      $('[data-reel-name]', reels).textContent = it.dataset.name;
      $('[data-reel-role]', reels).textContent = it.dataset.role;
      $('[data-reel-quote]', reels).textContent = it.dataset.quote;
      $('[data-reel-next-name]', reels).textContent = items[(idx + 1) % items.length].dataset.name;
      if (!reduce) { info.classList.remove('swap'); void info.offsetWidth; info.classList.add('swap'); }
      if (list.scrollWidth > list.clientWidth) {
        list.scrollTo({ left: it.offsetLeft - list.clientWidth / 2 + it.offsetWidth / 2, behavior: reduce ? 'auto' : 'smooth' });
      }
      setPlaying(false);
      if (autoplay) video.play().catch(() => {});
    };
    const toggle = () => { if (video.paused) video.play().catch(() => {}); else video.pause(); };

    items.forEach((b, k) => b.addEventListener('click', () => select(k, true)));
    playBtn.addEventListener('click', toggle);
    video.addEventListener('click', toggle);
    $('[data-reel-next]', reels).addEventListener('click', () => select(idx + 1, true));
    muteBtn.addEventListener('click', () => {
      video.muted = !video.muted;
      muteBtn.setAttribute('aria-pressed', String(video.muted));
      muteBtn.setAttribute('aria-label', video.muted ? 'Unmute' : 'Mute');
    });
    video.addEventListener('play', () => { setPlaying(true); muteBtn.hidden = false; });
    video.addEventListener('pause', () => setPlaying(false));
    video.addEventListener('timeupdate', () => {
      if (video.duration) bar.style.setProperty('--p', (video.currentTime / video.duration).toFixed(3));
    });
    video.addEventListener('ended', () => { if (idx < items.length - 1) select(idx + 1, true); else setPlaying(false); });
    list.addEventListener('keydown', (e) => {
      const map = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 };
      if (!(e.key in map)) return;
      e.preventDefault();
      select(idx + map[e.key], false);
      items[idx].focus();
    });
    watch([reels], (_, on) => { if (!on && !video.paused) video.pause(); }, { threshold: 0.2 });
  }

  /* ---------- Prefill + jump to the lead form ---------- */
  const leadForm = $('#apply [data-lead-form]');
  const goApply = (courseName) => {
    if (!leadForm) return false;
    const sel = $('select[name="program"]', leadForm);
    if (sel && courseName) sel.value = courseName;
    $('#apply').scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    setTimeout(() => { const n = $('input[name="name"]', leadForm); if (n) n.focus({ preventScroll: true }); }, reduce ? 0 : 700);
    return true;
  };
  d.addEventListener('click', (e) => {
    const a = e.target.closest('[data-apply]');
    if (!a || !DATA) return;
    const c = DATA.courses[a.dataset.apply];
    if (c && goApply(c.name)) e.preventDefault();
  });

  /* ---------- Track finder quiz ---------- */
  const dlg = $('#finder');
  if (dlg && DATA) {
    const stage = $('[data-finder-stage]', dlg);
    const bar = $('.finder__bar', dlg);
    const order = Object.keys(DATA.tracks);
    let scores = {};

    const progress = (p) => bar.style.setProperty('--p', `${p}%`);
    const renderQ = (qi) => {
      const q = DATA.quiz[qi];
      progress((qi / DATA.quiz.length) * 100);
      stage.innerHTML = `<div class="fstep"><h3>${esc(q.q)}</h3><div class="fopts">${q.options.map((o, k) =>
        `<button type="button" class="fopt" style="--i:${k}" data-k="${k}"><span class="fopt__e" aria-hidden="true">${esc(o.emoji)}</span>${esc(o.label)}</button>`).join('')}</div></div>`;
      $$('.fopt', stage).forEach((b) => b.addEventListener('click', () => {
        const opt = q.options[Number(b.dataset.k)];
        Object.entries(opt.w).forEach(([k, v]) => { scores[k] = (scores[k] || 0) + v; });
        b.classList.add('is-picked');
        $$('.fopt', stage).forEach((x) => { x.disabled = true; });
        setTimeout(() => (qi + 1 < DATA.quiz.length ? renderQ(qi + 1) : renderResult()), reduce ? 0 : 320);
      }));
      const first = $('.fopt', stage);
      if (first) first.focus({ preventScroll: true });
    };
    const renderResult = () => {
      progress(100);
      const best = order.reduce((a, b) => ((scores[b] || 0) > (scores[a] || 0) ? b : a), order[0]);
      const track = DATA.tracks[best];
      const slug = DATA.pick[best];
      const course = DATA.courses[slug];
      stage.innerHTML = `<div class="fstep fresult">
          <span class="fresult__kicker">Your track</span>
          <span class="fresult__track">${esc(track.name)}</span>
          <p>${esc(track.tagline)}. Start with:</p>
          <div class="fresult__course">${esc(course.name)}${course.duration ? ` · ${esc(course.duration)}` : ''}</div>
          <div class="fresult__ctas">
            <a class="btn btn--glow" href="/apply?program=${esc(slug)}" data-go-apply>Apply for this · ₹0 upfront</a>
            ${course.featured ? `<a class="btn btn--soft" href="/courses/${esc(slug)}">View course</a>` : ''}
          </div>
          <button type="button" class="fresult__retake" data-retake>Retake quiz</button>
        </div>`;
      $('[data-retake]', stage).addEventListener('click', start);
      $('[data-go-apply]', stage).addEventListener('click', (e) => {
        if (!leadForm) return;
        e.preventDefault();
        close();
        selectTrack(best);
        goApply(course.name);
      });
      selectTrack(best);
    };
    const start = () => { scores = {}; renderQ(0); };
    const open = () => {
      start();
      if (typeof dlg.showModal === 'function') dlg.showModal(); else dlg.setAttribute('open', '');
      h.classList.add('nav-open');
    };
    const close = () => {
      if (typeof dlg.close === 'function' && dlg.open) dlg.close(); else dlg.removeAttribute('open');
    };
    dlg.addEventListener('close', () => h.classList.remove('nav-open'));
    d.addEventListener('click', (e) => {
      const opener = e.target.closest('[data-finder-open]');
      if (opener) { e.preventDefault(); open(); }
    });
    $('[data-finder-close]', dlg).addEventListener('click', close);
    dlg.addEventListener('click', (e) => { if (e.target === dlg) close(); });
  }

  /* ---------- Lead forms (fetch + inline validation) ---------- */
  const PHONE = /^(?:\+?91|0)?[6-9]\d{9}$/;
  const EMAIL = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
  const burst = (host) => {
    if (lite || reduce) return;
    const wrap = d.createElement('div');
    wrap.className = 'burst';
    const colors = ['#ff4fb8', '#ffd23f', '#2ee6f0', '#9b4dff', '#22c55e'];
    for (let i = 0; i < 26; i += 1) {
      const p = d.createElement('i');
      const a = (Math.PI * 2 * i) / 26;
      const r = 90 + Math.random() * 110;
      p.style.cssText = `--x:${Math.cos(a) * r}px;--y:${Math.sin(a) * r - 40}px;--r:${Math.random() * 720 - 360}deg;background:${colors[i % colors.length]}`;
      wrap.appendChild(p);
    }
    host.appendChild(wrap);
    setTimeout(() => wrap.remove(), 1300);
  };

  $$('[data-lead-form]').forEach((form) => {
    const setErr = (name, msg) => {
      const slot = $(`[data-err="${name}"]`, form);
      if (!slot) return;
      slot.textContent = msg || '';
      const field = slot.closest('.field');
      field.classList.toggle('is-bad', !!msg);
      if (msg && !reduce) { field.classList.remove('shake'); void field.offsetWidth; field.classList.add('shake'); }
    };
    const setFormErr = (msg) => {
      let alert = $('.lead__alert', form);
      if (!msg) { if (alert) alert.remove(); return; }
      if (!alert) {
        alert = d.createElement('p');
        alert.className = 'lead__alert';
        alert.setAttribute('role', 'alert');
        $('.lead__body', form).prepend(alert);
      }
      alert.textContent = msg;
    };
    form.addEventListener('input', (e) => { if (e.target.name) setErr(e.target.name, ''); });
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const data = Object.fromEntries(new FormData(form));
      const errs = {};
      if ((data.name || '').trim().length < 2) errs.name = 'Please enter your name.';
      if (!PHONE.test((data.phone || '').replace(/[\s\-()]/g, ''))) errs.phone = 'Enter a valid 10-digit mobile number.';
      if (data.email && !EMAIL.test(data.email.trim())) errs.email = "That email doesn't look right.";
      if (!data.program) errs.program = 'Pick a program.';
      ['name', 'phone', 'email', 'program', 'audience'].forEach((k) => setErr(k, errs[k]));
      setFormErr('');
      const firstBad = Object.keys(errs)[0];
      if (firstBad) { const el = $(`[name="${firstBad}"]`, form); if (el) el.focus(); return; }

      form.classList.add('is-loading');
      try {
        const res = await fetch('/api/leads', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify(data),
        });
        const json = await res.json().catch(() => ({}));
        if (res.ok && json.ok) {
          $('[data-first-name]', form).textContent = json.first_name || 'friend';
          $('.lead__body', form).hidden = true;
          const done = $('.lead__done', form);
          done.hidden = false;
          done.focus({ preventScroll: true });
          burst(form);
        } else {
          const errors = json.errors || { form: 'Something went wrong. Please try again.' };
          Object.entries(errors).forEach(([k, v]) => (k === 'form' ? setFormErr(v) : setErr(k, v)));
        }
      } catch (err) {
        HTMLFormElement.prototype.submit.call(form); // network hiccup: fall back to a normal POST
      } finally {
        form.classList.remove('is-loading');
      }
    });
  });

  /* ---------- Spike "typing" demo ---------- */
  $$('[data-typing]').forEach((el) => {
    if (reduce) return;
    const phrases = el.dataset.typing.split('|');
    let p = 0;
    let c = 0;
    let del = false;
    let on = false;
    watch([el], (_, vis) => { on = vis; }, {});
    const loop = () => {
      let wait = 55;
      if (on && !d.hidden) {
        const s = phrases[p];
        c += del ? -1 : 1;
        el.textContent = s.slice(0, c);
        if (!del && c === s.length) { del = true; wait = 1700; }
        else if (del && c === 0) { del = false; p = (p + 1) % phrases.length; wait = 400; }
        else if (del) wait = 24;
      } else wait = 600;
      setTimeout(loop, wait);
    };
    setTimeout(loop, 1200);
  });

  /* ---------- Sticky mobile dock ---------- */
  const dock = $('#dock');
  if (dock) {
    const hero = $('.hero');
    const apply = $('#apply');
    const footer = $('.ftr');
    const state = { hero: true, apply: false, footer: false };
    const links = $$('a', dock);
    const sync = () => {
      const on = !state.hero && !state.apply && !state.footer;
      dock.classList.toggle('is-on', on);
      dock.setAttribute('aria-hidden', String(!on));
      links.forEach((a) => { a.tabIndex = on ? 0 : -1; });
    };
    const targets = [hero, apply, footer].filter(Boolean);
    watch(targets, (el, vis) => {
      if (el === hero) state.hero = vis;
      if (el === apply) state.apply = vis;
      if (el === footer) state.footer = vis;
      sync();
    }, {});
    if (!hero) { state.hero = false; sync(); }
  }

  /* ---------- Touch: hold to pause marquees ---------- */
  $$('.marquee').forEach((m) => {
    m.addEventListener('pointerdown', () => m.classList.add('is-held'), { passive: true });
    ['pointerup', 'pointercancel', 'pointerleave'].forEach((t) => m.addEventListener(t, () => m.classList.remove('is-held'), { passive: true }));
  });

  /* ---------- Desktop-only pointer delight (skipped on touch, lite, reduced motion) ---------- */
  if (finePointer && !lite && !reduce) {
    $$('[data-magnetic]').forEach((el) => {
      el.addEventListener('pointermove', (e) => {
        const r = el.getBoundingClientRect();
        const x = (e.clientX - r.left - r.width / 2) * 0.18;
        const y = (e.clientY - r.top - r.height / 2) * 0.3;
        el.style.transform = `translate3d(${x}px, ${y}px, 0)`;
      });
      el.addEventListener('pointerleave', () => { el.style.transform = ''; });
    });

    d.addEventListener('pointermove', (e) => {
      const card = e.target.closest && e.target.closest('.spot');
      if (!card) return;
      const r = card.getBoundingClientRect();
      card.style.setProperty('--mx', `${e.clientX - r.left}px`);
      card.style.setProperty('--my', `${e.clientY - r.top}px`);
    }, { passive: true });

    const art = $('[data-parallax]');
    const heroEl = $('.hero');
    if (art && heroEl) {
      const orbit = $('.orbit', art);
      let raf = 0;
      let tx = 0;
      let ty = 0;
      heroEl.addEventListener('pointermove', (e) => {
        tx = (e.clientX / innerWidth - 0.5) * 2;
        ty = (e.clientY / innerHeight - 0.5) * 2;
        if (!raf) raf = requestAnimationFrame(() => {
          orbit.style.transform = `perspective(900px) rotateY(${tx * 6}deg) rotateX(${-ty * 6}deg) translate3d(${tx * 8}px, ${ty * 8}px, 0)`;
          raf = 0;
        });
      }, { passive: true });
      heroEl.addEventListener('pointerleave', () => { orbit.style.transform = ''; });
      orbit.style.transition = 'transform .6s cubic-bezier(.16,1,.3,1)';
    }
  }
})();
