# ... (Keep your previous API setup and search box) ...

if zip_code:
    # (Keep your requests.get logic here)
    if response.status_code == 200:
        listings = response.json()
        if listings:
            st.success(f"Found {len(listings)} houses in {zip_code}!")
            for house in listings:
                # NEW: Getting city and state from the API data
                address = house.get('addressLine1')
                city = house.get('city', 'Unknown City')
                state = house.get('state', 'CA')
                price = house.get('price', 0)

                # NEW: Displaying City and State in the title
                with st.expander(f"🏠 {address}, {city}, {state} - ${price:,}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**City:** {city}")  # Clearly showing city name
                        st.write(f"**Bedrooms:** {house.get('bedrooms')}")
                        st.write(f"**Bathrooms:** {house.get('bathrooms')}")
                    with col2:
                        st.write(f"**Zip Code:** {house.get('zipCode')}")
                        st.write(f"**Property Type:** {house.get('propertyType')}")
                        st.write(f"**Square Footage:** {house.get('squareFootage')} sqft")
                st.divider()
