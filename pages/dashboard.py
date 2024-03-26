import streamlit as st
import sys, os
import sys
sys.path.append('.')
sys.path.append(os.path.abspath(os.path.join('./scripts')))
import test
from pages import Data_Overview
from pages import user_engagement
from pages import experiance_new
from pages import user_satisfaction
from pages import user_experience
from pages import over
from pages import Bussines
#import streamlit as st
# from flask import Flask



PAGES = {
    "Bussines Need": Bussines,
    "Data Overview": Data_Overview,
    "User Engagement Analysis":  user_engagement,
    "User Engagement Analysis":  over,
    "User Experience Analytics": experiance_new,
    "User Experience Analytics2": user_experience,
    "User Satisfaction Analysis": user_satisfaction,
}

selection = st.sidebar.radio("Go to page", list(PAGES.keys()))
page = PAGES[selection]
page.app()
