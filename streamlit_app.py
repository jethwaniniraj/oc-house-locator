import streamlit as st
import requests

st.title("🍊 Orange County Live Real Estate Search")
st.write("Enter any OC ZIP code to see real-time listings from RentCast.")

# 1. Access your API Key securely
API_KEY = st.secrets["RENTCAST_API_KEY"]

# 2. User Input for any ZIP code
zip_code = st.text_input("Enter ZIP Code", placeholder="e.g., 92660, 92705, 92801")

if zip_code:
    if len(zip_code) == 5 and zip_code.isdigit():
        # The API URL uses the variable {zip_code} to search anywhere in OC
        url = f"https://api.rentcast.io/v1/listings/sale?zipCode={zip_code}&limit=15"
        headers = {"accept": "application/json", "X-Api-Key": API_KEY}

        with st.spinner(f"Searching all active listings in {zip_code}..."):
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                listings = response.json()
                if listings:
                    st.success(f"Found {len(listings)} houses in {zip_code}!")
                    for house in listings:
                        with st.expander(f"🏠 {house.get('addressLine1')} - ${house.get('price', 0):,}"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**Bedrooms:** {house.get('bedrooms')}")
                                st.write(f"**Bathrooms:** {house.get('bathrooms')}")
                            with col2:
                                st.write(f"**Property Type:** {house.get('propertyType')}")
                                st.write(f"**Square Footage:** {house.get('squareFootage')} sqft")
                else:
                    st.warning(f"No active listings currently found for {zip_code}. Try a neighboring area like 92618.")
            else:
                st.error("API Connection failed. Please check your Secret Key.")
    else:
        st.info("Please enter a valid 5-digit ZIP code.")
