# House Price Prediction Project

## Overview
This project involves building a machine learning model to predict house prices using features like latitude, longitude, and other property-related data. It includes data preprocessing, feature engineering, and model training, using both classification and regression algorithms. The project is structured into different parts for data collection, analysis, and model building.

## Project Structure
The project consists of the following files and directories:

- `data/`: Contains the pickle file with the latitude and longitude data along with the corresponding county and road information.
- `fetched_location_data.py`: A Python script that fetches the actual county and road information using latitude and longitude data from the dataset. It uses the Geopy library to retrieve the data and saves the results as a pickle file.
- `main.ipynb`: The main Jupyter notebook that:
  1. Loads and imports the data from the pickle file.
  2. Performs exploratory data analysis (EDA) to examine the features and target variables.
  3. Implements Random Forest Regressor to assess the importance of each feature.
  4. Conducts data preprocessing, including feature engineering and dropping unnecessary features.
  5. Uses classification algorithms (SGDClassifier) to predict missing values for the `Road` and `County` columns.
  6. Trains two models: Random Forest Regressor and Linear Regression, using the processed dataset.

## Dependencies
- `pandas`
- `numpy`
- `scikit-learn`
- `geopy`
- `matplotlib`
- `seaborn`

You can install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```
## Workflow

### Data Loading:
The `fetched_location_data.py` script creates a pickle file with latitude and longitude coordinates along with corresponding county and road information fetched using Geopy.

### Exploratory Data Analysis (EDA):
The `main.ipynb` file loads the pickle file and performs an initial analysis of the dataset using EDA techniques. This helps to understand the data distribution, feature correlation, and feature importance.

### Data Preprocessing:
The dataset undergoes feature engineering and cleaning. The latitude and longitude features are used to fetch missing data, specifically the `County` and `Road` features. Some irrelevant or non-correlated features are dropped to improve the model's performance.

### Modeling:
- **SGDClassifier** is used to predict missing values for the `Road` and `County` columns.
- **Random Forest Regressor** and **Linear Regression** models are trained on the preprocessed data to predict house prices.

### Model Evaluation:
The performance of the trained models is evaluated using metrics such as R², RMSE, and MAE to determine the best model for price prediction.

## How to Run the Project
1. Clone or download the repository.
2. Install the required dependencies.
3. Run the `fetched_location_data.py` script to create the pickle file(suggest not doing it and using the pickle file already in data folder as it takes 5-7hrs).
4. Open and run the `main.ipynb` notebook to load the data, preprocess it, and train the models.

## Notes
- This is a temporary README to describe the project's current structure and steps.
- The project is still under development and might undergo changes, especially in terms of model performance and evaluation.
