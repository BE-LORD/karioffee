/* ═══════════════════════════════════════════════════════════════
   KARIOFFEE — "FROM THE ROAST" CINEMATIC INTRO
   Act I   ROASTING  — a galaxy of beans ignites in the dark
   Act II  GRINDING/BREWING — the galaxy collapses into a vortex
           above a glowing cup rim
   Act III POURING   — the camera dives through the rim into a
           live crema swirl; the brand surfaces
   Exit    the crema calms and brightens to the site's cream,
           the letterbox opens onto the hero
   Fallbacks: 2D swirl (no WebGL/CDN), reduced-motion fast path,
   skip button, hard safety timeout. Never traps the user.
   ═══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var root = document.getElementById('liceria-intro');
  if (!root) return;

  function announceDone() {
    if (window.__liceriaIntroDone) return;
    window.__liceriaIntroDone = true;
    document.body.classList.remove('lc-lock');
    window.dispatchEvent(new CustomEvent('liceria:introdone'));
  }

  /* If GSAP failed to load there is no show — get out of the way. */
  if (typeof gsap === 'undefined') {
    root.style.display = 'none';
    announceDone();
    return;
  }

  document.body.classList.add('lc-lock');
  window.scrollTo(0, 0);

  var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };
  var lerp = function (a, b, t) { return a + (b - a) * t; };

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var canvas = document.getElementById('lcCanvas');
  var can3D = !reduced && typeof THREE !== 'undefined' && (function () {
    try {
      var c = document.createElement('canvas');
      return !!(window.WebGLRenderingContext && (c.getContext('webgl') || c.getContext('experimental-webgl')));
    } catch (e) { return false; }
  })();

  /* ── DOM: rolling odometer + stage readout ─────────────────── */
  var strips = root.querySelectorAll('[data-lc-strip]');
  Array.prototype.forEach.call(strips, function (s) {
    s.innerHTML = '0123456789'.split('').map(function (d) { return '<i>' + d + '</i>'; }).join('');
  });
  var stageWordEl = root.querySelector('[data-lc-stage]');
  var stageNoteEl = root.querySelector('[data-lc-note]');
  var lineEl = root.querySelector('.lc-progressline i');

  var STAGES = [
    { at: 0,  word: 'Roasting', note: 'first crack · 196°C' },
    { at: 34, word: 'Grinding', note: 'burr set fine · 400 microns' },
    { at: 58, word: 'Brewing',  note: '93° water · slow bloom' },
    { at: 80, word: 'Pouring',  note: 'crema rising' }
  ];
  var stageIx = 0;

  function setStage(ix) {
    if (ix === stageIx) return;
    stageIx = ix;
    var s = STAGES[ix];
    gsap.timeline()
      .to([stageWordEl, stageNoteEl], { yPercent: -115, opacity: 0, duration: 0.32, stagger: 0.05, ease: 'power2.in' })
      .add(function () { stageWordEl.textContent = s.word; stageNoteEl.textContent = s.note; })
      .fromTo([stageWordEl, stageNoteEl],
        { yPercent: 115, opacity: 0 },
        { yPercent: 0, opacity: 1, duration: 0.55, stagger: 0.07, ease: 'power3.out' });
  }

  var shownInt = -1;
  function renderReadout(p) {
    lineEl.style.transform = 'scaleX(' + clamp(p / 100, 0, 1) + ')';
    var v = Math.min(100, Math.floor(p));
    if (v !== shownInt) {
      shownInt = v;
      if (v >= 100) {
        root.classList.add('lc-hundred');
        gsap.to(strips[0], { yPercent: 0, duration: 0.5, ease: 'power3.out', overwrite: true });
        gsap.to(strips[1], { yPercent: 0, duration: 0.5, ease: 'power3.out', overwrite: true });
      } else {
        gsap.to(strips[0], { yPercent: -(Math.floor(v / 10) * 10), duration: 0.55, ease: 'power3.out', overwrite: true });
        gsap.to(strips[1], { yPercent: -((v % 10) * 10), duration: 0.4, ease: 'power3.out', overwrite: true });
      }
    }
    for (var i = STAGES.length - 1; i >= 0; i--) {
      if (p >= STAGES[i].at) { setStage(i); break; }
    }
    if (p >= 80) showBrand();
    if (p >= 82) sweepLeak();
  }

  /* ── Brand reveal (Act III) ─────────────────────────────────── */
  var brandShown = false;
  function showBrand() {
    if (brandShown) return;
    brandShown = true;
    gsap.timeline({ defaults: { ease: 'power3.out' } })
      .set('.lc-brand', { opacity: 1 })
      .fromTo('.lc-brand-name', { yPercent: 118 }, { yPercent: 0, duration: 1.15, ease: 'power4.out' }, 0)
      .fromTo('.lc-brand-eyebrow', { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.8 }, 0.25)
      .fromTo('.lc-brand-rule', { scaleX: 0 }, { scaleX: 1, duration: 1.0, ease: 'power2.inOut' }, 0.35)
      .fromTo('.lc-brand-sub',
        { opacity: 0, letterSpacing: '1.3em' },
        { opacity: 1, letterSpacing: '0.55em', duration: 1.2, ease: 'power2.out' }, 0.4);
  }

  var leakDone = false;
  function sweepLeak() {
    if (leakDone) return;
    leakDone = true;
    gsap.fromTo('.lc-leak',
      { x: '-30vw', opacity: 0 },
      { x: '150vw', opacity: 0.9, duration: 1.6, ease: 'power1.inOut',
        onComplete: function () { gsap.set('.lc-leak', { opacity: 0 }); } });
  }

  /* ── Progress engine ────────────────────────────────────────── */
  var state = { target: 0, shown: 0 };
  var exiting = false;
  var pushed = false;
  var chaseBoost = 1;

  var paceDur = reduced ? 0.6 : 1.5;
  var pace = gsap.to(state, { target: 92, duration: paceDur, ease: 'sine.inOut' });

  var loaded = document.readyState === 'complete' || document.readyState === 'interactive';
  if (!loaded) {
    window.addEventListener('load', function () { loaded = true; }, { once: true });
    setTimeout(function () { loaded = true; }, 1200);
  }

  function pushFull(fast) {
    if (pushed) return;
    pushed = true;
    pace.kill();
    gsap.to(state, { target: 100, duration: fast ? 0.3 : 0.6, ease: 'power2.inOut', overwrite: true });
  }

  function skip() {
    if (exiting) return;
    chaseBoost = 2.6;
    pushFull(true);
  }
  var skipBtn = document.getElementById('lcSkip');
  if (skipBtn) skipBtn.addEventListener('click', skip);
  window.addEventListener('keydown', function (e) { if (e.key === 'Escape') skip(); });

  /* ══ 3D SCENE ═══════════════════════════════════════════════ */

  /* Everything the camera/timeline choreographs lives on `shot`;
     the GSAP timeline below keyframes it, and the ticker's playhead
     chases the loading progress so the film never outruns the load. */
  var shot = {
    dist: 27, yaw: -0.55, pitch: 0.07, lookY: 0.9, fov: 40,
    ember: 0, collapse: 0, ringGlow: 0,
    beanFade: 1, cremaO: 0, cremaCalm: 0, cremaCream: 0
  };
  var CINE = 7.0;
  var cine = null;
  var scene3d = null;

  function makeRadialTex(stops) {
    var c = document.createElement('canvas');
    c.width = c.height = 128;
    var g = c.getContext('2d');
    var gr = g.createRadialGradient(64, 64, 0, 64, 64, 64);
    stops.forEach(function (s) { gr.addColorStop(s[0], s[1]); });
    g.fillStyle = gr;
    g.fillRect(0, 0, 128, 128);
    return new THREE.CanvasTexture(c);
  }

  function build3D() {
    var renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: false, powerPreference: 'high-performance' });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, window.innerWidth < 720 ? 1.5 : 1.75));
    renderer.setSize(window.innerWidth, window.innerHeight);
    if ('outputEncoding' in renderer && THREE.sRGBEncoding !== undefined) renderer.outputEncoding = THREE.sRGBEncoding;
    renderer.autoClear = false;

    var scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0d0704);
    scene.fog = new THREE.FogExp2(0x0d0704, 0.042);

    var camera = new THREE.PerspectiveCamera(40, window.innerWidth / window.innerHeight, 0.1, 140);

    var key = new THREE.DirectionalLight(0xffd9a8, 0.5);
    key.position.set(6, 9, 6);
    scene.add(key);
    var rim = new THREE.DirectionalLight(0xd4af37, 0.32);
    rim.position.set(-7, 3, -6);
    scene.add(rim);
    scene.add(new THREE.AmbientLight(0x40230f, 0.85));
    var emberLight = new THREE.PointLight(0xff7a2f, 0, 44, 1.7);
    emberLight.position.set(0, -0.4, 0);
    scene.add(emberLight);

    /* — coffee bean geometry: ellipsoid with a centre crease — */
    var geo = new THREE.SphereGeometry(1, 20, 16);
    var pos = geo.attributes.position;
    var v = new THREE.Vector3();
    for (var i = 0; i < pos.count; i++) {
      v.fromBufferAttribute(pos, i);
      var x = v.x * 0.66, y = v.y * 0.3, z = v.z * 0.46;
      if (y > 0) y *= 1 - 0.62 * Math.exp(-(z * z) / 0.015);
      y += 0.045 * Math.cos(x * 2.4);
      pos.setXYZ(i, x, y, z);
    }
    geo.computeVertexNormals();

    var beanMat = new THREE.MeshStandardMaterial({
      color: 0xffffff, roughness: 0.52, metalness: 0.12,
      emissive: new THREE.Color(0xff5f1e), emissiveIntensity: 0,
      transparent: true, opacity: 1
    });

    var COUNT = window.innerWidth < 720 ? 650 : 1500;
    var beans = new THREE.InstancedMesh(geo, beanMat, COUNT);
    beans.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
    var bp = [];
    var col = new THREE.Color();
    for (i = 0; i < COUNT; i++) {
      var r0 = 3.2 + Math.pow(Math.random(), 0.65) * 11.5;
      bp.push({
        r0: r0,
        ang: Math.random() * Math.PI * 2,
        y0: (Math.random() + Math.random() + Math.random() - 1.5) * 2.7,
        sc: 0.5 + Math.random() * 0.72,
        orbit: (0.16 + Math.random() * 0.1) / Math.sqrt(r0 * 0.35),
        bobA: 0.1 + Math.random() * 0.25,
        bobW: 0.3 + Math.random() * 0.7,
        ph: Math.random() * Math.PI * 2,
        rx: Math.random() * Math.PI * 2,
        ry: Math.random() * Math.PI * 2,
        wx: (Math.random() - 0.5) * 1.7,
        wy: (Math.random() - 0.5) * 1.7,
        fall: 0.55 + Math.random() * 0.5
      });
      col.setHSL(0.065 + Math.random() * 0.03, 0.5 + Math.random() * 0.22, 0.2 + Math.random() * 0.17);
      beans.setColorAt(i, col);
    }
    scene.add(beans);
    var dummy = new THREE.Object3D();

    /* — rising ember sparks — */
    var S = window.innerWidth < 720 ? 150 : 320;
    var sparkGeo = new THREE.BufferGeometry();
    var sparkPos = new Float32Array(S * 3);
    var sd = [];
    for (i = 0; i < S; i++) {
      sd.push({
        r: 1 + Math.random() * 9,
        a: Math.random() * Math.PI * 2,
        y: -3 + Math.random() * 9.5,
        v: 0.35 + Math.random() * 0.95,
        w: (Math.random() - 0.5) * 0.7
      });
    }
    sparkGeo.setAttribute('position', new THREE.BufferAttribute(sparkPos, 3));
    var sparkTex = makeRadialTex([[0, 'rgba(255,214,160,1)'], [0.3, 'rgba(255,162,77,0.85)'], [1, 'rgba(255,122,47,0)']]);
    var sparkMat = new THREE.PointsMaterial({
      color: 0xffb066, size: 0.16, map: sparkTex, transparent: true, opacity: 0,
      blending: THREE.AdditiveBlending, depthWrite: false, sizeAttenuation: true
    });
    var sparks = new THREE.Points(sparkGeo, sparkMat);
    scene.add(sparks);

    /* — the cup: gold rim + dark liquid + halo, target of the dive — */
    var CUP_Y = -2.6;
    var ring = new THREE.Mesh(
      new THREE.TorusGeometry(1.55, 0.035, 12, 96),
      new THREE.MeshBasicMaterial({ color: 0xd4af37, transparent: true, opacity: 0 })
    );
    ring.rotation.x = Math.PI / 2;
    ring.position.y = CUP_Y;
    scene.add(ring);

    var liquid = new THREE.Mesh(
      new THREE.CircleGeometry(1.52, 48),
      new THREE.MeshBasicMaterial({ color: 0x2b1608, transparent: true, opacity: 0 })
    );
    liquid.rotation.x = -Math.PI / 2;
    liquid.position.y = CUP_Y - 0.02;
    scene.add(liquid);

    /* — steam: soft wisps climbing out of the cup as we dive — */
    var STEAM = window.innerWidth < 720 ? 40 : 90;
    var steamGeo = new THREE.BufferGeometry();
    var steamPos = new Float32Array(STEAM * 3);
    var std = [];
    for (i = 0; i < STEAM; i++) {
      std.push({
        r: Math.random() * 1.1,
        a: Math.random() * Math.PI * 2,
        y: Math.random() * 4.5,
        v: 0.25 + Math.random() * 0.5,
        w: (Math.random() - 0.5) * 1.4,
        drift: 0.15 + Math.random() * 0.3
      });
    }
    steamGeo.setAttribute('position', new THREE.BufferAttribute(steamPos, 3));
    var steamTex = makeRadialTex([[0, 'rgba(248,244,240,0.65)'], [0.45, 'rgba(238,230,222,0.25)'], [1, 'rgba(238,230,222,0)']]);
    var steamMat = new THREE.PointsMaterial({
      color: 0xf5efe9, size: 0.85, map: steamTex, transparent: true, opacity: 0,
      blending: THREE.NormalBlending, depthWrite: false, sizeAttenuation: true
    });
    var steam = new THREE.Points(steamGeo, steamMat);
    steam.position.y = CUP_Y;
    scene.add(steam);

    var haloTex = makeRadialTex([[0, 'rgba(255,181,69,0.55)'], [0.4, 'rgba(212,175,55,0.22)'], [1, 'rgba(212,175,55,0)']]);
    var halo = new THREE.Sprite(new THREE.SpriteMaterial({
      map: haloTex, color: 0xffffff, transparent: true, opacity: 0,
      blending: THREE.AdditiveBlending, depthWrite: false
    }));
    halo.scale.set(7, 7, 1);
    halo.position.y = CUP_Y;
    scene.add(halo);

    /* — crema overlay: fullscreen swirl shader, Act III backdrop — */
    var cremaScene = new THREE.Scene();
    var cremaCam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
    var cremaMat = new THREE.ShaderMaterial({
      transparent: true,
      depthTest: false,
      depthWrite: false,
      uniforms: {
        uTime: { value: 0 },
        uOpacity: { value: 0 },
        uCalm: { value: 0 },
        uCream: { value: 0 },
        uAspect: { value: window.innerWidth / window.innerHeight }
      },
      vertexShader: [
        'varying vec2 vUv;',
        'void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }'
      ].join('\n'),
      fragmentShader: [
        'precision highp float;',
        'varying vec2 vUv;',
        'uniform float uTime, uOpacity, uCalm, uCream, uAspect;',
        'float hash(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123); }',
        'float noise(in vec2 p){',
        '  vec2 i = floor(p), f = fract(p);',
        '  vec2 u = f * f * (3.0 - 2.0 * f);',
        '  return mix(mix(hash(i), hash(i + vec2(1.0, 0.0)), u.x),',
        '             mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), u.x), u.y);',
        '}',
        'float fbm(vec2 p){',
        '  float v = 0.0, a = 0.5;',
        '  mat2 r = mat2(0.8, 0.6, -0.6, 0.8);',
        '  for (int i = 0; i < 5; i++){ v += a * noise(p); p = r * p * 2.03; a *= 0.52; }',
        '  return v;',
        '}',
        'void main(){',
        '  vec2 p = vUv - 0.5;',
        '  p.x *= uAspect;',
        '  float r = length(p);',
        '  float ang = atan(p.y, p.x);',
        '  float live = 1.0 - uCalm;',
        '  float spin = uTime * (0.10 + 0.22 * live);',
        '  float spiral = ang + 5.5 * r - spin * 2.2;',
        '  vec2 q = vec2(fbm(p * 3.1 + uTime * 0.06), fbm(p * 3.1 - uTime * 0.045 + 4.7));',
        '  float n = fbm(p * 2.6 + q * 1.7 + vec2(cos(spiral), sin(spiral)) * 0.35 * live);',
        '  float bands = 0.5 + 0.5 * sin(spiral * 2.0 + n * (3.0 + 3.5 * live));',
        '  bands = pow(bands, 1.6);',
        '  vec3 espresso = vec3(0.16, 0.08, 0.03);',
        '  vec3 roast = vec3(0.42, 0.24, 0.11);',
        '  vec3 crema = vec3(0.91, 0.78, 0.60);',
        '  vec3 colr = mix(espresso, roast, smoothstep(0.15, 0.85, n));',
        '  colr = mix(colr, crema, bands * (0.55 + 0.25 * live) * smoothstep(1.0, 0.15, r));',
        '  colr += crema * exp(-r * 4.5) * 0.35;',
        '  colr *= 1.0 - 0.35 * smoothstep(0.55, 1.05, r);',
        '  vec3 cream = vec3(0.980, 0.980, 0.972);',
        '  colr = mix(colr, cream, smoothstep(0.0, 1.0, uCream));',
        '  gl_FragColor = vec4(colr, uOpacity);',
        '}'
      ].join('\n')
    });
    cremaScene.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), cremaMat));

    /* — mouse parallax (desktop nicety) — */
    var mx = 0, my = 0, mxT = 0, myT = 0;
    if (window.innerWidth > 992) {
      window.addEventListener('mousemove', function (e) {
        mxT = (e.clientX / window.innerWidth - 0.5) * 2;
        myT = (e.clientY / window.innerHeight - 0.5) * 2;
      });
    }

    function onResize() {
      renderer.setSize(window.innerWidth, window.innerHeight);
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      cremaMat.uniforms.uAspect.value = window.innerWidth / window.innerHeight;
    }
    window.addEventListener('resize', onResize);

    function update(t, dt) {
      /* beans: orbit → staggered vortex collapse */
      var c = shot.collapse;
      var showBeans = shot.beanFade > 0.02;
      beans.visible = showBeans;
      if (showBeans) {
        for (var i = 0; i < COUNT; i++) {
          var b = bp[i];
          var cc = clamp(c * b.fall * 1.6, 0, 1);
          var e = cc * cc * (3 - 2 * cc);
          b.ang += dt * b.orbit * (1 + e * 9);
          var rr = lerp(b.r0, 0.55 + b.r0 * 0.045, e);
          var yy = lerp(b.y0 + Math.sin(t * b.bobW + b.ph) * b.bobA, CUP_Y - 0.2 - b.r0 * 0.14, e);
          dummy.position.set(Math.cos(b.ang) * rr, yy, Math.sin(b.ang) * rr);
          b.rx += dt * b.wx;
          b.ry += dt * b.wy;
          dummy.rotation.set(b.rx, b.ry, 0);
          dummy.scale.setScalar(b.sc * (1 - e * 0.42));
          dummy.updateMatrix();
          beans.setMatrixAt(i, dummy.matrix);
        }
        beans.instanceMatrix.needsUpdate = true;
      }
      beanMat.emissiveIntensity = shot.ember * (0.5 + 0.12 * Math.sin(t * 7.3) + 0.08 * Math.sin(t * 11.7));
      beanMat.opacity = shot.beanFade;
      emberLight.intensity = shot.ember * (2.4 + 0.45 * Math.sin(t * 9.1)) + shot.ringGlow * 1.6;
      emberLight.position.y = lerp(-0.4, CUP_Y, c);

      /* sparks drift upward, tightening with the vortex */
      var sVis = shot.ember * 0.75 * shot.beanFade;
      sparkMat.opacity = sVis;
      if (sVis > 0.01) {
        for (i = 0; i < S; i++) {
          var s = sd[i];
          s.y += s.v * dt;
          s.a += s.w * dt * (1 + c * 5);
          if (s.y > 7) s.y = -3.5;
          var sr = s.r * (1 - c * 0.75);
          sparkPos[i * 3] = Math.cos(s.a) * sr;
          sparkPos[i * 3 + 1] = s.y;
          sparkPos[i * 3 + 2] = Math.sin(s.a) * sr;
        }
        sparkGeo.attributes.position.needsUpdate = true;
      }
      sparks.visible = sVis > 0.01;

      /* steam wisps rise from the cup once the rim is alive */
      var stVis = Math.max(shot.ringGlow, shot.cremaO * 0.5) * 0.55;
      steamMat.opacity = stVis;
      steam.visible = stVis > 0.01;
      if (steam.visible) {
        for (i = 0; i < STEAM; i++) {
          var w = std[i];
          w.y += w.v * dt;
          w.a += w.w * dt;
          if (w.y > 5) { w.y = 0; w.r = Math.random() * 1.1; }
          var spread = w.r + w.y * w.drift;         /* plume widens as it climbs */
          steamPos[i * 3] = Math.cos(w.a) * spread;
          steamPos[i * 3 + 1] = w.y;
          steamPos[i * 3 + 2] = Math.sin(w.a) * spread;
        }
        steamGeo.attributes.position.needsUpdate = true;
      }

      /* cup rim */
      var rg = shot.ringGlow;
      ring.material.opacity = rg * 0.95;
      liquid.material.opacity = rg * 0.9;
      halo.material.opacity = rg * 0.5 * (0.85 + 0.15 * Math.sin(t * 2.2));
      var pulse = 1 + 0.012 * Math.sin(t * 2.6);
      ring.scale.set(pulse, pulse, pulse);

      /* camera: choreographed shot + handheld drift + mouse */
      mx = lerp(mx, mxT, clamp(dt * 3, 0, 1));
      my = lerp(my, myT, clamp(dt * 3, 0, 1));
      var drift = 0.02 * Math.sin(t * 0.9) + 0.013 * Math.sin(t * 1.7 + 2.1);
      var yaw = shot.yaw + drift + mx * 0.05;
      var pitch = clamp(shot.pitch + 0.015 * Math.sin(t * 1.3 + 1) + my * 0.03, -1.4, 1.49);
      var d = shot.dist;
      var ty = shot.lookY;
      camera.position.set(
        d * Math.cos(pitch) * Math.sin(yaw),
        ty + d * Math.sin(pitch),
        d * Math.cos(pitch) * Math.cos(yaw)
      );
      camera.lookAt(0, ty, 0);
      camera.fov = shot.fov;
      camera.updateProjectionMatrix();

      /* render: roastery scene, then crema overlay */
      cremaMat.uniforms.uTime.value = t;
      cremaMat.uniforms.uOpacity.value = shot.cremaO;
      cremaMat.uniforms.uCalm.value = shot.cremaCalm;
      cremaMat.uniforms.uCream.value = shot.cremaCream;
      renderer.clear();
      renderer.render(scene, camera);
      if (shot.cremaO > 0.001) renderer.render(cremaScene, cremaCam);
    }

    function dispose() {
      window.removeEventListener('resize', onResize);
      geo.dispose();
      beanMat.dispose();
      sparkGeo.dispose();
      sparkMat.dispose();
      steamGeo.dispose();
      steamMat.dispose();
      cremaMat.dispose();
      renderer.dispose();
    }

    return { update: update, dispose: dispose };
  }

  if (can3D) {
    try {
      scene3d = build3D();
    } catch (err) {
      scene3d = null;
    }
  }
  if (!scene3d) root.classList.add('lc-2d');

  /* — the film: a paused timeline whose playhead chases progress — */
  if (scene3d) {
    cine = gsap.timeline({ paused: true, defaults: { ease: 'power2.inOut' } });
    cine
      /* Act I — roast */
      .to(shot, { ember: 0.9, duration: 2.0, ease: 'power2.in' }, 0.15)
      .to(shot, { dist: 16.5, yaw: 0.16, pitch: 0.14, lookY: 0.4, duration: 2.5, ease: 'sine.inOut' }, 0)
      /* Act II — collapse into the vortex, rim appears */
      .to(shot, { collapse: 1, duration: 2.15, ease: 'power3.inOut' }, 2.35)
      .to(shot, { dist: 9.5, yaw: 1.25, pitch: 0.8, lookY: -1.5, duration: 2.0, ease: 'sine.inOut' }, 2.35)
      .to(shot, { ringGlow: 1, duration: 0.9, ease: 'power2.out' }, 3.3)
      .to(shot, { ember: 0.35, duration: 1.4 }, 3.5)
      /* Act III — the dive */
      .to(shot, { dist: 1.5, pitch: 1.45, lookY: -2.6, fov: 52, duration: 1.35, ease: 'power3.in' }, 4.55)
      .to(shot, { beanFade: 0, duration: 0.75, ease: 'power2.in' }, 4.85)
      .to(shot, { ringGlow: 0, duration: 0.4 }, 5.3)
      .to(shot, { cremaO: 1, duration: 0.5, ease: 'power1.inOut' }, 5.3)
      .to(shot, { cremaCalm: 0.55, duration: 1.2, ease: 'sine.out' }, 5.9)
      .to(shot, { fov: 46, duration: 1.2, ease: 'sine.out' }, 5.9);
  }

  /* ── Exit: crema → cream, letterbox opens onto the hero ────── */
  var cleanupDone = false;
  function cleanup() {
    if (cleanupDone) return;
    cleanupDone = true;
    gsap.ticker.remove(tick);
    if (scene3d) scene3d.dispose();
    root.style.display = 'none';
    announceDone();
  }

  function exit() {
    if (exiting) return;
    exiting = true;
    var tl = gsap.timeline({ defaults: { ease: 'power3.inOut' }, onComplete: cleanup });
    if (scene3d) {
      tl.to(shot, { cremaCream: 1, cremaCalm: 0.9, duration: 1.05, ease: 'sine.inOut' }, 0);
    } else {
      tl.to('.lc-veil', { opacity: 1, duration: 0.9, ease: 'sine.inOut' }, 0);
    }
    tl.to('.lc-brand', { opacity: 0, y: -30, duration: 0.7, ease: 'power2.in' }, 0.25)
      .to('.lc-bar-inner', { opacity: 0, duration: 0.45, ease: 'power2.in' }, 0.1)
      .to('.lc-progressline', { opacity: 0, duration: 0.4 }, 0.3)
      .add(announceDone, 0.75) /* hero animation starts under the opening frame */
      .to('.lc-bar-top', { yPercent: -101, duration: 1.05, ease: 'power4.inOut' }, 0.7)
      .to('.lc-bar-bottom', { yPercent: 101, duration: 1.05, ease: 'power4.inOut' }, 0.7)
      .to([canvas, '.lc-swirl2d', '.lc-vignette', '.lc-grain', '.lc-veil'],
        { opacity: 0, duration: 0.95, ease: 'sine.inOut' }, 0.85);
  }

  /* Reduced motion: no film — quiet fade through and straight in. */
  function exitReduced() {
    if (exiting) return;
    exiting = true;
    announceDone();
    gsap.to(root, { opacity: 0, duration: 0.6, ease: 'sine.out', onComplete: cleanup });
  }

  /* ── Main loop ──────────────────────────────────────────────── */
  var playhead = 0;
  var last = performance.now() / 1000;

  function tick() {
    var now = performance.now() / 1000;
    var dt = Math.min(now - last, 0.05);
    last = now;
    var t = now;

    if (!pushed && loaded && state.target >= 91.5) pushFull(false);

    /* displayed % chases the target so it always glides */
    var k = 1 - Math.exp(-dt * 3.4 * chaseBoost);
    state.shown = state.shown + (state.target - state.shown) * k;
    if (state.target >= 100 && state.shown > 99.4) state.shown = 100;
    renderReadout(state.shown);

    if (scene3d) {
      playhead = lerp(playhead, (state.shown / 100) * CINE, clamp(dt * 3.0 * chaseBoost, 0, 1));
      cine.time(Math.min(playhead, CINE - 0.0001), false);
      scene3d.update(t, dt);
      if (state.shown >= 100 && playhead > CINE - 0.06) {
        reduced ? exitReduced() : exit();
      }
    } else if (state.shown >= 100) {
      reduced ? exitReduced() : exit();
    }
  }
  gsap.ticker.add(tick);

  /* Hard safety net: whatever happens, the site opens. */
  setTimeout(function () {
    if (!cleanupDone) {
      announceDone();
      gsap.to(root, { opacity: 0, duration: 0.5, onComplete: cleanup });
    }
  }, 5000);

  /* Debug/testing hook */
  window.LiceriaIntro = {
    seek: function (p) {
      pace.kill();
      pushed = true;
      gsap.killTweensOf(state);
      state.target = p;
      state.shown = p;
      playhead = (p / 100) * CINE;
    },
    skip: skip,
    state: state
  };
})();
