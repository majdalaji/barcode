import streamlit as st
from pyzbar.pyzbar import decode
from PIL import Image
import requests

st.set_page_config(page_title="Barcode Nutrition Scanner", page_icon="📱")

st.title("📱 Mobile Barcode Nutrition Scanner")
st.write("Take a photo of a product barcode and get nutrition information.")

# Use phone camera
uploaded_file = st.camera_input("Take a photo of the barcode")

if uploaded_file:
    # Open the image
    img = Image.open(uploaded_file)
    result = decode(img)

    if result:
        barcode = result[0].data.decode("utf-8")
        st.success(f"✅ Scanned Barcode: **{barcode}**")

        # Fetch product info from OpenFoodFacts
        url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
        res = requests.get(url).json()

        if res.get("status") == 1:
            product = res["product"]
            nutriments = product.get("nutriments", {})

            st.subheader("🍫 Product Information")
            st.write("**Product:**", product.get("product_name", "Unknown"))
            st.write("**Brand:**", product.get("brands", "Unknown"))

            st.subheader("📊 Nutrition per 100g")
            st.write("**Calories:**", nutriments.get("energy-kcal_100g", "N/A"), "kcal")
            st.write("**Fat:**", nutriments.get("fat_100g", "N/A"), "g")
            st.write("**Carbs:**", nutriments.get("carbohydrates_100g", "N/A"), "g")
            st.write("**Protein:**", nutriments.get("proteins_100g", "N/A"), "g")
        else:
            st.error("❌ Product not found in database.")
    else:
        st.error("⚠️ No barcode detected in the image. Try again with better lighting or focus.")
