import pandas as pd
import joblib
import streamlit as st
model = joblib.load('./model/trained_model.pkl')
road_encoded_df = pd.read_csv('./data/encoded_Road.csv')
county_encoded_df = pd.read_csv('./data/encoded_County.csv')


county_mapping = dict(zip(county_encoded_df['County'], county_encoded_df['County_encoded']))
road_mapping = dict(zip(road_encoded_df['Road'], road_encoded_df['Road_encoded']))

def encode_input(county,road):
    if county in county_mapping:
        encoded_county = county_mapping[county]
    else:
        print(f"Warning: '{county}' not found in the encoding. Please check the input.")
        encoded_county = None
    
    if road in road_mapping:
        encoded_road = road_mapping[road]
    else:
        print(f"Warning: '{road}' not found in the encoding. Please check the input.")
        encoded_road = None
    
    return encoded_county,encoded_road
        
st.title("California House Price Predictor")


st.header("Enter the details below:")

county = st.selectbox("Select County:", list(county_mapping.keys()))
road = st.selectbox("Select Road:", list(road_mapping.keys()))
feature1 = st.number_input("Median Income:", min_value=0.0, step=0.1)
feature2 = st.number_input("House Age:", min_value=0.0, step=0.1)
feature3 = st.number_input("Average Number of Rooms:", min_value=0.0, step=0.1)
feature4 = st.number_input("Average Number of Bedrooms", min_value=0.0, step=0.1)
feature5 = st.number_input("Neighborhood Population", min_value=0.0, step=0.1)
feature6 = st.number_input("Average Number of Occupants", min_value=0.0, step=0.1)

# Encode user inputs
encoded_county, encoded_road = encode_input(county, road)

# Predict button
if st.button("Predict"):
    # Ensure all inputs are provided
    if encoded_county is None or encoded_road is None:
        st.error("Invalid input for County or Road. Please select valid options.")
    else:
        # Prepare input for the model
        input_features = [feature1, feature2, feature3, feature4,feature5,feature6,encoded_county,encoded_road]
        prediction = model.predict([input_features])
        st.success(f"Predicted House Price: ${prediction[0]:,.2f}")


