# The credit card fraud detection system web-based GUI code
import streamlit as st
import pandas as pd
import joblib

# Set page configuration
st.set_page_config(page_title="Credit Card Fraud Detection", layout="wide")

# Define sections
header = st.container()
dataset = st.container()
model_training = st.container()

# Load model
@st.cache_data
def load_model():
    model = joblib.load("credit card model")  # Ensure this path is correct
    return model

# Load dataset
@st.cache_data
def get_data(filename):
    return pd.read_csv(filename)

# Load the model and dataset
model = load_model()
online_transactions = get_data("creditcard_head.csv")  # Ensure this file exists

# Header section
with header:
    st.title("Credit Card Fraud Detection System")
    st.text("In my project, I explored the patterns of \nfraudulent credit card transactions using machine learning.")

# Dataset section
with dataset:
    st.header("The Credit Card Transactions Dataset")
    st.text("I got this dataset from Kaggle.\nIt contains over 280,000 samples and 31 features of online transactions.")
    st.subheader("The Dataset's First Five Rows (Head)")
    st.dataframe(online_transactions.head())

# Model training (input & prediction) section
with model_training:
    st.subheader("**User's Input**")
    st.text("Provide the transaction feature values below to predict if it's fraudulent.")

    # Predefined input values
    predefined_values = [
    1.179633244, -0.825075328, 0.07056147, -0.546119174, -1.072243861, 
    -1.130536645, -0.210234325, -0.30969987, -0.880267704, 0.603743735, 
    -0.29156231, -0.729390736, -0.022542461, 0.000418675, 0.694645565, 
    1.018129376, 0.305363651, -1.335399765, 0.481580942, 0.315578362, 
    0.286865405, 0.464789858, -0.22431576, 0.428562434, 0.578224494, 
    -0.129546096, -0.031476695, 0.032365628, 139
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

            if prediction[0] == 0:
                st.success("✅ Normal Transaction")
            else:
                st.error("⚠️ Fraudulent Transaction")
        except ValueError:
            st.error("Please enter valid numeric values.")
        except Exception as e:
            st.error(f"An unexpected error occurred:\n{str(e)}")
