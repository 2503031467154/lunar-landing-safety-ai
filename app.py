import streamlit as st
from PIL import Image
from terrain_analyzer import analyze_lunar_terrain

st.set_page_config(
    page_title="Lunar Landing Safety AI",
    page_icon="🚀",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #0b1020;
}
.title {
    font-size: 48px;
    font-weight: bold;
    color: white;
}
.subtitle {
    font-size: 20px;
    color: #cbd5e1;
}
.card {
    background-color: #111827;
    padding: 25px;
    border-radius: 15px;
    color: white;
    border: 1px solid #334155;
}
.success-box {
    background-color: #064e3b;
    padding: 15px;
    border-radius: 10px;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🚀 Lunar Landing Safety AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI-powered system to detect safe and unsafe lunar landing zones</div>',
    unsafe_allow_html=True
)

st.write("")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
    <h3>🌑 Terrain Input</h3>
    <p>Upload lunar surface images for analysis.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
    <h3>🧠 AI Analysis</h3>
    <p>Detects craters, rough areas, and unsafe zones.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
    <h3>✅ Safe Zone</h3>
    <p>Marks possible safe landing areas visually.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.divider()

uploaded_file = st.file_uploader(
    "📤 Upload Lunar Surface Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    st.subheader("📷 Uploaded Lunar Image")
    st.image(image, use_container_width=True)

    analyze_button = st.button("🚀 Analyze Landing Safety")

    if analyze_button:
        with st.spinner("Analyzing lunar terrain..."):
            result, edges, heatmap, dashboard = analyze_lunar_terrain(image)

        st.markdown("""
        <div class="success-box">
        ✅ Terrain analysis completed successfully.
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🧭 Edge Detection Map")
            st.image(edges, use_container_width=True, clamp=True)

        with col2:
            st.subheader("🟢 Safe Landing Zone Result")
            st.image(result, use_container_width=True)

        st.divider()

        st.subheader("📊 Landing Safety Dashboard")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "🕳️ Craters",
             dashboard["crater_count"]
        )

        c2.metric(
            "✅ Safe Area",
            f"{dashboard['safe_area_percentage']}%"
        )

        c3.metric(
            "⛰️ Roughness",
            dashboard["terrain_roughness_score"]
        )

        c4.metric(
            "⚠️ Risk Score",
            f"{dashboard['risk_score']}/100"
       )

        st.subheader("🗺️ Risk Heatmap")
        st.image(heatmap, use_container_width=True)

        st.subheader("📍 Recommended Landing Coordinates")
        st.write(dashboard["recommended_coordinates"])

        st.info("Green boxes indicate possible safe landing zones. Red circles indicate dangerous crater regions.")

else:
    st.info("Please upload a lunar surface image to begin analysis.")