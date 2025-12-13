import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Global Health Dashboard",
    layout="wide",
)

# ---------- CUSTOM CSS (VERY IMPORTANT) ----------
st.markdown("""
<style>
/* Remove default padding */
.block-container {
    padding-top: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* Card style */
.card {
    background: #ffffff;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

/* Hover-like effect */
.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 28px rgba(0,0,0,0.12);
}

/* Title text */
.card-title {
    font-size: 18px;
    font-weight: 600;
    color: #111827;
}

/* Value text */
.card-value {
    font-size: 32px;
    font-weight: 700;
    color: #2563EB;
    margin-top: 8px;
}

/* Subtitle */
.card-sub {
    font-size: 14px;
    color: #6B7280;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("## 🌍 Global Health & Demographics Dashboard")
st.markdown("Conceptual UI based on Figma · Functional Implementation in Streamlit")

# ---------- KPI CARDS ----------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-title">Life Expectancy</div>
        <div class="card-value">72.4</div>
        <div class="card-sub">Global Average</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-title">Median Age</div>
        <div class="card-value">30.9</div>
        <div class="card-sub">Years</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <div class="card-title">HDI Index</div>
        <div class="card-value">0.74</div>
        <div class="card-sub">Human Development</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="card">
        <div class="card-title">Gini Index</div>
        <div class="card-value">38.2</div>
        <div class="card-sub">Income Inequality</div>
    </div>
    """, unsafe_allow_html=True)

# ---------- SPACING ----------
st.markdown("<br>", unsafe_allow_html=True)

# ---------- CONTENT ROW ----------
left, right = st.columns([2, 1])

with left:
    st.markdown("""
    <div class="card">
        <div class="card-title">World Overview</div>
        <div class="card-sub">Interactive map will be placed here</div>
        <br>
        <div style="height:240px; background:#F3F4F6; border-radius:10px;
             display:flex; align-items:center; justify-content:center;
             color:#6B7280;">
            MAP PLACEHOLDER
        </div>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="card">
        <div class="card-title">Country Insights</div>
        <div class="card-sub">Select a country to view details</div>
        <br>
        <ul style="color:#374151; font-size:15px;">
            <li>GDP per capita</li>
            <li>Life expectancy</li>
            <li>Health coverage</li>
            <li>COVID impact</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
