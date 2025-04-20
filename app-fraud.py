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
    -3.519029545, 4.140867176, -3.628202369, 5.505672037, -4.057462506,
    -0.905945283, -6.652031121, 2.634524165, -4.67940204, -6.546241815,
    3.53820204, -8.042285142, 1.697509384, -8.051048902, 1.070457396,
    -7.395956925, -14.32962616, -4.868010236, 2.463843039, 0.898723234,
    1.582555933, 0.778710245, -0.135707278, -0.0042778, 0.032706159,
    0.362014053, 0.900925138, 0.554897499, 9.13
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
