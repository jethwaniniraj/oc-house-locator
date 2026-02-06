import streamlit as st
import json
import difflib

# 1. Page Configuration (Vibrant Oranges preserved)
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

# 2. LOAD SAVED DATA & PREP CITY LIST
@st.cache_data
def load_and_prep_data():
    try:
        with open('data.json', 'r') as f:
            full_data = json.load(f)
        
        # Flatten the data so we can search by City easily
        all_listings = []
        cities = set()
        for zip_code in full_data:
            for listing in full_data[zip_code]:
                all_listings.append(listing)
                if listing.get("city"):
                    cities.add(listing["city"])
        
        return full_data, all_listings, list(cities)
    except FileNotFoundError:
        return {}, [], []

DATA_BY_ZIP, ALL_LISTINGS, KNOWN_CITIES = load_and_prep_data()

# 3. Search Interface
search_type = st.radio("Search by:", ["ZIP Code", "City Name"])
search_query = st.text_input(f"Enter {search_type}")

# 4. Filter Logic
if search_query:
    results = []
    
    if search_type == "ZIP Code":
        # Direct lookup in the dictionary keys
        results = DATA_BY_ZIP.get(search_query, [])
    else:
        # City Search with Autocorrect
        normalized = search_query.strip().title()
        matches = difflib.get_close_matches(normalized, KNOWN_CITIES, n=1, cutoff=0.6)
        
        if matches:
            target_city = matches[0]
            if target_city != normalized:
                st.info(f"🔍 Showing results for: **{target_city}**")
            # Filter all listings for this city
            results = [h for h in ALL_LISTINGS if h.get("city") == target_city]

    # 5. Display Results
    if results:
        st.success(f"Showing {len(results)} listings in {search_query}")
        for house in results:
            price = house.get('price', 0)
            addr = house.get('addressLine1', 'Unknown Address')
            with st.expander(f"🏠 {addr} - ${price:,}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Price:** ${price:,}")
                    st.write(f"**Beds:** {house.get('bedrooms', 'N/A')}")
                with col2:
                    st.write(f"**Baths:** {house.get('bathrooms', 'N/A')}")
                    st.button("View Details", key=addr)
    else:
        st.warning(f"No listings found for that {search_type.lower()}.")
else:
    st.write("Enter a ZIP or City to see your saved Orange County listings.")
