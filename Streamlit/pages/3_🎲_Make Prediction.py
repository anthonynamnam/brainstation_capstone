# Libraries
import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import time

import os
from pathlib import Path
import pickle
import joblib
import warnings 
  
# Settings the warnings to be ignored 
warnings.filterwarnings('ignore')

# Function
def load_model(model_name):
    return joblib.load(os.path.join(st.session_state.MODEL_PATH, f"{model_name}_gs.pkl"))

def update_current_model(model_name = "full_rf"):
    pass

def load_available_option(feature):
    # Read dictionary pkl file
    name = f"available_{feature}"
    if name in st.session_state:
        return st.session_state[name]
    else:
        with open(os.path.join(st.session_state.CAPSTONE_PATH,"Notebooks/data/available_features.pkl"), 'rb') as f:
            df = pickle.load(f)
        st.session_state[name] = sorted(df[feature])
    

def make_placeholder(feature,action = "Select"):
    return f"{action}{feature[7:]}"

def transform(data,miles = 0, fuels = []):
    # log transformation on miles
    data["log_miles"] = np.log(miles+1)\
        
    # Flatten Supported Fuel
    for fuel in fuels:
        fuel = fuel.replace(" ","")
        data[f"fuel_{fuel}"] = 1

    # Add missing columns with 0    
    data_new = data.reindex(columns=st.session_state.REQUIRE_COLUMNS, fill_value=0)
    return data_new

def predict(data):
    if st.session_state.CURRENT_MODEL is None:
        st.write("Please select model")
    else:
        return st.session_state.CURRENT_MODEL.predict(data)
        
def handle_idk(val):
    if val is None:
        return val
    if val == "I don't know":
        return None
    else:
        return val
        
def check_none(val,dtype):
    
    new_val = handle_idk(val)
    if new_val is None:
        if str == dtype:
            return ""
        elif int == dtype:
            return 0
        elif float == dtype:
            return 0.0
    else:
        return val

    
def submit_form():
    # Create dataframe
    data = pd.DataFrame({"year":check_none(st.session_state.year,int),
                            "make":check_none(st.session_state.make,str),
                            "model":check_none(st.session_state.model,str),
                            "trim":check_none(st.session_state.trim,str),
                            "body_type":check_none(st.session_state.body_type,str),
                            "vehicle_type":check_none(st.session_state.vehicle_type,str),
                            "drivetrain":check_none(st.session_state.drivetrain,str),
                            "transmission":check_none(st.session_state.transmission,str),
                            "engine_size":check_none(st.session_state.engine_size,float),
                            "engine_block":check_none(st.session_state.engine_block,str),
                            },index = ["Your Input"])
    with st.status("Loading your data...",expanded = False) as status:
        # Transform the data for model input
        data = transform(data,miles = st.session_state.miles,fuels = st.session_state.fuels)
        st.caption("Your Input:")
        time.sleep(1)
        st.dataframe(data)
        status.update(label="Data Loaded!", state="complete")

    with st.status("Predicting...",expanded = False) as status:
        # Make Predictiton
        pred = predict(data)
        time.sleep(1)
        
        # Show Prediction
        pred = pd.DataFrame(pred+1,columns=["Prediction Price Range"],index = ["Your Input"])
        st.write(pred)
        status.update(label="Prediction Result", state="complete",expanded = True)
        
    
    
    st.toast('Your Prediction is done', icon='😍')
######################

# Config
st.set_page_config(page_title='Used Car Price Range Prediction', page_icon=':bar_chart:', layout='wide')

# Title
st.title('Reveal Your Vehicle Listing Price Now!')

# State Initialization
with st.spinner('Loading...'):
    if 'CAPSTONE_PATH' not in st.session_state:
        st.session_state.CAPSTONE_PATH = Path(os.getcwd())
    if 'MODEL_PATH' not in st.session_state:
        st.session_state.MODEL_PATH = os.path.join(st.session_state.CAPSTONE_PATH,"Models")
    if 'CURRENT_MODEL' not in st.session_state:
        st.session_state.CURRENT_MODEL_NAME = "full_rf"
        st.session_state.CURRENT_MODEL = load_model(st.session_state.CURRENT_MODEL_NAME)
        st.session_state.REQUIRE_COLUMNS = st.session_state.CURRENT_MODEL.feature_names_in_ 

    if 'AVAILABLE_FUEL' not in st.session_state:
        st.session_state.AVAILABLE_FUEL = sorted(["M85","Lpg","Diesel",
                                        "Unleaded","Hydrogen",
                                        "Premium Unleaded","Biodiesel",
                                        "E85","Electric","Compressed Natural Gas"])

    if "ALL_AVAILABLE_LIST" not in st.session_state:
        with open(os.path.join(st.session_state.CAPSTONE_PATH,"Notebooks/data/available_features.pkl"), 'rb') as f:
            df = pickle.load(f)
            st.session_state["ALL_AVAILABLE_LIST"] = df
            
        st.session_state.DAFAULT_LIST = ["I don't know"]
        for col in ["make","model","trim","body_type","vehicle_type","drivetrain","transmission","engine_block"]:
            st.session_state[f"available_{col}"] = st.session_state.DAFAULT_LIST + st.session_state["ALL_AVAILABLE_LIST"][col]
            # st.write(st.session_state[f"available_{col}"]) # For debug



# Form - Row 1
c1, c2, c3 = st.columns(3)
with c1:
    display_name = "Vehicle Make"
    state_name = "make"
    # Check is in the session
    if state_name not in st.session_state:
        st.session_state[f"{state_name}"] = None      
        
    # Selection Box
    st.session_state[f"{state_name}"] = st.selectbox(
        display_name,
        st.session_state[f"available_{state_name}"],
        index=10,
        placeholder = make_placeholder(display_name),
    )
            

with c2:
    # Model
    display_name = "Vehicle Model"
    state_name = "model"
    # Check is in the session
    if state_name not in st.session_state:
        st.session_state[f"{state_name}"] = None      
        
    # Selection Box
    st.session_state[f"{state_name}"] = st.selectbox(
        display_name,
        st.session_state[f"available_{state_name}"],
        index=5,
        placeholder = make_placeholder(display_name),
    )

with c3:
    if "year_opt" not in st.session_state:
        st.session_state.year_opt = st.session_state.DAFAULT_LIST.copy()
        for i in range(2023,1980,-1):
            st.session_state.year_opt.append(i)            
    # Model Year
    display_name = "Vehicle Model Year"
    st.session_state.year = st.selectbox(
        display_name,
        st.session_state.year_opt,
        index=3,
        placeholder=make_placeholder(display_name),
    )
        
# Form - Row 2
c1, c2, c3 = st.columns(3)
with c1:
    # Trim
    display_name = "Vehicle Trim"
    state_name = "trim"
    # Check is in the session
    if state_name not in st.session_state:
        st.session_state[f"{state_name}"] = None      
        
    # Selection Box
    st.session_state[f"{state_name}"] = st.selectbox(
        display_name,
        st.session_state[f"available_{state_name}"],
        index=1,
        placeholder = make_placeholder(display_name),
    )

with c2:
    # Body Type
    display_name = "Vehicle Body Type"
    state_name = "body_type"
    # Check is in the session
    if state_name not in st.session_state:
        st.session_state[f"{state_name}"] = None      
        
    # Selection Box
    st.session_state[f"{state_name}"] = st.selectbox(
        display_name,
        st.session_state[f"available_{state_name}"],
        index=1,
        placeholder = make_placeholder(display_name),
    )

with c3:
    # Vehicle Type
    display_name = "Vehicle Type"
    state_name = "vehicle_type"
    # Check is in the session
    if state_name not in st.session_state:
        st.session_state[f"{state_name}"] = None      
        
    # Selection Box
    st.session_state[f"{state_name}"] = st.selectbox(
        display_name,
        st.session_state[f"available_{state_name}"],
        index=1,
        placeholder = make_placeholder(display_name),
    )
    
# Form - Row 3
c1, c2, c3 = st.columns(3)
with c1:
    # Drivetrain
    display_name = "Vehicle Drivetrain Type"
    state_name = "drivetrain"
    # Check is in the session
    if state_name not in st.session_state:
        st.session_state[f"{state_name}"] = None      
        
    # Selection Box
    st.session_state[f"{state_name}"] = st.selectbox(
        display_name,
        st.session_state[f"available_{state_name}"],
        index=1,
        placeholder = make_placeholder(display_name),
    )
with c2:
    # Transmission
    display_name = "Vehicle Transmission Type"
    state_name = "transmission"
    # Check is in the session
    if state_name not in st.session_state:
        st.session_state[f"{state_name}"] = None 
         
        
    # Selection Box
    st.session_state[f"{state_name}"] = st.selectbox(
        display_name,
        st.session_state[f"available_{state_name}"],
        index=1,
        placeholder = make_placeholder(display_name),
    )

with c3:
    # Fuel Support
    display_name = "Vehicle Supported Fuel"
    st.session_state.fuels = st.multiselect(
        display_name,
        st.session_state.DAFAULT_LIST + st.session_state.AVAILABLE_FUEL,
        ["Electric","Unleaded"],
        placeholder=make_placeholder(display_name),
    )
    
# Form - Row 4
c1, c2, c3 = st.columns(3)
with c1:
    # Engine Block
    display_name = "Vehicle Engine Block"
    state_name = "engine_block"
    # Check is in the session
    if state_name not in st.session_state:
        st.session_state[f"{state_name}"] = None      
        
    # Selection Box
    st.session_state[f"{state_name}"] = st.selectbox(
        display_name,
        st.session_state[f"available_{state_name}"],
        index=1,
        placeholder = make_placeholder(display_name),
    )

with c2:
    # Engine Size
    display_name = "Vehicle Engine Size"
    st.session_state.engine_size = st.number_input(
        display_name,
        placeholder=make_placeholder(display_name),
        value=3.5 if "engine_size" not in st.session_state else st.session_state.engine_size,
        step = 0.1
    )

with c3:
    # Miles Travelled (Odometer Value)
    display_name = "Vehicle Odometer Value"
    st.session_state.miles = st.number_input(
        display_name,
        placeholder=make_placeholder(display_name),
        value=100,
        step = 1
    )

c1, c2, _, _, _, _, _, _, _, _ = st.columns(10)
if st.button(label="Predict",type="primary"):
    submit_form()
# with c2:
#     if st.button(label="Reset"):
#         submit_form()
