import random
import streamlit as st

st.set_page_config(
    page_title="GUESS LAB ARCADE",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- GAME STATE ----------
def new_game():
    st.session_state.secret = random.randint(1, 100)
    st.session_state.guesses = []
    st.session_state.score = 100
    st.session_state.status = "playing"
    st.session_state.message = "FIND THE SECRET NUMBER!"
    st.session_state.next_guess = 50


if "secret" not in st.session_state:
    new_game()

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

# ---------- THEME ----------
st.session_state.theme = st.radio(
    "THEME",
    ["Dark", "Light"],
    horizontal=True,
    key="theme_choice",
    label_visibility="collapsed",
)

dark = st.session_state.theme == "Dark"

if dark:
    bg = "#080817"
    panel = "#15152B"
    panel2 = "#20203B"
    text = "#F6F3FF"
    muted = "#AAA9CB"
    accent = "#B66DFF"
    accent2 = "#38E8FF"
    border = "#39345D"
    good = "#5DFFB1"
    danger = "#FF6289"
    chip = "#252343"
else:
    bg = "#F3F0FF"
    panel = "#FFFFFF"
    panel2 = "#EAE5FF"
    text = "#241744"
    muted = "#71668F"
    accent = "#7A35DF"
    accent2 = "#087EAC"
    border = "#D5C9F2"
    good = "#087D52"
    danger = "#D52D55"
    chip = "#E9E1FF"

# ---------- ARCADE DESIGN ----------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;600;700;800;900&family=Inter:wght@400;500;600;700;800&display=swap');

:root {{
    --bg:{bg};
    --panel:{panel};
    --panel2:{panel2};
    --text:{text};
    --muted:{muted};
    --accent:{accent};
    --accent2:{accent2};
    --border:{border};
    --good:{good};
    --danger:{danger};
    --chip:{chip};
}}

.stApp {{
    background:
        radial-gradient(ellipse at 50% 0%, color-mix(in srgb, var(--accent) 20%, transparent), transparent 48%),
        radial-gradient(ellipse at 0% 65%, color-mix(in srgb, var(--accent2) 10%, transparent), transparent 45%),
        var(--bg);
    color:var(--text);
    font-family:'Inter',sans-serif;
}}

header,footer,#MainMenu {{visibility:hidden;}}
.block-container {{max-width:1050px;padding:1rem 1.3rem 2rem;}}

h1,h2,h3,p,label {{color:var(--text);}}

.brand {{
    text-align:center;
    font-family:'Orbitron',sans-serif;
    font-weight:900;
    font-size:clamp(1.8rem,5vw,3rem);
    letter-spacing:clamp(2px,1vw,7px);
    color:var(--accent2);
    text-shadow:0 0 22px color-mix(in srgb,var(--accent2) 45%,transparent);
}}

.subtitle {{
    text-align:center;
    font-size:.7rem;
    letter-spacing:3px;
    color:var(--muted);
    margin:5px 0 24px;
}}

div[role="radiogroup"] {{justify-content:center;gap:10px;}}
div[role="radiogroup"] label {{
    background:var(--panel);
    border:1px solid var(--border);
    border-radius:20px;
    padding:5px 12px;
}}
div[role="radiogroup"] label p {{font-size:.8rem;margin:0;}}

.stats {{
    display:grid;
    grid-template-columns:repeat(3,minmax(0,1fr));
    gap:10px;
    margin:20px 0;
}}

.stat {{
    background:var(--panel);
    border:1px solid var(--border);
    border-radius:15px;
    text-align:center;
    padding:13px 6px;
    box-shadow:0 8px 24px #0000000b;
}}

.stat-label {{
    font-size:.65rem;
    letter-spacing:1.4px;
    color:var(--muted);
}}

.stat-value {{
    font-family:'Orbitron',sans-serif;
    font-size:clamp(1.1rem,3vw,1.7rem);
    font-weight:800;
    color:var(--accent2);
    margin-top:7px;
}}

.arena {{
    background:linear-gradient(145deg,var(--panel),var(--panel2));
    border:1px solid var(--border);
    border-radius:24px;
    padding:24px;
    text-align:center;
    box-shadow:0 18px 45px #00000016;
}}

.arena-label {{
    font-family:'Orbitron',sans-serif;
    font-size:.8rem;
    letter-spacing:2px;
    color:var(--muted);
}}

.orb {{
    width:clamp(165px,27vw,230px);
    height:clamp(165px,27vw,230px);
    margin:25px auto;
    border-radius:50%;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    position:relative;
    background:
        radial-gradient(circle at 35% 25%, color-mix(in srgb,var(--accent) 45%,var(--panel)), var(--panel) 70%);
    border:3px solid var(--accent2);
    box-shadow:
        0 0 0 9px color-mix(in srgb,var(--accent2) 8%,transparent),
        0 0 35px color-mix(in srgb,var(--accent2) 25%,transparent),
        inset 0 0 28px color-mix(in srgb,var(--accent) 20%,transparent);
}}

.orb-number {{
    font-family:'Orbitron',sans-serif;
    font-size:clamp(3.2rem,8vw,5rem);
    font-weight:900;
    color:var(--text);
    line-height:1;
}}

.orb-caption {{
    font-size:.65rem;
    letter-spacing:2px;
    color:var(--accent2);
    margin-top:12px;
}}

.feedback {{
    background:var(--panel);
    border:1px solid var(--border);
    border-radius:14px;
    padding:15px 10px;
    font-weight:700;
    font-size:.95rem;
    line-height:1.5;
    margin:12px 0;
}}

.hint {{
    color:var(--muted);
    font-size:.78rem;
    letter-spacing:1px;
}}

.section-title {{
    font-family:'Orbitron',sans-serif;
    font-size:.82rem;
    letter-spacing:1.5px;
    margin:20px 0 12px;
}}

div[data-testid="stNumberInput"] input {{
    background:var(--panel);
    color:var(--text);
    border:1px solid var(--border);
    border-radius:14px;
    text-align:center;
    font-family:'Orbitron',sans-serif;
    font-size:1.4rem;
    min-height:55px;
}}

div[data-testid="stNumberInput"] label {{color:var(--muted);}}

div[data-testid="stFormSubmitButton"] button,
div.stButton button {{
    width:100%;
    min-height:52px;
    border:0;
    border-radius:14px;
    background:linear-gradient(110deg,var(--accent),var(--accent2));
    color:white;
    font-weight:900;
    font-size:.95rem;
    letter-spacing:1px;
    box-shadow:0 7px 20px color-mix(in srgb,var(--accent) 25%,transparent);
}}

div[data-testid="stFormSubmitButton"] button:hover,
div.stButton button:hover {{
    filter:brightness(1.1);
    color:white;
    box-shadow:0 0 24px color-mix(in srgb,var(--accent2) 30%,transparent);
}}

.history {{
    display:flex;
    flex-wrap:wrap;
    justify-content:center;
    gap:8px;
}}

.guess-chip {{
    background:var(--chip);
    border:1px solid var(--border);
    border-radius:10px;
    padding:9px 12px;
    font-family:'Orbitron',sans-serif;
    font-size:.8rem;
    color:var(--text);
}}

.footer {{
    text-align:center;
    font-size:.65rem;
    color:var(--muted);
    letter-spacing:2px;
    margin-top:30px;
}}

div[data-testid="stProgressBar"] > div > div {{
    background:linear-gradient(90deg,var(--accent),var(--accent2));
}}
div[data-testid="stProgressBar"] > div {{background:var(--panel2);}}

@media(max-width:650px) {{
    .block-container {{padding:.65rem .65rem 1.2rem;}}
    .brand {{font-size:1.75rem;letter-spacing:3px;}}
    .subtitle {{font-size:.59rem;letter-spacing:1.5px;margin-bottom:15px;}}
    .stats {{grid-template-columns:repeat(3,minmax(0,1fr));gap:6px;margin:14px 0;}}
    .stat {{padding:11px 3px;border-radius:12px;}}
    .stat-label {{font-size:.52rem;letter-spacing:.4px;}}
    .stat-value {{font-size:1rem;margin-top:6px;}}
    .arena {{padding:17px 12px;border-radius:20px;}}
    .orb {{width:160px;height:160px;margin:20px auto;}}
    .orb-number {{font-size:3.4rem;}}
    .feedback {{font-size:.88rem;padding:13px 8px;}}
    div[data-testid="stNumberInput"] input {{min-height:58px;font-size:1.3rem;}}
    div[data-testid="stFormSubmitButton"] button,
    div.stButton button {{min-height:55px;font-size:.9rem;}}
    .section-title {{font-size:.75rem;}}
    .guess-chip {{padding:8px 10px;font-size:.72rem;}}
}}

@media(max-width:360px) {{
    .block-container {{padding-left:.4rem;padding-right:.4rem;}}
    .brand {{font-size:1.5rem;}}
    .stat-label {{font-size:.48rem;}}
    .stat-value {{font-size:.9rem;}}
    .orb {{width:145px;height:145px;}}
}}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="brand">GUESS LAB</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">⚡ THE NUMBER HUNT ARCADE ⚡</div>',
    unsafe_allow_html=True,
)

attempts = len(st.session_state.guesses)
remaining = max(0, 10 - attempts)

st.markdown(f"""
<div class="stats">
  <div class="stat"><div class="stat-label">SCORE</div>
  <div class="stat-value">{st.session_state.score}<span style="font-size:.7rem">/100</span></div></div>
  <div class="stat"><div class="stat-label">ATTEMPTS</div>
  <div class="stat-value">{attempts}/10</div></div>
  <div class="stat"><div class="stat-label">LEFT</div>
  <div class="stat-value">{remaining}</div></div>
</div>
""", unsafe_allow_html=True)

# ---------- GAME ARENA ----------
if st.session_state.status == "won":
    orb_number, orb_caption = "🏆", "YOU WIN!"
elif st.session_state.status == "lost":
    orb_number, orb_caption = str(st.session_state.secret), "ANSWER REVEALED"
else:
    orb_number, orb_caption = "?", "SECRET NUMBER"

st.markdown(f"""
<div class="arena">
  <div class="arena-label">◈ TARGET CHAMBER ◈</div>
  <div class="orb">
    <div class="orb-number">{orb_number}</div>
    <div class="orb-caption">{orb_caption}</div>
  </div>
  <div class="feedback">{st.session_state.message}</div>
  <div class="hint">RANGE 01—100 &nbsp; • &nbsp; 10 CHANCES</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">🎮 YOUR MOVE</div>', unsafe_allow_html=True)

if st.session_state.status == "playing":
    with st.form("guess_form", clear_on_submit=False):
        guess = st.number_input(
            "Choose your number",
            min_value=1,
            max_value=100,
            value=int(st.session_state.next_guess),
            step=1,
            key="guess_input",
            label_visibility="collapsed",
        )
        submitted = st.form_submit_button("⚡ LOCK IN GUESS")

    if submitted:
        submitted_guess = int(guess)

        if submitted_guess in st.session_state.guesses:
            st.session_state.message = (
                f"🔁 {submitted_guess} WAS ALREADY TRIED! PICK ANOTHER."
            )
        else:
            st.session_state.guesses.append(submitted_guess)
            attempts = len(st.session_state.guesses)

            if submitted_guess == st.session_state.secret:
                st.session_state.status = "won"
                st.session_state.score = max(10, 110 - attempts * 10)
                st.session_state.message = (
                    f"🎉 PERFECT HIT! YOU FOUND {submitted_guess} "
                    f"IN {attempts} ATTEMPT(S)!"
                )
                st.balloons()

            elif attempts >= 10:
                st.session_state.status = "lost"
                st.session_state.score = 0
                st.session_state.message = (
                    f"💥 GAME OVER! THE NUMBER WAS {st.session_state.secret}."
                )

            else:
                st.session_state.score = max(0, 100 - attempts * 10)
                difference = abs(st.session_state.secret - submitted_guess)

                if submitted_guess < st.session_state.secret:
                    direction = "HIGHER ⬆️"
                else:
                    direction = "LOWER ⬇️"

                if difference <= 5:
                    st.session_state.message = f"🔥 SO CLOSE! GO {direction}"
                elif difference <= 15:
                    st.session_state.message = f"🎯 GETTING WARM! GO {direction}"
                else:
                    st.session_state.message = f"❄️ NOT QUITE! GO {direction}"

            st.session_state.next_guess = submitted_guess

        st.rerun()
else:
    if st.session_state.status == "won":
        st.success(f"VICTORY! FINAL SCORE: {st.session_state.score}/100")
    else:
        st.error("ROUND OVER — TAKE ANOTHER SHOT!")

    if st.button("🔄 PLAY AGAIN"):
        new_game()
        st.rerun()

# ---------- PROGRESS ----------
st.markdown('<div class="section-title">⚡ ROUND PROGRESS</div>', unsafe_allow_html=True)
st.progress(attempts / 10)

# ---------- GUESS HISTORY ----------
st.markdown('<div class="section-title">▦ YOUR GUESSES</div>', unsafe_allow_html=True)

if st.session_state.guesses:
    chips = []
    for number in st.session_state.guesses:
        if st.session_state.status == "won" and number == st.session_state.secret:
            chips.append(
                f'<span class="guess-chip" style="border-color:{good};color:{good}">'
                f'{number} ✓</span>'
            )
        else:
            chips.append(f'<span class="guess-chip">{number}</span>')

    st.markdown(
        '<div class="history">' + "".join(chips) + '</div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        '<div class="feedback">🎯 NO GUESSES YET — MAKE YOUR FIRST MOVE!</div>',
        unsafe_allow_html=True,
    )

st.markdown(
    '<div class="footer">GUESS LAB &nbsp; • &nbsp; INSERT COIN? NO — JUST PLAY.</div>',
    unsafe_allow_html=True,
)