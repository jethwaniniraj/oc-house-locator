import streamlit as st
import requests
import difflib # 1. Added this import

# --- AESTHETICS ---
st.markdown("<style>.stApp {background: #FFF9F2;}</style>", unsafe_allow_html=True)

st.title("🍊 Orange County Home Finder")

# 2. MASTER CITY LIST (Defined once at the top)
OC_CITIES = [
    "Aliso Viejo", "Anaheim", "Brea", "Buena Park", "Costa Mesa", "Cypress", 
    "Dana Point", "Fountain Valley", "Fullerton", "Garden Grove", "Huntington Beach", 
    "Irvine", "La Habra", "La Palma", "Laguna Beach", "Laguna Hills", 
    "Laguna Niguel", "Laguna Woods", "Lake Forest", "Los Alamitos", "Mission Viejo", 
    "Newport Beach", "Orange", "Placentia", "Rancho Santa Margarita", 
    "San Clemente", "San Juan Capistrano", "Santa Ana", "Seal Beach", 
    "Stanton", "Tustin", "Villa Park", "Westminster", "Yorba Linda"
]

# 3. USER INPUT
search_query = st.text_input("Enter OC City Name (e.g., Orange)")

if search_query:
    # NORMALIZATION: Fixes "irvine" -> "Irvine"
    normalized_query = search_query.strip().title()
    
    # SPELLING CHECK: Finds the closest match
    matches = difflib.get_close_matches(normalized_query, OC_CITIES, n=1, cutoff=0.6)
    
    if matches:
        matched_city = matches[0]
        
        # If it's a typo, show a helpful message but proceed with the fix
        if matched_city != normalized_query:
            st.info(f"🔍 Searching for **{matched_city}** (Corrected from '{search_query}')")
        
        # 4. API CALL (Using the corrected city)
        API_KEY = st.secrets["RENTCAST_API_KEY"]
        url = f"https://api.rentcast.io/v1/listings/sale?city={matched_city}&state=CA&limit=10"
        
        # ... [Rest of your results display code] ...
    else:
        st.error("City not found in Orange County. Please check your spelling!")
