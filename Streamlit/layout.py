# footer.py
import streamlit as st

def title():
    st.title('Used Car Price Range Prediction')

def footer():
    
    st.subheader('Contact Me')
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info('**Repo: [This Project](https://github.com/anthonynamnam/brainstation_capstone)**', icon="💡")
    with c2:
        st.info('**My GitHub: [@anthonynamnam](https://github.com/anthonynamnam)**', icon="💻")
    with c3:
        st.info('**Data Source: [Kaggle](https://www.kaggle.com/datasets/3ea0a6a45dbd4713a8759988845f1a58038036d84515ded58f65a2ff2bd32e00/data)**', icon="🧠")