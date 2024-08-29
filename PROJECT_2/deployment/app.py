import streamlit as st
import pandas as pd
import joblib


st.header('FTDS Model Deployment')
st.write("""
Created by ojan

""")

@st.cache # mencegah penghambatan running saat rerun
def fetch_data():
    df = pd.read_csv("D:\HACKTIV8\HACKTIV 2\PHASE 1\GITHUB\p1-ftds033-rmt-m2-MuhammadRozzaaq\diabetes_prediction_dataset.csv")
    return df

df = fetch_data()
st.write(df)

st.sidebar.header('User Input Features') # menempatkan di head

def user_input():
    age = st.sidebar.number_input('age', value=100)
    hypertension = st.sidebar.selectbox('hypertension', df['hypertension'].unique())
    heart_disease = st.sidebar.selectbox('heart_disease', df['heart_disease'].unique())
    smoking_history = st.sidebar.selectbox('smoking_history', df['smoking_history'].unique())
    bmi = st.sidebar.number_input('bmi', value= 96.01)
    HbA1c_level = st.sidebar.number_input('HbA1c_level', value=10.0)
    blood_glucose_level = st.sidebar.number_input('blood_glucose_level', value=310)
    
    data = {
        'age': age,
        'hypertension': hypertension,
        'heart_disease':heart_disease,
        'smoking_history': smoking_history,
        'bmi': bmi,
        'HbA1c_level': HbA1c_level,
        'blood_glucose_level': blood_glucose_level}

   
    features = pd.DataFrame(data, index=[0]) # dikompile menjadi dataframe dalam 1 baris
    return features


input = user_input()

st.subheader('User Input')
st.write(input)

load_model = joblib.load("model_dt.pkl")

if st.button('predict'):
    prediction = load_model.predict(input)
    if prediction == 1:
        prediction = 'diabetes'
    else:
        prediction = 'no diabetes'

    st.write('Based on user input, the placement model predicted: ')
    st.write(prediction) 