# different type of plotters module


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plotly_plot_pie(df, column, limit=None):
    a = pd.DataFrame({'count': df.groupby([column]).size()}).reset_index()
    a = a.sort_values("count", ascending=False)
    if limit:
        a.loc[a['count'] < limit, column] = f'Other {column}s'
    fig = px.pie(a, values='count', names=column, title=f'Distribution of {column}s', width=800, height=500)
    fig.show()

def plotly_plot_hist(df, column, color=['cornflowerblue']):
    fig = px.histogram(
            df,
            x=column,
            marginal='box',
            color_discrete_sequence=color,
            title=f'Distribution of {column}')
    fig.update_layout(bargap=0.01)
    fig.show()
    
def plotly_plot_scatter(df, x_col, y_col, marker_size, hover=[]):
    fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            opacity=0.8,
            hover_data=hover,
            title=f'{x_col} vs. {y_col}')
    fig.update_traces(marker_size=marker_size)
    fig.show()
