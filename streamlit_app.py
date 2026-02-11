import streamlit as st
import folium
from streamlit_folium import st_folium

# 1. CSS for the Orange UI Blend
st.markdown("""
    <style>
    /* Your existing Orange Background */
    .stApp {
        background-color: #FFF9F2;
        background-image:  url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Ctext x='10' y='30' style='font-size:16px; opacity: 0.9;'%3E🍊%3C/text%3E%3C/svg%3E");
    }

    /* THE MAGIC: Blending the Map */
    iframe {
        border-radius: 20px !important;
        border: 2px solid #FF8C00 !important;
        box-shadow: 0 0 20px rgba(255, 140, 0, 0.2);
        /* This filter turns the map orange/sepia */
        filter: sepia(0.6) hue-rotate(15deg) saturate(1.2) brightness(0.95);
    }

    /* Fixed Bottom Search Bar Logic */
    div[data-testid="stHorizontalBlock"] {
        position: fixed;
        bottom: 50px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1000;
        width: 100%;
        max-width: 800px;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 15px !important;
    }
    
    div[data-baseweb="input"] {
        background-color: white !important;
        border: 2px solid #FF8C00 !important;
        border-radius: 25px !important;
        box-shadow: 0 0 15px 5px rgba(255, 140, 0, 0.4) !important;
    }
    
    /* Hide Instructions & Streamlit Overlays */
    div[data-testid="InputInstructions"] { display: none !important; }
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 2. Interactive Map with Sepia-Tone Tile
def draw_orange_map():
    # Use a 'CartoDB positron' tile as the base (it's grey/white, which takes orange tinting best)
    m = folium.Map(location=[33.7175, -117.8311], zoom_start=10, tiles='CartoDB positron')
    
    # Major OC Cities for Click-to-Search
    oc_cities = {
        "Irvine": [33.6846, -117.8265],
        "Newport Beach": [33.6189, -117.9298],
        "Anaheim": [33.8366, -117.9143]
    }
    
    for city, coords in oc_cities.items():
        folium.Marker(
            coords, 
            tooltip=f"View {city}",
            icon=folium.Icon(color="orange", icon="home")
        ).add_to(m)
    
    return st_folium(m, height=450, width="100%", returned_objects=["last_object_clicked_tooltip"])

# 3. App Layout
st.title("🍊 OC Interactive Home Finder")

# Display Map above the search bar
map_data = draw_orange_map()

# Logic to update search based on map click
selected_city = ""
if map_data and map_data.get("last_object_clicked_tooltip"):
    selected_city = map_data["last_object_clicked_tooltip"].replace("View ", "")

# Pinned Bottom Bar (Search + Filter)
col1, col2 = st.columns([6, 1])
with col1:
    search_query = st.text_input("", value=selected_city, placeholder="Search by ZIP or City", label_visibility="collapsed")
with col2:
    st.button("🛏️", key="filter_btn")
