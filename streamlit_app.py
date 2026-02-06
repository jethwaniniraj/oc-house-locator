import streamlit as st
import difflib

# 1. Page Configuration & Aesthetic Fix
st.set_page_config(page_title="OC House Locator", page_icon="🍊")

# Custom CSS for the Orange Pattern Background
st.markdown("""
    <style>
    .stApp {
        background-color: #FFF9F2;
        /* Creating a subtle repeating pattern of small oranges */
        background-image:  url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Ctext x='10' y='30' style='font-size:12px; opacity: 0.1;'%3E🍊%3C/text%3E%3C/text%3E%3C/svg%3E");
        background-attachment: fixed;
    }
    
    /* Ensuring text is high-contrast and readable over the pattern */
    h1, h2, h3, p, label, .stText {
        color: #31333F !important;
        font-weight: 500;
    }

    /* Making the search containers solid white so they pop against the background */
    div[data-baseweb="input"] {
        background-color: white !important;
        border: 1px solid #FFCC80 !important;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Styling the success/info boxes to match the theme */
    .stAlert {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid #FFCC80 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🍊 Orange County Home Finder")

# 2. Database (Professional Data)
LISTINGS = [
    {"address": "29 Small Grove", "city": "Irvine", "zip": "92618", "price": 4080000, "beds": 5, "baths": 6, "type": "Single Family", "sqft": 4209},
    {"address": "136 Pineview", "city": "Irvine", "zip": "92620", "price": 899000, "beds": 2, "baths": 3, "type": "Condo", "sqft": 1366},
    {"address": "412 Heliotrope Ave", "city": "Corona Del Mar", "zip": "92625", "price": 8495000, "beds": 4, "baths": 6, "type": "Luxury Villa", "sqft": 3120},
    {"address": "821 S Fairmont Way", "city": "Orange", "zip": "92869", "price": 1374999, "beds": 4,
