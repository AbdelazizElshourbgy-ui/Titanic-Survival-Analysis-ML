import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

st.set_page_config(page_title="Titanic Analysis", page_icon="📈", layout="wide")

engine = create_engine("postgresql://postgres:postgres@localhost:5432/Titanic")

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
def live_analysis():

    df = load_data()
    df["survival_status"] = df["survived"].map({
        0:"Did Not Survive",1:"Survived"
    })

    st.title("📈 Titanic Analysis")
    st.markdown("🔴 **LIVE DATA** — charts update automatically from PostgreSQL.")

    st.subheader("⚓ Passenger & Fare Analysis")
    c1,c2 = st.columns(2)

    with c1:
        temp = df.groupby(
            ["embarked","survival_status"]
        ).size().reset_index(name="count")

        fig = px.bar(
            temp,x="embarked",y="count",color="survival_status",
            barmode="group",title="Passengers by Embarkation",
            color_discrete_sequence=["steelblue","mediumseagreen"]
        )
        st.plotly_chart(fig,use_container_width=True)

    with c2:
        fig = px.scatter(
            df,x="age",y="fare",color="survival_status",
            title="Age vs Fare",opacity=.7,
            color_discrete_sequence=["mediumvioletred","deepskyblue"]
        )
        fig.update_traces(marker_size=9)
        st.plotly_chart(fig,use_container_width=True)

    st.divider()
    st.subheader("👥 Survival Patterns")
    c1,c2 = st.columns(2)

    with c1:
        temp = df.groupby("sex")["survived"].mean().reset_index()

        fig = px.bar(
            temp,x="sex",y="survived",color="sex",text_auto=".1%",
            title="Survival Rate by Gender",
            color_discrete_sequence=["royalblue","mediumvioletred"]
        )
        fig.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig,use_container_width=True)

    with c2:
        temp = df.groupby("embarked")["survived"].mean().reset_index()

        fig = px.bar(
            temp,x="embarked",y="survived",color="embarked",
            text_auto=".1%",title="Survival Rate by Embarkation",
            color_discrete_sequence=[
                "deepskyblue","mediumpurple","mediumturquoise"
            ]
        )
        fig.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig,use_container_width=True)

    st.caption(f"🕒 Live refresh • Rows: {len(df)}")

live_analysis()
