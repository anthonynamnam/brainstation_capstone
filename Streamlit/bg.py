import base64

import streamlit as st


# Function
def sidebar_bg(side_bg):
    ext = side_bg.split('.')[-1]
    st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] > div:first-child {{
            background: url(data:images/{ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});

        }}
        </style>
        """,
        unsafe_allow_html=True,
        )
   
def mainpage_bg(main_bg):

    st.markdown(
        f"""
        <style>
        .main {{
            background: url("{main_bg}");
        }}
        </style>
        """,
        unsafe_allow_html=True,
        )
   