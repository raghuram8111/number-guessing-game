import random
import streamlit as st

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Number Guessing Game",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# =========================================================
# SESSION STATE INITIALIZATION
# =========================================================

defaults = {
    "secret": random.randint(1, 100),
    "attempts": 0,
    "history": [],
    "score": 100,
    "best_score": 0,
    "game_over": False,
    "won": False,
    "message": "Find the hidden number!",
    "message_type": "info",
    "theme": "Dark",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# GAME FUNCTIONS
# =========================================================

def restart_game():
    """Start a fresh game while preserving the best score and theme."""
    st.session_state.secret = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.history = []
    st.session_state.score = 100
    st.session_state.game_over = False
    st.session_state.won = False
    st.session_state.message = "Find the hidden number!"
    st.session_state.message_type = "info"


def make_guess():
    """Process the submitted guess."""
    if st.session_state.game_over:
        return

    guess = st.session_state.get("guess_input")

    if guess is None:
        st.session_state.message = "Enter a number before locking in!"
        st.session_state.message_type = "warning"
        return

    guess = int(guess)

    if not 1 <= guess <= 100:
        st.session_state.message = "Your guess must be between 1 and 100."
        st.session_state.message_type = "warning"
        return

    if guess in [item["guess"] for item in st.session_state.history]:
        st.session_state.message = "You already tried that number. Try another!"
        st.session_state.message_type = "warning"
        return

    st.session_state.attempts += 1

    secret = st.session_state.secret
    attempts = st.session_state.attempts

    st.session_state.history.append({
        "guess": guess,
        "result": (
            "correct" if guess == secret
            else "high" if guess > secret
            else "low"
        )
    })

    if guess == secret:
        st.session_state.won = True
        st.session_state.game_over = True

        # First-guess win = 100 points.
        points = max(10, 110 - (attempts * 10))
        st.session_state.score = points
        st.session_state.best_score = max(
            st.session_state.best_score,
            points
        )

        st.session_state.message = (
            f"🎉 Incredible! You found {secret} in {attempts} "
            f"{'attempt' if attempts == 1 else 'attempts'}!"
        )
        st.session_state.message_type = "success"

    elif attempts >= 10:
        st.session_state.score = 0
        st.session_state.game_over = True
        st.session_state.message = (
            f"💥 Game over! The hidden number was {secret}."
        )
        st.session_state.message_type = "error"

    else:
        st.session_state.score = max(0, 100 - attempts * 10)

        if guess < secret:
            st.session_state.message = (
                "📈 Too low! The mystery number is HIGHER."
            )
        else:
            st.session_state.message = (
                "📉 Too high! The mystery number is LOWER."
            )

        st.session_state.message_type = "info"


# =========================================================
# THEME SELECTION
# =========================================================

st.markdown(
    """
    <style>
    /* Hide default Streamlit chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {background: transparent;}
    [data-testid="stSidebar"] {display: none;}

    /* Main layout */
    .block-container {
        max-width: 760px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    /* Theme selector */
    div[role="radiogroup"] {
        display: flex;
        justify-content: center;
        gap: 12px;
        flex-wrap: wrap;
    }

    div[role="radiogroup"] label {
        border-radius: 12px;
        padding: 7px 15px;
        font-weight: 600;
    }

    /* Game title */
    .game-title {
        text-align: center;
        font-size: clamp(2.1rem, 7vw, 3.7rem);
        font-weight: 900;
        letter-spacing: -2px;
        line-height: 1.1;
        margin-top: 12px;
        margin-bottom: 8px;
    }

    .game-subtitle {
        text-align: center;
        font-size: 1rem;
        margin-bottom: 28px;
    }

    /* Mystery orb */
    .orb {
        width: clamp(145px, 35vw, 190px);
        height: clamp(145px, 35vw, 190px);
        margin: 18px auto 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: clamp(4rem, 14vw, 6rem);
        font-weight: 900;
        color: white;
        background: radial-gradient(
            circle at 35% 25%,
            #7b8cff,
            #5b3ed6 55%,
            #26134d
        );
        box-shadow:
            0 0 25px rgba(112, 92, 255, 0.35),
            inset -12px -15px 30px rgba(0, 0, 0, 0.28),
            inset 8px 8px 24px rgba(255, 255, 255, 0.22);
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-7px); }
    }

    /* Stats */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 10px;
        margin: 15px 0 24px;
    }

    .stat-card {
        padding: 16px 8px;
        border-radius: 16px;
        text-align: center;
        border: 1px solid var(--card-border);
        background: var(--card-bg);
        min-width: 0;
    }

    .stat-label {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        opacity: 0.72;
        margin-bottom: 6px;
    }

    .stat-value {
        font-size: clamp(1.4rem, 5vw, 2rem);
        font-weight: 900;
        line-height: 1.2;
    }

    /* Section cards */
    .game-card {
        border: 1px solid var(--card-border);
        background: var(--card-bg);
        border-radius: 18px;
        padding: 20px;
        margin-top: 18px;
    }

    .section-title {
        font-size: 1.15rem;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .muted {
        opacity: 0.72;
        font-size: 0.9rem;
    }

    /* Guess history */
    .history-row {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 12px;
    }

    .history-chip {
        border-radius: 10px;
        padding: 8px 12px;
        font-size: 0.9rem;
        font-weight: 800;
        border: 1px solid var(--card-border);
    }

    .chip-low {
        background: rgba(46, 160, 120, 0.13);
    }

    .chip-high {
        background: rgba(235, 90, 90, 0.13);
    }

    .chip-correct {
        background: rgba(120, 95, 255, 0.2);
    }

    /* Buttons */
    div.stButton > button,
    div[data-testid="stFormSubmitButton"] > button {
        min-height: 48px;
        width: 100%;
        border-radius: 13px;
        font-weight: 800;
        transition: transform 0.15s ease;
    }

    div.stButton > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {
        transform: translateY(-2px);
    }

    /* Number input */
    div[data-testid="stNumberInput"] input {
        min-height: 52px;
        font-size: 1.3rem;
        font-weight: 800;
        text-align: center;
    }

    /* Mobile adjustments */
    @media (max-width: 480px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            padding-top: 1rem;
        }

        .game-title {
            letter-spacing: -1px;
        }

        .game-card {
            padding: 15px;
            border-radius: 15px;
        }

        .stats-grid {
            gap: 7px;
        }

        .stat-card {
            padding: 12px 4px;
            border-radius: 12px;
        }

        .stat-label {
            font-size: 0.65rem;
            letter-spacing: 0.5px;
        }

        div[role="radiogroup"] {
            gap: 5px;
        }
    }

    @media (prefers-reduced-motion: reduce) {
        .orb {
            animation: none;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Theme controls using radio buttons
theme_col1, theme_col2, theme_col3 = st.columns([1, 2, 1])

with theme_col2:
    st.radio(
        "Choose appearance",
        options=["Dark", "Light"],
        horizontal=True,
        key="theme",
        label_visibility="collapsed",
    )

# =========================================================
# APPLY SELECTED THEME
# =========================================================

if st.session_state.theme == "Dark":
    bg = "#0B1020"
    text_color = "#F2F4FF"
    muted_color = "#A3ADC7"
    card_bg = "#151C30"
    card_border = "#29334D"
    input_bg = "#11182A"
    accent = "#8875FF"
else:
    bg = "#F3F5FC"
    text_color = "#19213A"
    muted_color = "#64708A"
    card_bg = "#FFFFFF"
    card_border = "#DDE3F0"
    input_bg = "#FFFFFF"
    accent = "#6447E8"

st.markdown(
    f"""
    <style>
    :root {{
        --card-bg: {card_bg};
        --card-border: {card_border};
    }}

    .stApp {{
        background: {bg};
        color: {text_color};
    }}

    .stApp,
    .stApp p,
    .stApp label,
    .stApp h1,
    .stApp h2,
    .stApp h3 {{
        color: {text_color};
    }}

    .game-subtitle,
    .muted {{
        color: {muted_color} !important;
    }}

    div[data-testid="stNumberInput"] input {{
        background: {input_bg};
        color: {text_color};
        border-color: {card_border};
    }}

    div.stButton > button,
    div[data-testid="stFormSubmitButton"] > button {{
        border: 1px solid {accent};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="game-title">NUMBER GUESSING GAME</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="game-subtitle">'
    '🎯 One mystery number. Ten chances. Can you beat the game?'
    '</div>',
    unsafe_allow_html=True,
)

# =========================================================
# MYSTERY ORB
# =========================================================

if st.session_state.won:
    orb_text = str(st.session_state.secret)
elif st.session_state.game_over:
    orb_text = "💥"
else:
    orb_text = "?"

st.markdown(
    f'<div class="orb">{orb_text}</div>',
    unsafe_allow_html=True,
)

# =========================================================
# LIVE STATS
# =========================================================

remaining = max(0, 10 - st.session_state.attempts)

st.markdown(
    f"""
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-label">Your Score</div>
            <div class="stat-value">{st.session_state.score}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Attempts Left</div>
            <div class="stat-value">{remaining}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Best Score</div>
            <div class="stat-value">{st.session_state.best_score}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# GUESS FORM
# =========================================================

st.markdown(
    '<div class="game-card">'
    '<div class="section-title">🔐 Crack the Code</div>'
    '<div class="muted">Choose a number between 1 and 100.</div>'
    '</div>',
    unsafe_allow_html=True,
)

if not st.session_state.game_over:
    with st.form("guess_form", clear_on_submit=True):
        st.number_input(
            "Enter your guess",
            min_value=1,
            max_value=100,
            value=None,
            step=1,
            placeholder="Enter 1–100",
            key="guess_input",
        )

        st.form_submit_button(
            "⚡ LOCK IN GUESS",
            on_click=make_guess,
            use_container_width=True,
        )

else:
    if st.session_state.won:
        st.success("🏆 YOU WIN! The mystery number is yours.")
    else:
        st.error("💥 GAME OVER! Better luck next time.")

    st.button(
        "🔄 PLAY AGAIN",
        on_click=restart_game,
        use_container_width=True,
    )

# =========================================================
# FEEDBACK
# =========================================================

if st.session_state.message_type == "success":
    st.success(st.session_state.message)
elif st.session_state.message_type == "error":
    st.error(st.session_state.message)
elif st.session_state.message_type == "warning":
    st.warning(st.session_state.message)
else:
    st.info(st.session_state.message)

# =========================================================
# GUESS HISTORY
# =========================================================

st.markdown(
    '<div class="game-card">'
    '<div class="section-title">📊 Guess History</div>'
    '<div class="muted">Every guess brings you closer to the answer.</div>'
    '</div>',
    unsafe_allow_html=True,
)

if st.session_state.history:
    chips = []

    for item in reversed(st.session_state.history):
        guess = item["guess"]
        result = item["result"]

        if result == "correct":
            css_class = "chip-correct"
            symbol = "✓"
        elif result == "low":
            css_class = "chip-low"
            symbol = "↑"
        else:
            css_class = "chip-high"
            symbol = "↓"

        chips.append(
            f'<div class="history-chip {css_class}">'
            f'{guess} {symbol}'
            f'</div>'
        )

    st.markdown(
        '<div class="history-row">' + "".join(chips) + '</div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        '<p class="muted" style="text-align:center; padding:18px 0;">'
        'No guesses yet. Make your first move!'
        '</p>',
        unsafe_allow_html=True,
    )

# =========================================================
# GAME RULES
# =========================================================

with st.expander("🎮 HOW TO PLAY"):
    st.markdown(
        """
        - 🎯 Guess the hidden number between **1 and 100**.
        - 🔟 You have a maximum of **10 attempts**.
        - 📈 **Too low** means the answer is higher.
        - 📉 **Too high** means the answer is lower.
        - 🏆 Your score starts at **100 points**.
        - ⚡ Every incorrect guess reduces your score by **10 points**.
        - 💯 A first-guess win earns **100 points**.
        - 🌗 Use the radio buttons at the top to switch between
          **Dark Mode** and **Light Mode**.
        """
    )

st.markdown(
    f"""
    <div style="text-align:center; margin-top:30px;
                font-size:0.8rem; opacity:0.65;">
        MADE FOR THE LOVE OF GAMES · SCORE LIMIT: 100
    </div>
    """,
    unsafe_allow_html=True,
)
