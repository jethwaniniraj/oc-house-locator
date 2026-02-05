import streamlit as st
import requests
import difflib

# 1. Page Config & Aesthetic (Subtle Orange Tint)
st.set_page_config(page_title="OC House Locator", page_icon="🍊")
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #FFF9F2 0%, #FFFFFF 100%);
    }
    </style>
    """, 
    unsafe_allow_html=True
)

st.title("🍊 Orange County Real Estate Finder")

# Master list of Orange County cities for spell-check
OC_CITIES = [
    "Aliso Viejo", "Anaheim", "Brea", "Buena Park", "Costa Mesa", "Cypress", 
    "Dana Point", "Fountain Valley", "Fullerton", "Garden Grove", "Huntington Beach", 
    "Irvine", "La Habra", "La Palma", "Laguna Beach", "Laguna Hills", 
    "Laguna Niguel", "Laguna Woods", "Lake Forest", "Los Alamitos", "Mission Viejo", 
    "Newport Beach", "Orange", "Placentia", "Rancho Santa Margarita", 
    "San Clemente", "San Juan Capistrano", "Santa Ana", "Seal Beach", 
    "Stanton", "Tustin", "Villa Park", "Westminster", "Yorba Linda"
]

# 2. API Key Check
if "RENTCAST_API_KEY" in st.secrets:
    API_KEY = st.secrets["RENTCAST_API_KEY"]
else:
    # Use a dummy key if you've deactivated yours for testing
    API_KEY = "DEMO_MODE"
    st.info("🛠️ Demo Mode: API key is deactivated. Please add a valid key to Secrets for live data.")

# 3. Search Options
search_type = st.radio("Search by:", ["ZIP Code", "City Name"])
api_param = "" # Initializing empty to prevent errors

if search_type == "ZIP Code":
    search_query = st.text_input("Enter 5-digit ZIP", placeholder="e.g. 92618")
    if search_query:
        api_param = f"zipCode={search_query}"
else:
    search_query = st.text_input("Enter OC City Name", placeholder="e.g. Ivrine")
    if search_query:
        # Normalize and Check Spelling
        normalized = search_query.strip().title()
        matches = difflib.get_close_matches(normalized, OC_CITIES, n=1, cutoff=0.6)
        
        if matches:
            matched_city = matches[0]
            if matched_city != normalized:
                st.info(f"🔍 Did you mean: **{matched_city}**?")
            api_param = f"city={matched_city}&state=CA"
        else:
            api_param = f"city={normalized}&state=CA"

# 4. Fetch and Display Data
if search_query and api_param and API_KEY != "DEMO_MODE":
    url = f"https://api.rentcast.io/v1/listings/sale?{api_param}&limit=15"
    headers = {"accept": "application/json", "X-Api-Key": API_KEY}

    with st.spinner(f"Searching {search_query}..."):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            listings = response.json()
            if listings:
                st.success(f"Found {len(listings)} houses!")
                for house in listings:
                    addr = house.get('addressLine1')
                    city = house.get('city')
                    price = house.get('price', 0)
                    with st.expander(f"🏠 {addr}, {city} - ${price:,}"):
                        st.write(f"**Price:** ${price:,}")
                        st.write(f"**Beds/Baths:** {house.get('bedrooms')} / {house.get('bathrooms')}")
                        st.write(f"**Type:** {house.get('propertyType')}")
            else:
                st.warning("No listings found. Try a different search.")
        else:
            st.error(f"API Error: {response.status_code}")
