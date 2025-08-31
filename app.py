import streamlit as st
from PIL import Image
from pyzxing import BarCodeReader
import io

reader = BarCodeReader()

uploaded_file = st.file_uploader("Take a photo of the barcode", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Convert image to RGB and save temporarily
    image = Image.open(uploaded_file).convert("RGB")
    temp_path = "temp_barcode.jpg"
    image.save(temp_path, format="JPEG", quality=95)

    # Decode using pyzxing
    results = reader.decode(temp_path)
    
    if results and results[0].get("parsed"):
        barcode = results[0]["parsed"]
        st.success(f"✅ Scanned Barcode: **{barcode}**")
    else:
        st.error("⚠️ No barcode detected. Try taking a **clearer, closer, well-lit photo** of the barcode.")
