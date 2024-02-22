# Libraries
import streamlit as st

import layout
import bg


# Config
layout.init_page_title()
st.set_page_config(page_title=st.session_state["PAGE_TITLE"], page_icon=':bar_chart:', layout='wide')
layout.sidebar()

# Background
bg.mainpage_bg("https://res.cloudinary.com/dnzjbmzag/image/upload/v1692679078/SubtlePastel1.jpg")

# Vehicle Brand Logo
layout.brand_logo_bar()

# Title
st.title('Used Car Price Range Prediction - Project Overview')

# Links
layout.project_info_link()

st.subheader('Introduction 📋')
st.write(
    """
    The North American used car market is a boundless and dynamic landscape, 
    characterized by a huge industry of vehicle makes, models, and relentnessly 
    evolving market dynamics. In 2022, the used car market recorded 38.6 millions 
    sales volume in United States ([Source: statista](#https://www.statista.com/statistics/183713/value-of-us-passenger-cas-sales-and-leases-since-1990/)).

    Buyers and sellers often grapple with the challenge of accurately determining 
    the fair market value of a used car, leading to potential disparities in pricing, 
    suboptimal transactions, and general market inefficiencies. The dilemma of accurately 
    pricing a used vehicles remains a persistent enigma for years. According to [canadadrives](#https://www.canadadrives.ca/blog/car-guide/selling-a-used-car-privately), 
    it takes up to 4 weeks to sell a used car. For both sellers and buyers, this dilemma often 
    transforms into uncertainty, frustration, and even missed opportunities.
    """
)



st.subheader('Story Behind 📔')
st.write(
    """
    My friend, Jason, who lived in Vancouver for 2 years, wanted to get a car recently. 
    He did not have enough budget to get a new car. Therefore, he decided to buy a second-hand vehicle. 
    He went to several dealers for inquiries. However, all dealer agents tried to persuade him to pay at
    a higher price to get a better car. At last, he got his car from craigslist directly from the previous
    owner within his budget and his requirement. 
    """
)

st.subheader('Problem Statement 😩')
st.write(
    """
    The problem we try to address in this project remains focus on the need for accurate and transparent pricing 
    in the North American used car market. The wide variety of vehicles, including numerous makes, models, years, 
    mileage, drivetrains, transmission and geographic locations, contributes to the complexity of this problem.

    - Buyers often find it difficult to assess whether a listed car's price is reasonable, leading to price 
    uncertainty and the potential for overpayment.
    - Sellers may often struggle to set competitive (higher) and attractive (lower) listing prices, potentially
    resulting in unsuccessful sales or missed opportunity.
    """
)

st.subheader('Objectives 🎯')
st.write(
    """
    1️⃣ Develop advanced predictive models that estimates the price range for used cars.
    - The primary objective is the development of machine learning / deep learning models 
    capable of accurately predicting price ranges for a used car, which will assist both 
    sellers and buyers make informed pricing decisions.

    2️⃣ Improve market efficiency by enhancing the transparency and fairness in the used car market.
    - One of the objectives is to the improve the market efficiency. By providing AI price range 
    predictions, it reduces information asymmetry between buyers and sellers ,which also helps 
    users understand the fair market value of the used vehicle.

    3️⃣ Faciliate decision-making process for both sellers and buyers with informed pricing prediction.
    - Sellers can benefit by setting competitive and fair prices, which can lead to faster sales. 
    Buyers can make more informed and data-driven decisions to ensure they are not overpaying for a used vehicle.

    4️⃣ Provide a user-friendly interface (simple website) for easy access to price range predictions.
    - The project includes the development of a simple and interactive user interface, making it accessible 
    to a wide range of users. This interface allows sellers and buyers to input their vehicle details easily
    and obtain price range predictions quickly and conveniently.
    """
)
