import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page

def load_data():
    # Load the dataset from Google Drive
    df = pd.read_csv('https://drive.google.com/uc?id=1ebNIs3jPNJpz1jOF2VBusHU2BsUneVU6&export=download')
    
    
    # Filter rows where 'Salary' is not null
    df = df[df['ConvertedCompYearly'].notnull()]

    # Categorize 'Country' based on a cutoff for value counts
    types = df['Country'].value_counts()
    cutoff = 400
    categories = divide_types(types, cutoff)  # Ensure divide_types is defined correctly
    df['Country'] = df['Country'].apply(lambda x: x if x in categories else 'Others')

    # Select relevant columns
    df = df[['Country', 'EdLevel', 'YearsCodePro', 'Employment', 'ConvertedCompYearly']]

    # Drop rows with any missing values
    df.dropna(inplace=True)

    # Apply transformations to 'YearsCodePro' and 'EdLevel'
    df['YearsCodePro'] = df['YearsCodePro'].apply(correct_exp)  # Ensure correct_exp is defined
    df['EdLevel'] = df['EdLevel'].apply(correct_Education)  # Ensure correct_Education is defined

    # Drop the 'Employment' column (correct method to drop in-place)
    df = df.drop(['Employment'], axis=1)

    return df

page = st.sidebar.selectbox("Explore or Predict", ("Explore", "Predict"))
df = load_data()
if page == 'Predict':
    show_predict_page()
else:
    show_explore_page(df)

#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

