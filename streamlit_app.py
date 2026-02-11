import streamlit as st
import json
import difflib
import requests
import folium
import re
from streamlit_folium import st_folium

# 1. Page Configuration
st.set_page_config(page_title="OC House Locator", page_icon="🍊")

# 2. CSS: EXACT STYLE + ORANGE GLOW
st.markdown("""
    <style>
    /* Your Vibrant Orange Background Pattern */
    .stApp {
        background-color: #FFF9F2;
        background-image:  url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Ctext x='10' y='30' style='font-size:16px; opacity: 0.9;'%3E🍊%3C/text%3E%3C/svg%3E");
        background-attachment: fixed;
    }
    
    /* ANCHOR SEARCH BAR TO BOTTOM */
    div[data-testid="stVerticalBlock"] > div:has(input) {
        position: fixed;
        bottom: 50px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1000;
        width: 90%;
        max-width: 600px;
    }

    /* PRESERVED SEARCH BAR STYLE + ORANGE GLOW EFFECT */
    div[data-baseweb="input"] {
        background-color: white !important;
        border: 2px solid #FF8C00 !important; /* Slightly deeper orange for the border */
        border-radius: 25px !important;
        height: 55px;
        /* Glowing Box Shadow: Horizontal, Vertical, Blur, Spread, Color */
        box-shadow: 0 0 15px 5px rgba(255, 140, 0, 0.5) !important;
        transition: box-shadow 0.3s ease-in-out;
    }

    /* Pulse effect when the user clicks inside the bar */
    div[data-baseweb="input"]:focus-within {
        box-shadow: 0 0 25px 8px rgba(255, 140, 0, 0.7) !important;
    }
    
    header, footer {visibility: hidden;}
    .main .block-container { padding-bottom: 150px; }
    </style>
    """, unsafe_allow_html=True)

# 3. DATA LOADING (Offline Mode)
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

# 3.5 MAP DATA LOADING
@st.cache_data(show_spinner=False)
def load_oc_city_geojson():
    url = "https://services.arcgis.com/UXmFoWC7yDHcDN5Q/ArcGIS/rest/services/Orange_County_Boundaries/FeatureServer/2/query"
    params = {
        "where": "PLACETYPE = 'City'",
        "outFields": "NAME,PLACETYPE",
        "returnGeometry": "true",
        "outSR": "4326",
        "f": "geojson",
    }
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()

def _extract_city(popup_html):
    if not popup_html:
        return None
    text = re.sub(r"<[^>]+>", "", str(popup_html)).strip()
    return text or None

if "selected_city" not in st.session_state:
    st.session_state.selected_city = None

def render_oc_map():
    try:
        geojson = load_oc_city_geojson()
        selected = st.session_state.selected_city

        m = folium.Map(location=[33.67, -117.78], zoom_start=10, tiles="CartoDB positron")

        def style_fn(feature):
            name = feature["properties"].get("NAME")
            if selected and name == selected:
                return {
                    "color": "#FF7A00",
                    "weight": 3,
                    "fillColor": "#FFB347",
                    "fillOpacity": 0.55,
                }
            return {
                "color": "#444444",
                "weight": 1.3,
                "fillColor": "#f2e6d9",
                "fillOpacity": 0.12,
            }

        folium.GeoJson(
            geojson,
            name="OC Cities",
            style_function=style_fn,
            tooltip=folium.GeoJsonTooltip(fields=["NAME"], aliases=["City"]),
            popup=folium.GeoJsonPopup(fields=["NAME"], labels=False),
        ).add_to(m)

        map_data = st_folium(m, use_container_width=True, height=520)

        clicked_city = _extract_city(map_data.get("last_object_clicked_popup"))
        if clicked_city and clicked_city != st.session_state.selected_city:
            st.session_state.selected_city = clicked_city
            st.rerun()

    except Exception:
        st.info("Map is temporarily unavailable. Please try again later.")

# 4. MAP (ABOVE SEARCH BAR)
render_oc_map()

# 5. THE SEARCH BAR
search_query = st.text_input("", placeholder="Search by ZIP Code or City")

# 6. FILTER & DISPLAY (Indentation Verified)
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
