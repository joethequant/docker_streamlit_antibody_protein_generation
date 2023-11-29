import streamlit as st
from PIL import Image

logo = Image.open('logo.png')

def get_sidebar():
    with st.sidebar:
        # col1, col2 = st.columns([5, 7])  # Adjust the ratio as needed for your logo and title size
        # with col1:
            
        # with col2:
        #     st.title('Antigen.ai')
        st.image(logo, width=90)
        st.title('Antibody Protein Generation')