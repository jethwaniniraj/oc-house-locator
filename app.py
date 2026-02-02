from flask import Flask, render_template, request
from fetch_rentcast import fetch_listings_by_zip, save_listings_to_json
import json
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    listings = []
    zip_code = None
    error = None
    from_cache = False

    if request.method == "POST":
        zip_code = request.form.get("zipcode", "").strip()

        if not zip_code:
            error = "Please enter a ZIP code"
        elif not zip_code.isdigit() or len(zip_code) != 5:
            error = "Please enter a valid 5-digit ZIP code"
        else:
            # First, try to fetch from Rentcast API
            listings = fetch_listings_by_zip(zip_code)
            
            if listings:
                # Save to cache for future use
                save_listings_to_json(zip_code, listings)
            else:
                # If API fails, try to load from cached data.json
                try:
                    if os.path.exists("data.json"):
                        with open("data.json", "r") as f:
                            data = json.load(f)
                            listings = data.get(zip_code, [])
                            if listings:
                                from_cache = True
                                print(f"📂 Loaded {len(listings)} cached listings for {zip_code}")
                except Exception as e:
                    print(f"Error reading cache: {e}")
                
                if not listings:
                    error = f"No listings found for ZIP: {zip_code}. Try another Orange County ZIP like 92618, 92660, or 92672."

    return render_template(
        "index.html", 
        listings=listings, 
        zip_code=zip_code, 
        error=error,
        from_cache=from_cache,
        listing_count=len(listings)
    )

if __name__ == "__main__":
    app.run(debug=True, port=5001)