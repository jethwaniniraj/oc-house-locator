import streamlit as st
import requests
import difflib  # Built-in library for spelling/text comparison

st.set_page_config(page_title="OC House Locator", page_icon="🍊")
st.title("🍊 Orange County Home Finder")

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

# 1. API Key Check
if "RENTCAST_API_KEY" in st.secrets:
    API_KEY = st.secrets["RENTCAST_API_KEY"]
else:
    st.error("Please add RENTCAST_API_KEY to your Secrets.")
    st.stop()

# 2. Search Options: ZIP or City
search_type = st.radio("Search by:", ["ZIP Code", "City Name"])

if search_type == "ZIP Code":
    search_query = st.text_input("Enter 5-digit ZIP", placeholder="e.g. 92618")
    api_param = f"zipCode={search_query}"
else:
    search_query = st.text_input("Enter OC City Name", placeholder="e.g. Orange")
    
    # --- Spelling Correction Feature ---
    if search_query:
        # Normalize input (e.g., "ivrine" -> "Ivrine")
        normalized_input = search_query.strip().title()
        
        # Find the closest match in the OC cities list
        matches = difflib.get_close_matches(normalized_input, OC_CITIES, n=1, cutoff=0.6)
        
        if matches:
            matched_city = matches[0]
            # If the match isn't exactly what they typed, suggest the correct one
            if matched_city != normalized_input:
                st.info(f"🔍 Did you mean: **{matched_city}**?")
                # Update the parameter to use the correctly spelled city
                api_param = f"city={matched_city}&state=CA"
            else:
                api_param = f"city={normalized_input}&state=CA"
        else:
            api_param = f"city={search_query}&state=CA"
    else:
        api_param = ""

# 3. Fetch and Display Data
if search_query and api_param:
    url = f"https://api.rentcast.io/v1/listings/sale?{api_param}&limit=15"
    headers = {"accept": "application/json", "X-Api-Key": API_KEY}

    with st.spinner(f"Searching listings in {search_query}..."):
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            listings = response.json()
            if listings:
                st.success(f"Showing {len(listings)} houses in {search_query}")
                for house in listings:
                    addr = house.get('addressLine1')
                    city = house.get('city')
                    price = house.get('price', 0)
                    with st.expander(f"🏠 {addr}, {city} - ${price:,}"):
                        st.write(f"**Price:** ${price:,}")
                        st.write(f"**Beds/Baths:** {house.get('bedrooms')} / {house.get('bathrooms')}")
                        st.write(f"**Property Type:** {house.get('propertyType')}")
            else:
                st.warning("No listings found. Try a different city or ZIP.")
        else:
            st.error(f"API Error: {response.status_code}. Check your API Key.")
