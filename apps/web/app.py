import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="TripPersona",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background:
        radial-gradient(circle at top left, rgba(255,110,50,0.16), transparent 26%),
        radial-gradient(circle at top right, rgba(200,35,35,0.13), transparent 28%),
        linear-gradient(180deg, #09090b 0%, #111114 50%, #151519 100%);
    color: #f5f5f7;
}

/* HERO */
.hero-title {
    font-size: 4.2rem;
    font-weight: 900;
    color: #fff7f3;
    letter-spacing: -0.04em;
}
.hero-tagline {
    font-size: 1.2rem;
    color: #ffb08f;
    margin-top: 0.5rem;
}
.hero-sub {
    color: #c9c9cf;
    margin-top: 0.5rem;
}

/* INPUT FIX */
input, textarea {
    background-color: rgba(20,20,25,0.9) !important;
    color: #ffffff !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
}

input::placeholder,
textarea::placeholder {
    color: #888 !important;
}

div[data-baseweb="input"] input {
    background-color: rgba(20,20,25,0.9) !important;
    color: white !important;
}

label {
    color: #ddd !important;
    font-weight: 600;
}

/* FOCUS */
input:focus, textarea:focus {
    outline: none !important;
    border: 1px solid rgba(255,110,50,0.6) !important;
    box-shadow: 0 0 0 1px rgba(255,110,50,0.3);
}

/* BUTTON */
.stButton button {
    background: linear-gradient(90deg, #ff6c39, #cf3d35);
    color: white;
    border-radius: 14px;
    font-weight: bold;
}

/* PANELS */
.mini-panel {
    border-radius: 18px;
    padding: 1rem;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,110,50,0.1);
}

.mini-title {
    font-weight: 700;
    margin-bottom: 0.6rem;
    color: #fff3ed;
}

.bullet-item {
    margin-bottom: 0.45rem;
    color: #ddd;
    line-height: 1.5;
}

/* ITINERARY */
.day-card {
    padding: 1rem;
    border-radius: 16px;
    background: rgba(255,255,255,0.03);
    margin-bottom: 0.7rem;
}

</style>
""", unsafe_allow_html=True)

# HERO
st.markdown("""
<h1 class="hero-title">TripPersona</h1>
<div class="hero-tagline">One grounded trip. Four personalities.</div>
<div class="hero-sub">
Plan your trip as a planner, chaotic explorer, local insider, or foodie.
</div>
""", unsafe_allow_html=True)

# INPUTS
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    source = st.text_input("From", "Bhubaneswar")
with c2:
    destination = st.text_input("To", "Goa")
with c3:
    days = st.number_input("Days", 1, 14, 4)
with c4:
    people = st.number_input("People", 1, 10, 2)
with c5:
    budget = st.number_input("Budget", 1000, 1000000, 70000)

preferences = st.text_input("Preferences", "love food, want chill vibes")

generate = st.button("Generate Trip")

if generate:
    payload = {
        "source": source,
        "destination": destination,
        "days": int(days),
        "people": int(people),
        "budget_inr": int(budget),
        "preferences": preferences,
    }

    with st.spinner("Generating trip personas..."):
        res = requests.post(f"{API_URL}/plan", json=payload)
        data = res.json()

    st.markdown("---")

    tabs = st.tabs(["Planner", "Chaotic", "Local", "Foodie"])

    def render_panel(title, emoji, items):
        items_html = "".join(
            [f'<div class="bullet-item">• {i}</div>' for i in items]
        )

        st.markdown(
            f"""
            <div class="mini-panel">
                <div class="mini-title">{emoji} {title}</div>
                {items_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

    def render(persona):
        st.subheader(persona["title"])
        st.write(persona["summary"])

        for d in persona["itinerary"]:
            st.markdown(f"""
            <div class="day-card">
            <b>Day {d['day']}</b><br>
            Morning: {d['morning']}<br>
            Afternoon: {d['afternoon']}<br>
            Evening: {d['evening']}
            </div>
            """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)

        with c1:
            render_panel("Stay", "🏨", persona["stay"])
        with c2:
            render_panel("Food", "🍽️", persona["food"])
        with c3:
            render_panel("Tips", "🔥", persona["tips"])

    with tabs[0]:
        render(data["personalities"]["planner"])
    with tabs[1]:
        render(data["personalities"]["chaotic"])
    with tabs[2]:
        render(data["personalities"]["local"])
    with tabs[3]:
        render(data["personalities"]["foodie"])