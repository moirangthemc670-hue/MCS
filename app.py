import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit.components.v1 as components
from io import BytesIO
import time
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="CurateX AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# SYSTEM ANNOUNCER
# =========================================================

def announce(message):

    components.html(f"""

    <script>

    const msg = new SpeechSynthesisUtterance();

    msg.text = "{message}";
    msg.rate = 1;
    msg.pitch = 0.9;
    msg.volume = 1;

    window.speechSynthesis.speak(msg);

    </script>

    """, height=0)

# =========================================================
# RUBY CUBE VIDEO LOADER
# =========================================================

loading = st.empty()

loading.markdown("""

<div id="ruby-loader">

<!-- Background Video -->

<video autoplay muted loop playsinline id="bg-video">
    <source src="https://cdn.pixabay.com/vimeo/328940142/digital-23315.mp4?width=1280&hash=4a8a5b6c4f1fcb2f8dfecfcf7f0d8cbf5f9c3c48" type="video/mp4">
</video>

<!-- Dark Overlay -->

<div class="overlay"></div>

<!-- Main Content -->

<div class="content">

<div class="scene">

<div class="cube">

<div class="face front"></div>
<div class="face back"></div>
<div class="face right"></div>
<div class="face left"></div>
<div class="face top"></div>
<div class="face bottom"></div>

</div>

</div>

<h1 class="loading-title">
🌐CurateX AI
</h1>

<p class="loading-sub">
INITIALIZING AI ...
</p>

</div>

</div>

<style>

/* Main Loader */

#ruby-loader{

position:fixed;
top:0;
left:0;

width:100%;
height:100%;

overflow:hidden;

z-index:999999;
}

/* Background Video */

#bg-video{

position:absolute;
top:0;
left:0;

width:100%;
height:100%;

object-fit:cover;

z-index:-3;
}

/* Overlay */

.overlay{

position:absolute;
top:0;
left:0;

width:100%;
height:100%;

background:
linear-gradient(
135deg,
rgba(0,0,0,0.82),
rgba(20,0,20,0.75),
rgba(0,0,0,0.9)
);

backdrop-filter:blur(3px);

z-index:-2;
}

/* Content */

.content{

position:relative;

width:100%;
height:100%;

display:flex;
flex-direction:column;
justify-content:center;
align-items:center;
}

/* 3D Scene */

.scene{

width:160px;
height:160px;

perspective:900px;

margin-bottom:40px;
}

/* Cube */

.cube{

width:100%;
height:100%;

position:relative;

transform-style:preserve-3d;

animation:rotateCube 6s infinite linear;
}

/* Faces */

.face{

position:absolute;

width:160px;
height:160px;

background:rgba(255,0,90,0.10);

border:2px solid #ff0055;

box-shadow:
0 0 25px #ff0055,
inset 0 0 25px #ff0055;
}

/* Cube Sides */

.front{
transform:rotateY(0deg) translateZ(80px);
}

.back{
transform:rotateY(180deg) translateZ(80px);
}

.right{
transform:rotateY(90deg) translateZ(80px);
}

.left{
transform:rotateY(-90deg) translateZ(80px);
}

.top{
transform:rotateX(90deg) translateZ(80px);
}

.bottom{
transform:rotateX(-90deg) translateZ(80px);
}

/* Rotation */

@keyframes rotateCube{

0%{
transform:rotateX(0deg) rotateY(0deg);
}

100%{
transform:rotateX(360deg) rotateY(360deg);
}
}

/* Title */

.loading-title{

font-size:54px;
font-weight:900;

letter-spacing:4px;

color:#ff0055;

margin:0;

text-shadow:
0 0 10px #ff0055,
0 0 25px #ff0055,
0 0 50px #ff0055;

animation:pulseText 2s infinite;
}

/* Subtitle */

.loading-sub{

margin-top:18px;

font-size:18px;

font-family:monospace;

letter-spacing:6px;

color:white;

opacity:0.95;
}

/* Pulse */

@keyframes pulseText{

0%{
opacity:0.5;
transform:scale(1);
}

50%{
opacity:1;
transform:scale(1.05);
}

100%{
opacity:0.5;
transform:scale(1);
}
}

/* Mobile */

@media(max-width:768px){

.loading-title{
font-size:30px;
text-align:center;
}

.loading-sub{
font-size:13px;
letter-spacing:3px;
}

.scene{
width:120px;
height:120px;
}

.face{
width:120px;
height:120px;
}

.front{
transform:rotateY(0deg) translateZ(60px);
}

.back{
transform:rotateY(180deg) translateZ(60px);
}

.right{
transform:rotateY(90deg) translateZ(60px);
}

.left{
transform:rotateY(-90deg) translateZ(60px);
}

.top{
transform:rotateX(90deg) translateZ(60px);
}

.bottom{
transform:rotateX(-90deg) translateZ(60px);
}

}

</style>

""", unsafe_allow_html=True)

time.sleep(2)

loading.empty()
# =========================================================
# SOUND EFFECTS
# =========================================================

components.html("""

<!-- STARTUP SOUND -->
<audio id="startupSound" autoplay>
    <source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mp3">
</audio>

<!-- SUCCESS SOUND -->
<audio id="successSound">
    <source src="https://assets.mixkit.co/active_storage/sfx/1435/1435-preview.mp3" type="audio/mp3">
</audio>

<!-- WARNING SOUND -->
<audio id="warningSound">
    <source src="https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3" type="audio/mp3">
</audio>

<!-- HOVER SOUND -->
<audio id="hoverSound">
    <source src="https://assets.mixkit.co/active_storage/sfx/1114/1114-preview.mp3" type="audio/mp3">
</audio>

<script>

// ======================================
// STARTUP SOUND
// ======================================

window.addEventListener('load', () => {

    const startup =
    document.getElementById("startupSound");

    startup.volume = 0.4;

   startup.play().catch(function(error){});

});

// ======================================
// BUTTON HOVER SOUND
// ======================================

setTimeout(() => {

    const buttons =
    parent.document.querySelectorAll("button");

    buttons.forEach(btn => {

        btn.addEventListener("mouseenter", () => {

            const hover =
            document.getElementById("hoverSound");

            hover.volume = 0.15;

            hover.currentTime = 0;

            hover.play();

        });

    });

}, 2000);

// ======================================
// GLOBAL FUNCTIONS
// ======================================

window.playSuccess = function(){

    const s =
    document.getElementById("successSound");

    s.volume = 0.4;

    s.currentTime = 0;

    s.play();
}

window.playWarning = function(){

    const w =
    document.getElementById("warningSound");

    w.volume = 0.5;

    w.currentTime = 0;

    w.play();
}

</script>

""", height=0)
# =========================================================
# AI LOGO
# =========================================================

st.markdown("""
<div style="
display:flex;
align-items:center;
gap:18px;
margin-bottom:20px;
">

<div style="
width:80px;
height:80px;
border-radius:20px;
background:linear-gradient(135deg,#00FFA3,#00c3ff);
display:flex;
align-items:center;
justify-content:center;
font-size:40px;
font-weight:bold;
color:black;
box-shadow:0 0 30px #00FFA3;
animation:pulseLogo 2s infinite;
">
⚡
</div>

<div>

<h1 style="
margin:0;
font-size:42px;
font-weight:900;
color:white;
">
🌐CurateX AI
</h1>

<p style="
margin:0;
color:#00FFA3;
letter-spacing:3px;
">
Created by Moirangthem Chitaranjan Singh
</p>

</div>

</div>

<style>

@keyframes pulseLogo{
0%{transform:scale(1);}
50%{transform:scale(1.08);}
100%{transform:scale(1);}
}

</style>
""", unsafe_allow_html=True)
st.markdown(f"""
<div class="glass float">

<h2 class="neon">🚀 CurateX AI Enterprise System</h2>

<p>
Advanced Artificial Intelligence Data Intelligence Platform
</p>

</div>
""", unsafe_allow_html=True)
# =========================================================
# DATA CLEANING FUNCTIONS
# =========================================================

def remove_duplicates(df):
    return df.drop_duplicates()
def fill_missing(df):
    df = df.copy()

    for col in df.columns:
        if df[col].isnull().sum() == 0:
            continue

        # Handle numeric columns
        if pd.api.types.is_numeric_dtype(df[col]):

            median_value = df[col].median()

            if pd.isna(median_value):
                continue

            # Age and Experience must contain whole numbers
            if col.strip().lower() in ["age", "experience"]:
                median_value = int(round(median_value))

                df[col] = df[col].fillna(median_value)

                # Ensure all existing values are whole numbers too
                df[col] = df[col].round().astype("Int64")

            else:
                df[col] = df[col].fillna(median_value)

        # Handle text columns
        else:
            mode_values = df[col].mode(dropna=True)

            if not mode_values.empty:
                df[col] = df[col].fillna(mode_values.iloc[0])

    return df
def drop_missing_categorical(df):
    df = df.copy()

    # Find categorical columns
    categorical_cols = df.select_dtypes(
        include=["object", "category", "string"]
    ).columns

    # Remove rows with missing categorical values
    df = df.dropna(subset=categorical_cols)

    return df
def clean_age(df):
    df = df.copy()

    # Find the Age column, ignoring capitalization and spaces
    age_col = next(
        (col for col in df.columns if col.strip().lower() == "age"),
        None
    )

    # If the Age column doesn't exist, return the data unchanged
    if age_col is None:
        return df

    # Convert Age values to numeric
    df[age_col] = pd.to_numeric(df[age_col], errors="coerce")

    # Round ages to whole numbers
    df[age_col] = df[age_col].round()

    # Accept ages from 18 to 65
    valid_ages = df.loc[
        df[age_col].between(18, 65),
        age_col
    ]

    # Replace invalid ages with the median valid age
    if not valid_ages.empty:
        median_age = int(round(valid_ages.median()))

        df.loc[
            ~df[age_col].between(18, 65),
            age_col
        ] = median_age

    # Store Age as a nullable integer column
    df[age_col] = df[age_col].astype("Int64")

    return df

def clean_experience(df):
    """Convert Experience to non-negative whole years and fill missing values."""
    df = df.copy()
    col = next((c for c in df.columns if c.strip().lower() == "experience"), None)
    if col is None:
        return df
    values = pd.to_numeric(df[col], errors="coerce").round()
    valid = values[values >= 0]
    if not valid.empty:
        values = values.fillna(int(round(valid.median())))
    df[col] = values.clip(lower=0).astype("Int64")
    return df


def fix_salary_by_experience(df):
    """Clean salary values; do not invent salary estimates from experience."""
    df = df.copy()
    col = next((c for c in df.columns if c.strip().lower() == "salary"), None)
    if col is None:
        return df
    df[col] = pd.to_numeric(df[col], errors="coerce")
    # Negative salaries are invalid; treat them as missing and fill with median.
    df.loc[df[col] < 0, col] = np.nan
    if df[col].notna().any():
        df[col] = df[col].fillna(df[col].median())
    return df


def smart_fill_department(df):
    """Fill missing Department values using the most frequent department."""
    df = df.copy()
    col = next((c for c in df.columns if c.strip().lower() == "department"), None)
    if col is None:
        return df
    mode = df[col].dropna().astype(str).str.strip()
    mode = mode[mode.ne("")]
    if not mode.empty:
        fill_value = mode.mode().iloc[0]
        df[col] = df[col].replace(r"^\s*$", np.nan, regex=True).fillna(fill_value)
    return df


def smart_fill(df):
    """Predict missing numeric values where there are usable numeric predictors."""
    df = df.copy()
    # Normalize Age/Experience to numeric before selecting numeric columns.
    for target_name in ("age", "experience"):
        col = next((c for c in df.columns if c.strip().lower() == target_name), None)
        if col is not None:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    numeric_cols = list(df.select_dtypes(include="number").columns)
    for col in numeric_cols:
        missing_mask = df[col].isna()
        if not missing_mask.any():
            continue
        train = df.loc[~missing_mask, numeric_cols]
        test = df.loc[missing_mask, numeric_cols]
        if len(train) < 2 or test.empty:
            continue
        predictors = [c for c in numeric_cols if c != col]
        if not predictors:
            median = df[col].median()
            if pd.notna(median):
                value = round(median) if col.strip().lower() in ("age", "experience") else median
                df.loc[missing_mask, col] = value
            continue
        X_train = train[predictors].fillna(0)
        X_test = test[predictors].fillna(0)
        y_train = train[col]
        try:
            model = LinearRegression()
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            if col.strip().lower() in ("age", "experience"):
                predictions = np.round(predictions).astype(int)
            elif (df[col].dropna() % 1 == 0).all():
                predictions = np.round(predictions).astype(int)
            df.loc[missing_mask, col] = predictions
        except (ValueError, TypeError):
            # Safe fallback if model training is not possible.
            median = df[col].median()
            if pd.notna(median):
                df.loc[missing_mask, col] = median

    age_col = next((c for c in df.columns if c.strip().lower() == "age"), None)
    if age_col is not None:
        df[age_col] = pd.to_numeric(df[age_col], errors="coerce").round().astype("Int64")
    exp_col = next((c for c in df.columns if c.strip().lower() == "experience"), None)
    if exp_col is not None:
        df[exp_col] = pd.to_numeric(df[exp_col], errors="coerce").round().astype("Int64")
    return df


def encode_categorical(df):
    """Label-encode text/category columns, preserving missing values as a category."""
    df = df.copy()
    for col in df.select_dtypes(include=["object", "category", "string"]).columns:
        values = df[col].astype("string").fillna("Unknown")
        df[col] = LabelEncoder().fit_transform(values.astype(str))
    return df


def remove_outliers(df):
    """Remove rows with IQR outliers in numeric columns; skip constant/small columns."""
    df = df.copy()
    numeric_cols = list(df.select_dtypes(include="number").columns)
    for col in numeric_cols:
        values = df[col].dropna()
        if len(values) < 4 or values.nunique() < 2:
            continue
        q1, q3 = values.quantile([0.25, 0.75])
        iqr = q3 - q1
        if pd.isna(iqr) or iqr == 0:
            continue
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        df = df[df[col].isna() | df[col].between(lower, upper)]
    return df




# =========================================================
# PRIVACY-PRESERVING DATA PROCESSING
# =========================================================

def mask_email(value):
    """Mask the local part of an email address while keeping its domain."""
    if pd.isna(value):
        return value
    value = str(value).strip()
    if "@" not in value:
        return value
    local, domain = value.rsplit("@", 1)
    if not local:
        return "***@" + domain
    return local[0] + "***@" + domain


def mask_phone(value):
    """Keep only the last four digits of a phone number."""
    if pd.isna(value):
        return value
    value = str(value).strip()
    digits = "".join(ch for ch in value if ch.isdigit())
    if not digits:
        return value
    visible = digits[-4:]
    return "*" * max(0, len(digits) - len(visible)) + visible


def apply_privacy_protection(
    data,
    email_cols=None,
    phone_cols=None,
    name_cols=None,
    id_cols=None,
    mask_emails=True,
    mask_phones=True,
    anonymize_names=True,
    anonymize_ids=True,
):
    """Return a protected copy; the input DataFrame is never modified."""
    protected = data.copy(deep=True)
    email_cols = email_cols or []
    phone_cols = phone_cols or []
    name_cols = name_cols or []
    id_cols = id_cols or []

    if mask_emails:
        for col in email_cols:
            protected[col] = protected[col].apply(mask_email)

    if mask_phones:
        for col in phone_cols:
            protected[col] = protected[col].apply(mask_phone)

    if anonymize_names:
        for col in name_cols:
            values = protected[col]
            mapping = {}
            counter = 1
            anonymized = []
            for value in values:
                if pd.isna(value) or str(value).strip() == "":
                    anonymized.append(value)
                    continue
                key = str(value)
                if key not in mapping:
                    mapping[key] = f"Person_{counter:03d}"
                    counter += 1
                anonymized.append(mapping[key])
            protected[col] = anonymized

    if anonymize_ids:
        for col in id_cols:
            protected[col] = [
                pd.NA if pd.isna(value) or str(value).strip() == ""
                else f"ID_{i:04d}"
                for i, value in enumerate(protected[col], start=1)
            ]

    return protected


# =========================================================
# MATRIX BACKGROUND
# =========================================================

components.html("""

<canvas id="matrix"></canvas>

<style>

#matrix{
position:fixed;
top:0;
left:0;
width:100%;
height:100%;
z-index:-1;
pointer-events:none;
opacity:0.12;
}

</style>

<script>

const canvas = document.getElementById("matrix");
const ctx = canvas.getContext("2d");

canvas.height = window.innerHeight;
canvas.width = window.innerWidth;

const letters = "01アイウエオカキクケコABCDEFGHIJKLMNOPQRSTUVWXYZ";
const fontSize = 14;
const columns = canvas.width/fontSize;

const drops = [];

for(let i=0;i<columns;i++){
drops[i]=1;
}

function draw(){

ctx.fillStyle = "rgba(0,0,0,0.05)";
ctx.fillRect(0,0,canvas.width,canvas.height);

ctx.fillStyle="#00FFA3";
ctx.font=fontSize+"px monospace";

for(let i=0;i<drops.length;i++){

const text = letters[Math.floor(Math.random()*letters.length)];

ctx.fillText(text,i*fontSize,drops[i]*fontSize);

if(drops[i]*fontSize>canvas.height && Math.random()>0.975){
drops[i]=0;
}

drops[i]++;
}
}

setInterval(draw,33);

</script>

""", height=0)

# =========================================================
# SCANLINE EFFECT
# =========================================================

st.markdown("""
<style>

.scanline{

position:fixed;
top:0;
left:0;
width:100%;
height:6px;

background:linear-gradient(
90deg,
transparent,
#00FFA3,
transparent
);

z-index:9999;

animation:scanMove 4s linear infinite;
}

@keyframes scanMove{

0%{
top:0%;
}

100%{
top:100%;
}
}

</style>

<div class="scanline"></div>
""", unsafe_allow_html=True)

## =========================================================
# ULTRA FUTURISTIC UI
# =========================================================

st.markdown("""
<style>

/* =======================================================
GLOBAL
======================================================= */

html, body, [class*="css"]  {

    font-family: 'Segoe UI', sans-serif;
}

/* Main App */

.stApp {

    background:
    linear-gradient(
        135deg,
        #020617,
        #071426,
        #000000
    );

    color: white;
}

/* =======================================================
HEADINGS
======================================================= */

h1,h2,h3,h4,h5,h6 {

    color: white !important;
    font-weight: 800 !important;
}

/* =======================================================
SIDEBAR
======================================================= */

[data-testid="stSidebar"] {

    background: rgba(5,10,20,0.85);

    backdrop-filter: blur(20px);

    border-right: 1px solid rgba(255,255,255,0.08);
}

/* =======================================================
BUTTONS
======================================================= */

.stButton > button {

    width: 100%;

    border-radius: 18px;

    border: none;

    padding: 14px;

    font-size: 15px;

    font-weight: bold;

    color: black;

    background: linear-gradient(
        90deg,
        #00FFA3,
        #00c3ff
    );

    transition: 0.4s ease;
}

.stButton > button:hover {

    transform: scale(1.03);

    box-shadow:
    0 0 20px #00FFA3,
    0 0 50px #00c3ff;
}

/* =======================================================
DOWNLOAD BUTTON
======================================================= */

.stDownloadButton > button {

    width: 100%;

    border-radius: 18px;

    border: none;

    padding: 14px;

    font-weight: bold;

    color: black;

    background: linear-gradient(
        90deg,
        #00FFA3,
        #00c3ff
    );
}

/* =======================================================
INPUTS
======================================================= */

.stTextInput input,
.stNumberInput input,
.stSelectbox div {

    background-color: rgba(255,255,255,0.05) !important;

    color: white !important;

    border-radius: 12px !important;
}

/* =======================================================
DATAFRAME
======================================================= */

[data-testid="stDataFrame"] {

    border-radius: 20px;

    overflow: hidden;

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow:
    0 0 20px rgba(0,255,163,0.1);
}

/* =======================================================
METRIC CARDS
======================================================= */

[data-testid="metric-container"] {

    background: rgba(255,255,255,0.05);

    border: 1px solid rgba(255,255,255,0.08);

    padding: 15px;

    border-radius: 20px;

    backdrop-filter: blur(20px);

    box-shadow:
    0 0 25px rgba(0,255,163,0.12);

    transition: 0.3s;
}

[data-testid="metric-container"]:hover {

    transform: translateY(-5px);

    box-shadow:
    0 0 30px #00FFA3;
}

/* =======================================================
PLOTLY CHARTS
======================================================= */

.js-plotly-plot {

    border-radius: 20px;

    overflow: hidden;

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow:
    0 0 20px rgba(0,255,163,0.12);
}

/* =======================================================
SCROLLBAR
======================================================= */

::-webkit-scrollbar {

    width: 10px;
}

::-webkit-scrollbar-thumb {

    background: #00FFA3;

    border-radius: 20px;
}

/* =======================================================
GLASS CARD
======================================================= */

.glass {

    background: rgba(255,255,255,0.05);

    backdrop-filter: blur(20px);

    border-radius: 24px;

    padding: 25px;

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow:
    0 0 30px rgba(0,255,163,0.12);

    margin-bottom: 20px;
}

/* =======================================================
NEON TITLE
======================================================= */

.neon {

    color: #00FFA3;

    text-shadow:
    0 0 10px #00FFA3,
    0 0 20px #00FFA3,
    0 0 40px #00FFA3;
}

/* =======================================================
FLOAT ANIMATION
======================================================= */

.float {

    animation: floating 4s ease-in-out infinite;
}

@keyframes floating {

    0% {
        transform: translateY(0px);
    }

    50% {
        transform: translateY(-10px);
    }

    100% {
        transform: translateY(0px);
    }
}

</style>
""", unsafe_allow_html=True)
# =========================================================
# TYPING EFFECT
# =========================================================

components.html("""

<div id="typing"></div>

<script>

const text =
"BOSS I AM Waiting for Your Command";

let i = 0;

function type(){

if(i < text.length){

document.getElementById("typing").innerHTML += text.charAt(i);

i++;

setTimeout(type,50);

}
}

type();

</script>

<style>

#typing{

font-size:22px;
color:#00FFA3;
text-align:center;
font-family:monospace;
margin-bottom:20px;
letter-spacing:2px;
}

</style>

""", height=60)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("""
<div style="
background:linear-gradient(135deg,#00FFA3,#00c3ff);
padding:18px;
border-radius:18px;
text-align:center;
font-size:20px;
font-weight:bold;
color:black;
box-shadow:0 0 25px #00FFA3;
">
⚡ AI DATA CLEANER
</div>
""", unsafe_allow_html=True)

st.sidebar.success("🟢 KYANG MCS ONLINE")
# =========================================================
# THEME SWITCHER
# =========================================================
# =========================================================
# THEME SWITCHER
# =========================================================

st.sidebar.markdown("---")
st.sidebar.subheader("🎨 THEME")

theme = st.sidebar.radio(
    "Select Theme",
    [
        "Cyberpunk",
        "Ocean",
        "Midnight"
    ]
)

if theme == "Ocean":

    st.markdown("""
    <style>

    .stApp{
        background:
        linear-gradient(
            135deg,
            #021B79,
            #0575E6
        );
    }

    </style>
    """, unsafe_allow_html=True)

elif theme == "Midnight":

    st.markdown("""
    <style>

    .stApp{
        background:
        linear-gradient(
            135deg,
            #000000,
            #434343
        );
    }

    </style>
    """, unsafe_allow_html=True)
# =========================================================
# FILE UPLOAD
# =========================================================

uploaded_file = st.sidebar.file_uploader(
    "📂 Upload Dataset",
    type=["csv","xlsx"]
)

if uploaded_file:

    with st.spinner("🧠 AI analyzing dataset patterns..."):
        time.sleep(2)

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    status = "✅ Dataset Uploaded"

    announce("Dataset uploaded successfully Sir")

else:

    df = pd.read_csv("Data/sample_data.csv")

    status = "⚠ Using Sample Dataset"
# Ensure Age contains whole numbers immediately after loading.
df.columns = df.columns.str.strip()

if "Age" in df.columns:

    df["Age"] = pd.to_numeric(
        df["Age"],
        errors="coerce"
    ).round().astype("Int64")
original_df = df.copy()

st.sidebar.success(status)

# =========================================================
# AI HEALTH
# =========================================================

st.sidebar.markdown("---")
st.sidebar.subheader("🧠 AI HEALTH")

health = random.randint(85,100)

st.sidebar.metric(
    "AI Stability",
    f"{health}%"
)

st.sidebar.success(
    "Neural Systems Operational"
)

# =========================================================
# SYSTEM STATUS
# =========================================================

st.sidebar.markdown("---")
st.sidebar.subheader("🖥 SYSTEM STATUS")

cpu = random.randint(20,90)
ram = random.randint(30,95)
gpu = random.randint(15,100)

st.sidebar.progress(cpu/100)
st.sidebar.write(f"⚡ CPU : {cpu}%")

st.sidebar.progress(ram/100)
st.sidebar.write(f"🧠 RAM : {ram}%")

st.sidebar.progress(gpu/100)
st.sidebar.write(f"🔥 GPU : {gpu}%")

# =========================================================
# CLEANING TOOLS
# =========================================================

st.sidebar.markdown("---")
st.sidebar.subheader("🧹 CLEANING TOOLS")
if st.sidebar.button("🚀 AUTO CLEAN"):

    df = remove_duplicates(df)

    df = fill_missing(df)

    df = drop_missing_categorical(df)

    df = clean_age(df)

    df = clean_experience(df)

    df = fix_salary_by_experience(df)

    df = df.dropna(how="all")
    df = smart_fill_department(df)
if st.sidebar.button("🤖 SMART AI FILL"):

    announce("Artificial intelligence filling missing values")

    df = smart_fill(df)

    announce("AI fill completed")

if st.sidebar.button("⚡ ENCODE CATEGORIES"):

    announce("Encoding categorical values")

    df = encode_categorical(df)

    announce("Encoding completed")

if st.sidebar.button("🔥 REMOVE OUTLIERS"):

    announce("Removing outliers from dataset")

    df = remove_outliers(df)

    announce("Outlier removal completed")

# =========================================================
# METRICS
# =========================================================

st.markdown("## 📊 DATASET OVERVIEW")

c1,c2,c3,c4 = st.columns(4)

c1.metric("ROWS", df.shape[0])
c2.metric("COLUMNS", df.shape[1])
c3.metric("MISSING", df.isnull().sum().sum())
c4.metric("DUPLICATES", df.duplicated().sum())

# =========================================================
# QUALITY SCORE
# =========================================================
def data_quality_score(df):
    """Calculate a simple data quality score based on missing values."""

    if df.empty or df.shape[1] == 0:
        return 0

    total_cells = df.size
    missing_cells = df.isnull().sum().sum()

    score = ((total_cells - missing_cells) / total_cells) * 100

    return round(score, 2)
score = data_quality_score(df)

st.markdown("## 🎯 AI QUALITY SCORE")

st.progress(score/100)

# =========================================================
# AI INSIGHTS
# =========================================================

numeric_cols = df.select_dtypes(include=np.number).columns

st.markdown("## 🤖 AI INSIGHTS ENGINE")

missing = df.isnull().sum().sum()
duplicates = df.duplicated().sum()

insights = []

if missing > 0:
    insights.append(
        f"⚠ Dataset contains {missing} missing values."
    )

if duplicates > 0:
    insights.append(
        f"⚠ Dataset contains {duplicates} duplicate rows."
    )

if score > 90:
    insights.append(
        "✅ Excellent dataset quality detected."
    )

if len(numeric_cols) > 3:
    insights.append(
        "📊 Multiple numeric features available for AI analytics."
    )

for item in insights:
    st.info(item)

# =========================================================
# AI RECOMMENDATION ENGINE
# =========================================================

st.markdown("## 🤖 AI RECOMMENDATIONS")

recommendations = []

missing_percent = (
    df.isnull().sum().sum() / df.size
) * 100

if missing_percent > 10:
    recommendations.append(
        "⚠ High missing values detected. Use SMART AI FILL."
    )

if duplicates > 0:
    recommendations.append(
        "🧹 Duplicate rows found. Use AUTO CLEAN."
    )

if len(numeric_cols) > 5:
    recommendations.append(
        "📊 Large numeric dataset detected. Use correlation analytics."
    )

if score < 70:
    recommendations.append(
        "🚨 Dataset quality is low. AI optimization recommended."
    )

if len(recommendations) == 0:
    recommendations.append(
        "✅ Dataset looks highly optimized."
    )

for rec in recommendations:
    st.success(rec)

# =========================================================
# BEFORE / AFTER
# =========================================================

st.markdown("## 🔍 DATA TRANSFORMATION")

col1,col2 = st.columns(2)

with col1:
    st.markdown("### BEFORE CLEANING")
    st.dataframe(original_df, use_container_width=True)

with col2:
    st.markdown("### AFTER CLEANING")
    st.dataframe(df, use_container_width=True)

# =========================================================
# VISUALIZATION
# =========================================================

if len(numeric_cols) > 0:

    st.markdown("## 📊 DISTRIBUTION ANALYSIS")

    hist_col = st.selectbox(
        "SELECT NUMERIC COLUMN",
        numeric_cols
    )

    fig = px.histogram(
        df,
        x=hist_col,
        nbins=40,
        title="AI Distribution Analysis",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# HEATMAP
# =========================================================

if len(numeric_cols) > 1:

    st.markdown("## 🔥 CORRELATION HEATMAP")

    corr = df.corr(numeric_only=True)

    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="Viridis"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# ANOMALY DETECTION
# =========================================================

st.markdown("## 🚨 AI ANOMALY DETECTION")

for col in numeric_cols:

    mean = df[col].mean()
    std = df[col].std()

    anomalies = df[
        (df[col] > mean + 2*std) |
        (df[col] < mean - 2*std)
    ]

    st.write(
        f"{col} → {len(anomalies)} anomalies detected"
    )

# =========================================================
# AI PREDICTION MODEL
# =========================================================
# =========================================================
# AI PREDICTION MODEL
# =========================================================

if uploaded_file is not None:

    if len(numeric_cols) >= 2:

        st.markdown("## 🧠 AI PREDICTION ENGINE")

        target = st.selectbox(
            "SELECT TARGET COLUMN",
            numeric_cols
        )

        features = [c for c in numeric_cols if c != target]

        if len(features) > 0:

            if st.button("🚀 TRAIN AI MODEL"):

                announce("Training artificial intelligence model")

                X = df[features].fillna(0)
                y = df[target].fillna(0)

                model = RandomForestRegressor()

                model.fit(X, y)

                prediction = model.predict(X[:5])

                st.success("AI MODEL TRAINED SUCCESSFULLY")

                announce(
                    "Artificial intelligence model trained successfully"
                )

                pred_df = pd.DataFrame({
                    "Actual": y[:5].values,
                    "Predicted": prediction
                })

                st.dataframe(pred_df)

else:

    st.info(
        "📂 Upload dataset to enable AI prediction engine."
    )

# =========================================================
# LIVE STREAM
# =========================================================

st.markdown("## 📡 LIVE AI STREAM")

stream_data = pd.DataFrame(
    np.random.randn(30,3),
    columns=["AI SIGNAL","NETWORK","SECURITY"]
)

st.line_chart(stream_data)

#


# =========================================================
# PRIVACY-PRESERVING DATA PROCESSING
# =========================================================

st.markdown("## 🔐 PRIVACY-PRESERVING DATA PROCESSING")
st.info(
    "Protect personal information in a separate copy of the current dataset. "
    "The working dataset is not changed by these privacy options."
)

def _matching_columns(frame, keywords):
    return [
        col for col in frame.columns
        if any(keyword in str(col).strip().lower() for keyword in keywords)
    ]

privacy_email_cols = _matching_columns(df, ["email", "e-mail"])
privacy_phone_cols = _matching_columns(df, ["phone", "mobile", "contact", "telephone"])
privacy_name_cols = [
    col for col in _matching_columns(df, ["name", "full_name", "fullname"])
    if not any(word in str(col).strip().lower() for word in ["department", "filename", "username"])
]
privacy_id_cols = [
    col for col in _matching_columns(df, ["id", "identifier", "roll_no", "roll no", "student_no"])
    if not any(word in str(col).strip().lower() for word in ["valid", "identity_status"])
]

privacy_col1, privacy_col2 = st.columns(2)
with privacy_col1:
    protect_emails = st.checkbox("Mask email addresses", value=True, disabled=not bool(privacy_email_cols))
    protect_names = st.checkbox("Anonymize names", value=True, disabled=not bool(privacy_name_cols))
with privacy_col2:
    protect_phones = st.checkbox("Mask phone numbers", value=True, disabled=not bool(privacy_phone_cols))
    protect_ids = st.checkbox("Replace IDs with anonymous IDs", value=True, disabled=not bool(privacy_id_cols))

if not any([privacy_email_cols, privacy_phone_cols, privacy_name_cols, privacy_id_cols]):
    st.warning(
        "No likely email, phone, name, or ID columns were detected. "
        "Rename the relevant columns or add column detection for your dataset."
    )
else:
    # Prepare a separate copy using the same cleaning logic as CurateX AI.
    # This does not change the main working dataset shown elsewhere in the app.
    privacy_base_df = df.copy(deep=True)

    # Convert common text placeholders into real missing values before filling.
    missing_markers = ["", " ", "none", "null", "nan", "n/a", "na", "<na>"]
    for col in privacy_base_df.select_dtypes(include=["object", "string"]).columns:
        normalized = privacy_base_df[col].astype("string").str.strip()
        privacy_base_df[col] = normalized.mask(
            normalized.str.lower().isin(missing_markers), np.nan
        )

    # Ensure common numeric columns are numeric so they get median-based filling.
    for col in privacy_base_df.columns:
        if col.strip().lower() in {"age", "experience", "salary"}:
            privacy_base_df[col] = pd.to_numeric(privacy_base_df[col], errors="coerce")

    missing_before_privacy_clean = int(privacy_base_df.isna().sum().sum())
    privacy_base_df = remove_duplicates(privacy_base_df)
    privacy_base_df = fill_missing(privacy_base_df)
    privacy_base_df = clean_age(privacy_base_df)
    privacy_base_df = clean_experience(privacy_base_df)
    privacy_base_df = fix_salary_by_experience(privacy_base_df)
    privacy_base_df = smart_fill_department(privacy_base_df)
    # Run the general fill once more after specialized cleaning.
    privacy_base_df = fill_missing(privacy_base_df)
    missing_after_privacy_clean = int(privacy_base_df.isna().sum().sum())

    # Detect privacy columns against the cleaned copy too, in case the columns
    # are present but the input used inconsistent column-name spacing.
    protected_df = apply_privacy_protection(
        privacy_base_df,
        email_cols=privacy_email_cols,
        phone_cols=privacy_phone_cols,
        name_cols=privacy_name_cols,
        id_cols=privacy_id_cols,
        mask_emails=protect_emails,
        mask_phones=protect_phones,
        anonymize_names=protect_names,
        anonymize_ids=protect_ids,
    )

    filled_count = max(0, missing_before_privacy_clean - missing_after_privacy_clean)
    st.info(
        f"Privacy copy cleaned first: {filled_count} missing value(s) filled where possible. "
        f"Remaining missing values: {missing_after_privacy_clean}. "
        "Columns that are entirely empty cannot be filled reliably."
    )

    protected_count = sum([
        len(privacy_email_cols) if protect_emails else 0,
        len(privacy_phone_cols) if protect_phones else 0,
        len(privacy_name_cols) if protect_names else 0,
        len(privacy_id_cols) if protect_ids else 0,
    ])
    st.success(f"Privacy protection preview ready. {protected_count} column(s) selected for protection.")
    with st.expander("🔎 Preview protected dataset", expanded=False):
        st.dataframe(protected_df, use_container_width=True)

    protected_csv = protected_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "🔒 DOWNLOAD PRIVACY-PROTECTED CSV",
        data=protected_csv,
        file_name="privacy_protected_dataset.csv",
        mime="text/csv",
        key="download_privacy_protected_csv",
    )
    st.caption(
        "Note: masking and replacing direct identifiers reduce exposure but do not guarantee "
        "complete anonymization. Other columns may still identify someone when combined."
    )


# =========================================================
# DOWNLOAD
# =========================================================

st.markdown("## 🧹 DOWNLOAD CURATED DATASET")

csv = df.to_csv(index=False).encode("utf-8")

if st.download_button(
    "⬇ DOWNLOAD CSV",
    csv,
    "curated_dataset.csv",
    "text/csv"
):
    announce("CSV download started")

excel_buffer = BytesIO()

with pd.ExcelWriter(
    excel_buffer,
    engine="openpyxl"
) as writer:

    df.to_excel(
        writer,
        index=False,
        sheet_name="CuratedData"
    )

excel_data = excel_buffer.getvalue()

if st.download_button(
    "📥 DOWNLOAD EXCEL",
    excel_data,
    "curated_dataset.xlsx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
):
    announce("Excel download started")

# =========================================================
# FLOATING ORB
# =========================================================

components.html("""

<div id="orb"></div>

<style>

#orb{

position:fixed;

bottom:30px;
right:30px;

width:90px;
height:90px;

border-radius:50%;

background:radial-gradient(
circle,
#00FFA3,
#00c3ff
);

box-shadow:
0 0 30px #00FFA3,
0 0 60px #00c3ff;

animation:floatOrb 4s ease-in-out infinite;

z-index:999;
}

@keyframes floatOrb{

0%{
transform:translateY(0px);
}

50%{
transform:translateY(-20px);
}

100%{
transform:translateY(0px);
}
}

</style>

""", height=0)

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
---
<center>

⚡ KYANG MCS  
One of the best Data Curation Platform

</center>
""", unsafe_allow_html=True)