import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sqlalchemy import create_engine
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report
)
from xgboost import XGBClassifier
from catboost import CatBoostClassifier

st.set_page_config(
    page_title="Titanic Machine Learning",
    page_icon="🤖",
    layout="wide"
)

# ==========================
# Database
# ==========================

engine = create_engine(
    "postgresql://postgres:postgres@localhost:5432/Titanic"
)


# ==========================
# Load Data
# ==========================

@st.cache_data
def load_data():

    df = pd.read_sql("SELECT * FROM titanic;",engine)

    df["age"] = df["age"].fillna(df["age"].median())

    df["embarked"] = df["embarked"].fillna(df["embarked"].mode()[0])

    df = df.drop(columns=["cabin"],errors="ignore").drop_duplicates()

    df["embarked"] = df["embarked"].replace({
        "S": "Southampton",
        "C": "Cherbourg",
        "Q": "Queenstown"
    })

    return df


# ==========================
# Data Refresh
# ==========================

col1, col2 = st.columns([5, 1])

with col2:

    if st.button(
        "🔄 Refresh Data",
        use_container_width=True
    ):
        st.cache_data.clear()
        st.rerun()


# ==========================
# Load Current Data
# ==========================

df = load_data()

st.caption(
    f"🟢 Live Data • Rows: {len(df)}"
)


# ==========================
# Machine Learning
# ==========================

st.title("🤖 Titanic Machine Learning")

st.markdown(
    "🟢 **LIVE DATA** — Click Refresh to load the latest PostgreSQL data."
)

# ==========================
# Your ML preprocessing
# ==========================

df.drop(["passengerid", "name", "ticket"], axis=1, inplace=True)

le = LabelEncoder()

df["sex"] = le.fit_transform(df["sex"])
df["embarked"] = le.fit_transform(df["embarked"])

scaler = StandardScaler()
df[["age", "fare"]] = scaler.fit_transform(df[["age", "fare"]])

X = df.drop("survived", axis=1)
y = df["survived"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ==========================
# Random Forest
# ==========================

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)

rf_accuracy = accuracy_score(y_test, rf_pred)
rf_precision = precision_score(y_test, rf_pred, zero_division=0)
rf_recall = recall_score(y_test, rf_pred, zero_division=0)
rf_f1 = f1_score(y_test, rf_pred, zero_division=0)

# ==========================
# Decision Tree
# ==========================

DT = DecisionTreeClassifier()
DT.fit(X_train, y_train)
dt_pred = DT.predict(X_test)

dt_accuracy = accuracy_score(y_test, dt_pred)
dt_precision = precision_score(y_test, dt_pred, zero_division=0)
dt_recall = recall_score(y_test, dt_pred, zero_division=0)
dt_f1 = f1_score(y_test, dt_pred, zero_division=0)

# ==========================
# Logistic Regression
# ==========================

Lg = LogisticRegression()
Lg.fit(X_train, y_train)
lg_pred = Lg.predict(X_test)

lg_accuracy = accuracy_score(y_test, lg_pred)
lg_precision = precision_score(y_test, lg_pred, zero_division=0)
lg_recall = recall_score(y_test, lg_pred, zero_division=0)
lg_f1 = f1_score(y_test, lg_pred, zero_division=0)

# ==========================
# XGBoost
# ==========================

xgb = XGBClassifier()
xgb.fit(X_train, y_train)
xgb_pred = xgb.predict(X_test)

xgb_accuracy = accuracy_score(y_test, xgb_pred)
xgb_precision = precision_score(y_test, xgb_pred, zero_division=0)
xgb_recall = recall_score(y_test, xgb_pred, zero_division=0)
xgb_f1 = f1_score(y_test, xgb_pred, zero_division=0)

# ==========================
# CatBoost
# ==========================

catboost_model = CatBoostClassifier(verbose=0)
catboost_model.fit(X_train, y_train)
cat_pred = catboost_model.predict(X_test)

cat_accuracy = accuracy_score(y_test, cat_pred)
cat_precision = precision_score(y_test, cat_pred, zero_division=0)
cat_recall = recall_score(y_test, cat_pred, zero_division=0)
cat_f1 = f1_score(y_test, cat_pred, zero_division=0)

# ==========================
# KPI Cards
# ==========================

st.subheader("🏆 Best Model Performance")

best_accuracy = max(
    rf_accuracy, dt_accuracy, lg_accuracy,
    xgb_accuracy, cat_accuracy
)

best_name = [
    "Random Forest", "Decision Tree", "Logistic Regression",
    "XGBoost", "CatBoost"
][[
    rf_accuracy, dt_accuracy, lg_accuracy,
    xgb_accuracy, cat_accuracy
].index(best_accuracy)]

c1, c2, c3, c4 = st.columns(4)
c1.metric("🤖 Best Model", best_name)
c2.metric("🎯 Accuracy", f"{best_accuracy:.2%}")
c3.metric("👥 Test Samples", len(y_test))
c4.metric("📊 Features", X.shape[1])

st.divider()

# ==========================
# Model Comparison
# ==========================

st.subheader("📊 Model Comparison")

results = pd.DataFrame({
    "Model": [
        "Random Forest",
        "Decision Tree",
        "Logistic Regression",
        "XGBoost",
        "CatBoost"
    ],
    "Accuracy": [
        rf_accuracy, dt_accuracy, lg_accuracy,
        xgb_accuracy, cat_accuracy
    ],
    "Precision": [
        rf_precision, dt_precision, lg_precision,
        xgb_precision, cat_precision
    ],
    "Recall": [
        rf_recall, dt_recall, lg_recall,
        xgb_recall, cat_recall
    ],
    "F1 Score": [
        rf_f1, dt_f1, lg_f1,
        xgb_f1, cat_f1
    ]
})

st.dataframe(
    results.style.format({
        "Accuracy": "{:.2%}",
        "Precision": "{:.2%}",
        "Recall": "{:.2%}",
        "F1 Score": "{:.2%}"
    }),
    use_container_width=True
)

st.divider()

# ==========================
# Accuracy Chart
# ==========================

st.subheader("📈 Accuracy Comparison")

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    data=results,
    x="Model",
    y="Accuracy",
    hue="Model",
    palette="deep",
    legend=False,
    ax=ax
)
ax.set_ylabel("Accuracy")
ax.set_xlabel("")
ax.tick_params(axis="x", rotation=15)
st.pyplot(fig)
plt.close(fig)

st.divider()

# ==========================
# Confusion Matrix
# ==========================

st.subheader("🔲 Confusion Matrix")

c1, c2 = st.columns(2)

with c1:
    CM = confusion_matrix(y_test, rf_pred)
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(CM, annot=True, fmt="d", cmap="Blues", ax=ax)
    ax.set_title("Random Forest")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    st.pyplot(fig)
    plt.close(fig)

with c2:
    CM = confusion_matrix(y_test, cat_pred)
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(CM, annot=True, fmt="d", cmap="Blues", ax=ax)
    ax.set_title("CatBoost")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    st.pyplot(fig)
    plt.close(fig)

st.divider()

# ==========================
# Classification Report
# ==========================

st.subheader("📋 CatBoost Classification Report")

report = classification_report(
    y_test,
    cat_pred,
    output_dict=True,
    zero_division=0
)

st.dataframe(
    pd.DataFrame(report).transpose(),
    use_container_width=True
)

st.caption(f"🕒 Live refresh • Rows: {len(df)}")



