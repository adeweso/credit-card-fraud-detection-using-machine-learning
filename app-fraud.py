import streamlit as st
import pandas as pd
import joblib

# Set page configuration
st.set_page_config(page_title="Credit Card Fraud Detection", layout="wide")

# Load model
@st.cache_data
def load_model():
    model = joblib.load("credit card model")  # Replace with your actual model path
    return model

# Load dataset
@st.cache_data
def get_data(filename):
    return pd.read_csv(filename)

# Load model and dataset
model = load_model()
online_transactions = get_data("creditcard.csv")  # Ensure this file is in your working directory

# Header
st.title("Credit Card Fraud Detection System")
st.text("In my project, I explored the patterns of \nfraudulent credit card transactions using machine learning.")

# Dataset Preview
st.header("The Online Credit Card Transactions Dataset")
st.text("I got this dataset from Kaggle.\nIt contains over 280,000 samples and 31 features of online transactions.")

st.subheader("The Dataset's First Five Rows (Head)")
st.write(online_transactions.head())

st.subheader("The Dataset's Last Five Rows (Tail)")
st.write(online_transactions.tail())

# Model Prediction
st.subheader("**User's Input**")
st.write("Please input the transaction feature values below (V1 to V29).")

# Predefined input values
predefined_values = [
    1.91958693, 0.474645763, -1.141566599, 3.405169984, 0.902664731,
    0.555090593, 0.107763016, 0.112205843, -1.235450444, 1.725155959, 0.062081874,
    -0.351102121, -0.870433912, 0.762318957, -0.790227277, 1.249135467, -1.252419172,
    0.483073221, -1.337571289, -0.27925373, 0.245742963, 0.58484475, 0.037563601, 0.183617039,
    0.125501175, 0.11406844, -0.060357445, -0.060477844, 15
]

col1, col2, col3 = st.columns(3)
input_values = []

for i in range(29):
    col = [col1, col2, col3][i % 3]
    input_value = col.text_input(f"Enter value of V{i+1}", key=f"V{i+1}", value=str(predefined_values[i]))
    input_values.append(input_value)

if st.button("Predict"):
    try:
        input_values = [float(v) for v in input_values]
        prediction = model.predict([input_values])
        result = "✅ Normal Transaction" if prediction[0] == 0 else "⚠️ Fraudulent Transaction"
        st.subheader("Prediction:")
        st.success(result) if prediction[0] == 0 else st.error(result)
    except ValueError:
        st.error("Please enter valid numeric values.")
    except Exception as e:
        st.error(f"Error occurred: {e}")