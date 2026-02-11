import streamlit as st
import folium
from streamlit_folium import st_folium

# 1. State Management (Remembers what you clicked on the map)
if 'selected_city' not in st.session_state:
    st.session_state.selected_city = ""

# 2. The Map with Clickable Markers
def draw_interactive_map():
    # Centered on Orange County
    m = folium.Map(location=[33.7175, -117.8311], zoom_start=10)
    
    # Adding City Markers
    cities = {"Irvine": [33.6846, -117.8265], "Newport Beach": [33.6189, -117.9298]}
    
    for city, coords in cities.items():
        folium.Marker(
            coords, 
            tooltip=f"View houses in {city}",
            icon=folium.Icon(color="orange")
        ).add_to(m)
    
    # Capture the click
    map_data = st_folium(m, height=400, width="100%")
    
    # If a user clicks a marker, update the "search"
    if map_data.get("last_object_clicked_tooltip"):
        st.session_state.selected_city = map_data["last_object_clicked_tooltip"].split("in ")[-1]

# 3. Use the state to filter results automatically
search_query = st.text_input("", value=st.session_state.selected_city, placeholder="Search by ZIP or City")
