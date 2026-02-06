import streamlit as st
import difflib

# 1. Page Configuration
st.set_page_config(page_title="OC House Locator", page_icon="🍊")

# Custom CSS for VIBRANT small oranges background
st.markdown("""
    <style>
    .stApp {
        background-color: #FFF9F2;
        /* Increased opacity to 0.9 for high visibility like the header icon */
        background-image:  url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Ctext x='10' y='30' style='font-size:16px; opacity: 0.9;'%3E🍊%3C/text%3E%3C/svg%3E");
        background-attachment: fixed;
    }
    
    /* Ensuring text remains the priority and highly readable */
    h1, h2, h3, p, label, .stText {
        color: #31333F !important;
        /* Adding a slight text-shadow to help title pop against the pattern */
        text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
    }

    /* Solid white search boxes so the background doesn't bleed through the text */
    div[data-baseweb="input"] {
        background-color: white !important;
        border: 2px solid #FFCC80 !important;
    }
    
    .stExpander {
        background-color: white !important;
        border-radius: 10px;
        border: 1px solid #FFCC80;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🍊 Orange County Home Finder")

# 2. Database
LISTINGS = [
    {"address": "29 Small Grove", "city": "Irvine", "zip": "92618", "price": 4080000, "beds": 5, "baths": 6, "type": "Single Family", "sqft": 4209},
    {"address": "136 Pineview", "city": "Irvine", "zip": "92620", "price": 899000, "beds": 2, "baths": 3, "type": "Condo", "sqft": 1366},
    {"address": "412 Heliotrope Ave", "city": "Corona Del Mar", "zip": "92625", "price": 8495000, "beds": 4, "baths": 6, "type": "Luxury Villa", "sqft": 3120},
    {"address": "821 S Fairmont Way", "city": "Orange", "zip": "92869", "price": 1374999, "beds": 4, "baths": 3, "type": "Single Family", "sqft": 2632},
    {"address": "1822 W 4th St", "city": "Santa Ana", "zip": "92703", "price": 449900, "beds": 3, "baths": 1, "type": "Single Family", "sqft": 767},
    {"address": "119 Alumroot", "city": "Irvine", "zip": "92620", "price": 2130000, "beds": 4, "baths": 4, "type": "Single Family", "sqft": 2800},
    {"address": "16779 Willow Cir", "city": "Fountain Valley", "zip": "92708", "price": 1498000, "beds": 4, "baths": 3, "type": "Single Family", "sqft": 1923}
]

OC_CITIES = list(set([h["city"] for h in LISTINGS])) + ["Anaheim", "Newport Beach", "Huntington Beach", "Fullerton"]

# 3. Search Interface
search_type = st.radio("Search by:", ["ZIP Code", "City Name"])
search_query = st.text_input(f"Enter {search_type}")

# 4. Filter Logic
if search_query:
    results = []
    
    if search_type == "ZIP Code":
        results = [h for h in LISTINGS if h["zip"] == search_query]
    else:
        normalized = search_query.strip().title()
        matches = difflib.get_close_matches(normalized, OC_CITIES, n=1, cutoff=0.6)
        
        if matches:
            if matches[0] != normalized:
                st.info(f"🔍 Showing results for: **{matches[0]}**")
            results = [h for h in LISTINGS if h["city"] == matches[0]]

    # 5. Display Results
    if results:
        st.success(f"Showing {len(results)} active listings in {search_query}")
        for house in results:
            with st.expander(f"🏠 {house['address']}, {house['city']} - ${house['price']:,}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Price:** ${house['price']:,}")
                    st.write(f"**Beds/Baths:** {house['beds']} / {house['baths']}")
                with col2:
                    st.write(f"**Type:** {house['type']}")
                    st.write(f"**SqFt:** {house['sqft']} sqft")
    else:
        st.warning("No listings currently found for that area.")
else:
    st.write("Please enter a search term above to browse listings.")
