import streamlit as st
import os
from Recommender import *
from Download import *
##################
st.set_page_config(page_title='👻👻🚗🌫️‍', page_icon='👻',
                   layout="centered", initial_sidebar_state="collapsed",
                   menu_items=None)
##################
page = st.sidebar.selectbox('Select page',['Recommender','Download Data'])
st.markdown(os.listdir(os.getcwd()))
st.markdown(os.listdir(f"{os.getcwd()}/pycache"))

if page=='Recommender':
    Recommender()
elif page=='Download Data':
    Download()
