import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt 

def divide_types(types, cutoff):
    categories = {}
    categories["Others"] = 0
    for index, val in types.items():
        if(val>=cutoff):
            categories[index] = val
        else:
            categories["Others"]+=val
    return categories

def correct_exp(x):
    if x == 'Less than 1 year':
        return 0.5
    if x == 'More than 50 years':
        return 50
    else:
        return float(x)

def correct_Education(x):
    if 'Master’s degree' in x:
        return 'Master degree'
    if 'Bachelor’s degree' in x:
        return 'Bachelor degree'
    if 'Professional degree' in x:
        return 'Professional degree'
    else:
        return 'Less than a Bachelor'

@st.cache_data
def load_data():
    # Load the dataset from Google Drive
    df = pd.read_csv('https://drive.google.com/uc?id=1ebNIs3jPNJpz1jOF2VBusHU2BsUneVU6&export=download')
    
    # Rename the 'ConvertedCompYearly' column to 'Salary'
    if 'ConvertedCompYearly' in df.columns:
        df = df.rename({'ConvertedCompYearly': 'Salary'}, axis=1)
    else:
        raise KeyError("The column 'ConvertedCompYearly' is missing in the dataset.")

    # Filter rows where 'Salary' is not null
    df = df[df['Salary'].notnull()]

    # Categorize 'Country' based on a cutoff for value counts
    types = df['Country'].value_counts()
    cutoff = 400
    categories = divide_types(types, cutoff)  # Ensure divide_types is defined correctly
    df['Country'] = df['Country'].apply(lambda x: x if x in categories else 'Others')

    # Select relevant columns
    df = df[['Country', 'EdLevel', 'YearsCodePro', 'Employment', 'Salary']]

    # Drop rows with any missing values
    df.dropna(inplace=True)

    # Apply transformations to 'YearsCodePro' and 'EdLevel'
    df['YearsCodePro'] = df['YearsCodePro'].apply(correct_exp)  # Ensure correct_exp is defined
    df['EdLevel'] = df['EdLevel'].apply(correct_Education)  # Ensure correct_Education is defined

    # Drop the 'Employment' column (correct method to drop in-place)
    df = df.drop(['Employment'], axis=1)

    return df

# Load data to use
try:
    df = load_data()
    print("Data loaded successfully!")
except Exception as e:
    print(f"Error loading data: {e}")

def show_explore_page(df):
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

    return df
    df = load_data()
    st.title("Explore Software Engineer Salaries")
    
    st.write("### Stack Overflow Developer Survey 2024")
    st.write(df.columns.tolist())
    # Check if required columns are present
    required_columns = {'Country', 'Salary', 'YearsCodePro'}
    if not required_columns.issubset(df.columns):
       st.error(f"The dataset must contain the following columns: {', '.join(required_columns)}")
       return
    
    # Country-wise data visualization
    st.write("#### Number of Responses by Country")
    country_data = df['Country'].value_counts()
    
    fig1, ax1 = plt.subplots()
    ax1.pie(country_data, labels=country_data.index, autopct="%1.2f%%", shadow=True, startangle=200)
    ax1.axis("equal")  # Equal aspect ratio ensures the pie is drawn as a circle.
    st.pyplot(fig1)

    # Mean salary by country
    st.write("#### Mean Salary by Country")
    salary_by_country = df.groupby('Country')['Salary'].mean().sort_values()
    st.bar_chart(salary_by_country, use_container_width=True)

    # Mean salary by experience
    st.write("#### Mean Salary by Years of Professional Coding Experience")
    salary_by_experience = df.groupby('YearsCodePro')['Salary'].mean().sort_values()
    st.line_chart(salary_by_experience, use_container_width=True)

    st.success("Analysis complete!")
