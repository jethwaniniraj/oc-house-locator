import streamlit as st
import difflib

# --- AESTHETICS ---
st.set_page_config(page_title="OC House Locator", page_icon="🍊")
st.markdown("<style>.stApp {background: #FFF9F2;}</style>", unsafe_allow_html=True)

st.title("🍊 Orange County Real Estate Finder")

# 1. DUMMY DATA (Mock Orange County Listings)
MOCK_DATA = [
    {"addressLine1": "29 Small Grv", "city": "Irvine", "state": "CA", "zipCode": "92618", "price": 4080000, "bedrooms": 5, "bathrooms": 6, "propertyType": "Single Family", "squareFootage": 4209},
    {"addressLine1": "136 Pineview", "city": "Irvine", "state": "CA", "zipCode": "92620", "price": 899000, "bedrooms": 2, "bathrooms": 3, "propertyType": "Condo", "squareFootage": 1366},
    {"addressLine1": "1822 W 4th St", "city": "Santa Ana", "state": "CA", "zipCode": "92703", "price": 449900, "bedrooms": 3, "bathrooms": 1, "propertyType": "Single Family", "squareFootage": 767},
    {"addressLine1": "821 S Fairmont Way", "city": "Orange", "state": "CA", "zipCode": "92869", "price": 1374999, "bedrooms": 4, "bathrooms": 3, "propertyType": "Single Family", "squareFootage": 2632},
    {"addressLine1": "412 Heliotrope Ave", "city": "Corona Del Mar", "state": "CA", "zipCode": "92625", "price": 8495000, "bedrooms": 4, "bathrooms": 6, "propertyType": "Luxury Villa", "squareFootage": 3120},
    {"addressLine1": "181 Seacountry Ln", "city": "Rancho Santa Margarita", "state": "CA", "zipCode": "92688", "price": 725000, "bedrooms": 2, "bathrooms": 3, "propertyType": "Condo", "squareFootage": 1080},
    {"addressLine1": "16779 Willow Cir", "city": "Fountain Valley", "state": "CA", "zipCode": "92708", "price": 1498000, "bedrooms": 4, "bathrooms": 3, "propertyType": "Single Family", "squareFootage": 1923}
]

OC_CITIES = [c["city"] for c in MOCK_DATA] + ["Anaheim", "Newport Beach", "Fullerton", "Costa Mesa"]

# 2. Setup Mode
# Check if API Key exists in secrets; if not, use Mock Mode
USE_MOCK = "RENTCAST_API_KEY" not in st.secrets

if USE_MOCK:
    st.info("🛠️ **Demo Mode:** API is currently inactive. Showing sample listings.")

# 3. Search Options
search_type = st.radio("Search by:", ["ZIP Code", "City Name"])
search_query = st.text_input(f"Enter {search_type}")

# 4. Filter and Display Data
if search_query:
    results = []
    
    # Logic for Mock Search
    if USE_MOCK:
        normalized = search_query.strip().title()
        # Filter mock data by ZIP or City
        if search_type == "ZIP Code":
            results = [h for h in MOCK_DATA if h["zipCode"] == search_query]
        else:
            # Spelling Correction for City
            matches = difflib.get_close_matches(normalized, OC_CITIES, n=1, cutoff=0.6)
            if matches:
                if matches[0] != normalized:
                    st.write(f"Did you mean: **{matches[0]}**?")
                results = [h for h in MOCK_DATA if h["city"] == matches[0]]
    
    # Display Results
    if results:
        st.success(f"Found {len(results)} sample listings in {search_query}:")
        for house in results:
            with st.expander(f"🏠 {house['addressLine1']}, {house['city']} - ${house['price']:,}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Beds/Baths:** {house['bedrooms']} / {house['bathrooms']}")
                    st.write(f"**Price:** ${house['price']:,}")
                with col2:
                    st.write(f"**Type:** {house['propertyType']}")
                    st.write(f"**SqFt:** {house['squareFootage']}")
    elif search_query:
        st.warning("No listings found in the demo database for that input.")
