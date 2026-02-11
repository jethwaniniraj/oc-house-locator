import requests
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="OC City Finder", layout="wide")

st.title("Orange County City Map")
st.caption("Click a city boundary to see its name, or use the dropdown to highlight a city.")

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
    data = resp.json()
    if "features" not in data:
        raise ValueError("No features returned from OC city boundary service.")
    return data

def feature_bounds(feature):
    geom = feature.get("geometry") or {}
    gtype = geom.get("type")
    coords = geom.get("coordinates") or []
    points = []

    if gtype == "Polygon":
        for ring in coords:
            points.extend(ring)
    elif gtype == "MultiPolygon":
        for poly in coords:
            for ring in poly:
                points.extend(ring)

    lats = [p[1] for p in points] if points else []
    lons = [p[0] for p in points] if points else []
    if not lats or not lons:
        return None
    return [[min(lats), min(lons)], [max(lats), max(lons)]]

geojson = load_oc_city_geojson()
city_names = sorted({f["properties"].get("NAME", "").strip() for f in geojson["features"] if f.get("properties")})

selected_city = st.selectbox("Select a city", ["(All cities)"] + city_names, index=0)

def style_fn(feature):
    name = feature["properties"].get("NAME")
    if selected_city != "(All cities)" and name == selected_city:
        return {"color": "#ff7a00", "weight": 3, "fillColor": "#ffb347", "fillOpacity": 0.55}
    return {"color": "#666666", "weight": 1.5, "fillColor": "#f3efe6", "fillOpacity": 0.15}

m = folium.Map(location=[33.67, -117.78], zoom_start=10, tiles="CartoDB positron")

folium.GeoJson(
    geojson,
    name="OC Cities",
    style_function=style_fn,
    tooltip=folium.GeoJsonTooltip(fields=["NAME"], aliases=["City"]),
).add_to(m)

if selected_city != "(All cities)":
    selected_feature = next(
        (f for f in geojson["features"] if f["properties"].get("NAME") == selected_city),
        None,
    )
    if selected_feature:
        bounds = feature_bounds(selected_feature)
        if bounds:
            m.fit_bounds(bounds)

st_folium(m, use_container_width=True, height=650)
