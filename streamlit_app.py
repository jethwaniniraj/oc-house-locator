import streamlit as st
import json
import difflib

# 1. Page Configuration
st.set_page_config(page_title="OC House Locator", page_icon="🍊")

# 2. CSS: PINNED BOTTOM BAR, ORANGE GLOW, & PERFECTLY ALIGNED BUTTONS
st.markdown("""
    <style>
    .stApp {
        background-color: #FFF9F2;
        background-image:  url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Ctext x='10' y='30' style='font-size:16px; opacity: 0.9;'%3E🍊%3C/text%3E%3C/svg%3E");
        background-attachment: fixed;
    }
    
    /* FIX THE ENTIRE ROW TO THE BOTTOM & REMOVE COLUMN GAPS */
    div[data-testid="stHorizontalBlock"] {
        position: fixed;
        bottom: 50px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1000;
        width: 100%;
        max-width: 850px;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 15px !important; /* Controlled spacing between buttons and bar */
    }

    /* PRESERVED SEARCH BAR STYLE WITH GLOW */
    div[data-baseweb="input"] {
        background-color: white !important;
        border: 2px solid #FF8C00 !important;
        border-radius: 25px !important;
        height: 55px;
        box-shadow: 0 0 15px 5px rgba(255, 140, 0, 0.4) !important;
    }

    /* STYLE FOR CIRCLE FILTER BUTTONS */
    .stButton > button {
        border-radius: 50% !important;
        width: 55px !important;
        height: 55px !important;
        padding: 0px !important;
        display: flex;
        justify-content: center;
        align-items: center;
        border: 2px solid #FF8C00 !important;
        background-color: white !important;
        color: #FF8C00 !important;
        box-shadow: 0 0 10px 2px rgba(255, 140, 0, 0.3) !important;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        box-shadow: 0 0 20px 5px rgba(255, 140, 0, 0.6) !important;
        background-color: #FFF9F2 !important;
    }

    /* REMOVE DEFAULT PADDING THAT THROWS OFF ALIGNMENT */
    div[data-testid="column"] {
        display: flex;
        justify-content: center;
        width: auto !important;
        flex: none !important;
    }

    div[data-testid="InputInstructions"] { display: none !important; }
    header, footer {visibility: hidden;}
    .main .block-container { padding-bottom: 180px; }
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

# 4. BOTTOM INTERFACE: PERFECTLY CENTERED ROW
col1, col2, col3 = st.columns([1, 5, 1])

with col1:
    st.button("⚖️", key="filter_left")

with col2:
    # Width of col2 is controlled by max-width in CSS above
    search_query = st.text_input("", placeholder="Search by ZIP or City", label_visibility="collapsed")

with col3:
    st.button("🛏️", key="filter_right")

# 5. FILTER & DISPLAY LOGIC
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
                st.write(f"**Price:** ${price:,} | **City:** {house.get('city', 'N/A')}")
    else:
        st.warning("No listings found.")
