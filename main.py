import pandas as pd
import joblib
from flask import Flask

app = Flask(__name__)

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
        
county_input = 'Los Angeles County'  # Replace with actual user input
road_input = 'Barry Avenue'  # Replace with actual user input

encoded_county, encoded_road = encode_input(county_input, road_input)
print(f"Encoded County: {encoded_county}, Encoded Road: {encoded_road}")


@app.route("/")
def hello_world():
    return "<p> Hello, World!</p>"



if __name__ == '__main__':
    app.run(debug=True)