import streamlit as st
import pandas as pd
import joblib

# Load models
clf_et = joblib.load('extra_trees_pipeline.pkl.gz')
clf_knn = joblib.load('knn_pipeline.pkl')
regressor_xgb = joblib.load('regressor_model.pkl')

# Define function to predict location from each model
def predict_location(bath, balcony, total_sqft_int, bhk):
    input_data = pd.DataFrame({'bath': [bath],
                               'balcony': [balcony],
                               'total_sqft_int': [total_sqft_int],
                               'bhk': [bhk]})
    # Predict location using each model
    location_pred_et = clf_et.predict(input_data)[0]
    location_pred_knn = clf_knn.predict(input_data)[0]

    return location_pred_et, location_pred_knn

# Define function to predict price using XGBoost regressor
def predict_price(location, bath, balcony, total_sqft_int, bhk):
    input_data = pd.DataFrame({'location': [location],
                               'bath': [bath],
                               'balcony': [balcony],
                               'total_sqft_int': [total_sqft_int],
                               'bhk': [bhk]})
    price_pred = regressor_xgb.predict(input_data)[0]
    return price_pred

# Streamlit app
st.title('House Recommendation System')

bath = st.number_input('Number of Bathrooms', min_value=1, max_value=10, step=1)
balcony = st.selectbox('Number of Balconies', options=[0, 1, 2, 3])

total_sqft_int = st.slider('Total Square Feet', min_value=350, max_value=30500, step=1, value=(350))
bhk = st.number_input('Number of Bedrooms (BHK)', min_value=1, max_value=10, step=1)

if st.button('Predict'):
    # Predict location using each model
    location_pred_et, location_pred_knn = predict_location(bath, balcony, total_sqft_int, bhk)
    st.success(f'Predicted Location 1 : {location_pred_et}')
    st.success(f'Predicted Location 2 : {location_pred_knn}')

    # Use XGBoost regressor to predict price
    price_pred_et = predict_price(location_pred_et, bath, balcony, total_sqft_int, bhk)
    st.success(f'Predicted Price 1 location: {price_pred_et:.2f} lakhs')

    price_pred_knn = predict_price(location_pred_knn, bath, balcony, total_sqft_int, bhk)
    st.success(f'Predicted Price 2 location : {price_pred_knn:.2f} lakhs')
