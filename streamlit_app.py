import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor 
from sklearn.datasets import fetch_california_housing

st.set_page_config(page_title="OC Housing Predictor", layout="centered")
st.title("🏠 OC Housing Price Predictor")

# Load and Train Model
@st.cache_resource
def get_model():
    housing = fetch_california_housing(as_frame=True)
    X = housing.frame.drop("MedHouseVal", axis=1)
    y = housing.frame["MedHouseVal"]
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X, y)
    return model, X.columns

model, features = get_model()

# User Inputs for Mobile
st.subheader("Property Details")
med_inc = st.number_input("Median Income (in $10k)", value=3.5)
house_age = st.slider("House Age", 1, 52, 25)
rooms = st.slider("Average Rooms", 1, 10, 5)

# Predict Button
if st.button("Predict Value", type="primary"):
    # We use default values for the other technical features for now
    input_data = pd.DataFrame([[med_inc, house_age, rooms, 1, 300, 3, 33.7, -117.8]], columns=features)
    prediction = model.predict(input_data)
    st.success(f"Estimated Market Value: ${prediction[0] * 100000:,.2f}")