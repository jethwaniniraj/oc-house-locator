import streamlit as st
import requests

# Page configuration
st.set_page_config(page_title="Orange County Home Finder", page_icon="🍊")

st.title("🍊 Orange County Live House Locator")
st.write("Search real-time listings across all of Orange County.")

# 1. Securely access the API Key from Streamlit Secrets
if "RENTCAST_API_KEY" in st.secrets:
    API_KEY = st.secrets["RENTCAST_API_KEY"]
else:
    st.error("Missing RENTCAST_API_KEY. Please add it to your Streamlit Cloud Secrets.")
    st.stop()

# 2. User Input for ZIP code
zip_code = st.text_input("Enter any OC ZIP Code", placeholder="e.g., 92618, 92660, 92701")

if zip_code:
    # Ensure it's a valid 5-digit ZIP
    if len(zip_code) == 5 and zip_code.isdigit():
        # Universal formula: searches any ZIP provided in the input
        url = f"https://api.rentcast.io/v1/listings/sale?zipCode={zip_code}&limit=15"
        headers = {
            "accept": "application/json",
            "X-Api-Key": API_KEY
        }

        with st.spinner(f"Finding houses in {zip_code}..."):
            try:
                response = requests.get(url, headers=headers)
                
                if response.status_code == 200:
                    listings = response.json()
                    
                    if listings:
                        st.success(f"Found {len(listings)} active listings!")
                        
                        for house in listings:
                            # Pulling specific fields: Address, City, State
                            addr = house.get('addressLine1', 'No Address')
                            city = house.get('city', 'Unknown City')
                            state = house.get('state', 'CA')
                            price = house.get('price', 0)
                            
                            # Displaying City and State clearly in the expander title
                            with st.expander(f"🏠 {addr}, {city}, {state} - ${price:,}"):
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.write(f"**City:** {city}")
                                    st.write(f"**Bedrooms:** {house.get('bedrooms')}")
                                    st.write(f"**Bathrooms:** {house.get('bathrooms')}")
                                with col2:
                                    st.write(f"**Property Type:** {house.get('propertyType')}")
                                    st.write(f"**Living Area:** {house.get('squareFootage')} sqft")
                    else:
                        st.warning(f"No active listings found for ZIP {zip_code}.")
                else:
                    st.error(f"API Error: {response.status_code}. Please check your API key.")
            
            except Exception as e:
                st.error(f"A connection error occurred: {e}")
    else:
        st.info("Please enter a valid 5-digit ZIP code to start the search.")
