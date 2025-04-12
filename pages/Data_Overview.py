import os,sys
sys.path.append(os.path.abspath(os.path.join('../scripts')))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math
import matplotlib
st.set_option('deprecation.showPyplotGlobalUse', False)
from scripts import data_visualizer
from scripts import df_overview
import df_overview as DfOverview
from scripts import data_selector
import plotly.express as px
from io import StringIO
from scripts import outlier_handler

from scripts import data_selector as ds
from scripts import data_cleaner as dc
#from scripts import outlier_handler as OutlierHandler
#from outlier_handler import OutlierHandler

#outlier = outlier_handler()

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

def data_info(df):
    st.markdown('**_______________________________________**')
    buffer = StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)

def count_values(data, column_name):
    value_counts = data[column_name].value_counts().reset_index()
    value_counts.columns = [column_name, 'counts']
    return value_counts





def app():
    st.sidebar.title('Data Overview')
    selected_section = st.sidebar.radio('Go to', ['Home', 'Preprocessing',
                                                  
                                                  'Data After preprocessing',
                                                  'Overview of Type and Usage statistics',
                                                  'Bivariate analysis',
                                                  'Correlation Analysis Results',
                                                  
                                                  ])
    st.title('Data Overview')
    if selected_section == 'Home':
        st.markdown(
    '''
        **The telecom dataset has 150001 observations with 55 features. 
        Here is description of all the features**
    ''')
        disc = load_description()
        st.write(disc)
        st.markdown('**Sample of Original df**')
        df = loadOriginalData()
        st.write(df.head(10))
        st.write('**Data Shape:**', df.shape)
        totalCells=df.size
        
    elif selected_section == 'Preprocessing':
        #st.header('Data Description')
        
        
        #st.header('Sample df from the Original data')
    
    
        #st.markdown('**Sample of Original df and Cleaning**')
        #df = loadOriginalData()
        #st.write(df.head(10))
        #st.write('**Data Shape:**', df.shape)
        #totalCells=df.size
        #st.markdown('**Total number of items in the dataset:**', totalCells)
        st.markdown('##### Data Cleaning, Transforming and Extraction')
        if st.checkbox('Handling Missing Values'):
            df = loadOriginalData()
            
            missingCount = df.isnull().sum()
            totalMissing = missingCount.sum()
            totalCells=df.size
            st.write('**Check Missing values**',missingCount)  
            st.write('**TotalMissing =**', missingCount.sum())
            st.write("**The TellCo dataset contains:**", round(((totalMissing/totalCells) * 100), 2),"%", "missing values.")
            missed = dc.missing_values_table(df)
            st.write("**Dataframe With percent of missing values:**\n",missed )
            
            st.markdown('**Note:** From the above result, I can see that some of the columns has a greater missing values and I decide to drop a column with missing value of greater than or equal to 30% of the entire column data')
            columns_to_remove = missed[missed['% of Total Values'] >= 30.00].index.tolist()
            st.write('**Columns With data loss:**', columns_to_remove)
            
            #st.markdown('Column to be removed based on tha above criterion:',missed[missed['% of Total Values'] >= 30.00].index.tolist())
            st.markdown('**Note:-** From Business requirement we have understood that TCP UL Retrans and TCP DL Retrans are required for Experience of user analysis. so we will not remove them')
            columns_to_remove = [col for col in columns_to_remove if col not in ['TCP UL Retrans. Vol (Bytes)','TCP DL Retrans. Vol (Bytes)']]
            df_copy = df.copy()
            my_df = df.drop(columns_to_remove, axis=1)
            st.write("Data shape after dropping:", my_df.shape)
            missing_new = dc.missing_values_table(my_df)
            
            st.markdown('##### Apply filling techniques')
            st.markdown("Backward Filling for **TCP UL Retrans. Vol (Bytes)** and **Avg RTT DL (ms)** is  applied")        
                # backward filling
            dc.fix_missing_bfill(my_df, 'TCP UL Retrans. Vol (Bytes)')
            dc.fix_missing_ffill(my_df, 'Avg RTT DL (ms)')
            dc.fix_missing_bfill(my_df, 'TCP DL Retrans. Vol (Bytes)')
            st.markdown("**Skew data check**") 
            my_df['Avg RTT DL (ms)'].skew(skipna=True)
            my_df['Avg RTT UL (ms)'].skew(skipna=True)
            missing_new = dc.fix_missing_ffill(my_df, 'Avg RTT UL (ms)')
            st.write(missing_new)
            st.write("**Here-** We have Handset Type and Handset Manufacturer are catagorical values so we can change there value to not_known")
        
            dc.fix_missing_value(my_df, 'Handset Type', 'not_known')
            dc.fix_missing_value(my_df, 'Handset Manufacturer', 'not_known')
        
            missing_new2=dc.drop_rows_with_missing_values(my_df)
            st.write("**Final data missing Values:**", missing_new2)
            data_info(my_df)
        
            st.write("From the above e we can observe that **Start** and **End** columns are datetime values, but labelled as objects.")
            if st.button("Convert to Date_Time"):
                dc.convert_to_datetime(my_df, ['Start', 'End'])
                data_info(my_df)
            st.markdown('**Select other object datatypes and convert it to string**')    
            if st.button("Convert to String"):
               strings = my_df.select_dtypes(include='object').columns.tolist()
               dc.convert_to_string(my_df, strings)
               st.write(my_df.dtypes) 
           
            st.markdown("'Bearer Id', 'IMSI', 'MSISDN/Number', 'IMEI' are float types" )      
            if st.button("Conversion to int"):
                int_columns = ['Bearer Id', 'IMSI', 'MSISDN/Number', 'IMEI',]
                dc.convert_to_int(my_df, int_columns)
                st.write(my_df.dtypes) 
                
            if st.button('check and drop duplicates'):
                st.write(dc.drop_duplicates(my_df))    
                
            
            st.markdown('Check and drop if "Dur. (ms)","Dur. (ms).1" are similar')
            if st.button("Check and Drop one of it after backup"):
                
                selected_columns = my_df[["Dur. (ms)","Dur. (ms).1"]]
                dc.multiply_by_factor(selected_columns, ['Dur. (ms).1'], 1/1000)
                selected_columns['comparison'] = (selected_columns['Dur. (ms)'] == selected_columns['Dur. (ms).1'].apply(math.floor))
                st.write(selected_columns)
                
                st.write(all(selected_columns['comparison']))
                backup_df = my_df.copy()
                st.write(dc.drop_columns(backup_df, ['Dur. (ms)']))
                st.markdown("**Check and Mange Outliers**") 
            #if st.button("Manage outliers"):
                st.markdown("Descriptive statistics for numerical columns:")
                columns = backup_df.select_dtypes('float32').columns.tolist()
               # df_out1 = outlier_handler.OutlierHandler.getOverview(backup_df, columns)
                st.write(outlier_handler.OutlierHandler.getOverview(backup_df, columns))
                st.markdown("Replace outliers with fences(Upper and Lower):")
                df_out2 = outlier_handler.OutlierHandler.replace_outliers_with_fences(columns)
                st.write(df_out2)

            st.markdown("Descriptive names for some Columns for next phase")
            st.markdown(
                """ 
                backup_df['Social Media Data Volume (Bytes)'] = backup_df['Social Media UL (Bytes)'] + backup_df['Social Media DL (Bytes)']
                backup_df['Google Data Volume (Bytes)'] = backup_df['Google UL (Bytes)'] + backup_df['Google DL (Bytes)']
                backup_df['Email Data Volume (Bytes)'] = backup_df['Email UL (Bytes)'] + backup_df['Email DL (Bytes)']
                backup_df['Youtube Data Volume (Bytes)'] = backup_df['Youtube UL (Bytes)'] + backup_df['Youtube DL (Bytes)']
                backup_df['Netflix Data Volume (Bytes)'] = backup_df['Netflix UL (Bytes)'] + backup_df['Netflix DL (Bytes)']
                backup_df['Gaming Data Volume (Bytes)'] = backup_df['Gaming UL (Bytes)'] + backup_df['Gaming DL (Bytes)']
                backup_df['Other Data Volume (Bytes)'] = backup_df['Other UL (Bytes)'] + backup_df['Other DL (Bytes)']
                backup_df['Total Data Volume (Bytes)'] = backup_df['Total UL (Bytes)'] + backup_df['Total DL (Bytes)']
                """)
                        
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
   