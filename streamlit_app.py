import streamlit as st
import requests
import difflib

st.set_page_config(page_title="OC House Locator", page_icon="🍊")

# --- AESTHETIC FIX ---
st.markdown("""<style>.stApp { background: #FFF9F2; } p, h1, h2, h3, label { color: #31333F !important; }</style>""", unsafe_allow_html=True)

st.title("🍊 OC Real Estate Finder")

OC_CITIES = ["Irvine", "Anaheim", "Newport Beach", "Santa Ana", "Huntington Beach"] # Add all 34 OC cities here

# --- API SECURE LOAD ---
API_KEY = st.secrets.get("RENTCAST_API_KEY", None)

search_query = st.text_input("Enter OC City Name", placeholder="e.g. Ivrine")

if search_query:
    normalized = search_query.strip().title()
    matches = difflib.get_close_matches(normalized, OC_CITIES, n=1, cutoff=0.6)
    city_to_search = matches[0] if matches else normalized
    
    if matches and matches[0] != normalized:
        st.info(f"🔍 Did you mean: **{matched_city}**?")

    if not API_KEY:
        st.error("🚨 API Key missing! Please add RENTCAST_API_KEY to your Streamlit Secrets.")
    else:
        url = f"https://api.rentcast.io/v1/listings/sale?city={city_to_search}&state=CA&limit=10"
        headers = {"X-Api-Key": API_KEY}
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            listings = response.json()
            if listings:
                for house in listings:
                    with st.expander(f"🏠 {house.get('addressLine1')} - ${house.get('price', 0):,}"):
                        st.write(f"**City:** {house.get('city')}")
                        st.write(f"**Beds/Baths:** {house.get('bedrooms')}/{house.get('bathrooms')}")
            else:
                st.warning("No listings found.")
        elif response.status_code == 401:
            st.error("🔑 API Error 401: Your RentCast API key is invalid or inactive.")
        else:
            st.error(f"Error {response.status_code}: Something went wrong.")
