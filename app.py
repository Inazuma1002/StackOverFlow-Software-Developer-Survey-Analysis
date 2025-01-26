import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page
from explore_page import load_data
page = st.sidebar.selectbox("Explore or Predict", ("Explore", "Predict"))
df = load_data()
if page == 'Predict':
    show_predict_page()
else:
    show_explore_page(df)

#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

