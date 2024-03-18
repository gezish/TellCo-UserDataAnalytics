import pickle
import numpy as np
import pandas as pd
from math import floor
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import zscore
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import sys, os




def app():
    st.title('User Satisfaction Analysis')
    # load data
    df = pd.read_csv("../data/my_clean_data.csv")
    df.info()

    user_engagements = pd.read_csv("../data/TellCo_user_engagements.csv")
    
    user_experiance = pd.read_csv("../data/TellCo_user_experience_data.csv")
    user_experiance.head(5)
    
    # load models
    with open("../models/TellCo_user_engagement.pkl", "rb") as f:
        kmeans1 = pickle.load(f)
        kmeans1.n_init='auto'
        
        
    # Distance between the centroid and samples
    eng_df = user_engagements.set_index('MSISDN/Number')[
    ['time_duration', 'Total Data Volume (Bytes)', 'user_sessions']]
    scaler = StandardScaler()
    scaled_array = scaler.fit_transform(eng_df)
    pd.DataFrame(scaled_array).head(5)    
    
    # normalize the data for the model
    data_normalized = normalize(scaled_array)
    pd.DataFrame(data_normalized).head(5)
    
    #check from the centeroid
    distance = kmeans1.fit_transform(data_normalized)
    distance_from_less_engagement = list(map(lambda x: x[less_engagement], distance))
    user_engagements['engagement_score'] = distance_from_less_engagement
    user_engagements.head(5)
    
    #Considering the experience score as the Euclidean distance between the user data point & the worst experience’s cluster members
    
    with open("../models/TellCo_user_experiance.pkl", "rb") as f:
        kmeans2 = pickle.load(f)
        kmeans2.n_init='auto'
    
    worst_experiance = 0
    exp_df = user_experiance.set_index('MSISDN/Number')[['total_avg_rtt', 'total_avg_tp', 'total_avg_tcp']]
    scaler = StandardScaler()
    scaled_array = scaler.fit_transform(exp_df)
    pd.DataFrame(scaled_array).head(5)    
    
    data_normalized = normalize(scaled_array)
    pd.DataFrame(data_normalized).head(5)
    
    
    exp_df = user_experiance.set_index('MSISDN/Number')
    distance = kmeans2.fit_transform(data_normalized)
    distance_from_worest_experiance = list(map(lambda x: x[worst_experiance], distance))
    user_experiance['experience_score'] = distance_from_worest_experiance
    user_experiance.head(5)
    
    # Consider the average of both engagement & experience scores as the satisfaction score & report the top 10 satisfied customer
    
    user_id_engagement = user_engagements['MSISDN/Number'].values
    user_id_experiance = user_experiance['MSISDN/Number'].values
    user_intersection = list(set(user_id_engagement).intersection(user_id_experiance))
    user_intersection[:5]
    
    user_engagement_df = user_engagements[user_engagements['MSISDN/Number'].isin(user_intersection)]
    user_engagement_df.shape
    
    user_experiance_df = user_experiance[user_experiance['MSISDN/Number'].isin(user_intersection)]
    user_experiance_df.shape
    
    user_df = pd.merge(user_engagement_df, user_experiance_df, on='MSISDN/Number')
    user_df['satisfaction_score'] = (user_df['engagement_score'] + user_df['experience_score'])/2
    user_df.head(5)
    
    sat_score_df = user_df[['MSISDN/Number', 'engagement_score', 'experience_score', 'satisfaction_score']]
    sat_score_df = sat_score_df.set_index('MSISDN/Number')
    sat_score_df.head(5)
    
    sorted_by_satisfaction = sat_score_df.sort_values('satisfaction_score', ascending=False)
    sat_top_10 = sorted_by_satisfaction['satisfaction_score'].head(10)
    
    hist(sat_top_10)
    
    # Build a regression model of your choice to predict the satisfaction score of a customer.
    
    px.scatter(sat_score_df, 'engagement_score','experience_score', 'satisfaction_score')
    
    # Here we can clearly see whene expirience score and engament score increase, satisfaction score will also increase.
    X = sat_score_df[['engagement_score', 'experience_score']]
    y = sat_score_df[['satisfaction_score']]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2) 
    
    linear_reg = LinearRegression()
    model = linear_reg.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    print('Coefficients: \n', model.coef_)
    print("Mean squared error: %.2f" %
        np.mean((model.predict(X_test) - y_test) ** 2))
    print('Variance score: %.2f' % model.score(X_test, y_test))
    
    
    #Run a k-means(k=2) on the engagement & the experience score .
    user_satisfaction_df = user_df[[
    'MSISDN/Number', 
    'engagement_score',
    'experience_score']].copy()
    user_satisfaction_df = user_satisfaction_df.set_index('MSISDN/Number')
    user_satisfaction_df.head(5)
    #no outlier
    scaler = StandardScaler()
    scaled_array = scaler.fit_transform(user_satisfaction_df)
    scaled_array
    pd.DataFrame(scaled_array).head(5)
    
    data_normalized = normalize(scaled_array)
    pd.DataFrame(data_normalized).head(5)
    
    kmeans = KMeans(n_clusters=2, random_state= 'auto').fit(data_normalized)
    kmeans.labels_
    
    
    user_satisfaction_df.insert(0, 'cluster', kmeans.labels_)
    user_satisfaction_df.head(5)
    user_satisfaction_df['cluster'].value_counts()
    
    fig = px.scatter(user_satisfaction_df, x='engagement_score', y="experience_score",
                 color='cluster')
    Image(pio.to_image(fig, format='png', width=1200))
    
    user_satisfaction_df.to_csv('../data/TellCo_user_satisfaction.csv')
    
    # Aggregate the average satisfaction & experience score per cluster.
    
    user_satisfaction_df.groupby('cluster').agg(
    {'engagement_score': 'sum', 'experience_score': 'sum'})
    
    #Cluster 1 has higher Engagement and satisfaction score. Cluster 2 has vert low expirience score but higher engagement score.
    #Export your final table containing all user id + engagement, experience & satisfaction scores in your local MySQL database. Report a screenshot of a select query output on the exported table.
    engine = create_engine('mysql+pymysql://root:2203@localhost/telecom_user_db')
    
    
    #Model deployment tracking - deploy the model and monitor your model. Here you can use MlOps tools which can help you to track your model’s change. Your model tracking report includes code version, start and end time, source, parameters, metrics(loss convergence) and artifacts or any output file regarding each specific run. (CSV file, screenshot)