import streamlit as st
import pickle
import json
import numpy as np
import pandas as pd

# ── Page config ───────────────────────────────────────────
st.set_page_config(
    page_title="Bangalore Home Price Prediction",
    page_icon="🏠",
    layout="centered"
)

# ── Load artifacts ────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    with open("artifacts/banglore_home_prices_model.pickle", "rb") as f:
        model = pickle.load(f)
    with open("artifacts/columns.json", "r") as f:
        data_columns = json.load(f)["data_columns"]
    locations = data_columns[3:]
    return model, data_columns, locations

model, data_columns, locations = load_artifacts()

# ── Predict function ──────────────────────────────────────
def predict_price(location, sqft, bath, bhk):
    try:
        loc_index = data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk

    if loc_index >= 0:
        x[loc_index] = 1

    # x_df wali line hata do, seedha numpy array do
    return round(model.predict([x])[0], 2)

# ── Custom CSS ────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Playfair+Display:wght@700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0f0f0f !important;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] { display: none !important; }
#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* Hero */
.hero {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    padding: 3rem 2rem 2rem;
    text-align: center;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: '';
    position: absolute;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(99,179,237,0.12) 0%, transparent 70%);
    top: -100px; right: -100px;
    border-radius: 50%;
}

.hero-tag {
    display: inline-block;
    background: rgba(99,179,237,0.15);
    color: #63b3ed;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.35rem 1rem;
    border-radius: 100px;
    border: 1px solid rgba(99,179,237,0.25);
    margin-bottom: 1.2rem;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.2;
    margin-bottom: 0.75rem;
}

.hero-title span { color: #63b3ed; }

.hero-sub {
    color: rgba(255,255,255,0.45);
    font-size: 0.95rem;
    font-weight: 300;
}

/* Form card */
.form-card {
    background: #161616;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 2rem;
    margin: 2rem auto;
    max-width: 520px;
}

/* Widget labels */
label[data-testid="stWidgetLabel"] p {
    color: rgba(255,255,255,0.5) !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Number input */
[data-testid="stNumberInput"] input {
    background: #1e1e1e !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
}

/* Radio */
[data-testid="stRadio"] label,
[data-testid="stRadio"] label p,
[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] p {
    background: #1e1e1e !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    padding: 0.4rem 1.1rem !important;
    color: rgba(255,255,255,0.9) !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
    cursor: pointer !important;
}

[data-testid="stRadio"] label:has(input:checked),
[data-testid="stRadio"] label:has(input:checked) p {
    background: rgba(99,179,237,0.15) !important;
    border-color: #63b3ed !important;
    color: #63b3ed !important;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background: #1e1e1e !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: white !important;
}

/* Button */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #63b3ed 0%, #4299e1 100%) !important;
    color: #0f1923 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    border: none !important;
    border-radius: 12px !important;
    width: 100% !important;
    padding: 0.75rem !important;
    box-shadow: 0 4px 20px rgba(99,179,237,0.25) !important;
    transition: all 0.2s ease !important;
}

[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(99,179,237,0.35) !important;
}

/* Result */
.result-box {
    background: linear-gradient(135deg, #1a2a1a, #1e3a1e);
    border: 1px solid rgba(72,187,120,0.3);
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
    margin-top: 1rem;
}

.result-label {
    color: rgba(255,255,255,0.4);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.result-price {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #68d391;
}

.result-note {
    color: rgba(255,255,255,0.3);
    font-size: 0.78rem;
    margin-top: 0.4rem;
}

hr {
    border: none !important;
    border-top: 1px solid rgba(255,255,255,0.06) !important;
    margin: 1rem 0 !important;
}

[data-testid="stAlert"] {
    background: rgba(237,137,54,0.1) !important;
    border: 1px solid rgba(237,137,54,0.3) !important;
    border-radius: 10px !important;
    color: #f6ad55 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-tag">🏙️ Bangalore Real Estate</div>
    <div class="hero-title">Home Price <span>Predictor</span></div>
    <div class="hero-sub">ML-powered estimates based on 13,000+ property records</div>
</div>
""", unsafe_allow_html=True)

# ── Form ─────────────────────────────────────────────────
st.markdown('<div class="form-card">', unsafe_allow_html=True)

sqft = st.number_input(
    "📐 Area (Square Feet)",
    min_value=100,
    max_value=10000,
    value=1000,
    step=50
)

st.markdown("<hr>", unsafe_allow_html=True)

bhk = st.radio(
    "🛏️ BHK (Bedrooms)",
    options=[1, 2, 3, 4, 5],
    index=1,
    horizontal=True
)

st.markdown("<hr>", unsafe_allow_html=True)

bath = st.radio(
    "🚿 Bathrooms",
    options=[1, 2, 3, 4, 5],
    index=1,
    horizontal=True
)

st.markdown("<hr>", unsafe_allow_html=True)

location = st.selectbox(
    "📍 Location",
    options=["Choose a Location"] + sorted(locations),
    index=0
)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Estimate Price →", use_container_width=True):
    if location == "Choose a Location":
        st.warning("Please select a location to get an estimate.")
    else:
        price = predict_price(location, sqft, bath, bhk)
        st.markdown(f"""
        <div class="result-box">
            <div class="result-label">Estimated Price</div>
            <div class="result-price">₹ {price} Lakh</div>
            <div class="result-note">{location} &nbsp;·&nbsp; {sqft} sqft &nbsp;·&nbsp; {bhk} BHK &nbsp;·&nbsp; {bath} Bath</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)