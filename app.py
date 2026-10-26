import html
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Hello World Motion Lab",
    page_icon="✨",
    layout="wide",
)

st.title("✨ Hello World Motion Lab")
st.write("Enter a name, style it, and add a looping motion effect. Use the sidebar to experiment.")

# Controls
st.sidebar.header("Controls")
name = st.sidebar.text_input("Enter your name", value="Hello World", max_chars=80)
font_family = st.sidebar.selectbox(
    "Font type",
    ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana", "Trebuchet MS", "Impact", "Comic Sans MS"],
)
font_size = st.sidebar.slider("Font size (px)", min_value=20, max_value=120, value=48)
background = st.sidebar.selectbox(
    "Background",
    ["Light", "Dark", "Ocean", "Sunset", "Forest", "Lavender", "Midnight"],
)
name_mode = st.sidebar.selectbox("Name display mode", ["Centered", "Ticker Tape", "Repeated"])
effect = st.sidebar.selectbox(
    "Dynamic action",
    ["None", "Rain", "Snow", "Hail", "Wind Gust", "Confetti", "Tornado"],
)
speed = st.sidebar.slider("Animation speed", min_value=1, max_value=10, value=5,
                          help="Higher values make the animation move faster.")

themes = {
    "Light": ("#ffffff", "#171717"),
    "Dark": ("#101114", "#ffffff"),
    "Ocean": ("linear-gradient(135deg, #073b4c, #118ab2)", "#ffffff"),
    "Sunset": ("linear-gradient(135deg, #ff7e5f, #feb47b)", "#2b1635"),
    "Forest": ("linear-gradient(135deg, #163a2b, #5b8c5a)", "#ffffff"),
    "Lavender": ("linear-gradient(135deg, #e6d9ff, #c8b6ff)", "#2d2145"),
    "Midnight": ("linear-gradient(135deg, #090979, #020024 70%)", "#ffffff"),
}
bg, fg = themes[background]

# Escape user input before placing it in HTML.
safe_name = html.escape(name.strip() or "Hello World")
font_css = {
    "Arial": "Arial, sans-serif",
    "Courier New": "'Courier New', monospace",
    "Georgia": "Georgia, serif",
    "Times New Roman": "'Times New Roman', serif",
    "Verdana": "Verdana, sans-serif",
    "Trebuchet MS": "'Trebuchet MS', sans-serif",
    "Impact": "Impact, sans-serif",
    "Comic Sans MS": "'Comic Sans MS', cursive",
}[font_family]

# Generate a single self-contained HTML/CSS/JS scene. Animation runs in the
# browser, so it loops smoothly without repeatedly rerunning the Streamlit app.
scene_html = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; }
  #scene {
    position: relative; width: 100%; height: 610px; overflow: hidden;
    border-radius: 18px; background: __BACKGROUND__; color: __FOREGROUND__;
    font-family: __FONT__; isolation: isolate;
  }
  #effects { position: absolute; inset: 0; overflow: hidden; pointer-events: none; z-index: 1; }
  #name-layer {
    position: absolute; inset: 0; display: flex; align-items: center;
    justify-content: center; z-index: 5; padding: 28px; overflow: hidden;
  }
  #name {
    font-size: __FONTSIZE__px; line-height: 1.15; font-weight: 700;
    text-align: center; overflow-wrap: anywhere; max-width: 100%;
    text-shadow: 0 2px 12px rgba(0,0,0,.18);
  }
  #name.repeated { display: flex; flex-direction: column; gap: .18em; }
  #name.ticker {
    position: absolute; white-space: nowrap; max-width: none; overflow-wrap: normal;
    animation: ticker __TICKER_DURATION__s linear infinite;
  }
  @keyframes ticker {
    from { transform: translateX(110%); }
    to { transform: translateX(-110%); }
  }
  .particle { position: absolute; top: -12%; user-select: none; will-change: transform; }
  .rain { animation: rain __DURATION__s linear infinite; }
  .snow { animation: snow __DURATION__s linear infinite; }
  .hail { animation: hail __DURATION__s linear infinite; }
  .confetti { animation: confetti __DURATION__s linear infinite; }
  .wind { animation: wind __DURATION__s ease-in-out infinite; }
  .tornado { animation: tornado __DURATION__s linear infinite; }
  @keyframes rain { from { transform: translate3d(0,-20px,0) rotate(12deg); } to { transform: translate3d(-45px,700px,0) rotate(12deg); } }
  @keyframes snow { 0% { transform: translate3d(0,-20px,0) rotate(0); } 50% { transform: translate3d(32px,320px,0) rotate(180deg); } 100% { transform: translate3d(-15px,700px,0) rotate(360deg); } }
  @keyframes hail { from { transform: translate3d(0,-20px,0); } to { transform: translate3d(-20px,700px,0); } }
  @keyframes confetti { 0% { transform: translate3d(0,-20px,0) rotate(0); } 100% { transform: translate3d(var(--drift),700px,0) rotate(900deg); } }
  @keyframes wind { 0%,100% { transform: translate3d(-100px,0,0) rotate(-8deg); opacity: 0; } 20%,80% { opacity: .9; } 50% { transform: translate3d(110vw,0,0) rotate(8deg); } }
  @keyframes tornado { 0% { transform: translate3d(0,-30px,0) rotate(0) scale(.5); opacity: 0; } 15%,85% { opacity: .9; } 100% { transform: translate3d(var(--drift),680px,0) rotate(900deg) scale(1.3); opacity: 0; } }
  @media (prefers-reduced-motion: reduce) {
    .particle, #name.ticker { animation-duration: 20s !important; }
  }
</style>
</head>
<body>
<div id="scene">
  <div id="effects" aria-hidden="true"></div>
  <div id="name-layer"><div id="name" class="__MODE__">__NAME__</div></div>
</div>
<script>
(() => {
  const effect = "__EFFECT__";
  const effects = document.getElementById("effects");
  const nameEl = document.getElementById("name");
  const speed = __SPEED__;
  const duration = (11 - speed) * 0.85 + 1.5;
  document.querySelectorAll(".rain,.snow,.hail,.confetti,.wind,.tornado").forEach(el => {
    el.style.animationDuration = duration + "s";
  });
  if (nameEl.classList.contains("repeated")) {
    const text = nameEl.textContent;
    nameEl.replaceChildren();
    for (let i = 0; i < 6; i++) {
      const line = document.createElement("div");
      line.textContent = text;
      line.style.fontSize = "min(0.72em, 5vw)";
      nameEl.appendChild(line);
    }
  }
  const configs = {
    "Rain": { chars: ["💧","💦","│"], count: 55, cls: "rain", size: [12,24] },
    "Snow": { chars: ["❄","❅","❆","✳"], count: 42, cls: "snow", size: [13,27] },
    "Hail": { chars: ["🧊","●","○"], count: 38, cls: "hail", size: [10,20] },
    "Wind Gust": { chars: ["〰","〜","💨","➝"], count: 16, cls: "wind", size: [18,38] },
    "Confetti": { chars: ["🎉","✦","✳","●","■","◆","🎊"], count: 48, cls: "confetti", size: [12,25] },
    "Tornado": { chars: ["🌪","〰","🌀"], count: 24, cls: "tornado", size: [18,34] }
  };
  const config = configs[effect];
  if (!config) return;
  for (let i = 0; i < config.count; i++) {
    const p = document.createElement("span");
    p.className = "particle " + config.cls;
    p.textContent = config.chars[Math.floor(Math.random() * config.chars.length)];
    p.style.left = (Math.random() * 100) + "%";
    p.style.fontSize = (config.size[0] + Math.random() * (config.size[1] - config.size[0])) + "px";
    p.style.opacity = (0.45 + Math.random() * 0.55).toFixed(2);
    p.style.animationDelay = (-Math.random() * duration) + "s";
    p.style.animationDuration = (duration * (0.65 + Math.random() * 0.8)) + "s";
    p.style.setProperty("--drift", ((Math.random() - 0.5) * 260) + "px");
    if (config.cls === "wind") p.style.top = (10 + Math.random() * 80) + "%";
    effects.appendChild(p);
  }
})();
</script>
</body>
</html>
"""

# Replace template tokens with controlled values. The name is HTML-escaped above.
replacements = {
    "__BACKGROUND__": bg,
    "__FOREGROUND__": fg,
    "__FONT__": font_css,
    "__FONTSIZE__": str(font_size),
    "__TICKER_DURATION__": str(round(13 / (speed / 5), 2)),
    "__DURATION__": str(round((11 - speed) * 0.85 + 1.5, 2)),
    "__MODE__": {"Centered": "", "Ticker Tape": "ticker", "Repeated": "repeated"}[name_mode],
    "__NAME__": safe_name,
    "__EFFECT__": effect,
    "__SPEED__": str(speed),
}
for token, value in replacements.items():
    scene_html = scene_html.replace(token, value)

components.html(scene_html, height=630, scrolling=False)
st.caption("Tip: change the name, font, background, or motion effect in the sidebar. The animation loops in the preview without refreshing the page.")
