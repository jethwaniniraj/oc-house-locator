import streamlit as st
import json

# Page styling
st.set_page_config(page_title="OC House Locator", page_icon="🔍")

st.title("Orange County House Locator")
st.write("Find real houses for sale by ZIP Code")

# Search Box (Replaces the Flask Form)
zip_code = st.text_input("Enter ZIP (e.g. 92618)", placeholder="92618")

if zip_code:
    try:
        # Open your existing data.json
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            listings = data.get(zip_code, [])

            if listings:
                st.subheader(f"Houses in {zip_code}")
                
                # Display results in a clean grid
                for house in listings:
                    with st.container():
                        # Using Markdown for nice formatting
                        st.markdown(f"### ${house['price']:,}")
                        st.write(f"**Address:** {house['addressLine1']}")
                        st.write(f"🛏️ {house['bedrooms']} Bed | 🚿 {house['bathrooms']} Bath")
                        st.divider()
            else:
                st.error(f"No data found for ZIP: {zip_code}")
                
    except FileNotFoundError:
        st.error("Missing 'data.json' file. Please upload it to your GitHub repository.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
