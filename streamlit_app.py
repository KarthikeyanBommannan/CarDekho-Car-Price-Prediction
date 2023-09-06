import pandas as pd
import numpy as np
import pickle
import streamlit as st
# import xgboost

# Set Streamlit page configuration
st.set_page_config(
    page_title="Car Price Prediction",
    page_icon="📄",
    layout="wide"
)

# Load the trained model
model_path = r'https://github.com/KarthikeyanBommannan/Car-Price-Prediction/blob/main/xgboost_model.pkl'  # Update with your actual model path
try:
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error("Error: Model file not found. Please check the file path.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while loading the model: {str(e)}")
    st.stop()

# Mapping Dictionaries
car_maker = {
    'Audi': 0, 'BMW': 1, 'Chevrolet': 2, 'Datsun': 3, 'Ferrari': 4, 'Fiat': 5, 'Ford': 6, 'Honda': 7,
    'Hyundai': 8, 'Isuzu': 9, 'Jaguar': 10, 'Jeep': 11, 'Kia': 12, 'Land Rover': 13, 'Lexus': 14,
    'MG': 15, 'MINI': 16, 'Mahindra': 17, 'Maruti Suzuki': 18, 'Maserati': 19, 'Mercedes-Benz': 20,
    'Mitsubishi': 21, 'Nissan': 22, 'Porsche': 23, 'Renault': 24, 'Rolls-Royce': 25, 'Skoda': 26,
    'Ssangyong': 27, 'Tata': 28, 'Toyota': 29, 'Volkswagen': 30, 'Volvo': 31
}

Transmission = {'Manual': 1, 'Automatic': 0}
Drivetrain = {'AWD': 2, 'RWD': 1, 'FWD': 0}

# Create Streamlit columns for input fields
col1, col2, col3 = st.sidebar.columns(3)

with col1:
    selected_car_maker = st.selectbox('Brand Name', car_maker.keys())

with col2:
    trans = st.selectbox('Transmission', Transmission.keys())

with col3:
    dvt = st.selectbox('Drivetrain', Drivetrain.keys())

col4, col5, col6 = st.sidebar.columns(3)

with col4:
    bhp_number = st.number_input("Enter Brake Horse Power")

with col5:
    year = st.number_input("Enter Make year of car")

with col6:
    fuel_tank = st.number_input("Enter Fuel Tank Capacity")

col7, col8 = st.sidebar.columns(2)

with col7:
    seating = st.number_input("Enter the No. of Seats")

with col8:
    kilometer = st.number_input("Enter the Kilometer driven")

# Create a prediction button
predict = st.sidebar.button("Predict", type="primary")

if predict:
    data = {
        'Make': [selected_car_maker],
        'Year': [year],
        'Kilometer': [kilometer],
        'Transmission': [trans],
        'Max_Power_in_bhp': [bhp_number],
        'Drivetrain': [dvt],
        'Seating Capacity': [seating],
        'Fuel Tank Capacity': [fuel_tank]
    }

    inputs_df = pd.DataFrame(data)
    inputs_df['Make'] = inputs_df['Make'].map(car_maker)
    inputs_df['Transmission'] = inputs_df['Transmission'].map(Transmission)
    inputs_df['Drivetrain'] = inputs_df['Drivetrain'].map(Drivetrain)

    try:
        col9,col10,col11 = st.columns(3)
        with col9:
            st.write("The Car Brand:",selected_car_maker)
            st.write("The Make Year is:",year)
            st.write("The Transmission:",trans)
            st.write("The Drivetrain:",dvt)
            st.write("Horse power:",bhp_number)
            st.write("Fuel Tank Capacity:",fuel_tank)
            st.write("Total Kilometer Driven:",kilometer)
            st.write("Number of Seats:",seating)
        prediction = model.predict(inputs_df)
        st.success(f"Predicted Car Price: Rs {prediction[0]:,.2f}")
    except Exception as e:
        st.error(f"An error occurred while making the prediction: {str(e)}")
