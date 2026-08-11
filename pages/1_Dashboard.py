import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

st.set_page_config(page_title="Titanic Dashboard", page_icon="📊", layout="wide")

engine = create_engine(st.secrets["postgresql://neondb_owner:npg_AlaixrM8Gw3m@ep-winter-smoke-ayurdpve-pooler.c-5.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"])

def load_data():
    df = pd.read_sql("SELECT * FROM titanic;", engine)
    df["age"] = df["age"].fillna(df["age"].median())
    df["embarked"] = df["embarked"].fillna(df["embarked"].mode()[0])
    df = df.drop(columns=["cabin"], errors="ignore").drop_duplicates()
    df["embarked"] = df["embarked"].replace({
        "S":"Southampton","C":"Cherbourg","Q":"Queenstown"
    })
    return df

@st.fragment(run_every="2s")
def live_dashboard():

    df = load_data()
    df["survival_status"] = df["survived"].map({0:"Did Not Survive", 1:"Survived"})

    st.title("📊 Titanic Dashboard")
    st.markdown("🔴 **LIVE DATA** — updates automatically from PostgreSQL.")

    st.subheader("📊 Key Performance Indicators")
    c1,c2,c3,c4 = st.columns(4)

    total = len(df)
    survivors = int(df["survived"].sum())
    rate = survivors / total * 100 if total else 0

    c1.metric("🚢 Total Passengers", total)
    c2.metric("🛟 Survivors", survivors)
    c3.metric("❤️ Survival Rate", f"{rate:.1f}%")
    c4.metric("💰 Average Fare", f"{df['fare'].mean():.2f}")

    st.divider()
    
    
    st.subheader("🛟 Survival Analysis")
    c1,c2 = st.columns(2)

    with c1:
        temp = df.groupby(["pclass","sex"])["survived"].mean().reset_index()
        fig = px.bar(
            temp,x="pclass",y="survived",color="sex",barmode="group",
            text_auto=".1%",title="Survival Rate by Class & Gender",
            color_discrete_sequence=["royalblue","mediumturquoise"]
        )
        fig.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig,use_container_width=True)

    with c2:
        fig = px.histogram(
            df,x="age",color="survival_status",nbins=30,
            barmode="stack",title="Age Distribution by Survival",
            color_discrete_sequence=["coral","deepskyblue"]
        )
        st.plotly_chart(fig,use_container_width=True)

    st.divider()
    
    
    st.subheader("⚓ Passenger Insights")
    c1,c2 = st.columns(2)

    with c1:
        fig = px.histogram(
            df,x="pclass",color="survival_status",barmode="group",
            title="Passenger Count by Class",
            color_discrete_sequence=["slateblue","mediumaquamarine"]
        )
        st.plotly_chart(fig,use_container_width=True)

    with c2:
        fig = px.box(
            df,x="survival_status",y="fare",color="survival_status",
            title="Fare Distribution by Survival",
            color_discrete_sequence=["mediumpurple","mediumturquoise"]
        )
        st.plotly_chart(fig,use_container_width=True)

    st.caption(f"🕒 Live refresh • Rows: {len(df)}")

live_dashboard()
