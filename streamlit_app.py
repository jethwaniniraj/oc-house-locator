import streamlit as st
import folium
from streamlit_folium import st_folium

# 1. CSS for the Thicker, Pinned Bottom Search Bar
st.markdown("""
    <style>
    .stApp {
        background-color: #FFF9F2;
        background-image:  url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Ctext x='10' y='30' style='font-size:16px; opacity: 0.9;'%3E🍊%3C/text%3E%3C/svg%3E");
    }

    /* Map Styling */
    iframe {
        border-radius: 20px !important;
        border: 2px solid #FF8C00 !important;
        box-shadow: 0 0 20px rgba(255, 140, 0, 0.2);
        filter: sepia(0.5) hue-rotate(15deg) saturate(1.2);
        margin-top: 10px;
    }

    /* THE THICK PINNED SEARCH BAR */
    div[data-testid="stTextInput"] {
        position: fixed;
        bottom: 40px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1000;
        width: 100%;
        max-width: 850px; /* Wider footprint */
    }
    
    /* Adjusting the actual input box height and text size */
    div[data-baseweb="input"] {
        height: 70px !important; /* Increased thickness */
        background-color: white !important;
        border: 3px solid #FF8C00 !important;
        border-radius: 35px !important;
        box-shadow: 0 0 25px 8px rgba(255, 140, 0, 0.4) !important;
    }

    /* Making the typed text larger to match the thicker bar */
    input {
        font-size: 22px !important;
        padding-left: 25px !important;
    }
    
    /* UI Cleanup */
    div[data-testid="InputInstructions"] { display: none !important; }
    header, footer {visibility: hidden;}
    .main .block-container { padding-bottom: 150px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Map Function
def draw_interactive_map():
    m = folium.Map(location=[33.7175, -117.8311], zoom_start=10, tiles='CartoDB positron')
    oc_cities = {
        "Irvine": [33.6846, -117.8265],
        "Newport Beach": [33.6189, -117.9298],
        "Anaheim": [33.8366, -117.9143],
        "Huntington Beach": [33.6599, -117.9988]
    }
    for city, coords in oc_cities.items():
        folium.Marker(
            coords, 
            tooltip=f"View {city}",
            icon=folium.Icon(color="orange", icon="home")
        ).add_to(m)
    return st_folium(m, height=520, width="100%", returned_objects=["last_object_clicked_tooltip"])

# 3. Execution
map_data = draw_interactive_map()

selected_city = ""
if map_data and map_data.get("last_object_clicked_tooltip"):
    selected_city = map_data["last_object_clicked_tooltip"].replace("View ", "")

# Thicker Search Bar at the bottom
st.text_input("", value=selected_city, placeholder="Search by ZIP or City", label_visibility="collapsed")
