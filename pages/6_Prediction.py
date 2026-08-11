import streamlit as st
import pandas as pd
import plotly.express as px

from sqlalchemy import create_engine

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

from catboost import CatBoostClassifier


# ==========================
# Page Settings
# ==========================

st.set_page_config(
    page_title="Titanic Survival Prediction",
    page_icon="🔮",
    layout="wide"
)

st.title("🔮 Titanic Survival Prediction")
st.markdown(
    "Enter passenger information and predict the survival outcome."
)

st.divider()


# ==========================
# Load Data
# ==========================

engine = create_engine(st.secrets["DATABASE_URL"])

@st.cache_data
def load_data():

    df = pd.read_sql("SELECT * FROM titanic;",engine)

    df.columns = df.columns.str.lower()

    # Cleaning

    df["age"] = df["age"].fillna(df["age"].median())

    df["embarked"] = df["embarked"].fillna(df["embarked"].mode()[0])

    df.drop(columns=["cabin"],inplace=True,errors="ignore")

    df.drop_duplicates(inplace=True)

    df["embarked"] = df["embarked"].replace({
        "S": "Southampton",
        "C": "Cherbourg",
        "Q": "Queenstown"
    })

    return df



# ==========================
# Drop Coulmns
# ==========================
df = load_data()

ml_df = df.copy()

ml_df.drop(["passengerid", "name", "ticket"],axis=1,inplace=True,errors="ignore")

# ==========================
# Encoding
# ==========================
le_sex = LabelEncoder()
le_embarked = LabelEncoder()

ml_df["sex"] = le_sex.fit_transform(ml_df["sex"])

ml_df["embarked"] = le_embarked.fit_transform(ml_df["embarked"])

# ==========================
# Scaling
# ==========================

scaler = StandardScaler()

ml_df[["age", "fare"]] = scaler.fit_transform(ml_df[["age", "fare"]])


# ==========================
# Train Model
# ==========================

X = ml_df.drop("survived",axis=1)

y = ml_df["survived"]

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)

catboost_model = CatBoostClassifier(verbose=0)

catboost_model.fit(X_train,y_train)


# ==========================
# Passenger Information
# ==========================

st.subheader("👤 Passenger Information")

col1, col2 = st.columns(2)

with col1:

    pclass = st.selectbox(
        "🎫 Passenger Class",
        [1, 2, 3]
    )

    sex = st.selectbox(
        "👤 Sex",
        ["male", "female"]
    )

    age = st.number_input(
        "🎂 Age",
        min_value=0.0,
        max_value=100.0,
        value=25.0,
        step=1.0
    )

    sibsp = st.number_input(
        "👨‍👩‍👧 Siblings / Spouse",
        min_value=0,
        max_value=10,
        value=0,
        step=1
    )


with col2:

    parch = st.number_input(
        "👨‍👩‍👧 Parents / Children",
        min_value=0,
        max_value=10,
        value=0,
        step=1
    )

    fare = st.number_input(
        "💰 Fare",
        min_value=0.0,
        value=30.0,
        step=1.0
    )

    embarked = st.selectbox(
        "⚓ Embarked",
        ["Southampton", "Cherbourg", "Queenstown"]
    )


st.divider()


# ==========================
# Prediction
# ==========================

if st.button("🔮 Predict Survival",use_container_width=True):

    # Convert user input to DataFrame

    passenger = pd.DataFrame({
        "pclass": [pclass],
        "sex": [sex],
        "age": [age],
        "sibsp": [sibsp],
        "parch": [parch],
        "fare": [fare],
        "embarked": [embarked]
    })


    # ==========================
    # Encoding User Input
    # ==========================

    passenger["sex"] = le_sex.transform(passenger["sex"])

    passenger["embarked"] = le_embarked.transform(passenger["embarked"])


    # ==========================
    # Scaling User Input
    # ==========================

    passenger[["age", "fare"]] = scaler.transform(passenger[["age", "fare"]])


    # ==========================
    # Prediction
    # ==========================

    prediction = catboost_model.predict(passenger)

    probability = catboost_model.predict_proba(passenger)[0]


    survived_probability = probability[1] * 100
    not_survived_probability = probability[0] * 100


    st.divider()

    st.subheader("🎯 Prediction Result")


    # ==========================
    # Result
    # ==========================

    if prediction[0] == 1:

        st.success(
            f"🟢 SURVIVED\n\n"
            f"Survival Probability: "
            f"{survived_probability:.2f}%"
        )

    else:

        st.error(
            f"🔴 DID NOT SURVIVE\n\n"
            f"Survival Probability: "
            f"{survived_probability:.2f}%"
        )


    # ==========================
    # KPI Cards
    # ==========================

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🟢 Survived",
        f"{survived_probability:.2f}%"
    )

    col2.metric(
        "🔴 Not Survived",
        f"{not_survived_probability:.2f}%"
    )

    col3.metric(
        "🤖 Model",
        "CatBoost"
    )


    # ==========================
    # Probability Graph
    # ==========================

    st.subheader("📊 Survival Probability")

    graph = pd.DataFrame({
        "Outcome": [
            "Survived",
            "Did Not Survive"
        ],
        "Probability": [
            survived_probability,
            not_survived_probability
        ]
    })


    fig = px.pie(
        graph,
        names="Outcome",
        values="Probability",
        hole=0.55,
        title="Passenger Survival Probability",
        color_discrete_sequence=[
            "mediumseagreen",
            "lightcoral"
        ]
    )

    fig.update_traces(
        textinfo="percent+label"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    st.caption(
        "Prediction generated using the CatBoost model trained on the Titanic dataset."
    )
