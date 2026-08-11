import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(page_title="Titanic Data Description", page_icon="📋", layout="wide")

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
def live_description():

    df = load_data()

    st.title("📋 Titanic Dataset Description")
    st.markdown("🔴 **LIVE DATA** — information is read continuously from PostgreSQL.")

    st.markdown("""
    ### 🚢 Project Overview

    This project analyzes the Titanic passenger dataset to understand
    which passenger characteristics were associated with survival.

    The analysis focuses on passenger class, gender, age, fare and
    embarkation location.
    """)

    st.divider()
    st.subheader("📊 Dataset Overview")

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("👥 Passengers",len(df))
    c2.metric("📊 Columns",len(df.columns))
    c3.metric("🎂 Average Age",f"{df['age'].mean():.1f}")
    c4.metric("💰 Average Fare",f"{df['fare'].mean():.2f}")

    st.divider()
    st.subheader("🧩 Important Features")

    st.markdown("""
    | Column | Description |
    |---|---|
    | `survived` | Survival status: 0 = No, 1 = Yes |
    | `pclass` | Passenger class |
    | `sex` | Passenger gender |
    | `age` | Passenger age |
    | `fare` | Ticket price |
    | `embarked` | Port where the passenger boarded |
    """)

    st.divider()
    st.subheader("🧹 Data Cleaning")

    st.markdown("""
    - Missing `age` values → median.
    - Missing `embarked` values → mode.
    - `cabin` removed because of many missing values.
    - Duplicate rows removed.
    - `S`, `C`, `Q` converted to city names.
    """)

    st.divider()
    st.subheader("🔎 Main Analytical Questions")

    st.markdown("""
    - Does passenger class affect survival?
    - Was survival different between males and females?
    - How did age relate to survival?
    - Was fare associated with survival?
    - Did survival rates differ by embarkation location?
    """)

    st.divider()
    st.subheader("👀 Current Dataset")
    st.dataframe(df,use_container_width=True)

    st.caption(f"🕒 Live refresh • Rows: {len(df)}")

live_description()
