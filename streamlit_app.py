import streamlit as st
import json
import difflib

# 1. Page Configuration
st.set_page_config(page_title="OC House Locator", page_icon="🍊")

# Custom CSS for the "Bottom Search" minimalist Look
st.markdown("""
    <style>
    /* Vibrant Orange Background Pattern */
    .stApp {
        background-color: #FFF9F2;
        background-image:  url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Ctext x='10' y='30' style='font-size:16px; opacity: 0.9;'%3E🍊%3C/text%3E%3C/svg%3E");
        background-attachment: fixed;
    }
    
    /* Create a fixed container at the bottom for the search bar */
    div[data-testid="stVerticalBlock"] > div:has(input) {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1000;
        width: 90%;
        max-width: 700px;
        background-color: rgba(255, 255, 255, 0.9);
        padding: 10px;
        border-radius: 35px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 2px solid #FFCC80;
    }

    /* Style the inner Input field to match */
    div[data-baseweb="input"] {
        background-color: transparent !important;
        border: none !important;
        height: 50px;
    }
    
    /* Hide default Streamlit clutter */
    header, footer {visibility: hidden;}
    
    /* Adjust result spacing so they don't get covered by the bottom bar */
    .main .block-container {
        padding-bottom: 120px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA LOADING (Pulling from your local JSON)
@st.cache_data
def load_and_index_data():
    try:
        with open('data.json', 'r') as f:
            raw_data = json.load(f)
        
        flattened_list = []
        city_to_listings = {}
        
        for zip_key, listings in raw_data.items():
            for house in listings:
                house['zipCode'] = zip_key
                flattened_list.append(house)
                city_name = house.get('city', 'Unknown').strip().title()
                if city_name not in city_to_listings:
                    city_to_listings[city_name] = []
                city_to_listings[city_name].append(house)
                
        return raw_data, city_to_listings, list(city_to_listings.keys())
    except FileNotFoundError:
        return {}, {}, []

DATA_BY_ZIP, DATA_BY_CITY, KNOWN_CITIES = load_and_index_data()

# 3. Search Logic (Invisible Label for Minimalist Look)
search_query = st.text_input("label_hidden", placeholder="Search OC Listings by ZIP or City...", label_visibility="collapsed")

# 4. Filter and Display Results
results = []
if search_query:
