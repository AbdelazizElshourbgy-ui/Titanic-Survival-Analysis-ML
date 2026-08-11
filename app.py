import streamlit as st
import base64
from pathlib import Path

st.set_page_config(page_title="Titanic Project", page_icon="🚢", layout="wide")

image_path = Path(__file__).parent / "titanic.jpg"

if image_path.exists() and image_path.stat().st_size > 0:
    image = base64.b64encode(image_path.read_bytes()).decode()
    st.markdown(f"""
    <style>
    .stApp {{
        background-image:
        linear-gradient(rgba(5,15,30,.48), rgba(5,15,30,.58)),
        url("data:image/jpeg;base64,{image}");
        background-size:cover;
        background-position:center;
        background-attachment:fixed;
    }}
    .hero {{text-align:center;padding:100px 20px 45px;color:white;}}
    .hero h1 {{font-size:55px;}}
    .hero p {{font-size:21px;}}
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>🚢 Titanic Passenger Survival Analysis</h1>
<p>Data Cleaning • Exploratory Data Analysis • Visualization</p>
</div>
""", unsafe_allow_html=True)

st.divider()
st.subheader("📂 Explore Project")

c1,c2,c3,c4,c5,c6 = st.columns(6)

with c1:
    st.markdown("### 📊 Dashboard")
    st.caption("Live KPIs & survival insights")
    if st.button("Open Dashboard", use_container_width=True):
        st.switch_page("pages/1_Dashboard.py")

with c2:
    st.markdown("### 📈 Analysis")
    st.caption("Live charts & relationships")
    if st.button("Open Analysis", use_container_width=True):
        st.switch_page("pages/2_Analysis.py")

with c3:
    st.markdown("### 📋 Data Description")
    st.caption("Live dataset information")
    if st.button("Open Data Description", use_container_width=True):
        st.switch_page("pages/3_Data_Description.py")

with c4:
    st.markdown("### 📝 Report")
    st.caption("Findings & recommendations")
    if st.button("Open Report", use_container_width=True):
        st.switch_page("pages/4_Report.py")
        
with c5:
    st.markdown("### 🤖 Machine Learning")
    st.caption("Models & Performance")

    if st.button("Open ML", use_container_width=True):
        st.switch_page("pages/5_Machine_Learning.py")   
        
with c6:
    st.markdown("### 🔮 Prediction")
    st.caption("Survival Prediction")

    if st.button("Open Prediction", use_container_width=True):
        st.switch_page("pages/6_Prediction.py")             

st.divider()
st.info("🔴 Live Mode: dashboard pages refresh automatically from PostgreSQL.")
