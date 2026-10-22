import pandas as pd

df = pd.read_csv("customer_journey.csv")

X = df[[
    "acquisition_channel",
    "device_type",
    "region",
    "customer_type",
    "viewed_product",
    "started_checkout"
]]

y = df["completed_purchase"]

print(X.head())
print(y.head())

X_encoded = pd.get_dummies(X, dtype=int)

print(X_encoded.head())
print(X_encoded.shape)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training:", X_train.shape)
print("Testing:", X_test.shape)

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.linear_model import LogisticRegression

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer

preprocessor = make_column_transformer(
    (
        OneHotEncoder(handle_unknown="ignore"),
        [
            "acquisition_channel",
            "device_type",
            "region",
            "customer_type"
        ]
    ),
    remainder="passthrough"
)
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression

model = make_pipeline(
    preprocessor,
    LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    )
)

model.fit(X_train, y_train)

print("Model trained successfully!")

y_pred = model.predict(X_test)

print("First 10 predictions:", y_pred[:10])

print("Predicted purchases:", sum(y_pred))
print("Actual purchases:", sum(y_test))

from sklearn.metrics import classification_report

print(classification_report(y_test, y_pred, zero_division=0))

from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_test, y_pred)

print("Confusion Matrix:")
print(cm)

from sklearn.ensemble import RandomForestClassifier

rf_model = make_pipeline(
    preprocessor,
    RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    )
)

rf_model.fit(X_train, y_train)

rf_pred = rf_model.predict(X_test)

print("\nRandom Forest Results:")
print(classification_report(y_test, rf_pred, zero_division=0))

from sklearn.metrics import roc_auc_score

lr_prob = model.predict_proba(X_test)[:, 1]
rf_prob = rf_model.predict_proba(X_test)[:, 1]

print("Logistic Regression ROC-AUC:", round(roc_auc_score(y_test, lr_prob), 3))
print("Random Forest ROC-AUC:", round(roc_auc_score(y_test, rf_prob), 3))

df = pd.read_csv("customer_journey.csv")
# Add existing customer journey signals
df["viewed_product"] = df["viewed_product"].astype(int)
df["started_checkout"] = df["started_checkout"].astype(int)

import joblib

joblib.dump(rf_model, "purchase_prediction_model.pkl")

print("Model saved successfully!")

import joblib
import streamlit as st
@st.cache_resource
def load_prediction_model():
    return joblib.load("purchase_prediction_model.pkl")

prediction_model = load_prediction_model()