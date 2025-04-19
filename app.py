import streamlit as st
import joblib

# Set page configuration as the first command
st.set_page_config(page_title="Credit Card Fraud Detection", layout="wide")

# Load your model
@st.cache_data
def load_model():
    model_path = 'credit card model'  # Replace with your actual model path
    model = joblib.load(model_path)
    return model

model = load_model()

# Streamlit app structure
st.title("Credit Card Fraud Detection System")
st.write("Please input the transaction feature values below (V1 to V29).")

# Create 3 columns for better layout
col1, col2, col3 = st.columns(3)
input_values = []

# Create 29 text inputs for full precision numbers
for i in range(29):
    col = [col1, col2, col3][i % 3]
    input_value = col.text_input(f"Enter value of V{i+1}", key=f"V{i+1}", value="0.0")
    input_values.append(input_value)

# Predict button
if st.button("Predict"):
    try:
        # Convert inputs to floats (with full precision) after validating
        input_values = [float(val) for val in input_values]
        
        # Make prediction
        prediction = model.predict([input_values])
        result = "✅ Normal Transaction" if prediction[0] == 0 else "⚠️ Fraudulent Transaction"
        
        st.subheader("Prediction:")
        st.success(result) if prediction[0] == 0 else st.error(result)
    
    except ValueError:
        st.error("Error: Please make sure all inputs are valid numbers with the correct format.")
    except Exception as e:
        st.error(f"Error occurred during prediction: {e}")