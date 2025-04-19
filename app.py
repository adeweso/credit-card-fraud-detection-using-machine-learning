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
online_transactions = get_data("creditcard_head.csv")  # Ensure this file is in your working directory

# Header
st.title("Credit Card Fraud Detection System")
st.text("In my project, I explored the patterns of \nfraudulent credit card transactions using machine learning.")

# Dataset Preview
st.header("The Online Credit Card Transactions Dataset")
st.text("I got this dataset from Kaggle.\nIt contains over 280,000 samples and 31 features of online transactions.")

st.subheader("The Dataset's First Five Rows (Head)")
st.dataframe(online_transactions.head())


# Model Prediction
st.subheader("**User's Input**")
st.write("Please input the transaction feature values below (V1 to V29).")

col1, col2, col3 = st.columns(3)
input_values = []

for i in range(29):
    col = [col1, col2, col3][i % 3]
    val = col.text_input(f"Enter value of V{i+1}", value="0.0", key=f"V{i+1}")
    input_values.append(val)

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
