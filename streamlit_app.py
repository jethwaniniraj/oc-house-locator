import streamlit as st
import json
import difflib

# 1. Page Configuration (Vibrant Oranges)
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

# 2. LOAD YOUR REAL SAVED DATA
@st.cache_data
def load_data():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

DATA_BY_ZIP = load_data()

# 3. Search Interface
search_query = st.text_input("Enter 5-digit ZIP Code", placeholder="e.g. 92660")

# 4. Filter and Display
if search_query:
    # Check if the ZIP exists in your file
    if search_query in DATA_BY_ZIP:
        results = DATA_BY_ZIP[search_query]
        st.success(f"Showing {len(results)} active listings in {search_query}")
        
        for house in results:
            price = house.get('price', 0)
            addr = house.get('addressLine1', 'Unknown Address')
            beds = house.get('bedrooms', 'N/A')
            baths = house.get('bathrooms', 'N/A')
            
            with st.expander(f"🏠 {addr} - ${price:,}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Price:** ${price:,}")
                    st.write(f"**Beds:** {beds}")
                with col2:
                    st.write(f"**Baths:** {baths}")
                    st.button("View Details", key=addr)
    else:
        st.warning("No listings saved for that ZIP code. Try 92660 or 92672!")
else:
    st.write("Enter a ZIP code from your database to see real-time property details.")
