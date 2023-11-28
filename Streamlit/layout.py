# footer.py
import streamlit as st
from PIL import Image

def title():
    st.title("Used Car Price Range Prediction")

def footer():
    
    st.subheader("Contact Me")
    
    c1, c2, c3= st.columns(3)
    with c1:
        st.info("**[My Github](https://github.com/anthonynamnam)**", icon="💻")
    with c2:
        st.info("**[LinkedIn](https://www.linkedin.com/in/anthony-kwok01)**", icon="🛜")
    with c3:
        st.info("**[Medium](https://kwokanthony.medium.com/)**", icon="✍🏻")
        
def project_info_link():
    st.subheader("Links")
    c1, c2,c3 = st.columns([0.2,0.2,0.6])
    with c1:
        st.info("**[Project Repo](https://github.com/anthonynamnam/brainstation_capstone)**", icon="💡")
    with c2:
        st.info("**[Kaggle Data Source](https://www.kaggle.com/datasets/3ea0a6a45dbd4713a8759988845f1a58038036d84515ded58f65a2ff2bd32e00/data)**", icon="🧠")
        
def brand_logo_bar():
    # Content
    cols = st.columns(14)
    standard_width = None
    
    brand_list = ["acura","tesla","bmw","bentley","chevrolet","isuzu","kia","benz","ferrari","audi","suzuki","volkswagen"]
    brand_list.sort()
    
    for brand_name in brand_list:
        if f"images/logo-{brand_name}.png" not in st.session_state:
            st.session_state[f"{brand_name}"] = Image.open(f"images/logo-{brand_name}.png")
    
    for i, brand_name in enumerate(brand_list):
        cols[i].image(st.session_state[f"{brand_name}"],width=standard_width)
