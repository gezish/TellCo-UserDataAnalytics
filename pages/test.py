import sys, os
import streamlit as st
import pickle
import numpy as np
import pandas as pd
#st.set_option('deprecation.showPyplotGlobalUse', False)
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objects as go


from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.model_selection import train_test_split
#import matplotlib.pyplot as plt

from sqlalchemy import create_engine
from scripts import data_visualizer
from io import StringIO

@st.cache_data
def load_data():
    data = pd.read_csv('./data/my_clean_data.csv')
    return data

@st.cache_data
def load_engagement_data():
    data = pd.read_csv("../data/TellCo_user_engagements.csv")
    return data

@st.cache_data
def user_experiance_data():
    data = pd.read_csv("../data/TellCo_user_experience_data.csv")
    return data
def data_info(df):
    st.markdown('**Data Info**')
    buffer = StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)
def load_model(models):
    with open("../models/models", "rb") as f:
        kmeans1 = pickle.load(f)
        kmeans1.n_init='auto'
            
    return kmeans1
def main():
    st.title('User Satisfaction Analysis')
    
    # load data
    data_load_state = st.text('Loading data...')
    data = load_data()
    data_load_state.text('Loading data... done!') 
    data_info(data)
        
    data_load_state.text('Loading engagement data...!') 
    user_engagements = load_engagement_data()
    data_load_state.text('Loading engagement data... done!')
    data_info(user_engagements)
    
    data_load_state.text('Loading user experiance data...!') 
    user_experiance = user_experiance_data()
    data_load_state.text('Loading user experiance data... done!')
    data_info(user_experiance)
    
    # load models
    data_load_state.text('Loading user engagement model . . .!')
    kmeans1 = load_model(TellCo_user_engagement.pkl)
    data_load_state.text('Loading model completed!')  
    # Distance between the centroid and samples
    eng_df = user_engagements.set_index('MSISDN/Number')[
    ['time_duration', 'Total Data Volume (Bytes)', 'user_sessions']]
    scaler = StandardScaler()
    scaled_array = scaler.fit_transform(eng_df)
    pd.DataFrame(scaled_array).head(5) 
    
    
    
if __name__ == '__main__':
    main()    