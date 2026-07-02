import re

html_path = r'c:\Users\pr7n8\Downloads\anti coffee\index.html'
css_path = r'c:\Users\pr7n8\Downloads\anti coffee\css\style.css'
js_path = r'c:\Users\pr7n8\Downloads\anti coffee\js\main.js'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# ----------------- HTML INJECTIONS -----------------
# 1. Preloader and Scroll Progress
preloader_html = '''
  <!-- PRELOADER -->
  <div class="preloader">
    <div class="preloader-counter">0%</div>
    <div class="preloader-overlay preloader-left"></div>
    <div class="preloader-overlay preloader-right"></div>
  </div>

  <!-- SCROLL PROGRESS -->
  <svg class="progress-ring" width="50" height="50">
    <circle class="progress-ring__circle" stroke="#8C5A2B" stroke-width="2" fill="transparent" r="20" cx="25" cy="25"/>
  </svg>
'''
if 'class="preloader"' not in html:
    html = html.replace('<body>', f'<body>\n{preloader_html}')

# 2. Kinetic Marquee
marquee_html = '''
  <!-- KINETIC MARQUEE -->
  <section class="marquee-section">
    <div class="marquee-container">
      <div class="marquee-content">
        <span class="marquee-text">PREMIUM QUALITY ? FRESHLY ROASTED ? ETHICALLY SOURCED ? </span>
        <span class="marquee-text">PREMIUM QUALITY ? FRESHLY ROASTED ? ETHICALLY SOURCED ? </span>
        <span class="marquee-text">PREMIUM QUALITY ? FRESHLY ROASTED ? ETHICALLY SOURCED ? </span>
      </div>
    </div>
  </section>
'''
if 'class="marquee-section"' not in html:
    html = html.replace('<!-- BESTSELLERS -->', f'{marquee_html}\n  <!-- BESTSELLERS -->')

# 3. Vanilla Tilt Script
if 'vanilla-tilt' not in html:
    html = html.replace('<script src="js/main.js"></script>', '<script src="https://cdnjs.cloudflare.com/ajax/libs/vanilla-tilt/1.8.0/vanilla-tilt.min.js"></script>\n  <script src="js/main.js"></script>')

# Add split-text-target class to headings
html = html.replace('<h1 class="hero-title">', '<h1 class="hero-title split-text-target">')
html = html.replace('<h2 class="section-title">', '<h2 class="section-title split-text-target">')

# Modify Cursor Follower to support text
if '<span class="cursor-text"></span>' not in html:
    html = html.replace('<div class="cursor-follower"></div>', '<div class="cursor-follower"><span class="cursor-text"></span></div>')

# ----------------- CSS INJECTIONS -----------------
css_additions = '''
/* --- AWWWARDS UPGRADES --- */
/* Preloader */
.preloader {
  position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
  z-index: 10000; display: flex; justify-content: center; align-items: center;
  pointer-events: none;
}
.preloader-overlay {
  position: absolute; top: 0; width: 50vw; height: 100vh;
  background: var(--text-dark); z-index: 1;
}
.preloader-left { left: 0; }
.preloader-right { right: 0; }
.preloader-counter {
  position: relative; z-index: 2; color: var(--accent-gold);
  font-family: var(--font-serif); font-size: 6rem; font-weight: 700;
}

/* Scroll Progress */
.progress-ring {
  position: fixed; bottom: 30px; right: 30px; z-index: 999;
  transform: rotate(-90deg); opacity: 0.6; mix-blend-mode: difference;
}
.progress-ring__circle {
  stroke-dasharray: 126; stroke-dashoffset: 126;
  transition: stroke-dashoffset 0.1s linear;
}

/* Kinetic Marquee */
.marquee-section {
  padding: 40px 0; background: var(--text-dark);
  color: var(--text-light); overflow: hidden;
  border-top: 1px solid rgba(255,255,255,0.1); border-bottom: 1px solid rgba(255,255,255,0.1);
}
.marquee-container { width: 100%; overflow: hidden; white-space: nowrap; }
.marquee-content { display: inline-flex; align-items: center; }
.marquee-text {
  font-family: var(--font-serif); font-size: 4rem; font-weight: 600;
  text-transform: uppercase; letter-spacing: 4px; padding: 0 20px;
  -webkit-text-fill-color: transparent; -webkit-text-stroke: 1px rgba(255,255,255,0.3);
  transition: -webkit-text-stroke 0.3s;
}
.marquee-text:hover { -webkit-text-stroke: 1px var(--accent-gold); }

/* Split Text */
.char { display: inline-block; opacity: 0; transform: translateY(50px) rotate(15deg); }

/* Upgraded Cursor */
.cursor, .cursor-follower { mix-blend-mode: difference; background: #fff !important; border-color: #fff !important; }
.cursor-follower { display: flex; justify-content: center; align-items: center; }
.cursor-text { font-size: 0; opacity: 0; transition: 0.3s; color: var(--text-dark); font-weight: 600; font-family: var(--font-sans); }
.cursor-follower.drag-mode { width: 80px; height: 80px; mix-blend-mode: normal; background: var(--accent-gold) !important; border-color: var(--accent-gold) !important; }
.cursor-follower.drag-mode .cursor-text { font-size: 0.8rem; opacity: 1; }
'''
if '.preloader' not in css:
    css += css_additions

# ----------------- JS INJECTIONS -----------------
js_additions = '''
// --- Custom Split Text Utility ---
function splitText(selector) {
  document.querySelectorAll(selector).forEach(el => {
    const text = el.innerText;
    el.innerHTML = '';
    text.split(' ').forEach((word, i) => {
      const wordSpan = document.createElement('span');
      wordSpan.style.display = 'inline-block';
      wordSpan.style.marginRight = '10px';
      word.split('').forEach(char => {
        const charSpan = document.createElement('span');
        charSpan.className = 'char';
        charSpan.innerText = char;
        wordSpan.appendChild(charSpan);
      });
      el.appendChild(wordSpan);
    });
  });
}
splitText('.split-text-target');

// --- Preloader & Initial Reveal ---
function initPreloader() {
  const counter = document.querySelector('.preloader-counter');
  let progress = { val: 0 };
  
  // Disable lenis temporarily
  lenis.stop();
  window.scrollTo(0, 0);

  gsap.to(progress, {
    val: 100,
    duration: 2.5,
    ease: 'power3.inOut',
    onUpdate: function() {
      counter.innerText = Math.round(progress.val) + '%';
    },
    onComplete: () => {
      const tl = gsap.timeline();
      tl.to(counter, { opacity: 0, y: -50, duration: 0.5, ease: 'power2.in' })
        .to('.preloader-left', { xPercent: -100, duration: 1, ease: 'power4.inOut' }, 'split')
        .to('.preloader-right', { xPercent: 100, duration: 1, ease: 'power4.inOut' }, 'split')
        .set('.preloader', { display: 'none' })
        .call(() => {
          lenis.start();
          playHeroAnimation();
        });
    }
  });
}

function playHeroAnimation() {
  const tl = gsap.timeline();
  // Hero split text stagger
  tl.to('.hero-title .char', { y: 0, rotation: 0, opacity: 1, duration: 1, stagger: 0.02, ease: 'back.out(1.2)' })
    .fromTo('.hero-anim', { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 1, stagger: 0.1, ease: 'power3.out' }, "-=0.5")
    .fromTo('.main-cup', { y: 100, scale: 0.8, opacity: 0 }, { y: 0, scale: 1, opacity: 1, duration: 1.5, ease: 'elastic.out(1, 0.7)' }, "-=1")
    .fromTo('.hero-anim-stats', { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8, ease: 'power3.out' }, "-=0.8");
    
  runCounters();
}

// Override original window load animation
window.addEventListener('load', () => {
  initPreloader();
});

// --- Scroll Progress Ring ---
const circle = document.querySelector('.progress-ring__circle');
const radius = circle.r.baseVal.value;
const circumference = radius * 2 * Math.PI;
circle.style.strokeDasharray = ${circumference} ;
circle.style.strokeDashoffset = circumference;

lenis.on('scroll', (e) => {
  const scrollPercent = e.scroll / (e.limit || 1);
  const offset = circumference - scrollPercent * circumference;
  circle.style.strokeDashoffset = offset;
});

// --- Kinetic Marquee ---
const marqueeContent = document.querySelector('.marquee-content');
if (marqueeContent) {
  // Clone for infinite effect
  marqueeContent.appendChild(marqueeContent.firstElementChild.cloneNode(true));
  
  let xPos = 0;
  let direction = -1;
  let speed = 1;
  
  // Increase speed based on scroll velocity
  lenis.on('scroll', (e) => {
    direction = e.velocity > 0 ? -1 : 1;
    speed = 1 + Math.abs(e.velocity) * 0.05;
  });

  gsap.ticker.add(() => {
    xPos += 2 * speed * direction;
    // Reset condition based on width of one item (roughly)
    if (xPos <= -marqueeContent.scrollWidth / 2) xPos = 0;
    if (xPos >= 0 && direction === 1) xPos = -marqueeContent.scrollWidth / 2;
    gsap.set(marqueeContent, { x: xPos });
    
    // Decay speed back to normal
    speed += (1 - speed) * 0.05;
  });
}

// --- 3D Tilt Initialization ---
if (typeof VanillaTilt !== 'undefined') {
  VanillaTilt.init(document.querySelectorAll('.card-reveal'), {
    max: 15,
    speed: 400,
    glare: true,
    'max-glare': 0.2,
  });
}

// --- Upgraded Cursor Drag Hover ---
document.querySelectorAll('.product-card').forEach(card => {
  card.addEventListener('mouseenter', () => {
    cursorFollower.classList.add('drag-mode');
    document.querySelector('.cursor-text').innerText = 'VIEW';
  });
  card.addEventListener('mouseleave', () => {
    cursorFollower.classList.remove('drag-mode');
  });
});
'''
if 'splitText(' not in js:
    js += js_additions
    
    # We need to remove or comment out the old window.addEventListener('load') hero animation 
    # so it doesn't conflict with our new initPreloader and playHeroAnimation
    old_hero_anim = re.search(r'window\.addEventListener\(\'load\', \(\) => {[\s\S]*?runCounters\(\);\n}\);', js)
    if old_hero_anim:
        js = js.replace(old_hero_anim.group(0), '/* OLD HERO ANIMATION REPLACED BY PRELOADER */')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)
with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)

print("Awwwards features injected successfully!")
