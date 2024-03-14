import streamlit as st
import sys, os
import sys
sys.path.append('.')
sys.path.append(os.path.abspath(os.path.join('./scripts')))
import test
from pages import overview
from pages import user_engagement
from pages import user_experience
from pages import user_satisfaction

#import streamlit as st
# from flask import Flask

PAGES = {
    "Data Overview": overview,
    "User Engagement Analysis":  user_engagement,
    "User Experience Analytics": user_experience,
    "User Satisfaction Analysis": user_satisfaction,
}

selection = st.sidebar.radio("Go to page", list(PAGES.keys()))
page = PAGES[selection]
page.app()
