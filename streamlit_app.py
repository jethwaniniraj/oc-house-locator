import streamlit as st
import requests

st.set_page_config(page_title="OC House Locator", page_icon="🍊")
st.title("🍊 Orange County Real Estate Finder")

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
    search_query = st.text_input("Enter OC City Name", placeholder="e.g. Fullerton, Irvine")
    # API requires City and State for accuracy
    api_param = f"city={search_query}&state=CA"

# 3. Fetch and Display Data
if search_query:
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
