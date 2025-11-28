import streamlit as st
import os
import zipfile
import io
import torch
import numpy as np
from PIL import Image
import time

from src.core import load_model, infer_depth, DEVICE
from src.utils import get_system_metrics, create_gdepth_xmp, embed_xmp_jpeg
from src.ui import inject_custom_css, render_header, render_footer
from src.config import load_settings, save_settings, resolve_theme
from src.components import render_upload_zone, render_comparison_slider, render_preview_gallery, render_processing_progress, render_results_summary

st.set_page_config(
    page_title="Depth Generator Pro",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():
    # Load settings and determine theme
    settings = load_settings()
    current_theme = resolve_theme(settings)
    
    # Inject CSS with appropriate theme
    inject_custom_css(theme_mode=current_theme, accent_color=settings.get("accent_color", "#238636"))
    
    # Render header with theme toggle
    render_header(theme_mode=current_theme)
    
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
        uploaded_files = render_upload_zone()

    with col2:
        st.markdown("### Actions")
        st.info("Click below to start processing. This may take a while depending on your hardware.")
        
        process_btn = st.button("🚀 Generate Depth Maps", type="primary", disabled=not uploaded_files, use_container_width=True)
        
        result_placeholder = st.empty()

    if process_btn and uploaded_files:
        with st.spinner("Initializing model..."):
            model = load_model(model_type)
        
        if model:
            process_batch(uploaded_files, model, result_placeholder, settings)

    render_footer()

def process_batch(files, model, placeholder, settings):
    """Process batch of images with live preview.
    
    Args:
        files: List of uploaded files
        model: Loaded depth model
        placeholder: Streamlit container for results
        settings: User settings dict
    """
    # Create tabs for organization
    tab1, tab2 = st.tabs(["📊 Processing", "🖼️ Results Gallery"])
    
    with tab1:
        progress_bar = st.progress(0)
        status_text = st.empty()
        preview_container = st.container()
        
        zip_buffer = io.BytesIO()
        depth_maps = []
        original_images = []
        filenames = []
        start_time = time.time()
        
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            total = len(files)
            for idx, file in enumerate(files):
                status_text.text(f"⏳ Processing {idx+1}/{total}: {file.name}")
                
                try:
                    image = Image.open(file).convert("RGB")
                    w, h = image.size
                    
                    # Infer
                    depth = infer_depth(model, image)
                    
                    # Post-process
                    depth_norm = (depth - depth.min()) / (depth.max() - depth.min() + 1e-6)
                    depth_img = Image.fromarray((depth_norm * 255).astype(np.uint8))
                    
                    # Store for gallery
                    depth_maps.append(depth_img)
                    original_images.append(image)
                    filenames.append(file.name)
                    
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
                    
                    # Show live preview if enabled
                    if settings.get("show_live_preview", True):
                        with preview_container:
                            # Show thumbnail comparison for current image
                            preview_col1, preview_col2 = st.columns(2)
                            with preview_col1:
                                st.image(image, caption=f"Original - {file.name}", use_column_width=True)
                            with preview_col2:
                                st.image(depth_img, caption="Depth Map", use_column_width=True)
                    
                except Exception as e:
                    st.error(f"Error processing {file.name}: {e}")
                    status_text.text(f"❌ Failed: {file.name}")
                
                progress_bar.progress((idx + 1) / total)
        
        elapsed_time = time.time() - start_time
        status_text.empty()
        progress_bar.empty()
        
        st.success(f"✅ Processing complete in {elapsed_time:.1f}s!")
    
    with tab2:
        # Show gallery
        st.markdown("### 📸 Results Gallery")
        
        # Create grid of results
        cols = st.columns(2)
        for idx, (orig, depth, name) in enumerate(zip(original_images, depth_maps, filenames)):
            with cols[idx % 2]:
                render_comparison_slider(orig, depth, title=os.path.splitext(name)[0])
    
    # Final download button
    with placeholder.container():
        st.divider()
        st.markdown("### ⬇️ Download Results")
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📦 Download All (ZIP)",
                data=zip_buffer.getvalue(),
                file_name="depth_maps.zip",
                mime="application/zip",
                type="primary",
                use_container_width=True
            )
        
        with col2:
            st.info(f"✨ {len(depth_maps)} images processed successfully!")
        
        # Show stats
        render_results_summary(len(depth_maps), elapsed_time, ["PNG Depth", "JPEG 3D"])

if __name__ == "__main__":
    main()
