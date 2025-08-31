import streamlit as st
from PIL import Image
from pyzxing import BarCodeReader
import requests
import io

st.set_page_config(page_title="Barcode Nutrition Scanner", page_icon="📱")
st.title("📱 Mobile Barcode Nutrition Scanner")
st.write("Take a photo of a product barcode and get nutrition information.")

# Initialize barcode reader
reader = BarCodeReader()

# Camera input
uploaded_file = st.file_uploader("Take a photo of the barcode")

if uploaded_file:
    # Convert Streamlit uploaded file to PIL Image
    image = Image.open(uploaded_file)
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    # Save temporarily because pyzxing needs a file path
    with open("temp_barcode.png", "wb") as f:
        f.write(image_bytes.read())

    # Decode barcode using pyzxing
    results = reader.decode("temp_barcode.png")
    if results:
        barcode = results[0].get("parsed")
        st.success(f"✅ Scanned Barcode: **{barcode}**")

        # Fetch nutrition info from OpenFoodFacts
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
        st.error("⚠️ No barcode detected. Try again with better lighting or focus.")
