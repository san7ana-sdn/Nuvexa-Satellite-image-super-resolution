"""
SRM-GEO — Reliability-Aware Satellite Super-Resolution Demo
Prototype Streamlit app skeleton.

Run with:
    pip install streamlit streamlit-image-comparison pillow numpy
    streamlit run app.py
"""

import streamlit as st
from streamlit_image_comparison import image_comparison
from PIL import Image
import numpy as np

# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="SRM-GEO | Satellite Super-Resolution",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# HELPER: dummy placeholder image generator
# (Replace with real Sentinel-2 / PlanetScope / SR arrays later)
# ---------------------------------------------------------------------------
def make_placeholder_image(size=(400, 400), seed=0, label=""):
    rng = np.random.default_rng(seed)
    arr = rng.integers(low=60, high=200, size=(size[1], size[0], 3), dtype=np.uint8)
    img = Image.fromarray(arr)
    return img


# ---------------------------------------------------------------------------
# SIDEBAR — parameter selection
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("🛰️ SRM-GEO")
    st.caption("Reliability-Aware Satellite Super-Resolution")

    st.header("Study Region")

    region = st.selectbox(
        "Select Study Region",
        ["Telangana", "Rajasthan", "Maharashtra", "Odisha"],
        index=0,
    )

    st.subheader("Bounding Box (AOI)")
    st.caption("⚠️ Placeholder coordinates — replace with your actual scene's bounds.")
    col1, col2 = st.columns(2)
    with col1:
        min_lat = st.number_input("Min Latitude", value=17.20, format="%.4f")
        min_lon = st.number_input("Min Longitude", value=78.30, format="%.4f")
    with col2:
        max_lat = st.number_input("Max Latitude", value=17.55, format="%.4f")
        max_lon = st.number_input("Max Longitude", value=78.65, format="%.4f")

    st.divider()

    st.header("Acquisition")
    date = st.selectbox("Date", ["24-Apr-2023", "12-May-2023", "03-Jun-2023"])
    sensor_input = st.selectbox("Input Sensor", ["Sentinel-2 (RGBN, 10m)"])

    st.divider()

    st.header("Model")
    model_choice = st.selectbox("SR Model", ["EDSR-Lite (trained)", "SwinIR (planned)"])
    if model_choice == "SwinIR (planned)":
        st.info("SwinIR — integration planned / prototype stage", icon="ℹ️")

    st.divider()

    generate = st.button("🚀 Generate Super-Resolution", use_container_width=True, type="primary")

# ---------------------------------------------------------------------------
# MAIN PAGE
# ---------------------------------------------------------------------------
st.title("Reliability-Aware Satellite Super-Resolution")
st.caption(
    f"Region: **{region}**  |  Date: **{date}**  |  "
    f"Input: **{sensor_input}**  |  Model: **{model_choice}**"
)

# Processing status placeholder — filled in once real pipeline is wired up
if generate:
    status = st.status("Running pipeline...", expanded=True)
    status.write("✅ Image loaded")
    status.write("✅ Preprocessing")
    status.write("✅ Model inference")
    status.write("✅ NDVI generated")
    status.write("✅ Reliability calculated")
    status.write("✅ Quality evaluated")
    status.update(label="Done", state="complete")

st.divider()

# ---------------------------------------------------------------------------
# TABS — RGB / NIR / NDVI / Reliability / Metrics
# ---------------------------------------------------------------------------
tab_rgb, tab_nir, tab_ndvi, tab_reliability, tab_metrics, tab_map = st.tabs(
    ["RGB", "NIR", "NDVI", "Reliability", "Metrics", "Study Area"]
)

# --- RGB tab: before/after slider (the core interactive feature) ---
with tab_rgb:
    st.subheader("Before / After — 10m Sentinel-2 vs ~3m Super-Resolved")

    # Placeholder images — swap these for real loaded/generated arrays later
    before_img = make_placeholder_image(seed=1, label="Sentinel-2 10m")
    after_img = make_placeholder_image(seed=2, label="SR Output ~3m")

    image_comparison(
        img1=before_img,
        img2=after_img,
        label1="Sentinel-2 (10m)",
        label2="Super-Resolved (~3m)",
        width=700,
        starting_position=50,
        show_labels=True,
        make_responsive=True,
        in_memory=True,
    )

    st.caption(
        "⚠️ Placeholder imagery shown. Wire in real Sentinel-2 input and model "
        "output once the pipeline is connected."
    )

# --- NIR tab ---
with tab_nir:
    st.subheader("Near-Infrared Comparison")
    nir_before = make_placeholder_image(seed=3)
    nir_after = make_placeholder_image(seed=4)
    image_comparison(
        img1=nir_before,
        img2=nir_after,
        label1="NIR — 10m",
        label2="NIR — ~3m",
        width=700,
    )

# --- NDVI tab ---
with tab_ndvi:
    st.subheader("NDVI Comparison")
    ndvi_before = make_placeholder_image(seed=5)
    ndvi_after = make_placeholder_image(seed=6)
    image_comparison(
        img1=ndvi_before,
        img2=ndvi_after,
        label1="NDVI — Original",
        label2="NDVI — Super-Resolved",
        width=700,
    )
    st.metric("NDVI Consistency (illustrative)", "—", help="Populate once real NDVI arrays are wired in.")

# --- Reliability tab ---
with tab_reliability:
    st.subheader("Pixel Reliability")
    st.image(make_placeholder_image(seed=7), caption="Reliability map placeholder", use_container_width=True)
    r1, r2, r3 = st.columns(3)
    r1.metric("High Reliability", "—")
    r2.metric("Medium Reliability", "—")
    r3.metric("Low Reliability", "—")
    st.caption("Reliability = valid-data score + cloud/shadow score + registration score + spectral-consistency score")

# --- Metrics tab ---
with tab_metrics:
    st.subheader("SR Quality Metrics")

    ground_truth_available = st.toggle("Ground Truth Available", value=True)

    if ground_truth_available:
        m1, m2, m3 = st.columns(3)
        m1.metric("PSNR", "— dB")
        m2.metric("SSIM", "—")
        m3.metric("SAM", "— °")
        m4, m5 = st.columns(2)
        m4.metric("MAE", "—")
        m5.metric("NDVI Consistency", "— %")
        st.caption("Metrics will populate once a real PlanetScope reference is loaded for this scene.")
    else:
        st.warning("No ground-truth reference available for this scene — metrics cannot be computed.")

    st.divider()
    st.download_button("⬇️ Download Metrics CSV", data="metric,value\n", file_name="metrics.csv", disabled=True)

# --- Study Area tab (map placeholder) ---
with tab_map:
    st.subheader("Study Area")
    st.map(
        data={"lat": [(min_lat + max_lat) / 2], "lon": [(min_lon + max_lon) / 2]},
        zoom=8,
    )
    st.caption(f"Latitude: {(min_lat + max_lat) / 2:.4f} | Longitude: {(min_lon + max_lon) / 2:.4f} | Region: {region}")

st.divider()

# ---------------------------------------------------------------------------
# DOWNLOADS
# ---------------------------------------------------------------------------
st.subheader("Download Results")
d1, d2, d3, d4 = st.columns(4)
with d1:
    st.download_button("SR GeoTIFF", data=b"", file_name="sr_output.tif", disabled=True)
with d2:
    st.download_button("NDVI", data=b"", file_name="ndvi.tif", disabled=True)
with d3:
    st.download_button("Reliability Map", data=b"", file_name="reliability.tif", disabled=True)
with d4:
    st.download_button("Metrics CSV", data="", file_name="metrics.csv", disabled=True)

st.caption("Download buttons are disabled placeholders until real outputs are wired in.")
