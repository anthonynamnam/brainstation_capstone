# Libraries
import os
import time
import datetime

import warnings 
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

import pickle
import joblib

from PIL import Image

# custom function
import bg
import layout



# Settings the warnings to be ignored 
warnings.filterwarnings('ignore')

UNKNOWN_NAME = "I don't know / Others"
st.session_state.img_this_make = ""
st.session_state.img_this_model = ""

def make_placeholder(feature,action = "Select"):
    return f"{action}{feature[7:].split('(')[0]}"


def load_available_option(feature):
    # Read dictionary pkl file
    name = f"available_{feature}"
    if name in st.session_state:
        return st.session_state[name]
    else:
        with open("../Models/available_features.pkl", 'rb') as f:
            df = pickle.load(f)
        st.session_state[name] = sorted(df[feature])
    
    
def load_model(model_name):
    return joblib.load(f"../Models/{model_name}_gs.pkl")

def update_current_model(selected_model_name):
    if selected_model_name == "":
        st.warning('Please choose a model to proceed.', icon="⚠️")
    if st.session_state.CURRENT_MODEL_NAME == st.session_state.model_option[selected_model_name]:
        pass
    else:
        with st.spinner("Loading new model..."):
            st.session_state.CURRENT_MODEL_NAME = st.session_state.model_option[selected_model_name]
            st.session_state.CURRENT_MODEL = load_model(st.session_state.CURRENT_MODEL_NAME)
            st.session_state.REQUIRE_COLUMNS = st.session_state.CURRENT_MODEL.feature_names_in_ 
            time.sleep(1)
            st.toast(f"The Current Model is {st.session_state.selected_model}!", icon='✅')

def transform(data,miles = 0, fuels = []):
    
    # log transformation on miles
    if type(miles) == str:
        data["log_miles"] = miles
    else:
        data["log_miles"] = np.log(miles+1)
        
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
    if val == UNKNOWN_NAME:
        return None
    else:
        return val
        
def check_none(val,return_val_if_none = None):
    
    new_val = handle_idk(val)
    if new_val is None:
        if return_val_if_none is not None:
            return return_val_if_none
    else:
        return val

def convert_price_range(n:int):
    assert 1 <= n and n <=5
    if n == 1:
        return "< USD 15,000"
    elif n == 2:
        return "USD 15,000 - USD 29,999"
    elif n == 3:
        return "USD 30,000 - USD 44,999"
    elif n == 4:
        return "USD 45,000 - USD 59,999"
    elif n == 5:
        return "> USD 60,000"

def submit_form():
    # Input Validation
    if check_none(st.session_state.make) is None :
        st.error("The field 'Make' cannot be empty.", icon="🚨")
        return 

    
    # Create dataframe
    actual_data = pd.DataFrame({"year":check_none(st.session_state.year,datetime.datetime.now().year-5),
                            "make":check_none(st.session_state.make),
                            "model":check_none(st.session_state.model,return_val_if_none = "Not Provided"),
                            "trim":check_none(st.session_state.trim,return_val_if_none = "Not Provided"),
                            "body_type":check_none(st.session_state.body_type,return_val_if_none = "Not Provided"),
                            "vehicle_type":check_none(st.session_state.vehicle_type,"Truck"),
                            "drivetrain":check_none(st.session_state.drivetrain,"4WD"),
                            "transmission":check_none(st.session_state.transmission,"Automatic"),
                            "engine_size":check_none(st.session_state.engine_size,1.5),
                            "engine_block":check_none(st.session_state.engine_block,"I"),
                            },index = ["Your Vehicle"])
    
    show_data = pd.DataFrame({"year":check_none(st.session_state.year,""),
                            "make":check_none(st.session_state.make),
                            "model":check_none(st.session_state.model,UNKNOWN_NAME),
                            "trim":check_none(st.session_state.trim,UNKNOWN_NAME),
                            "body_type":check_none(st.session_state.body_type,UNKNOWN_NAME),
                            "vehicle_type":check_none(st.session_state.vehicle_type,UNKNOWN_NAME),
                            "drivetrain":check_none(st.session_state.drivetrain,UNKNOWN_NAME),
                            "transmission":check_none(st.session_state.transmission,UNKNOWN_NAME),
                            "engine_size":check_none(st.session_state.engine_size,UNKNOWN_NAME),
                            "engine_block":check_none(st.session_state.engine_block,UNKNOWN_NAME),
                            },index = ["Your Vehicle"])
    with st.status("Loading your data...",expanded = False) as status:
        # Transform the data for model input
        actual_data = transform(actual_data,miles = check_none(st.session_state.miles,100000),fuels = st.session_state.fuels)
        show_data = transform(show_data,miles = check_none(st.session_state.miles,UNKNOWN_NAME),fuels = st.session_state.fuels)
        st.caption("Your Input:")
        time.sleep(0.5)
        st.dataframe(show_data)
        # st.caption("Your actual Input:")
        # time.sleep(0.5)
        # st.dataframe(actual_data)
        status.update(label="Data Loaded!", state="complete")

    with st.status("Predicting...",expanded = False) as status:
        # Make Predictiton
        pred = predict(actual_data)
        time.sleep(1)
        
        # Show Prediction
        pred = pd.DataFrame(convert_price_range(pred+1),columns=["Suggested Price Range"],index = ["Your Vehicle"])
        st.write(pred)
        status.update(label="Prediction Result", state="complete",expanded = True)
        if st.session_state.year is None or st.session_state.make is None or st.session_state.model is None or\
            st.session_state.trim is None or st.session_state.body_type is None or st.session_state.vehicle_type is None or \
                st.session_state.drivetrain is None or st.session_state.transmission is None or st.session_state.engine_size is None or \
                    st.session_state.engine_block is None or st.session_state.miles is None:
            st.warning("Any missing input will lower prediction accuracy. You are recommended to fill in all the information.")
    
    st.toast('Your Prediction is done', icon='😍')
    
######################

# Config
st.set_page_config(page_title='Used Car Price Range Prediction', page_icon=':bar_chart:', layout='wide')

# State Initialization
# with st.spinner('Loading Page...'):
#     if 'CAPSTONE_PATH' not in st.session_state:
#         st.session_state.CAPSTONE_PATH = Path(os.getcwd())
#     if 'MODEL_PATH' not in st.session_state:
#         st.session_state.MODEL_PATH = os.path.join(st.session_state.CAPSTONE_PATH,"Models")
with st.spinner('Loading Model...'):
    if 'CURRENT_MODEL' not in st.session_state:
        st.session_state.model_option = {"Random Forest":"full_rf",
                                         "Random Forest - with 10% of Data":"rf",
                                         "AdaBoost":"full_abc"
                                         }
        st.session_state.selected_model = list(st.session_state.model_option.keys())[0]
        
        st.session_state.CURRENT_MODEL_NAME = st.session_state.model_option[st.session_state.selected_model]
        st.session_state.CURRENT_MODEL = load_model(st.session_state.CURRENT_MODEL_NAME)
        st.session_state.REQUIRE_COLUMNS = st.session_state.CURRENT_MODEL.feature_names_in_ 

with st.spinner('Loading Variables...'):
    if 'AVAILABLE_FUEL' not in st.session_state:
        st.session_state.AVAILABLE_FUEL = sorted(["M85","Lpg","Diesel",
                                        "Unleaded","Hydrogen",
                                        "Premium Unleaded","Biodiesel",
                                        "E85","Electric","Compressed Natural Gas"])

    if "ALL_AVAILABLE_LIST" not in st.session_state:
        with open("../Models/available_features.pkl", 'rb') as f:
            df = pickle.load(f)
            st.session_state["ALL_AVAILABLE_LIST"] = df
            
        st.session_state.DAFAULT_LIST = [UNKNOWN_NAME]
        for col in ["make","model","trim","body_type","vehicle_type","drivetrain","transmission","engine_block"]:
            st.session_state[f"available_{col}"] = sorted(st.session_state["ALL_AVAILABLE_LIST"][col])
            
    if "AVAILABLE_MAKE_MODEL_TRIM" not in st.session_state:
        st.session_state.AVAILABLE_MAKE_MODEL_TRIM = pd.read_csv("../Models/make_model_trim_body.csv")


# Background
bg.mainpage_bg("https://res.cloudinary.com/dnzjbmzag/image/upload/v1692679078/SubtlePastel1.jpg")

st.warning("** This feature is just a prototype. Use wisely.")

# Title and Model option
c1, c2 = st.columns([0.7,0.3])
with c1:
    # Title
    st.title('Reveal Your Vehicle Suggested Listing Price Now!')
with c2:
    selected_model = st.selectbox("Selected Model",
                 st.session_state.model_option.keys(),
                 index=list(st.session_state.model_option.keys()).index(st.session_state.selected_model),
                 placeholder="Choose a model")
    update_current_model(selected_model)


    
# Form - Row 1
c1, c2 = st.columns([0.6,0.4])
with c1:
    # Row 1 beside Image
    cc1, cc2 = st.columns([0.5,0.5])
    with cc1:
        display_name = "Vehicle Make (*Mandatory)"
        state_name = "make"

        # Selection Box
        make = st.selectbox(
            display_name,
            st.session_state[f"available_{state_name}"],
            index=None if f"last_{state_name}_ind" not in st.session_state else st.session_state[f"last_{state_name}_ind"],
            placeholder = make_placeholder(display_name),
            key=state_name,
        )
        
        

    with cc2:
        # Model
        display_name = "Vehicle Model"
        state_name = "model"   
            
        # Selection Box
        model = st.selectbox(
            display_name,
            st.session_state.DAFAULT_LIST + \
                list(st.session_state.AVAILABLE_MAKE_MODEL_TRIM.loc[\
                    (st.session_state.AVAILABLE_MAKE_MODEL_TRIM["make"] == st.session_state.make),state_name].unique()) \
                        if st.session_state.make != st.session_state.DAFAULT_LIST[0] else \
                            st.session_state[f"available_{state_name}"] ,
            index=None,
            placeholder = make_placeholder(display_name),
            disabled= make is None,
            key=state_name
        )
        
    # Row 2 beside Image
    cc3, cc4 = st.columns([0.5,0.5])
    with cc3:
        # Trim
        display_name = "Vehicle Trim"
        state_name = "trim"
            
        # Selection Box
        trim = st.selectbox(
            display_name,
            st.session_state.DAFAULT_LIST + \
                list(st.session_state.AVAILABLE_MAKE_MODEL_TRIM.loc[\
                    (st.session_state.AVAILABLE_MAKE_MODEL_TRIM["make"] == st.session_state.make)&\
                        (st.session_state.AVAILABLE_MAKE_MODEL_TRIM["model"] == st.session_state.model),state_name].unique()) \
                            if st.session_state.make != st.session_state.DAFAULT_LIST[0] else \
                                st.session_state[f"available_{state_name}"] ,
            index=None,
            placeholder = make_placeholder(display_name),
            disabled= make is None or model is None,
            key=state_name
        )

    with cc4:           
        # Model Year
        display_name = "Vehicle Model Year"
        state_name = "year"
        
        st.session_state[f"available_{state_name}"] = st.session_state.DAFAULT_LIST.copy()
        for i in range(2023,1980,-1):
            st.session_state[f"available_{state_name}"].append(i) 
        
        st.selectbox(
            display_name,
            st.session_state[f"available_{state_name}"],
            index=None,
            placeholder=make_placeholder(display_name),
            disabled= make is None,
            key=state_name
        )
        
    # Row 3 beside Image
    cc5, cc6 = st.columns([0.5,0.5])
    with cc5:
        # Body Type
        display_name = "Vehicle Body Type"
        state_name = "body_type"    
            
        # Selection Box
        st.selectbox(
            display_name,
            st.session_state.DAFAULT_LIST + \
                list(st.session_state.AVAILABLE_MAKE_MODEL_TRIM.loc[\
                    (st.session_state.AVAILABLE_MAKE_MODEL_TRIM["make"] == st.session_state.make)&\
                        (st.session_state.AVAILABLE_MAKE_MODEL_TRIM["model"] == st.session_state.model),state_name].unique()) \
                            if st.session_state.make != st.session_state.DAFAULT_LIST[0] else \
                                st.session_state[f"available_{state_name}"] ,
            index=None,
            placeholder = make_placeholder(display_name),
            key=state_name
        )

    with cc6:
        # Vehicle Type
        display_name = "Vehicle Type"
        state_name = "vehicle_type"
            
        # Selection Box
        st.selectbox(
            display_name,
            st.session_state[f"available_{state_name}"],
            index=None,
            placeholder = make_placeholder(display_name),
            key=state_name
        )   
        

   
with c2:
    try:
        path = f"./images/{make.lower().replace(' ','_')}{f'_{model.lower()}' if model is not None else ''}.png"
        time.sleep(0.5)
        st.image(Image.open(path),caption = f"Your {make}{f' - {model}' if model is not None else ''}")
    except:
        # st.write("Image Not Available")
        pass

    
# Form - Row 4
c1, c2, c3 = st.columns([0.3,0.3,0.4])
with c1:
    # Drivetrain
    display_name = "Vehicle Drivetrain Type"
    state_name = "drivetrain"
        
    # Selection Box
    st.selectbox(
        display_name,
        st.session_state[f"available_{state_name}"],
        index=None,
        placeholder = make_placeholder(display_name),
        key=state_name
    )
with c2:
    # Transmission
    display_name = "Vehicle Transmission Type"
    state_name = "transmission"            
        
    # Selection Box
    st.selectbox(
        display_name,
        st.session_state[f"available_{state_name}"],
        index=None,
        placeholder = make_placeholder(display_name),
        key=state_name
    )

with c3:
    # Fuel Support
    display_name = "Vehicle Supported Fuel"
    st.multiselect(
        display_name,
        st.session_state.AVAILABLE_FUEL,
        [],
        placeholder=make_placeholder(display_name),
        key="fuels"
    )
    
# Form - Row 5
c1, c2, c3 = st.columns([0.3,0.3,0.4])
with c1:
    # Engine Block
    display_name = "Vehicle Engine Block"
    state_name = "engine_block"    
        
    # Selection Box
    st.selectbox(
        display_name,
        st.session_state[f"available_{state_name}"],
        index=None,
        placeholder = make_placeholder(display_name),
        key=state_name
    )

with c2:
    # Engine Size
    display_name = "Vehicle Engine Size"
    st.number_input(
        display_name,
        placeholder=make_placeholder(display_name),
        value = None,
        step = 0.1,
        key="engine_size"
    )

with c3:
    # Miles Travelled (Odometer Value)
    display_name = "Vehicle Odometer Value"
    st.number_input(
        display_name,
        placeholder=make_placeholder(display_name),
        value = None,
        step = 1,
        key="miles"
    )




c1, c2, c3, = st.columns([0.1,0.1,0.8])
with c1:
    submit = st.button(f"Predict",type="primary")
# with c2:
#     reset = st.button(f"Clear")
    
if submit:
    submit_form()
# if reset:
#     pass
        
# layout.footer()
    
