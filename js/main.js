// GSAP and ScrollTrigger initialization
gsap.registerPlugin(ScrollTrigger);

const prefersReducedMotion = window.matchMedia(
  "(prefers-reduced-motion: reduce)",
).matches;

// --- 1. Smooth Scrolling with Lenis ---
const lenis = new Lenis({
  duration: 1.2,
  easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
  direction: "vertical",
  gestureDirection: "vertical",
  smooth: true,
  mouseMultiplier: 1,
  smoothTouch: false,
  touchMultiplier: 2,
  infinite: false,
});

// Single driver: GSAP's ticker runs Lenis (a second rAF loop here would
// double-pump the scroll every frame and cause visible jank).
lenis.on("scroll", ScrollTrigger.update);

gsap.ticker.add((time) => {
  lenis.raf(time * 1000);
});
gsap.ticker.lagSmoothing(0, 0);

// --- 2. Custom Cursor ---
const cursor = document.querySelector(".cursor");
const cursorFollower = document.querySelector(".cursor-follower");
const hoverTargets = document.querySelectorAll(".hover-target");

if (cursor && cursorFollower && window.innerWidth > 992) {
  let mouseX = 0,
    mouseY = 0;
  let cursorX = 0,
    cursorY = 0;
  let followerX = 0,
    followerY = 0;

  document.addEventListener("mousemove", (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
  });

  // Animation loop for cursor smooth following
  gsap.ticker.add(() => {
    cursorX += (mouseX - cursorX) * 0.5;
    cursorY += (mouseY - cursorY) * 0.5;

    followerX += (mouseX - followerX) * 0.15;
    followerY += (mouseY - followerY) * 0.15;

    // xPercent keeps the dot centered on the pointer (gsap transforms would
    // otherwise overwrite the CSS translate(-50%,-50%) centering)
    gsap.set(cursor, { x: cursorX, y: cursorY, xPercent: -50, yPercent: -50 });
    gsap.set(cursorFollower, {
      x: followerX,
      y: followerY,
      xPercent: -50,
      yPercent: -50,
    });
  });

  // Hover Effects
  hoverTargets.forEach((target) => {
    target.addEventListener("mouseenter", () => {
      cursor.classList.add("hover");
      cursorFollower.classList.add("hover");
    });
    target.addEventListener("mouseleave", () => {
      cursor.classList.remove("hover");
      cursorFollower.classList.remove("hover");
    });
  });
}

// --- 3. Magnetic Buttons ---
const magneticEls = document.querySelectorAll(".magnetic, .magnetic-btn");

magneticEls.forEach((el) => {
  if (window.innerWidth > 992) {
    el.addEventListener("mousemove", function (e) {
      const position = el.getBoundingClientRect();
      // clientX/Y match getBoundingClientRect's viewport space (pageX drifts once scrolled)
      const x = e.clientX - position.left - position.width / 2;
      const y = e.clientY - position.top - position.height / 2;

      const strength = el.classList.contains("magnetic-btn") ? 20 : 10;

      gsap.to(el, {
        x: x * (strength / 100),
        y: y * (strength / 100),
        duration: 0.5,
        ease: "power3.out",
      });
    });

    el.addEventListener("mouseleave", function () {
      gsap.to(el, {
        x: 0,
        y: 0,
        duration: 0.5,
        ease: "elastic.out(1, 0.3)",
      });
    });
  }
});

// --- 4. Hero Animations (Initial Load) ---
/* OLD HERO ANIMATION REPLACED BY PRELOADER */

// --- 5. Parallax on Mouse Move (Hero) ---
const parallaxElements = document.querySelectorAll(".parallax-mouse");
const quickTos = Array.from(parallaxElements).map((el) => ({
  x: gsap.quickTo(el, "x", { duration: 0.8, ease: "power2.out" }),
  y: gsap.quickTo(el, "y", { duration: 0.8, ease: "power2.out" }),
  speed: parseFloat(el.getAttribute("data-speed")),
}));

document.addEventListener(
  "mousemove",
  (e) => {
    if (window.innerWidth > 992) {
      const x = (e.clientX - window.innerWidth / 2) / 100;
      const y = (e.clientY - window.innerHeight / 2) / 100;
      quickTos.forEach((qt) => {
        qt.x(x * qt.speed);
        qt.y(y * qt.speed);
      });
    }
  },
  { passive: true },
);

// --- 6. ScrollTrigger Animations ---

// Split headings into chars BEFORE building the reveal timelines below,
// so each timeline can animate the chars it finds.
splitText(".split-text-target");

// Parallax Background elements (Leaves)
if (!prefersReducedMotion)
  gsap.utils.toArray(".parallax-bg").forEach((bg) => {
    const speed = bg.getAttribute("data-speed");
    gsap.to(bg, {
      y: () => ScrollTrigger.maxScroll(window) * speed,
      ease: "none",
      scrollTrigger: {
        trigger: "body",
        start: "top top",
        end: "bottom bottom",
        scrub: 1,
      },
    });
  });

// Section Title Reveal
gsap.utils.toArray(".section-reveal").forEach((section) => {
  const tag = section.querySelector(".tag");
  const tagNote = section.querySelector(".tag-note");
  const title = section.querySelector(".section-title");
  const subtitle = section.querySelector(".section-subtitle");

  if (prefersReducedMotion) {
    if (title)
      gsap.set(title.querySelectorAll(".char"), {
        y: 0,
        rotation: 0,
        opacity: 1,
      });
    return;
  }

  const tl = gsap.timeline({
    scrollTrigger: {
      trigger: section,
      start: "top 80%",
    },
  });

  if (tag)
    tl.fromTo(
      tag,
      { y: 20, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.6, ease: "power3.out" },
    );
  if (tagNote)
    tl.fromTo(
      tagNote,
      { y: 16, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.5, ease: "power3.out" },
      "-=0.4",
    );
  if (title) {
    tl.fromTo(
      title,
      { y: 30, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.7, ease: "power3.out" },
      "-=0.4",
    );
    const chars = title.querySelectorAll(".char");
    if (chars.length)
      tl.to(
        chars,
        {
          y: 0,
          rotation: 0,
          opacity: 1,
          duration: 0.8,
          stagger: 0.02,
          ease: "power3.out",
        },
        "<",
      );
  }
  if (subtitle)
    tl.fromTo(
      subtitle,
      { y: 30, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.7, ease: "power3.out" },
      "-=0.5",
    );
});

// Stagger Cards Reveal
gsap.utils.toArray(".product-grid").forEach((grid) => {
  const cards = grid.querySelectorAll(".card-reveal");
  gsap.fromTo(
    cards,
    { y: 50, opacity: 0 },
    {
      y: 0,
      opacity: 1,
      duration: 0.8,
      stagger: 0.15,
      ease: "power3.out",
      scrollTrigger: {
        trigger: grid,
        start: "top 85%",
      },
    },
  );
});

// Discover Feature List Stagger
const featuresList = document.querySelector(".features-list");
if (featuresList) {
  gsap.fromTo(
    featuresList.querySelectorAll(".stagger-item"),
    { x: -50, opacity: 0 },
    {
      x: 0,
      opacity: 1,
      duration: 0.8,
      stagger: 0.2,
      ease: "power3.out",
      scrollTrigger: {
        trigger: featuresList,
        start: "top 80%",
      },
    },
  );
}

// Hero cup: scroll-linked cinematic drift — works on touch too, where mouse parallax can't
if (!prefersReducedMotion) {
  gsap.to(".main-cup-wrapper", {
    yPercent: 12,
    rotation: 6,
    scale: 0.94,
    ease: "none",
    scrollTrigger: {
      trigger: ".hero",
      start: "top top",
      end: "bottom top",
      scrub: 1,
    },
  });
  // (circle text already spins via CSS keyframes — scroll-scrubbing its
  // transform would fight the animation, so we scrub opacity instead)
  gsap.to(".hero-circle-text", {
    opacity: 0.1,
    ease: "none",
    scrollTrigger: {
      trigger: ".hero",
      start: "top top",
      end: "bottom top",
      scrub: 1.5,
    },
  });
}

// Image Parallax Effect
if (!prefersReducedMotion)
  gsap.utils.toArray(".parallax-img img").forEach((img) => {
    gsap.to(img, {
      yPercent: 15,
      ease: "none",
      scrollTrigger: {
        trigger: img.parentElement,
        start: "top bottom",
        end: "bottom top",
        scrub: true,
      },
    });
  });

// --- 7. Navbar Scroll Effect & Active Link Tracking ---
const navbar = document.getElementById("navbar");
const navLinksArr = document.querySelectorAll("#navLinks a");

window.addEventListener(
  "scroll",
  () => {
    if (window.scrollY > 50) {
      navbar.classList.add("scrolled");
    } else {
      navbar.classList.remove("scrolled");
    }
  },
  { passive: true },
);

// --- MOBILE MENU TOGGLER & CLICK ACTIVE LINK SWITCH ---
const mobileBtn = document.querySelector(".nav-mobile-btn");
const navLinks = document.getElementById("navLinks");
if (mobileBtn && navLinks) {
  mobileBtn.addEventListener("click", () => {
    mobileBtn.classList.toggle("open");
    navLinks.classList.toggle("open");

    if (navLinks.classList.contains("open")) {
      lenis.stop();
    } else {
      lenis.start();
    }
  });

  navLinks.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      mobileBtn.classList.remove("open");
      navLinks.classList.remove("open");
      lenis.start();

      navLinksArr.forEach((l) => l.classList.remove("active"));
      link.classList.add("active");
    });
  });
}

// --- 8. Stat Number Counters (fire when the stats scroll into view) ---
function initCounters() {
  ScrollTrigger.create({
    trigger: ".hero-stats",
    start: "top 92%",
    once: true,
    onEnter: runCounters,
  });
}

function runCounters() {
  const counters = document.querySelectorAll(".stat-number");
  counters.forEach((counter) => {
    const target = +counter.getAttribute("data-target");
    const prefix = counter.getAttribute("data-prefix") || "";
    const state = { val: 0 }; // tween a plain number, not the "1,000+" markup

    gsap.to(state, {
      val: target,
      duration: 2.5,
      ease: "power3.out",
      onUpdate: function () {
        counter.textContent =
          prefix + Math.round(state.val).toLocaleString() + "+";
      },
    });
  });
}

// --- Custom Split Text Utility ---
function splitText(selector) {
  document.querySelectorAll(selector).forEach((el) => {
    const text = el.textContent.trim();
    el.innerHTML = "";
    text.split(/\s+/).forEach((word, i) => {
      const wordSpan = document.createElement("span");
      wordSpan.style.display = "inline-block";
      word.split("").forEach((char) => {
        const charSpan = document.createElement("span");
        charSpan.className = "char";
        charSpan.innerText = char;
        wordSpan.appendChild(charSpan);
      });
      el.appendChild(wordSpan);
      el.appendChild(document.createTextNode(" "));
    });
  });
}
// (split already ran once, before the section-reveal timelines were built)

function playHeroAnimation() {
  const tl = gsap.timeline();
  // Hero split text stagger
  tl.to(".hero-title .char", {
    y: 0,
    rotation: 0,
    opacity: 1,
    duration: 1,
    stagger: 0.02,
    ease: "back.out(1.2)",
  })
    .fromTo(
      ".hero-anim",
      { y: 50, opacity: 0 },
      { y: 0, opacity: 1, duration: 1, stagger: 0.1, ease: "power3.out" },
      "-=0.5",
    )
    .fromTo(
      ".main-cup",
      { y: 100, scale: 0.8, opacity: 0 },
      {
        y: 0,
        scale: 1,
        opacity: 1,
        duration: 1.5,
        ease: "elastic.out(1, 0.7)",
      },
      "-=1",
    )
    .fromTo(
      ".hero-anim-stats",
      { y: 50, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.8, ease: "power3.out" },
      "-=0.8",
    );
}

// --- Helper Linear Interpolation ---
const lerp = (a, b, t) => a + (b - a) * t;

// --- BACKGROUND 3D WEBGL SPACE ---
let bgScene, bgCamera, bgRenderer, bgBeans, bgSparks, bgSparksGeo, bgSparksPos;
const isMobile = window.innerWidth < 768;
const bgBeanCount = isMobile ? 12 : 22;
const bgSparkCount = isMobile ? 40 : 75;
const bgBeansData = [];
const bgSparksData = [];
let bgMouseX = 0,
  bgMouseY = 0;
let bgScrollVelocity = 0;

function initBg3d() {
  const canvas = document.getElementById("bg3dCanvas");
  if (!canvas || prefersReducedMotion || typeof THREE === "undefined") return;

  // 1. Scene, Camera, Renderer
  bgScene = new THREE.Scene();
  bgScene.fog = new THREE.FogExp2(0x0a0705, 0.05);

  bgCamera = new THREE.PerspectiveCamera(
    45,
    window.innerWidth / window.innerHeight,
    0.1,
    100,
  );
  bgCamera.position.z = 12;

  bgRenderer = new THREE.WebGLRenderer({
    canvas: canvas,
    antialias: true,
    alpha: true,
    powerPreference: "low-power",
  });
  bgRenderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.25)); // Performance cap
  bgRenderer.setSize(window.innerWidth, window.innerHeight);

  // Lights
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.3);
  bgScene.add(ambientLight);
  const dirLight = new THREE.DirectionalLight(0xffe5cc, 0.85);
  dirLight.position.set(5, 8, 5);
  bgScene.add(dirLight);
  const pointLight = new THREE.PointLight(0xff5511, 0.5, 15);
  pointLight.position.set(-3, -2, 2);
  bgScene.add(pointLight);

  // 2. Coffee Bean Geometry (ellipsoid)
  const geom = new THREE.SphereGeometry(0.35, 14, 12);
  const pos = geom.attributes.position;
  const v = new THREE.Vector3();
  for (let i = 0; i < pos.count; i++) {
    v.fromBufferAttribute(pos, i);
    let x = v.x * 0.66,
      y = v.y * 0.35,
      z = v.z * 0.5;
    if (y > 0) y *= 1 - 0.62 * Math.exp(-(z * z) / 0.02);
    y += 0.05 * Math.cos(x * 2.4);
    pos.setXYZ(i, x, y, z);
  }
  geom.computeVertexNormals();

  // Coffee Bean Material
  const mat = new THREE.MeshStandardMaterial({
    color: 0x3d2516,
    roughness: 0.6,
    metalness: 0.1,
  });

  // Coffee Bean Instanced Mesh
  bgBeans = new THREE.InstancedMesh(geom, mat, bgBeanCount);
  const dummy = new THREE.Object3D();

  for (let i = 0; i < bgBeanCount; i++) {
    const rx = (Math.random() - 0.5) * 14;
    const ry = (Math.random() - 0.5) * 10;
    const rz = (Math.random() - 0.5) * 6 - 2;

    bgBeansData.push({
      x: rx,
      y: ry,
      z: rz,
      rotX: Math.random() * Math.PI * 2,
      rotY: Math.random() * Math.PI * 2,
      rotZ: Math.random() * Math.PI * 2,
      speedX: (Math.random() - 0.5) * 0.02,
      speedY: (Math.random() - 0.5) * 0.02,
      rotSpeedX: (Math.random() - 0.5) * 0.4,
      rotSpeedY: (Math.random() - 0.5) * 0.4,
      wobbleAmp: 0.2 + Math.random() * 0.4,
      wobbleFreq: 0.2 + Math.random() * 0.8,
      wobblePhase: Math.random() * Math.PI * 2,
    });

    dummy.position.set(rx, ry, rz);
    dummy.rotation.set(Math.random() * Math.PI, Math.random() * Math.PI, 0);
    dummy.scale.setScalar(0.7 + Math.random() * 0.6);
    dummy.updateMatrix();
    bgBeans.setMatrixAt(i, dummy.matrix);
  }
  bgScene.add(bgBeans);

  // 3. Floating Sparks
  bgSparksGeo = new THREE.BufferGeometry();
  bgSparksPos = new Float32Array(bgSparkCount * 3);

  for (let i = 0; i < bgSparkCount; i++) {
    const sx = (Math.random() - 0.5) * 16;
    const sy = (Math.random() - 0.5) * 12;
    const sz = (Math.random() - 0.5) * 12 + 1;

    bgSparksData.push({
      x: sx,
      y: sy,
      z: sz,
      vy: 0.15 + Math.random() * 0.35,
      wFreq: 0.4 + Math.random() * 1.2,
      wAmp: 0.1 + Math.random() * 0.3,
      wPhase: Math.random() * Math.PI * 2,
    });

    bgSparksPos[i * 3] = sx;
    bgSparksPos[i * 3 + 1] = sy;
    bgSparksPos[i * 3 + 2] = sz;
  }

  bgSparksGeo.setAttribute(
    "position",
    new THREE.BufferAttribute(bgSparksPos, 3),
  );

  // Circular Texture for Particles
  const canvasTex = document.createElement("canvas");
  canvasTex.width = canvasTex.height = 32;
  const ctx = canvasTex.getContext("2d");
  const grad = ctx.createRadialGradient(16, 16, 0, 16, 16, 16);
  grad.addColorStop(0, "rgba(255,180,100,1)");
  grad.addColorStop(0.3, "rgba(213,180,151,0.6)");
  grad.addColorStop(1, "rgba(213,180,151,0)");
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, 32, 32);
  const sparkTexture = new THREE.CanvasTexture(canvasTex);

  const sparkMat = new THREE.PointsMaterial({
    color: 0xffcc88,
    size: 0.22,
    map: sparkTexture,
    transparent: true,
    opacity: 0.45,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
  });

  bgSparks = new THREE.Points(bgSparksGeo, sparkMat);
  bgScene.add(bgSparks);

  // Resize listener
  window.addEventListener("resize", () => {
    bgRenderer.setSize(window.innerWidth, window.innerHeight);
    bgCamera.aspect = window.innerWidth / window.innerHeight;
    bgCamera.updateProjectionMatrix();
  });

  // Mouse Listener (desktop) / Gyroscope (mobile) — the 3D space always answers the user
  if (window.innerWidth > 992) {
    document.addEventListener("mousemove", (e) => {
      bgMouseX = (e.clientX / window.innerWidth - 0.5) * 2.5;
      bgMouseY = (e.clientY / window.innerHeight - 0.5) * 2.5;
    });
  } else if (
    window.DeviceOrientationEvent &&
    typeof DeviceOrientationEvent.requestPermission !== "function"
  ) {
    // Android & non-permission browsers: tilt the phone, tilt the space
    window.addEventListener("deviceorientation", (e) => {
      if (e.gamma === null) return;
      bgMouseX = Math.max(-1.5, Math.min(1.5, (e.gamma / 45) * 1.5));
      bgMouseY = Math.max(-1.5, Math.min(1.5, ((e.beta - 45) / 45) * 1.2));
    });
  }

  // Animation Loop
  let lastTime = 0;
  function animateBg(time) {
    requestAnimationFrame(animateBg);
    const dt = Math.min((time - lastTime) * 0.001, 0.1);
    lastTime = time;

    // Track scroll velocity via Lenis
    bgScrollVelocity = lerp(
      bgScrollVelocity,
      Math.abs(lenis.velocity || 0) * 0.05,
      0.1,
    );

    // Damped camera movement based on mouse
    bgCamera.position.x = lerp(bgCamera.position.x, bgMouseX, 0.05);
    bgCamera.position.y = lerp(bgCamera.position.y, -bgMouseY, 0.05);
    bgCamera.lookAt(0, 0, 0);

    // Update Coffee Beans (reuse the setup-time dummy — allocating a fresh
    // Object3D every frame churns the GC)
    const dummyObj = dummy;
    for (let i = 0; i < bgBeanCount; i++) {
      const data = bgBeansData[i];

      // Drift vertical & horizontal
      data.y += data.speedY * dt * (1 + bgScrollVelocity * 4);
      data.x += data.speedX * dt;

      // Wrap around bounds
      if (data.y > 6.5) data.y = -6.5;
      if (data.y < -6.5) data.y = 6.5;
      if (data.x > 9.5) data.x = -9.5;
      if (data.x < -9.5) data.x = 9.5;

      // Rotations
      data.rotX += data.rotSpeedX * dt * (1 + bgScrollVelocity * 3);
      data.rotY += data.rotSpeedY * dt * (1 + bgScrollVelocity * 3);

      // Wobble
      const wobble =
        Math.sin(time * 0.001 * data.wobbleFreq + data.wobblePhase) *
        data.wobbleAmp;

      dummyObj.position.set(data.x + wobble, data.y, data.z);
      dummyObj.rotation.set(data.rotX, data.rotY, data.rotZ);
      dummyObj.scale.setScalar(0.75 + 0.1 * wobble);
      dummyObj.updateMatrix();
      bgBeans.setMatrixAt(i, dummyObj.matrix);
    }
    bgBeans.instanceMatrix.needsUpdate = true;

    // Update Sparks
    const positions = bgSparksGeo.attributes.position.array;
    for (let i = 0; i < bgSparkCount; i++) {
      const data = bgSparksData[i];

      data.y += data.vy * dt * (1 + bgScrollVelocity * 6);
      if (data.y > 6) data.y = -6;

      const wobbleX =
        Math.sin(time * 0.001 * data.wFreq + data.wPhase) * data.wAmp;

      positions[i * 3] = data.x + wobbleX;
      positions[i * 3 + 1] = data.y;
      positions[i * 3 + 2] = data.z;
    }
    bgSparksGeo.attributes.position.needsUpdate = true;

    // Subtle fog adjustments based on scroll themes
    const bodyCls = document.body.classList;
    if (bodyCls.contains("theme-crema")) {
      bgScene.fog.color.setHex(0xfdfbf7);
      mat.color.setHex(0x6b4420);
      mat.roughness = 0.7;
    } else if (bodyCls.contains("theme-moss")) {
      bgScene.fog.color.setHex(0x242e25);
      mat.color.setHex(0x302015);
      mat.roughness = 0.5;
    } else {
      bgScene.fog.color.setHex(0x0a0705);
      mat.color.setHex(0x2b1608);
      mat.roughness = 0.6;
    }

    bgRenderer.render(bgScene, bgCamera);
  }

  requestAnimationFrame(animateBg);
  document.body.classList.add("intro-complete");
}

// --- CHAPTER SCROLL THEME TRANSITIONS ---
// Swap theme classes only — never assign body.className directly,
// it would wipe 'intro-complete' and hide the 3D background.
const THEME_CLASSES = [
  "theme-espresso",
  "theme-crema",
  "theme-origin",
  "theme-moss",
];
function setTheme(theme) {
  if (document.body.classList.contains(theme)) return;
  document.body.classList.remove(...THEME_CLASSES);
  document.body.classList.add(theme);
}

function initScrollThemes() {
  // The intro exits by brightening to cream, so the hero opens in crema
  // for a seamless handoff; darkness returns in the Origin chapter.
  const sections = [
    { id: "#home", theme: "theme-crema" },
    { id: "#shop", theme: "theme-crema" },
    { id: "#about", theme: "theme-moss" },
    { id: "#ritual", theme: "theme-crema" },
    { id: "#blog", theme: "theme-espresso" },
    { id: "#contact", theme: "theme-espresso" },
  ];

  sections.forEach((sec) => {
    const el = document.querySelector(sec.id);
    if (el) {
      ScrollTrigger.create({
        trigger: el,
        start: "top 45%",
        end: "bottom 45%",
        onToggle: (self) => {
          if (self.isActive) {
            setTheme(sec.theme);

            // Set active navbar link based on scrolled section
            navLinksArr.forEach((link) => {
              let targetId = sec.id;
              if (sec.id === "#blog") {
                targetId = "#contact"; // Map newsletter section to contact link
              }
              if (link.getAttribute("href") === targetId) {
                link.classList.add("active");
              } else {
                link.classList.remove("active");
              }
            });
          }
        },
      });
    }
  });
}

// --- BREW RITUAL STEPPER LOGIC ---
let stepperTimer = null;
let currentStep = 1;

function playStep(stepIndex) {
  currentStep = stepIndex;

  // Update buttons state
  document.querySelectorAll(".stepper-step").forEach((btn) => {
    btn.classList.remove("active", "playing");
    const pBar = btn.querySelector(".step-progress-bar i");
    if (pBar) {
      pBar.style.transition = "none";
      pBar.style.transform = "scaleX(0)";
    }
  });

  // Update illustrations state
  document.querySelectorAll(".stepper-illust").forEach((img) => {
    img.classList.remove("active");
  });

  const activeBtn = document.querySelector(
    `.stepper-step[data-step="${stepIndex}"]`,
  );
  const activeImg = document.querySelector(
    `.stepper-illust[data-step="${stepIndex}"]`,
  );

  if (activeBtn) {
    activeBtn.classList.add("active");

    // Auto-scroll the horizontal carousel on mobile to center the active item WITHOUT yanking vertical page scroll
    if (window.innerWidth <= 767) {
      const container = document.querySelector(".stepper-steps");
      if (container) {
        const scrollPos = activeBtn.offsetLeft - (container.offsetWidth / 2) + (activeBtn.offsetWidth / 2);
        container.scrollTo({
          left: scrollPos,
          behavior: "smooth"
        });
      }
    }

    // Animate progress bar (5s auto advance)
    setTimeout(() => {
      activeBtn.classList.add("playing");
      const pBar = activeBtn.querySelector(".step-progress-bar i");
      if (pBar) {
        pBar.style.transition = "transform 5s linear";
        pBar.style.transform = "scaleX(1)";
      }
    }, 50);
  }

  if (activeImg) {
    activeImg.classList.add("active");
  }

  // Timer for auto-play (only if not manually interacted)
  clearTimeout(stepperTimer);
  if (!stepperInteracted) {
    stepperTimer = setTimeout(() => {
      let nextStep = (stepIndex % 4) + 1;
      playStep(nextStep);
    }, 5050);
  }
}

// Global flag to stop autoplay when user interacts
let stepperInteracted = false;

// Pause the autoplay loop when the tab is hidden (no invisible cycling)
document.addEventListener("visibilitychange", () => {
  if (document.hidden) {
    clearTimeout(stepperTimer);
  } else if (siteStarted && document.querySelector(".stepper-step")) {
    playStep(currentStep);
  }
});

function initBrewStepper() {
  const steps = document.querySelectorAll(".stepper-step");
  if (!steps.length) return;

  steps.forEach((step) => {
    step.addEventListener("click", () => {
      stepperInteracted = true;
      clearTimeout(stepperTimer);
      const stepIdx = parseInt(step.getAttribute("data-step"));
      playStep(stepIdx);
      clearTimeout(stepperTimer); // Clear again just in case playStep restarted it
    });
  });

  // Mobile Swipe Sync: If user manually scrolls the horizontal carousel, update active step
  if (window.innerWidth <= 767) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && entry.intersectionRatio >= 0.5) {
            const stepIdx = parseInt(entry.target.getAttribute("data-step"));
            if (currentStep !== stepIdx) {
              stepperInteracted = true;
              clearTimeout(stepperTimer);
              playStep(stepIdx);
              clearTimeout(stepperTimer); // Prevent autoplay from restarting
            }
          }
        });
      },
      {
        root: document.querySelector(".stepper-steps"),
        threshold: 0.5,
      },
    );

    steps.forEach((step) => observer.observe(step));
  }

  // Start autoplay on first step
  playStep(1);
}

// --- TESTIMONIALS STACKED DECK LOGIC ---
function initTestimonialsDeck() {
  // Mobile: CSS scroll-snap handles testimonials natively
  if (window.innerWidth <= 767) return;

  const deck = document.querySelector(".testi-deck");
  if (!deck) return;

  const cards = Array.from(deck.querySelectorAll(".testi-card"));
  let currentTop = 0;

  function updateDeck() {
    cards.forEach((card, index) => {
      // Relative index in the circular queue
      let relIndex = (index - currentTop + cards.length) % cards.length;
      card.classList.remove("swipe-out");

      if (relIndex === 0) {
        // Active top card
        card.style.transform = "translateZ(0px) translateY(0px) rotate(0deg)";
        card.style.opacity = "1";
        card.style.pointerEvents = "auto";
        card.style.zIndex = "3";
      } else if (relIndex === 1) {
        card.style.transform =
          "translateZ(-30px) translateY(14px) scale(0.96) rotate(-2deg)";
        card.style.opacity = "0.85";
        card.style.pointerEvents = "none";
        card.style.zIndex = "2";
      } else if (relIndex === 2) {
        card.style.transform =
          "translateZ(-60px) translateY(28px) scale(0.92) rotate(2deg)";
        card.style.opacity = "0.65";
        card.style.pointerEvents = "none";
        card.style.zIndex = "1";
      } else {
        // Hidden backing cards
        card.style.transform =
          "translateZ(-90px) translateY(42px) scale(0.88) rotate(0deg)";
        card.style.opacity = "0";
        card.style.pointerEvents = "none";
        card.style.zIndex = "0";
      }
    });
  }

  const prevBtn = document.getElementById("prevTesti");
  const nextBtn = document.getElementById("nextTesti");

  if (nextBtn) {
    nextBtn.addEventListener("click", () => {
      const topCard = cards[currentTop];
      topCard.classList.add("swipe-out");
      setTimeout(() => {
        currentTop = (currentTop + 1) % cards.length;
        updateDeck();
      }, 350); // Wait for card fly-out animation
    });
  }

  if (prevBtn) {
    prevBtn.addEventListener("click", () => {
      currentTop = (currentTop - 1 + cards.length) % cards.length;
      const newTopCard = cards[currentTop];

      newTopCard.style.transform =
        "translateX(-120%) translateY(-30px) rotate(-15deg)";
      newTopCard.style.opacity = "0";
      newTopCard.offsetHeight; // Force reflow
      updateDeck();
    });
  }

  // Touch swipe: flick the top card like a real deck
  let touchStartX = 0,
    touchStartY = 0,
    swiping = false;
  deck.addEventListener(
    "touchstart",
    (e) => {
      touchStartX = e.touches[0].clientX;
      touchStartY = e.touches[0].clientY;
      swiping = true;
    },
    { passive: true },
  );

  deck.addEventListener(
    "touchmove",
    (e) => {
      if (!swiping) return;
      const dx = e.touches[0].clientX - touchStartX;
      const dy = e.touches[0].clientY - touchStartY;
      if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 10) {
        const topCard = cards[currentTop];
        topCard.style.transition = "none";
        topCard.style.transform = `translateX(${dx}px) rotate(${dx * 0.05}deg)`;
      }
    },
    { passive: true },
  );

  deck.addEventListener(
    "touchend",
    (e) => {
      if (!swiping) return;
      swiping = false;
      const dx = e.changedTouches[0].clientX - touchStartX;
      const topCard = cards[currentTop];
      topCard.style.transition = "";
      if (Math.abs(dx) > 70) {
        topCard.style.transform = `translateX(${dx > 0 ? "" : "-"}120%) translateY(-30px) rotate(${dx > 0 ? 15 : -15}deg)`;
        topCard.style.opacity = "0";
        setTimeout(() => {
          currentTop = (currentTop + 1) % cards.length;
          updateDeck();
        }, 300);
      } else {
        updateDeck(); // snap back
      }
    },
    { passive: true },
  );

  updateDeck();
}

// --- Cinematic intro handshake ---
// js/intro.js runs the "From the Roast" loading sequence and fires
// `liceria:introdone` as the letterbox opens; the hero animates
// underneath the opening frame for a seamless handoff.
lenis.stop();
window.scrollTo(0, 0);
function initSmoothScrollAnchors() {
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      const targetId = this.getAttribute("href");
      if (targetId === "#") return;
      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        lenis.scrollTo(target);
      }
    });
  });
}

let siteStarted = false;
function startSite() {
  if (siteStarted) return;
  siteStarted = true;
  lenis.start();
  playHeroAnimation();
  initCounters();

  // Initialize Karioffee Cinematic Upgrades
  initBg3d();
  initScrollThemes();
  initBrewStepper();
  initTestimonialsDeck();
  initSmoothScrollAnchors();
}
if (window.__liceriaIntroDone || !document.getElementById("liceria-intro")) {
  startSite();
} else {
  window.addEventListener("liceria:introdone", startSite, { once: true });
  setTimeout(startSite, 6000); // Absolute safety
}

// --- Scroll Progress Ring ---
const circle = document.querySelector(".progress-ring__circle");
const radius = circle.r.baseVal.value;
const circumference = radius * 2 * Math.PI;
circle.style.strokeDasharray = `${circumference} ${circumference}`;
circle.style.strokeDashoffset = circumference;

lenis.on("scroll", (e) => {
  const scrollPercent = e.scroll / (e.limit || 1);
  const offset = circumference - scrollPercent * circumference;
  circle.style.strokeDashoffset = offset;
});

// --- Kinetic Marquee ---
const marqueeContent = document.querySelector(".marquee-content");
if (marqueeContent) {
  // Clone for infinite effect
  marqueeContent.appendChild(marqueeContent.firstElementChild.cloneNode(true));

  let xPos = 0;
  let direction = -1;
  let speed = 1;

  let cachedScrollWidth = marqueeContent.scrollWidth;
  window.addEventListener(
    "resize",
    () => {
      cachedScrollWidth = marqueeContent.scrollWidth;
    },
    { passive: true },
  );

  // Increase speed based on scroll velocity
  lenis.on("scroll", (e) => {
    direction = e.velocity > 0 ? -1 : 1;
    speed = 1 + Math.abs(e.velocity) * 0.05;
  });

  gsap.ticker.add((time, deltaTime) => {
    // px-per-second, scaled by real frame delta — same speed on 60Hz and 120Hz
    xPos += 120 * speed * direction * (deltaTime / 1000);
    const halfWidth = -cachedScrollWidth / 2;
    if (xPos <= halfWidth) xPos = 0;
    if (xPos >= 0 && direction === 1) xPos = halfWidth;
    gsap.set(marqueeContent, { x: xPos });

    speed += (1 - speed) * 0.05;
  });
}

// --- 3D Tilt Initialization (desktop only — tilt fights the scroll gesture on touch) ---
if (
  typeof VanillaTilt !== "undefined" &&
  window.matchMedia("(hover: hover)").matches
) {
  VanillaTilt.init(document.querySelectorAll(".card-reveal"), {
    max: 15,
    speed: 400,
    glare: true,
    "max-glare": 0.2,
  });
}

// --- Premium Toast Notifications ---
function showToast(message) {
  let toast = document.querySelector(".toast");
  if (!toast) {
    toast = document.createElement("div");
    toast.className = "toast";
    toast.setAttribute("role", "status");
    document.body.appendChild(toast);
  }
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(showToast._t);
  showToast._t = setTimeout(() => toast.classList.remove("show"), 2800);
}

// --- Newsletter Form (was reloading the page on submit) ---
const newsForm = document.querySelector(".news-form");
if (newsForm) {
  newsForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const email = newsForm.querySelector('input[type="email"]');
    if (email && email.value) {
      showToast("☕ Welcome to the roast — 25% off is in your inbox.");
      email.value = "";
    }
  });
}

// --- Cart & Wishlist micro-interactions (buttons previously did nothing) ---
let cartCount = 0;
const cartBadge = document.querySelector(".cart-badge");
document.querySelectorAll(".btn-cart").forEach((btn) => {
  btn.addEventListener("click", () => {
    cartCount++;
    if (cartBadge) {
      cartBadge.textContent = cartCount;
      gsap.fromTo(
        cartBadge,
        { scale: 1.6 },
        { scale: 1, duration: 0.5, ease: "elastic.out(1, 0.4)" },
      );
    }
    const name =
      btn.closest(".product-card")?.querySelector("h3")?.textContent || "Item";
    showToast(`${name} added to cart`);
    gsap.fromTo(
      btn,
      { scale: 0.85 },
      { scale: 1, duration: 0.4, ease: "back.out(3)" },
    );
  });
});
document.querySelectorAll(".btn-heart").forEach((btn) => {
  btn.addEventListener("click", () => {
    btn.classList.toggle("liked");
    gsap.fromTo(
      btn,
      { scale: 0.8 },
      { scale: 1, duration: 0.45, ease: "back.out(3)" },
    );
  });
});

// --- Upgraded Cursor Drag Hover ---
document.querySelectorAll(".product-card").forEach((card) => {
  card.addEventListener("mouseenter", () => {
    if (cursor) cursor.classList.add("hover");
    if (cursorFollower) {
      cursorFollower.classList.add("hover");
      cursorFollower.classList.add("drag-mode");
    }
    const cursorText = document.querySelector(".cursor-text");
    if (cursorText) cursorText.innerText = "VIEW";
  });
  card.addEventListener("mouseleave", () => {
    if (cursor) cursor.classList.remove("hover");
    if (cursorFollower) {
      cursorFollower.classList.remove("hover");
      cursorFollower.classList.remove("drag-mode");
    }
  });
});
