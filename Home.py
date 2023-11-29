# pip freeze > requirements.txt
# https://blog.runpod.io/serverless-create-a-basic-api/

import time
import streamlit as st
from PIL import Image
import helpers.sidebar as sidebar
import requests
import os
from dotenv import load_dotenv
load_dotenv()


runpod_id = os.getenv('runpod_id')
runpod_secret = os.getenv('runpod_secret')

# st.sidebar.markdown("## Main Menu")

logo = Image.open('logo.png')

st.set_page_config(
    page_title='AntibodyGPT: Antibody Protein Generation', 
    page_icon=logo)

sidebar.get_sidebar()
    
st.write("# Welcome to AntibodyGPT")


st.markdown(
    """
    This is a demo of our Antibody Protein Generation API.

"""
)



