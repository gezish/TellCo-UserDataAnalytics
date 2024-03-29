import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import matplotlib
st.set_option('deprecation.showPyplotGlobalUse', False)
from scripts import data_visualizer
from scripts import df_overview
import df_overview as DfOverview
from scripts import data_selector
import plotly.express as px
from io import StringIO

@st.cache_data
def load_description():
    des = pd.read_excel("./data/Field_Descriptions.xlsx")
    return des
@st.cache_data
def loadOriginalData():
    df = pd.read_csv("./data/Week1_challenge_data_source(CSV).csv")
    return df
@st.cache_data
def load_data():
    data = pd.read_csv('./data/my_clean_data.csv')
    return data


def count_values(data, column_name):
    value_counts = data[column_name].value_counts().reset_index()
    value_counts.columns = [column_name, 'counts']
    return value_counts





def app():
    st.sidebar.title('Data Overview')
    selected_section = st.sidebar.radio('Go to', ['Home', 'Table Description',
                                                  'Sample of orginal Df',
                                                  'Data After preprocessing',
                                                  'Overview of Type and Usage statistics',
                                                  'Bivariate analysis',
                                                  'Correlation Analysis Results',
                                                  
                                                  ])
    st.title('Data Overview')
    if selected_section == 'Home':
        st.markdown(
    '''
        The telecom dataset has 150001 observations with 55 features. 
        Here is description of all the features
    ''')
    elif selected_section == 'Table Description':
        st.header('Data Description')
        disc = load_description()
        st.write(disc)
        
        
        #st.header('Sample df from the Original data')
    
    elif selected_section == 'Sample of orginal Df':
        st.header('Sample of orginal Data Frame')
        df = loadOriginalData()
        st.write(df.head(10))
    
    elif selected_section == 'Data After preprocessing':
        st.header('Data After preprocessing complete')
        data_load_state = st.text('Loading data...')
        data = load_data()
        data_load_state.text('Loading data... done!')   
        # Display basic info about the loaded data
        st.subheader('Basic Info of Loaded Data')
        st.write("Number of rows & columns:", data.shape)   
        st.subheader('Data Info')
        buffer = StringIO()
        data.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)
        
    elif selected_section == 'Overview of Type and Usage statistics':
       # st.header('Top 10 Handset Types')
        data = load_data()
        #st.write(data.head())
        #st.title('To 10 Handset Types')
        
        st.header('Distribution of Handset Types')
        fig = data_visualizer.plotly_plot_pie(data, 'Handset Type', 10)  # Change 5 to the number of top values you want to show
        st.plotly_chart(fig)    
        st.header("Top 10 phone Manufacturers: ")
        #st.checkbox("Top Manufacturers: ")
        counts_HSM = data['Handset Type'].value_counts()
        st.write(counts_HSM.head(10))
        st.header('Call Duration(Dur. (ms).1) Destribution:')
   
        st.pyplot(data_visualizer.plot_hist(data, 'Dur. (ms).1', 'dodgerblue'))
        st.header('Total Download Distribution:')
        st.pyplot(data_visualizer.plot_hist(data, 'Total DL (Bytes)', 'dodgerblue'))
        st.header('Total Download Distribution:')
        st.pyplot(data_visualizer.plot_hist(data, 'Total UL (Bytes)', 'dodgerblue'))
        
        st.header('Distribution of Total Data Volumes:')
        st.pyplot(data_visualizer.plot_hist(data, 'Total Data Volume (Bytes)', 'dodgerblue'))

        st.header('Social Media Data Volume (Bytes)') 
        st.pyplot(data_visualizer.plot_hist(data, 'Social Media Data Volume (Bytes)', '#40E0D0'))
        
        st.header('Google Usage Data Volumes (Bytes)') 
        st.pyplot(data_visualizer.plot_hist(data, 'Google Data Volume (Bytes)', '#FF5733'))
        
        st.header('Email Usage Data Volumes (Bytes)') 
        st.pyplot(data_visualizer.plot_hist(data, 'Email Data Volume (Bytes)', '#800020'))
        
        st.header('Youtube Usage Data Volumes (Bytes)') 
        st.pyplot(data_visualizer.plot_hist(data, 'Youtube Data Volume (Bytes)', '#C04000'))
        
        st.header('Netflix Usage Data Volumes (Bytes)') 
        st.pyplot(data_visualizer.plot_hist(data, 'Netflix Data Volume (Bytes)'))
        
        st.header('Data Volumes Due to Gaming (Bytes)') 
        st.pyplot(data_visualizer.plot_hist(data, 'Gaming Data Volume (Bytes)', 'indigo'))
        
        st.header('Other Data Volume (Bytes)') 
        st.pyplot(data_visualizer.plot_hist(data, 'Other Data Volume (Bytes)', 'red'))
        st.header('Total Data Volumes (Bytes)') 
        st.pyplot(data_visualizer.plot_hist(data, 'Total Data Volume (Bytes)', '#FC9903'))
        
    elif selected_section == 'Bivariate analysis': 
        clean_data= load_data()   
        st.header('Social Media Data Volume Vs Total Data Volume (Bytes') 
        st.pyplot(data_visualizer.plot_scatter(clean_data.sample(10000), 'Social Media Data Volume (Bytes)', 'Total Data Volume (Bytes)'))
        
        st.header('Google Data Volume Vs Total Data Volume (Bytes)') 
        st.pyplot(data_visualizer.plot_scatter(clean_data.sample(10000), 'Google Data Volume (Bytes)', 'Total Data Volume (Bytes)'))
        
        st.header('Email Data Volume Vs Total Data Volume (Bytes)') 
        st.pyplot(data_visualizer.plot_scatter(clean_data.sample(10000), 'Email Data Volume (Bytes)', 'Total Data Volume (Bytes)'))
        
        st.header('Youtube Data Volume Vs Total Data Volume (Bytes)') 
        st.pyplot(data_visualizer.plot_scatter(clean_data.sample(10000), 'Youtube Data Volume (Bytes)', 'Total Data Volume (Bytes)'))
        
        st.header('Netflix Data Volume Vs Total Data Volume (Bytes)') 
        st.pyplot(data_visualizer.plot_scatter(clean_data.sample(10000), 'Netflix Data Volume (Bytes)', 'Total Data Volume (Bytes)'))
        
        st.header('Gaming Data Volume Vs Total Data Volume (Bytes)') 
        st.pyplot(data_visualizer.plot_scatter(clean_data.sample(10000), 'Gaming Data Volume (Bytes)', 'Total Data Volume (Bytes)'))
        
    elif selected_section == 'Correlation Analysis Results':
        clean_data= load_data()
        Application_used = ['Social Media Data Volume (Bytes)', 'Google Data Volume (Bytes)', 'Email Data Volume (Bytes)',
    'Youtube Data Volume (Bytes)', 'Netflix Data Volume (Bytes)', 'Gaming Data Volume (Bytes)',
    'Other Data Volume (Bytes)']
        st.header('Applications and Usage Correlation') 
        st.write(clean_data[Application_used].corr())
        st.pyplot(data_visualizer.plot_heatmap(clean_data[Application_used].corr(), "Correlation of Applications Data Volume", cmap='Reds', width=20, height=10))
        st.markdown('**Note:-** It looks those applications are not significantly correlated each other. On the other hand some appliatons has a negative correlation.I.e. Google usage sessions increase Gamming and social media data sessions decreases and vice versa.')
   