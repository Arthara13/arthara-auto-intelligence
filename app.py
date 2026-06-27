import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import warnings
warnings.filterwarnings('ignore')

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AutoPrice Intelligence",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #060B14; color: #C8D8E8; }
    [data-testid="stSidebar"] { background-color: #080E1A; }

    .stApp::before {
        content: '';
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background:
            radial-gradient(ellipse at 15% 50%, rgba(255,140,0,0.04) 0%, transparent 60%),
            radial-gradient(ellipse at 85% 20%, rgba(0,150,255,0.06) 0%, transparent 55%);
        pointer-events: none; z-index: 0;
    }

    /* HEADER */
    .hud-header {
        background: linear-gradient(135deg, rgba(8,18,35,0.95) 0%, rgba(12,25,50,0.90) 100%);
        border: 1px solid rgba(255,140,0,0.3);
        border-top: 3px solid #FF8C00;
        border-radius: 4px;
        padding: 1.2rem 2rem;
        margin-bottom: 1rem;
        position: relative;
        overflow: hidden;
    }
    .hud-header::after {
        content: '';
        position: absolute; top: 0; right: 0;
        width: 300px; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,140,0,0.03));
    }
    .hud-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.8rem; font-weight: 900;
        color: #FFFFFF; letter-spacing: 0.15em;
        text-shadow: 0 0 20px rgba(255,140,0,0.4);
        margin: 0; line-height: 1;
    }
    .hud-title span { color: #FF8C00; }
    .hud-sub {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.85rem; color: #5A8AAA; letter-spacing: 0.2em;
        margin-top: 0.3rem; text-transform: uppercase;
    }
    .hud-badge {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.7rem; font-weight: 700;
        background: rgba(255,140,0,0.12); border: 1px solid rgba(255,140,0,0.4);
        color: #FF8C00; padding: 0.2rem 0.6rem; border-radius: 2px;
        letter-spacing: 0.1em; text-transform: uppercase;
        display: inline-block; margin-top: 0.5rem;
    }

    /* INPUT PANEL */
    .input-panel {
        background: linear-gradient(135deg, rgba(8,18,35,0.97), rgba(10,22,44,0.95));
        border: 1px solid rgba(255,140,0,0.2);
        border-top: 2px solid rgba(255,140,0,0.5);
        border-radius: 4px; padding: 1.2rem;
        margin-bottom: 0.8rem;
    }
    .input-panel-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.78rem; font-weight: 700;
        color: #FF8C00; letter-spacing: 0.15em; text-transform: uppercase;
        margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;
    }
    .input-panel-title::before {
        content: ''; width: 8px; height: 8px;
        background: #FF8C00; border-radius: 50%;
        box-shadow: 0 0 8px #FF8C00;
    }

    /* Widget overrides */
    label { color: #5A8AAA !important; font-size: 0.73rem !important;
            font-family: 'Rajdhani', sans-serif !important;
            letter-spacing: 0.08em !important; text-transform: uppercase !important; }
    [data-testid="stSelectbox"] > div > div,
    [data-testid="stNumberInput"] input {
        background: rgba(4,12,25,0.9) !important;
        border: 1px solid rgba(255,140,0,0.2) !important;
        border-radius: 3px !important;
        color: #C8D8E8 !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 0.9rem !important;
    }

    /* PREDICT BUTTON */
    .stButton > button {
        background: linear-gradient(135deg, #CC6600, #FF8C00) !important;
        color: #000 !important; border: none !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 0.82rem !important; font-weight: 700 !important;
        letter-spacing: 0.12em !important; text-transform: uppercase !important;
        padding: 0.75rem 2rem !important; border-radius: 3px !important;
        width: 100% !important;
        box-shadow: 0 0 20px rgba(255,140,0,0.3) !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #FF8C00, #FFB347) !important;
        box-shadow: 0 0 35px rgba(255,140,0,0.5) !important;
    }

    /* PANELS */
    .car-panel {
        background: linear-gradient(135deg, rgba(6,14,28,0.98), rgba(10,20,40,0.95));
        border: 1px solid rgba(255,140,0,0.25);
        border-top: 2px solid #FF8C00;
        border-radius: 4px; padding: 1.1rem;
    }
    .price-panel {
        background: linear-gradient(135deg, rgba(6,14,28,0.98), rgba(10,20,40,0.95));
        border: 1px solid rgba(255,140,0,0.25);
        border-top: 2px solid #FF8C00;
        border-radius: 4px; padding: 1.1rem;
    }
    .chart-panel {
        background: linear-gradient(135deg, rgba(6,14,28,0.98), rgba(10,20,40,0.95));
        border: 1px solid rgba(255,140,0,0.18);
        border-radius: 4px; padding: 0.9rem;
        margin-top: 0.6rem;
    }

    /* Panel titles */
    .car-panel-title, .chart-title {
        font-family: 'Orbitron', sans-serif; font-size: 0.65rem; font-weight: 700;
        color: #FF8C00; letter-spacing: 0.18em; text-transform: uppercase;
        margin-bottom: 0.8rem; display: flex; align-items: center; gap: 0.4rem;
    }
    .car-panel-title::before, .chart-title::before {
        content: ''; width: 6px; height: 6px;
        background: #FF8C00; border-radius: 50%;
        box-shadow: 0 0 5px #FF8C00; flex-shrink: 0;
    }

    /* Spec grid cells */
    .spec-cell {
        background: rgba(4,10,22,0.8);
        border: 1px solid rgba(255,140,0,0.18);
        border-radius: 3px; padding: 0.45rem 0.7rem;
    }
    .spec-cell-lbl {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.6rem; color: #3A6070;
        text-transform: uppercase; letter-spacing: 0.1em;
    }
    .spec-cell-val {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.9rem; font-weight: 700; color: #C8D8E8;
    }

    /* Price display */
    .price-main {
        text-align: center; padding: 0.8rem 0 0.6rem 0;
        border-bottom: 1px solid rgba(255,140,0,0.1);
        margin-bottom: 0.8rem;
    }
    .price-lbl {
        font-family: 'Rajdhani', sans-serif; font-size: 0.68rem; font-weight: 700;
        letter-spacing: 0.2em; color: #5A8AAA; text-transform: uppercase; margin-bottom: 0.2rem;
    }
    .price-big {
        font-family: 'Orbitron', sans-serif; font-size: 2.2rem; font-weight: 900;
        color: #FF8C00; text-shadow: 0 0 25px rgba(255,140,0,0.4); line-height: 1.1;
    }
    .price-range {
        font-family: 'Rajdhani', sans-serif; font-size: 0.78rem;
        color: #5A8AAA; margin-top: 0.35rem;
    }
    .price-range span { color: #4AB3FF; font-weight: 700; }

    /* Stat boxes */
    .stat-box {
        background: rgba(4,10,22,0.8); border: 1px solid rgba(255,140,0,0.15);
        border-radius: 3px; padding: 0.55rem 0.4rem; text-align: center;
    }
    .stat-val {
        font-family: 'Orbitron', sans-serif; font-size: 1.1rem; font-weight: 700;
    }
    .stat-lbl {
        font-family: 'Rajdhani', sans-serif; font-size: 0.6rem; color: #3A5A70;
        letter-spacing: 0.07em; text-transform: uppercase; margin-top: 0.1rem;
    }

    /* Image HUD box */
    .img-hud {
        background: rgba(4,10,22,0.8);
        border: 1px solid rgba(255,140,0,0.15);
        border-radius: 4px; padding: 0.4rem;
        text-align: center; position: relative; margin-top: 0.6rem;
    }

    hr { border-color: rgba(255,140,0,0.1) !important; }
    [data-testid="stMetricValue"] { color: #FF8C00 !important; font-family: 'Orbitron', sans-serif !important; }
    [data-testid="stMetricLabel"] { color: #5A8AAA !important; }
</style>
""", unsafe_allow_html=True)

# ─── Config ────────────────────────────────────────────────────────────────────
BRANDS = ['Toyota', 'Honda', 'BMW']
BRAND_MODELS = {
    'Toyota': ['Highlander', 'Corolla', 'RAV4', 'Camry', 'Tacoma'],
    'Honda':  ['Civic', 'Accord', 'CR-V', 'Odyssey', 'Pilot'],
    'BMW':    ['3 Series', 'M3', 'X3', '5 Series', 'X5'],
}

# Body type → best matching model per brand (for smart default suggestion)
BODY_MODEL_SUGGEST = {
    'Toyota': {
        'SUV':         'Highlander',
        'Pickup Truck':'Tacoma',
        'Sedan':       'Camry',
        'Coupe':       'Corolla',
        'Minivan':     'Corolla',
    },
    'Honda': {
        'SUV':         'CR-V',
        'Minivan':     'Odyssey',
        'Sedan':       'Accord',
        'Coupe':       'Civic',
        'Pickup Truck':'Pilot',
    },
    'BMW': {
        'SUV':         'X5',
        'Sedan':       '5 Series',
        'Coupe':       'M3',
        'Minivan':     '3 Series',
        'Pickup Truck':'X3',
    },
}

# Image filename map — matches EXACT filenames on disk
IMAGE_FILENAMES = {
    ('Toyota', 'Highlander'): 'toyota_highlander',
    ('Toyota', 'Corolla'):    'toyota_corolla',
    ('Toyota', 'RAV4'):       'toyota_rav4',
    ('Toyota', 'Camry'):      'toyota_camry',
    ('Toyota', 'Tacoma'):     'toyota_tacoma',
    ('Honda',  'Civic'):      'honda_civic',
    ('Honda',  'Accord'):     'honda_accord',
    ('Honda',  'CR-V'):       'honda_cr_v',
    ('Honda',  'Odyssey'):    'honda_odyssey',
    ('Honda',  'Pilot'):      'honda_pilot',
    ('BMW',    '3 Series'):   'bmw_3_series',
    ('BMW',    'M3'):         'bmw_m3',
    ('BMW',    'X3'):         'bmw_x3',
    ('BMW',    '5 Series'):   'bmw_5_series',
    ('BMW',    'X5'):         'bmw_x5',
}

def get_image_path(brand, model):
    key = (brand, model)
    fname = IMAGE_FILENAMES.get(key)
    if fname:
        return f"images/{fname}.png"
    # fallback
    b = brand.lower().replace(' ', '_')
    m = model.lower().replace(' ', '_').replace('-', '_')
    return f"images/{b}_{m}.png"

PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#4A7090', family='Inter', size=9),
    title_font=dict(color='#C8D8E8', family='Orbitron', size=10),
    xaxis=dict(gridcolor='rgba(255,140,0,0.06)', linecolor='rgba(255,140,0,0.12)', tickfont=dict(size=8)),
    yaxis=dict(gridcolor='rgba(255,140,0,0.06)', linecolor='rgba(255,140,0,0.12)', tickfont=dict(size=8)),
    margin=dict(t=25, b=22, l=35, r=12),
)
ORANGE = '#FF8C00'; BLUE = '#4AB3FF'; GREEN = '#2ECC71'
COLORS = [ORANGE, BLUE, GREEN, '#D2A8FF', '#FF6B6B']

# ─── Data & Model ─────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    df = pd.read_csv("vehicle_price_prediction.csv", nrows=50_000)
    df['accident_history'] = df['accident_history'].fillna('None')
    df = df.dropna()
    df = df[df['make'].isin(BRANDS)]
    all_models = [m for ms in BRAND_MODELS.values() for m in ms]
    df = df[df['model'].isin(all_models)]
    return df

@st.cache_resource(show_spinner=False)
def train_model(df):
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.preprocessing import LabelEncoder
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    cat_cols = ['make', 'model', 'transmission', 'fuel_type', 'drivetrain',
                'body_type', 'condition', 'accident_history']
    num_cols = ['year', 'mileage', 'engine_hp', 'vehicle_age', 'mileage_per_year', 'brand_popularity']

    df_m = df.copy()
    encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        df_m[col] = le.fit_transform(df_m[col].astype(str))
        encoders[col] = le

    X = df_m[cat_cols + num_cols]; y = df_m['price']
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
    rf = RandomForestRegressor(n_estimators=100, max_depth=15, n_jobs=-1, random_state=42)
    rf.fit(Xtr, ytr); yp = rf.predict(Xte)

    return {
        'model': rf, 'encoders': encoders, 'cat_cols': cat_cols, 'num_cols': num_cols,
        'feature_names': cat_cols + num_cols,
        'mae': mean_absolute_error(yte, yp),
        'rmse': np.sqrt(mean_squared_error(yte, yp)),
        'r2': r2_score(yte, yp),
        'y_test': yte.values, 'y_pred': yp,
    }

with st.spinner("⚙ Initializing AutoPrice AI Engine..."):
    df  = load_data()
    mdl = train_model(df)

# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hud-header">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;">
        <div>
            <div class="hud-title">ARTHARA AUTO <span>INTELLIGENCE</span></div>
            <div class="hud-sub">AI-Powered Vehicle Valuation System · Random Forest Regressor</div>
            <div class="hud-badge">⬡ System Online · Model Active · Dataset Loaded</div>
            <div style="font-family:Rajdhani,sans-serif; font-size:0.75rem; color:#5A8AAA; margin-top:0.3rem; letter-spacing:0.08em;">Deploy by : Arthur Fikry Swara</div>
        </div>
        <div style="display:flex; gap:2rem; align-items:center;">
            <div style="text-align:center;">
                <div style="font-family:Rajdhani,sans-serif; font-size:0.62rem; color:#3A5A70; letter-spacing:0.15em; text-transform:uppercase;">R² Accuracy</div>
                <div style="font-family:Orbitron,sans-serif; font-size:1.6rem; font-weight:900; color:#FF8C00;">{mdl['r2']*100:.1f}%</div>
            </div>
            <div style="text-align:center;">
                <div style="font-family:Rajdhani,sans-serif; font-size:0.62rem; color:#3A5A70; letter-spacing:0.15em; text-transform:uppercase;">Mean Error</div>
                <div style="font-family:Orbitron,sans-serif; font-size:1.6rem; font-weight:900; color:#4AB3FF;">${mdl['mae']/1000:.1f}k</div>
            </div>
            <div style="text-align:center;">
                <div style="font-family:Rajdhani,sans-serif; font-size:0.62rem; color:#3A5A70; letter-spacing:0.15em; text-transform:uppercase;">Records</div>
                <div style="font-family:Orbitron,sans-serif; font-size:1.6rem; font-weight:900; color:#2ECC71;">{len(df):,}</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── INPUT PANEL ──────────────────────────────────────────────────────────────
st.markdown('<div class="input-panel">', unsafe_allow_html=True)
st.markdown('<div class="input-panel-title">Vehicle Specification Input</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    input_make = st.selectbox("Brand", BRANDS)
    input_year = st.selectbox("Tahun Produksi", sorted(df['year'].unique(), reverse=True))
with c2:
    input_body    = st.selectbox("Body Type", sorted(df['body_type'].unique()))
    input_mileage = st.number_input("Mileage (miles)", 500, 300_000, 80_000, 1_000)
with c3:
    input_fuel         = st.selectbox("Bahan Bakar", df['fuel_type'].unique())
    input_transmission = st.selectbox("Transmisi", df['transmission'].unique())
with c4:
    input_drivetrain = st.selectbox("Drivetrain", df['drivetrain'].unique())
    input_condition  = st.selectbox("Kondisi", ["Excellent", "Good", "Fair"])

ca, cb, cc, cd = st.columns([1.3, 1.3, 1.8, 1.3])
with ca:
    input_accident = st.selectbox("Riwayat Kecelakaan", ["None", "Minor", "Major"])
with cb:
    input_engine_hp = st.number_input("Engine HP", 50, 700, 200, 10)
with cc:
    suggested   = BODY_MODEL_SUGGEST.get(input_make, {}).get(input_body, BRAND_MODELS[input_make][0])
    model_list  = BRAND_MODELS[input_make]
    default_idx = model_list.index(suggested) if suggested in model_list else 0
    input_model = st.selectbox("Model (auto-saran dari Body Type)", model_list, index=default_idx)
with cd:
    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("⬡  ANALYZE & PREDICT")

st.markdown('</div>', unsafe_allow_html=True)

# ─── PREDICTION RESULTS ────────────────────────────────────────────────────────
if predict_btn:
    vehicle_age  = max(2025 - input_year, 1)
    mpery        = input_mileage / vehicle_age
    brand_pop    = df[df['make'] == input_make]['brand_popularity'].mean()

    enc = mdl['encoders']
    def safe_enc(encoder, v):
        return encoder.transform([v])[0] if v in list(encoder.classes_) else 0

    vec = {
        'make':             safe_enc(enc['make'], input_make),
        'model':            safe_enc(enc['model'], input_model),
        'transmission':     safe_enc(enc['transmission'], input_transmission),
        'fuel_type':        safe_enc(enc['fuel_type'], input_fuel),
        'drivetrain':       safe_enc(enc['drivetrain'], input_drivetrain),
        'body_type':        safe_enc(enc['body_type'], input_body),
        'condition':        safe_enc(enc['condition'], input_condition),
        'accident_history': safe_enc(enc['accident_history'], input_accident),
        'year': input_year, 'mileage': input_mileage, 'engine_hp': input_engine_hp,
        'vehicle_age': vehicle_age, 'mileage_per_year': mpery, 'brand_popularity': brand_pop,
    }
    Xinp       = pd.DataFrame([vec])[mdl['cat_cols'] + mdl['num_cols']]
    pred_price = mdl['model'].predict(Xinp)[0]
    low, high  = pred_price * 0.90, pred_price * 1.10

    price_min = float(df['price'].min())
    price_max = float(df['price'].max())
    score     = round(max(1.0, min(9.9, ((pred_price - price_min) / (price_max - price_min)) * 10)), 1)
    mpg_est   = round(max(10, 55 - input_engine_hp * 0.055 - input_mileage / 25000), 1)
    perf_s    = round(min(9.9, 3.5 + (input_engine_hp / 100) * 0.85), 1)

    cond_color = '#2ECC71' if input_condition == 'Excellent' else '#FF8C00' if input_condition == 'Good' else '#FF6B6B'
    acc_color  = '#FF6B6B' if input_accident != 'None' else '#2ECC71'
    acc_icon   = '⚠' if input_accident != 'None' else '✓'
    img_path   = get_image_path(input_make, input_model)

    # ═══════════════════════════════════════════════════════════════
    # ROW 1 — HERO: Car image CENTER flanked by specs & price
    # ═══════════════════════════════════════════════════════════════
    st.markdown("<br>", unsafe_allow_html=True)
    hero_l, hero_c, hero_r = st.columns([1, 1.6, 1], gap="medium")

    # ── HERO LEFT: Vehicle Specs ──
    with hero_l:
        st.markdown(f"""
        <div class="car-panel" style="height:100%;">
            <div class="car-panel-title">Vehicle Specs</div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.4rem;">
                <div class="spec-cell">
                    <div class="spec-cell-lbl">Brand</div>
                    <div class="spec-cell-val">{input_make}</div>
                </div>
                <div class="spec-cell">
                    <div class="spec-cell-lbl">Model</div>
                    <div class="spec-cell-val">{input_model}</div>
                </div>
                <div class="spec-cell">
                    <div class="spec-cell-lbl">Year</div>
                    <div class="spec-cell-val">📅 {input_year}</div>
                </div>
                <div class="spec-cell">
                    <div class="spec-cell-lbl">Mileage</div>
                    <div class="spec-cell-val">🔄 {input_mileage:,} mi</div>
                </div>
                <div class="spec-cell">
                    <div class="spec-cell-lbl">Fuel Type</div>
                    <div class="spec-cell-val">⛽ {input_fuel}</div>
                </div>
                <div class="spec-cell">
                    <div class="spec-cell-lbl">Body Type</div>
                    <div class="spec-cell-val">🚘 {input_body}</div>
                </div>
                <div class="spec-cell">
                    <div class="spec-cell-lbl">Transmission</div>
                    <div class="spec-cell-val">⚙ {input_transmission}</div>
                </div>
                <div class="spec-cell">
                    <div class="spec-cell-lbl">Drivetrain</div>
                    <div class="spec-cell-val">{input_drivetrain}</div>
                </div>
                <div class="spec-cell">
                    <div class="spec-cell-lbl">Condition</div>
                    <div class="spec-cell-val" style="color:{cond_color};">{input_condition}</div>
                </div>
                <div class="spec-cell">
                    <div class="spec-cell-lbl">Accident</div>
                    <div class="spec-cell-val" style="color:{acc_color};">{acc_icon} {input_accident}</div>
                </div>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:0.4rem; margin-top:0.6rem;">
                <div class="stat-box">
                    <div class="stat-val" style="color:#4AB3FF;">{input_engine_hp}</div>
                    <div class="stat-lbl">HP</div>
                </div>
                <div class="stat-box">
                    <div class="stat-val" style="color:#2ECC71;">{mpg_est}</div>
                    <div class="stat-lbl">Est. MPG</div>
                </div>
                <div class="stat-box">
                    <div class="stat-val" style="color:#FF8C00;">{perf_s}</div>
                    <div class="stat-lbl">Perf.</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── HERO CENTER: Car Image ──
    with hero_c:
        st.markdown(f"""
        <div style="
            background: linear-gradient(160deg, rgba(6,14,28,0.98) 0%, rgba(14,26,52,0.95) 100%);
            border: 1px solid rgba(255,140,0,0.35);
            border-top: 3px solid #FF8C00;
            border-radius: 6px;
            padding: 1.2rem 1.2rem 0.8rem 1.2rem;
            text-align: center;
            position: relative;
            overflow: hidden;
        ">
            <div style="
                position: absolute; top: 0; left: 0; right: 0; height: 3px;
                background: linear-gradient(90deg, transparent, #FF8C00, transparent);
            "></div>
            <div style="font-family:Orbitron,sans-serif; font-size:0.65rem; font-weight:700;
                 color:#FF8C00; letter-spacing:0.2em; text-transform:uppercase; margin-bottom:0.6rem;">
                ◈ {input_make} · {input_model} · {input_year} ◈
            </div>
        """, unsafe_allow_html=True)

        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
        else:
            st.markdown(f"""
            <div style="padding:3.5rem 1rem; color:#3A5A70; text-align:center;">
                <div style="font-size:5rem; filter: drop-shadow(0 0 20px rgba(255,140,0,0.3));">🚗</div>
                <div style="font-family:Rajdhani,sans-serif; font-size:0.72rem; margin-top:0.6rem;
                     letter-spacing:0.12em; text-transform:uppercase; color:#4A7090;">{input_make} {input_model}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown(f"""
            <div style="margin-top:0.7rem; padding-top:0.7rem;
                 border-top: 1px solid rgba(255,140,0,0.15); text-align:center;">
                <div style="font-family:Rajdhani,sans-serif; font-size:0.6rem; color:#3A5A70;
                     letter-spacing:0.15em; text-transform:uppercase; margin-bottom:0.3rem;">
                    Estimated Market Value
                </div>
                <div style="font-family:Orbitron,sans-serif; font-size:2.6rem; font-weight:900;
                     color:#FF8C00; text-shadow: 0 0 30px rgba(255,140,0,0.45); line-height:1.05;">
                    ${pred_price:,.0f}
                </div>
                <div style="font-family:Rajdhani,sans-serif; font-size:0.8rem; color:#5A8AAA; margin-top:0.25rem;">
                    Fair Range: <span style="color:#4AB3FF; font-weight:700;">${low:,.0f}</span>
                    &nbsp;—&nbsp;
                    <span style="color:#4AB3FF; font-weight:700;">${high:,.0f}</span>
                </div>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:0.5rem; margin-top:0.7rem;">
                <div class="stat-box">
                    <div class="stat-val" style="color:#2ECC71; font-size:1.3rem;">{score}<span style="font-size:0.65rem; color:#2A5040;">/10</span></div>
                    <div class="stat-lbl">Value Score</div>
                </div>
                <div class="stat-box">
                    <div class="stat-val" style="color:#4AB3FF; font-size:1.3rem;">{mpg_est}</div>
                    <div class="stat-lbl">Fuel Eff.</div>
                </div>
                <div class="stat-box">
                    <div class="stat-val" style="color:#FF8C00; font-size:1.3rem;">{perf_s}</div>
                    <div class="stat-lbl">Perf Score</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── HERO RIGHT: Gauge + Accuracy Scatter ──
    with hero_r:
        st.markdown('<div class="chart-panel"><div class="chart-title">Price Position in Market</div>', unsafe_allow_html=True)
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number", value=pred_price,
            number={'prefix': '$', 'valueformat': ',.0f',
                    'font': {'color': ORANGE, 'family': 'Orbitron', 'size': 18}},
            gauge={
                'axis': {'range': [price_min, price_max],
                         'tickcolor': '#3A5A70', 'tickfont': {'color': '#3A5A70', 'size': 7}},
                'bar': {'color': ORANGE, 'thickness': 0.22},
                'bgcolor': 'rgba(4,10,22,0)', 'bordercolor': 'rgba(255,140,0,0.15)',
                'steps': [
                    {'range': [price_min, price_max*0.33], 'color': 'rgba(74,179,255,0.06)'},
                    {'range': [price_max*0.33, price_max*0.66], 'color': 'rgba(255,140,0,0.06)'},
                    {'range': [price_max*0.66, price_max], 'color': 'rgba(255,107,107,0.06)'},
                ],
                'threshold': {'line': {'color': BLUE, 'width': 2}, 'thickness': 0.75,
                              'value': float(df['price'].median())}
            }
        ))
        fig_g.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': '#4A7090'},
                            height=200, margin=dict(t=8, b=5, l=12, r=12))
        st.plotly_chart(fig_g, use_container_width=True)
        st.markdown(f"""<div style="text-align:center; font-family:Rajdhani,sans-serif; font-size:0.6rem;
            color:#2A4A60; letter-spacing:0.08em; margin-top:-0.5rem;">
            MEDIAN ${df['price'].median():,.0f}</div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-panel" style="margin-top:0.6rem;"><div class="chart-title">Actual vs Predicted</div>', unsafe_allow_html=True)
        idx = np.random.choice(len(mdl['y_test']), min(280, len(mdl['y_test'])), replace=False)
        fig_sc = go.Figure()
        fig_sc.add_trace(go.Scatter(x=mdl['y_test'][idx], y=mdl['y_pred'][idx],
            mode='markers', marker=dict(color=ORANGE, opacity=0.28, size=3)))
        mx = max(mdl['y_test'][idx].max(), mdl['y_pred'][idx].max())
        fig_sc.add_trace(go.Scatter(x=[0, mx], y=[0, mx], mode='lines',
            line=dict(color=BLUE, dash='dash', width=1.2)))
        fig_sc.update_layout(**PLOTLY_LAYOUT, height=160, showlegend=False)
        fig_sc.update_xaxes(title="Actual ($)"); fig_sc.update_yaxes(title="Predicted ($)")
        st.plotly_chart(fig_sc, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════
    # ROW 2 — BOTTOM: 3 symmetric charts
    # ═══════════════════════════════════════════════════════════════
    st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)
    bot_l, bot_m, bot_r = st.columns([1, 1, 1], gap="medium")

    # ── BOTTOM LEFT: Feature Importance ──
    with bot_l:
        st.markdown('<div class="chart-panel"><div class="chart-title">Key Price Factors</div>', unsafe_allow_html=True)
        fi    = mdl['model'].feature_importances_
        fi_df = pd.DataFrame({'Factor': mdl['feature_names'], 'Score': fi})
        fi_df = fi_df.sort_values('Score', ascending=True).tail(8)
        fig_fi = px.bar(fi_df, x='Score', y='Factor', orientation='h', color='Score',
                        color_continuous_scale=[[0,'rgba(255,140,0,0.08)'],[0.4,'rgba(255,140,0,0.4)'],[1,ORANGE]])
        fig_fi.update_layout(**PLOTLY_LAYOUT, height=230, coloraxis_showscale=False)
        fig_fi.update_xaxes(title="Importance Score")
        fig_fi.update_yaxes(title="", tickfont=dict(size=8, color='#5A8AAA'))
        st.plotly_chart(fig_fi, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── BOTTOM MIDDLE: Market Comparison ──
    with bot_m:
        st.markdown(f'<div class="chart-panel"><div class="chart-title">Market Comparison — {input_make} Lineup</div>', unsafe_allow_html=True)
        mm = (df[df['make']==input_make].groupby('model')['price'].median()
              .reindex(BRAND_MODELS[input_make]).reset_index())
        mm.columns = ['model', 'price']
        fig_br = go.Figure(go.Bar(
            x=mm['model'], y=mm['price'],
            marker_color=[ORANGE if m == input_model else 'rgba(74,179,255,0.25)' for m in mm['model']],
            text=[f"${v/1000:.0f}k" for v in mm['price']],
            textposition='outside', textfont=dict(color='#4A7090', size=8),
        ))
        fig_br.add_hline(y=pred_price, line_color=GREEN, line_dash='dash', line_width=1.5,
                         annotation_text="Your Vehicle", annotation_font_color=GREEN, annotation_font_size=8)
        fig_br.update_layout(**PLOTLY_LAYOUT, height=230, showlegend=False)
        fig_br.update_xaxes(tickangle=-20, tickfont=dict(size=8))
        fig_br.update_yaxes(title="Price ($)")
        st.plotly_chart(fig_br, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── BOTTOM RIGHT: Brand Price Distribution ──
    with bot_r:
        st.markdown('<div class="chart-panel"><div class="chart-title">Brand Price Distribution</div>', unsafe_allow_html=True)
        fig_h = go.Figure()
        fig_h.add_trace(go.Histogram(x=df[df['make']==input_make]['price'], nbinsx=28,
            marker_color=ORANGE, opacity=0.45))
        fig_h.add_vline(x=pred_price, line_color=GREEN, line_width=2, line_dash='dash',
                        annotation_text="Predicted", annotation_font_color=GREEN, annotation_font_size=8)
        fig_h.update_layout(**PLOTLY_LAYOUT, height=230, showlegend=False)
        fig_h.update_xaxes(title="Price ($)"); fig_h.update_yaxes(title="Count")
        st.plotly_chart(fig_h, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # Default overview state
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="chart-panel"><div class="chart-title">Market Overview — Price Intelligence</div>', unsafe_allow_html=True)
    oc1, oc2 = st.columns(2)
    with oc1:
        bp = df.groupby('make')['price'].median().reset_index()
        fig_b = px.bar(bp, x='make', y='price', color='make', color_discrete_sequence=COLORS)
        fig_b.update_layout(**PLOTLY_LAYOUT, height=270, showlegend=False, title="Median Price by Brand")
        fig_b.update_yaxes(title="Price (USD)")
        st.plotly_chart(fig_b, use_container_width=True)
    with oc2:
        fig_bx = px.box(df, x='make', y='price', color='make', color_discrete_sequence=COLORS)
        fig_bx.update_layout(**PLOTLY_LAYOUT, height=270, showlegend=False, title="Price Distribution by Brand")
        fig_bx.update_yaxes(title="Price (USD)")
        st.plotly_chart(fig_bx, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; padding:1.8rem; font-family:Rajdhani,sans-serif; font-size:0.82rem;
         color:#2A4A60; letter-spacing:0.12em; text-transform:uppercase; margin-top:0.5rem;">
        ◈ Fill in vehicle specifications above and click
        <span style="color:#FF8C00; font-weight:700;">ANALYZE & PREDICT PRICE</span> ◈
    </div>
    """, unsafe_allow_html=True)
