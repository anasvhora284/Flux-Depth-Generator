import streamlit as st
import os
import zipfile
import io
import torch
import numpy as np
from PIL import Image

from src.core import load_model, infer_depth, DEVICE
from src.utils import get_system_metrics, create_gdepth_xmp, embed_xmp_jpeg
from src.ui import inject_custom_css, render_header, render_footer

st.set_page_config(
    page_title="Depth Generator Pro",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():
    inject_custom_css()
    render_header()
    
    # Sidebar for settings
    with st.sidebar:
        st.header("Settings")
        model_type = st.selectbox("Model Type", ["vits", "vitb", "vitl"], index=0, help="Select model size. Larger models are more accurate but slower.")
        st.info(f"Running on: {DEVICE.upper()}")
        
        st.divider()
        st.subheader("System Metrics")
        metrics_placeholder = st.empty()
        
        # Initial metrics
        cpu, mem, proc = get_system_metrics()
        metrics_placeholder.markdown(f"**CPU:** {cpu}%  \n**RAM:** {mem}%  \n**App:** {proc} MB")

    # Main content layout
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        st.markdown("### Upload Images")
        uploaded_files = st.file_uploader(
            "Drag and drop images here", 
            type=["jpg", "jpeg", "png"], 
            accept_multiple_files=True,
            label_visibility="collapsed"
        )

        if uploaded_files:
            st.success(f"Ready to process {len(uploaded_files)} images.")
            
            # Preview first few images
            st.markdown("#### Preview")
            cols = st.columns(min(4, len(uploaded_files)))
            for i, file in enumerate(uploaded_files[:4]):
                cols[i].image(file, width="stretch")
            if len(uploaded_files) > 4:
                st.caption(f"...and {len(uploaded_files)-4} more")

    with col2:
        st.markdown("### Actions")
        st.info("Click below to start processing. This may take a while depending on your hardware.")
        
        process_btn = st.button("Generate Depth Maps", type="primary", disabled=not uploaded_files)
        
        result_placeholder = st.empty()

    if process_btn and uploaded_files:
        with st.spinner("Initializing model..."):
            model = load_model(model_type)
        
        if model:
            process_batch(uploaded_files, model, result_placeholder)

    render_footer()

def process_batch(files, model, placeholder):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        total = len(files)
        for idx, file in enumerate(files):
            status_text.text(f"Processing {idx+1}/{total}: {file.name}")
            
            try:
                image = Image.open(file).convert("RGB")
                w, h = image.size
                
                # Infer
                depth = infer_depth(model, image)
                
                # Post-process
                depth_norm = (depth - depth.min()) / (depth.max() - depth.min() + 1e-6)
                depth_img = Image.fromarray((depth_norm * 255).astype(np.uint8))
                
                # Save Depth PNG
                depth_bytes = io.BytesIO()
                depth_img.save(depth_bytes, format="PNG")
                zip_file.writestr(f"{os.path.splitext(file.name)[0]}_depth.png", depth_bytes.getvalue())
                
                # Save 3D JPEG
                xmp = create_gdepth_xmp(depth, w, h)
                
                # Pass original file bytes to preserve quality if it's already a JPEG
                file.seek(0)
                original_bytes = file.getvalue()
                
                jpeg_bytes = embed_xmp_jpeg(image, xmp, original_bytes)
                zip_file.writestr(f"{os.path.splitext(file.name)[0]}_3d.jpg", jpeg_bytes)
                
            except Exception as e:
                st.error(f"Error processing {file.name}: {e}")
            
            progress_bar.progress((idx + 1) / total)
            
    status_text.empty()
    progress_bar.empty()
    
    with placeholder.container():
        st.success("Processing complete! 🎉")
        st.download_button(
            label="Download Results (ZIP)",
            data=zip_buffer.getvalue(),
            file_name="depth_maps.zip",
            mime="application/zip",
            type="primary"
        )

if __name__ == "__main__":
    main()
