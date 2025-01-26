import streamlit as st
import pandas as pd
from predict_page import show_predict_page
from explore_page import show_explore_page

def load_data():
    # Load dataset
    url = "https://drive.google.com/uc?id=1ebNIs3jPNJpz1jOF2VBusHU2BsUneVU6&export=download"
    df = pd.read_csv(url)

    # Check for 'ConvertedCompYearly' and rename it to 'Salary'
    if 'ConvertedCompYearly' in df.columns:
        df = df.rename({'ConvertedCompYearly': 'Salary'}, axis=1)
    else:
        print("ConvertedCompYearly column not found!")

    # Confirm that 'Salary' is now a column
    if 'Salary' in df.columns:
        # Filter rows where 'Salary' is not null
        df = df[df['Salary'].notnull()]
    else:
        print("Salary column not found!")
        return pd.DataFrame()  # Return an empty DataFrame if Salary column doesn't exist

    # Group smaller countries into 'Others'
    country_counts = df['Country'].value_counts()
    cutoff = 400
    countries_to_keep = country_counts[country_counts > cutoff].index
    df['Country'] = df['Country'].apply(lambda x: x if x in countries_to_keep else 'Others')

    # Select relevant columns
    df = df[['Country', 'EdLevel', 'YearsCodePro', 'Employment', 'Salary']]

    # Drop rows with missing values
    df.dropna(inplace=True)

    # Correct experience and education fields
    df['YearsCodePro'] = df['YearsCodePro'].apply(correct_exp)
    df['EdLevel'] = df['EdLevel'].apply(correct_Education)

    # Drop unnecessary columns
    df.drop(['Employment'], axis=1, inplace=True)
    st.write(df.columns.tolist())
    return df

page = st.sidebar.selectbox("Explore or Predict", ("Explore", "Predict"))
df = load_data()
st.write(df.columns.tolist())
if page == 'Predict':
    show_predict_page()
else:
    show_explore_page(df)

#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

