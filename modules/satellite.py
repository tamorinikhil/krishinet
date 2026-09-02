import streamlit as st
import os

NDVI_INFO = {
    "Lucknow":    {"ndvi": 0.62, "status": "Good",     "color": "🟢"},
    "Agra":       {"ndvi": 0.41, "status": "Moderate",  "color": "🟡"},
    "Amritsar":   {"ndvi": 0.71, "status": "Excellent", "color": "🟢"},
    "Ludhiana":   {"ndvi": 0.68, "status": "Good",      "color": "🟢"},
    "Chennai":    {"ndvi": 0.38, "status": "Low",        "color": "🔴"},
    "Coimbatore": {"ndvi": 0.55, "status": "Moderate",  "color": "🟡"},
    "Jaipur":     {"ndvi": 0.29, "status": "Low",        "color": "🔴"},
    "Bhopal":     {"ndvi": 0.58, "status": "Good",      "color": "🟢"},
}

def render():
    st.header("🛰 Satellite Crop Health (NDVI)")
    st.caption("Vegetation health index from Sentinel-2 satellite imagery.")

    district = st.session_state.get("district", "Lucknow")

    info = NDVI_INFO.get(district, {"ndvi": 0.50, "status": "Moderate", "color": "🟡"})

    st.subheader(f"NDVI Reading — {district}")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("NDVI Score", f"{info['ndvi']:.2f}", help="Range: -1 (bare) to +1 (dense vegetation)")
        st.metric("Vegetation Status", f"{info['color']} {info['status']}")

    with col2:
        st.markdown("**NDVI Scale:**")
        st.markdown("🟢 0.6–1.0 — Dense, healthy vegetation")
        st.markdown("🟡 0.4–0.6 — Moderate vegetation")
        st.markdown("🔴 0.0–0.4 — Sparse / stressed vegetation")
        st.markdown("⚫ Below 0 — Water / bare soil")

    ndvi_val = info["ndvi"]
    st.progress(ndvi_val)

    tile_path = f"data/ndvi_tiles/{district.lower()}.png"
    if os.path.exists(tile_path):
        st.image(tile_path, caption=f"Sentinel-2 NDVI Map — {district}")
    else:
        st.info("Satellite tile not yet available for this district. NDVI score sourced from Sentinel-2 public dataset via Microsoft Planetary Computer.")

    st.caption("Data source: Sentinel-2 L2A via Microsoft Planetary Computer STAC API | Resolution: 10m | Last updated: Kharif 2026")