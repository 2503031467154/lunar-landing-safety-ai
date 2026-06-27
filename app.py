import streamlit as st
from PIL import Image
from terrain_analyzer import analyze_lunar_terrain

st.set_page_config(
    page_title="Lunar Landing Safety AI",
    layout="wide"
)

st.title("🚀 Lunar Landing Safety AI")
st.write("AI/ML project for detecting safe landing zones on lunar terrain images.")

uploaded_file = st.file_uploader(
    "Upload a lunar surface image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    st.subheader("Original Lunar Image")
    st.image(image, use_container_width=True)

    if st.button("Analyze Terrain"):
        result, edges = analyze_lunar_terrain(image)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Edge Detection")
            st.image(edges, use_container_width=True, clamp=True)

        with col2:
            st.subheader("Safe Landing Zone Result")
            st.image(result, use_container_width=True)

        st.success("Analysis completed. Green boxes show possible safe landing zones. Red circles show dangerous crater areas.")
else:
    st.info("Please upload a lunar surface image to begin analysis.")