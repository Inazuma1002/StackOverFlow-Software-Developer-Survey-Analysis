import streamlit as st
import pickle
import numpy as np 

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data
data = load_model()

regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

def show_predict_page():
    st.title("Software Developer Salary Prediction")
    st.write("""### We need some information to predict Salary""")

    countries = (
        "United States of America",
        "India",
        "United Kingdom",
        "Germany",
        "Canada",
        "Brazil",
        "France",
        "Spain",
        "Australia",
        "Netherlands",
        "Poland",
        "Italy",
        "Russian Federation",
        "Sweden",
    )

    education = (
        "Less than a Bachelor",
        "Bachelor degree",
        "Master degree",
        "Professional degree",
    )
    country = st.selectbox("Country", countries)
    education = st.selectbox("Education", education)
    experience = st.slider("Years of Experience",0,50,2)

    ok = st.button("Calculated Salary")
    
    if ok:
        X = np.array([[country, education, experience]])
        X[:, 0] = le_country.transform(X[:, 0])  # Encode the Country
        X[:, 1] = le_education.transform(X[:, 1])  # Encode the EdLevel
        X = X.astype(float)

        salary = regressor.predict(X)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")

