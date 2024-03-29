import sys
import os
import sys
import pickle
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

sys.path.insert(1, '../scripts')
from constants import *
from df_outlier import DfOutlier
from df_overview import DfOverview
from df_utils import DfUtils
from df_helper import DfHelper
from streamlit_plot import *

utils = DfUtils()
helper = DfHelper()


@st.cache_data
def loadCleanData():
    df = pd.read_csv("./data/my_clean_data.csv")
    return df


@st.cache_data
def getExperienceDataFrame():
    df = loadCleanData().copy()
    user_experience_df = df[[
        "MSISDN/Number",
        "Avg RTT DL (ms)",
        "Avg RTT UL (ms)",
        "Avg Bearer TP DL (kbps)",
        "Avg Bearer TP UL (kbps)",
        "TCP DL Retrans. Vol (Bytes)",
        "TCP UL Retrans. Vol (Bytes)",
        "Handset Type"]].copy()
    
    user_experience_df['total_avg_rtt'] = user_experience_df['Avg RTT DL (ms)'] + user_experience_df['Avg RTT UL (ms)']
    user_experience_df['total_avg_tp'] = user_experience_df['Avg Bearer TP DL (kbps)'] + user_experience_df['Avg Bearer TP UL (kbps)']
    user_experience_df['total_avg_tcp'] = user_experience_df['TCP DL Retrans. Vol (Bytes)'] + user_experience_df['TCP UL Retrans. Vol (Bytes)']

    return user_experience_df


@st.cache_data
def getExperienceData():
    df = getExperienceDataFrame().copy()
    user_experience = df.groupby('MSISDN/Number').agg({
        'total_avg_rtt': 'sum',
        'total_avg_tp': 'sum',
        'total_avg_tcp': 'sum'})
    return user_experience


@st.cache_data
def getNormalData(df):
    res_df = utils.scale_and_normalize(df)
    return res_df

@st.cache_data
def get_distortion_andinertia(df, num):
    distortions, inertias = utils.choose_kmeans(df.copy(), num)
    return distortions, inertias


def plot10(df):
    col = st.selectbox("Compute & list 10 of the top, bottom and most frequent: from", (
        [
            "TCP values",
            "Duration", 
            "Throughput values"
        ]))
    if col == "TCP values":
        sorted_by_tcp = df.sort_values('total_avg_tcp', ascending=False)
        return plot10Sorted(sorted_by_tcp, 'total_avg_tcp')
    elif col == "RTT values":
        sorted_by_rtt = df.sort_values('total_avg_rtt', ascending=False)
        return plot10Sorted(sorted_by_rtt, 'total_avg_rtt')
    else:
        sorted_by_tp = df.sort_values('total_avg_tp', ascending=False)
        return plot10Sorted(sorted_by_tp, 'total_avg_tp')

def plot10Sorted(df, col_name):
    col = st.selectbox("Select from: from", (
        [
            "Top 10",
            "Last 10",
        ]))
    if col == "Top 10":
        _sorted = df.head(10)[col_name]
        return hist(_sorted)

    else:
        _sorted = df.tail(10)[col_name]
        return hist(_sorted)


def elbowPlot(df, num):
    distortions, inertias = get_distortion_andinertia(df, num)
    fig = make_subplots(
        rows=1, cols=2, subplot_titles=("Distortion", "Inertia")
    )
    fig.add_trace(go.Scatter(x=np.array(range(1, num)),
                             y=distortions), row=1, col=1)
    fig.add_trace(go.Scatter(x=np.array(
        range(1, num)), y=inertias), row=1, col=2)
    fig.update_layout(title_text="The Elbow Method")
    st.plotly_chart(fig)

def app():
    st.title('User Experience Analytics')
    st.header("Top 10 customers per engagement metrics")
    user_experience = getExperienceData().copy()

    df_outliers = DfOutlier(user_experience)
    cols = ["total_avg_rtt",
            "total_avg_tp",
            "total_avg_tcp"]    
    df_outliers.replace_outliers_with_iqr(cols)
    user_experience = df_outliers.df
    plot10(user_experience)

    st.header("Clustering customers based on their engagement")
    st.markdown(
    '''
        Here we will try to cluster customers based on their experience.
        To find the optimized value of k, first, let's plot an elbow curve graph.
        To start, choose the number of times to runs k-means.
    ''')
    num = st.selectbox('Select', range(0, 20))
    select_num = 1
    if(num != 0):
        normal_df = getNormalData(user_experience)
        elbowPlot(normal_df, num+1)

        select_num = st.selectbox('Select', range(1, num+1))

    if(select_num != 1):
        st.markdown(
        '''
            Based on the image above choose the number of clusters
        ''')
        kmeans = KMeans(n_clusters=select_num, random_state=0).fit(normal_df)
        user_experience["cluster"] = kmeans.labels_

        st.markdown(
        '''
            Number of elements in each cluster
        ''')
        st.write(user_experience['cluster'].value_counts())

        show2D = False
        if st.button('Show 2D visualization'):
            if(show2D):
                show2D = False
            else:
                show2D = True

        if(show2D):
            st.markdown(
                '''
                2D visualization of cluster
            ''')
        scatter(user_experience, x='total_avg_tcp', y="total_avg_rtt",
                c='cluster', s='total_avg_tp')

        show3D = False
        if st.button('Show 3D visualization'):
            if(show3D):
                show3D = False
            else:
                show3D = True
        if(show3D):
            st.markdown(
                '''
                3D visualization of cluster
            ''')
            scatter3D(user_experience, x="total_avg_tcp", y="total_avg_rtt", z="total_avg_tp",
                    c="cluster", interactive=True, rotation=[-1.5, -1.5, 1])

        st.warning(
            'Remember the cluster with the worst experience. we need that for satisfaction analysis')
        st.markdown(
        '''
            Save the model for satisfaction analysis
        ''')
        if st.button('Save CSV'):
            helper.save_csv(user_experience,
                            './data/TellCo_user_experience_data.csv', index=True)

            with open("./models/TellCo_user_experiance.pkl", "wb") as f:
                pickle.dump(kmeans, f)



