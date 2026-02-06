import streamlit as st
import json
import difflib

# 1. Page Configuration (Preserving your vibrant style)
st.set_page_config(page_title="OC House Locator", page_icon="🍊")

st.markdown("""
    <style>
    .stApp {
        background-color: #FFF9F2;
        background-image:  url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Ctext x='10' y='30' style='font-size:16px; opacity: 0.9;'%3E🍊%3C/text%3E%3C/svg%3E");
        background-attachment: fixed;
    }
    h1, h2, h3, p, label, .stText { color: #31333F !important; text-shadow: 1px 1px 2px rgba(255,255,255,0.8); }
    div[data-baseweb="input"] { background-color: white !important; border: 2px solid #FFCC80 !important; }
    .stExpander { background-color: white !important; border-radius: 10px; border: 1px solid #FFCC80; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍊 Orange County Home Finder")

# 2. LOAD DATA & FLATTEN FOR CITY SEARCH
@st.cache_data
def load_and_index_data():
    try:
        with open('data.json', 'r') as f:
            raw_data = json.load(f)
        
        # We need to transform the "ZIP-grouped" data into a searchable list
        flattened_list = []
        city_to_listings = {}
        
        for zip_key, listings in raw_data.items():
            for house in listings:
                # Add the ZIP back to the house object for display
                house['zipCode'] = zip_key
                flattened_list.append(house)
                
                # Group by city for fast lookup
                city_name = house.get('city', 'Unknown').strip().title()
                if city_name not in city_to_listings:
                    city_to_listings[city_name] = []
                city_to_listings[city_name].append(house)
                
        return raw_data, city_to_listings, list(city_to_listings.keys())
    except FileNotFoundError:
        return {}, {}, []

DATA_BY_ZIP, DATA_BY_CITY, KNOWN_CITIES = load_and_index_data()

# 3. Search Interface
search_mode = st.radio("Search by:", ["ZIP Code", "City Name"])
search_input = st.text_input(f"Enter {search_mode}")

# 4. Search Logic
results = []
if search_input:
    if search_mode == "ZIP Code":
        # Direct lookup by the ZIP key in your JSON
        results = DATA_BY_ZIP.get(search_input, [])
    else:
        # Autocorrect city names against the data you actually have
        matches = difflib.get_close_matches(search_input.title(), KNOWN_CITIES, n=1, cutoff=0.6)
        if matches:
            if matches[0] != search_input.title():
                st.info(f"🔍 Showing results for: **{matches[0]}**")
            results = DATA_BY_CITY.get(matches[0], [])

# 5. Display Results (Using the API fields from your JSON)
if results:
    st.success(f"Showing {len(results)} active listings found in our database.")
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
elif search_input:
    st.warning(f"No listings found in the saved data for that {search_mode.lower()}.")
