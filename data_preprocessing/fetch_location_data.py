import pickle
from geopy.geocoders import Nominatim
import pandas as pd
import time
from sklearn.datasets import fetch_california_housing
from tqdm import tqdm
import os

# Load dataset
data = fetch_california_housing()
df = pd.DataFrame(
    data.data,
    columns=data.feature_names
)
df = df.rename(columns={'LAT': 'Latitude', 'LONGITUDE': 'Longitude'})

def process_in_chunks(df, chunk_size=100, checkpoint_file='checkpoint.pkl', 
                     final_file='ca_locations_complete.pkl', 
                     start_from_checkpoint=True):
    
    geolocator = Nominatim(user_agent='california_housing_analysis')
    
    # Initialize or load checkpoint data
    if start_from_checkpoint and os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'rb') as f:
            loc_update = pickle.load(f)
            # Calculate starting point
            start_idx = len(loc_update['County'])
            print(f"Resuming from index {start_idx}")
    else:
        loc_update = {
            "County": [],
            "Road": []
        }
        start_idx = 0

    # Calculate number of chunks
    total_rows = len(df)
    chunks = range(start_idx, total_rows, chunk_size)
    
    try:
        # Create progress bar for chunks
        with tqdm(total=total_rows-start_idx) as pbar:
            for start in chunks:
                end = min(start + chunk_size, total_rows)
                chunk = df.iloc[start:end]
                
                # Process each row in the chunk
                for index, row in chunk.iterrows():
                    coordinates = f"{row['Latitude']}, {row['Longitude']}"
                    
                    try:
                        location = geolocator.reverse(coordinates, language='en', exactly_one=True)
                        if location:
                            address = location.raw.get('address', {})
                            county = address.get('county', 'Unknown')
                            road = address.get('road', 'Unknown')
                        else:
                            county = road = 'Unknown'
                            
                        loc_update["County"].append(county)
                        loc_update["Road"].append(road)
                        
                    except Exception as e:
                        print(f"\nError for coordinates {coordinates}: {e}")
                        loc_update["County"].append('Unknown')
                        loc_update["Road"].append('Unknown')
                    
                    time.sleep(1)  
                    pbar.update(1)
                
                # Save checkpoint after each chunk
                with open(checkpoint_file, 'wb') as f:
                    pickle.dump(loc_update, f)
                print(f"\nCheckpoint saved at index {end}")
        
        # Save final results
        with open(final_file, 'wb') as f:
            pickle.dump(loc_update, f)
        print(f"\nFinal results saved to {final_file}")
        
        return loc_update
        
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Progress has been saved to checkpoint file.")
        with open(checkpoint_file, 'wb') as f:
            pickle.dump(loc_update, f)
        return loc_update

def merge_results_with_df(df, results):
    """Merge the geocoding results back into the original dataframe"""
    df_result = df.copy()
    df_result['County'] = results['County']
    df_result['Road'] = results['Road']
    return df_result


CHUNK_SIZE = 100  

print(f"Total records to process: {len(df)}")
print(f"Processing in chunks of {CHUNK_SIZE}")
print("Press Ctrl+C to interrupt (progress will be saved)")

# Process the data
results = process_in_chunks(df, 
                          chunk_size=CHUNK_SIZE,
                          checkpoint_file='ca_housing_checkpoint.pkl',
                          final_file='ca_housing_complete.pkl',
                          start_from_checkpoint=True)

# Merge results back to dataframe
df_final = merge_results_with_df(df, results)

# Show sample of results
print("\nSample of processed data:")
print(df_final[['Latitude', 'Longitude', 'County', 'Road']].head())

# Save final DataFrame
df_final.to_csv('california_housing_with_locations.csv', index=False)
print("\nFinal DataFrame saved to california_housing_with_locations.csv")