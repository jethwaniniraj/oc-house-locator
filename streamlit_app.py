import streamlit as st
import requests

st.title("Orange County House Locator")

# Get your API Key from Streamlit Secrets (Set this up in Step 2)
API_KEY = st.secrets["RENTCAST_API_KEY"]

zip_code = st.text_input("Enter ZIP (e.g., 92620)")

if zip_code:
    # This URL asks the RentCast API for real listings in the entered ZIP
    url = f"https://api.rentcast.io/v1/listings/sale?zipCode={zip_code}&limit=10"
    headers = {"accept": "application/json", "X-Api-Key": API_KEY}

    with st.spinner(f"Fetching real-time data for {zip_code}..."):
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            listings = response.json()
            if listings:
                st.subheader(f"Live Houses in {zip_code}")
                for house in listings:
                    st.markdown(f"### ${house.get('price', 0):,}")
                    st.write(f"📍 {house.get('addressLine1')}")
                    st.write(f"🛌 {house.get('bedrooms')} Bed | 🛀 {house.get('bathrooms')} Bath")
                    st.divider()
            else:
                st.warning(f"No active listings found in RentCast for {zip_code}.")
        else:
            st.error("Could not connect to the API. Check your API Key in Secrets.")
