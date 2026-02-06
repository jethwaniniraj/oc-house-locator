import streamlit as st
import json
import difflib

# 1. Page Configuration
st.set_page_config(page_title="OC House Locator", page_icon="🍊")

# 2. CSS: EXACT STYLE, PINNED TO BOTTOM
st.markdown("""
    <style>
    /* Your Vibrant Orange Background */
    .stApp {
        background-color: #FFF9F2;
        background-image:  url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Ctext x='10' y='30' style='font-size:16px; opacity: 0.9;'%3E🍊%3C/text%3E%3C/svg%3E");
        background-attachment: fixed;
    }
    
    /* PINNING THE SEARCH BAR TO THE BOTTOM */
    /* This targets the container holding the input and moves it down */
    div[data-testid="stVerticalBlock"] > div:has(input) {
        position: fixed;
        bottom: 50px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1000;
        width: 90%;
        max-width: 600px;
    }

    /* KEEPING YOUR EXACT SEARCH BAR STYLE */
    div[data-baseweb="input"] {
        background-color: white !important;
        border: 2px solid #FFCC80 !important;
        border-radius: 25px !important;
        height: 55px;
    }
    
    header, footer {visibility: hidden;}
    
    /* Ensure results don't get covered by the bottom bar */
    .main .block-container { padding-bottom: 150px; }
    </style>
    """, unsafe_allow_html=True)

# 3. DATA LOADING
@st.cache_data
def load_and_index_data():
    try:
        with open('data.json', 'r') as f:
            raw_data = json.load(f)
        
        city_to_listings = {}
        for zip_key, listings in raw_data.items():
            for house in listings:
                city_name = house.get('city', 'Unknown').strip().title()
                if city_name not in city_to_listings:
                    city_to_listings[city_name] = []
                city_to_listings[city_name].append(house)
        return raw_data, city_to_listings, list(city_to_listings.keys())
    except FileNotFoundError:
        return {}, {}, []

DATA_BY_ZIP, DATA_BY_CITY, KNOWN_CITIES = load_and_index_data()

# 4. THE SEARCH BAR (Label hidden for clean look)
search_query = st.text_input("", placeholder="Search by ZIP Code or City")

# 5. FILTER & DISPLAY (INDENTATION FIXED)
if search_query:
    query = search_query.strip().title()
    results = []
    
    if query in DATA_BY_ZIP:
        results = DATA_BY_ZIP[query]
    else:
        matches = difflib.get_close_matches(query, KNOWN_CITIES, n=1, cutoff=0.6)
        if matches:
            results = DATA_BY_CITY.get(matches[0], [])

    if results:
        for house in results:
            addr = house.get('addressLine1', 'Listing')
            price = house.get('price', 0)
            with st.expander(f"🏠 {addr} - ${price:,}"):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**Price:** ${price:,}")
                    st.write(f"**Beds:** {house.get('bedrooms', 'N/A')}")
                with c2:
                    st.write(f"**Baths:** {house.get('bathrooms', 'N/A')}")
                    st.write(f"**City:** {house.get('city', 'N/A')}")
    else:
        st.warning("No listings found in the saved data.")
