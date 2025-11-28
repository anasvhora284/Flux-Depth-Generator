import streamlit as st
import os
import zipfile
import io
import torch
import numpy as np
from PIL import Image
import time
from datetime import datetime

from src.core import load_model, infer_depth, DEVICE
from src.utils import get_system_metrics, create_gdepth_xmp, embed_xmp_jpeg
from src.ui import inject_custom_css, render_header, render_footer
from src.config import load_settings, save_settings, resolve_theme
from src.components import (
    render_upload_zone, render_comparison_slider, render_preview_gallery, 
    render_processing_progress, render_results_summary,
    render_depth_options, render_batch_settings, render_depth_range_sliders,
    render_presets_manager, render_history_viewer, render_export_formats
)
from src.result_cards import render_results_gallery, render_download_summary
from src.depth_viz import apply_colormap, adjust_depth_range, create_heatmap_visualization, create_edge_detection_visualization
from src.history import HistoryManager, PresetsManager, ProcessingHistory
from src.export import DepthExporter
from src.onboarding import (
    render_welcome_modal, get_onboarding_state, mark_first_visit_complete,
    render_progress_indicator, render_tooltip, render_quick_tip, get_context_help
)

st.set_page_config(
    page_title="Depth Generator Pro",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():
    # Initialize managers
    history_manager = HistoryManager()
    presets_manager = PresetsManager()
    
    # Load settings and determine theme
    settings = load_settings()
    current_theme = resolve_theme(settings)
    
    # Inject CSS with appropriate theme
    inject_custom_css(theme_mode=current_theme, accent_color=settings.get("accent_color", "#238636"))
    
    # Render header with theme toggle
    render_header(theme_mode=current_theme)
    
    # Initialize onboarding state and show welcome modal if first visit
    onboarding_state = get_onboarding_state()
    if onboarding_state['show_welcome_modal']:
        render_welcome_modal()
        st.stop()  # Stop execution until user responds to welcome
    
    # Sidebar for settings - reorganized with progressive disclosure
    with st.sidebar:
        st.markdown("## ⚙️ Settings & Options")
        
        # QUICK START SECTION
        with st.container():
            st.markdown("### 🚀 Quick Start")
            model_type = st.selectbox(
                "Model Type",
                ["vits (Fast)", "vitb (Balanced)", "vitl (Quality)"],
                index=1,
                help="**ViT-S**: Fastest, less accurate • **ViT-B**: Best balance • **ViT-L**: Most accurate, slowest"
            )
            # Map display name back to code name
            model_type = model_type.split(" ")[0]
            
            device_status = f"✅ {DEVICE.upper()}"
            st.metric("Computing Device", device_status)
            st.caption("GPU processing is significantly faster")
        
        st.divider()
        
        # VISUALIZATION SECTION
        with st.container():
            st.markdown("### 🎨 Visualization")
            colormap, invert_depth = render_depth_options()
            near_distance, far_distance = render_depth_range_sliders()
        
        st.divider()
        
        # OUTPUT SECTION
        with st.container():
            st.markdown("### 📁 Output Formats")
            output_formats = st.multiselect(
                "Select formats to export",
                ["PNG (Depth Map)", "JPEG (3D)"],
                default=["PNG (Depth Map)", "JPEG (3D)"],
                help="Choose which output formats to generate"
            )
        
        st.divider()
        
        # ADVANCED SECTION - Collapsible
        with st.expander("🔬 Advanced Options", expanded=False):
            st.markdown("**Processing Presets**")
            render_presets_manager(presets_manager)
            
            st.divider()
            
            st.markdown("**Processing History**")
            render_history_viewer(history_manager)
        
        st.divider()
        
        # SYSTEM METRICS - Minimal, non-intrusive
        with st.container():
            st.markdown("### 📊 System Info")
            metrics_placeholder = st.empty()
            
            # Initial metrics
            cpu, mem, proc = get_system_metrics()
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("CPU", f"{cpu}%", delta=None)
            with col2:
                st.metric("RAM", f"{mem}%", delta=None)
            with col3:
                st.metric("Process", f"{proc}MB", delta=None)

    # Main content layout
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        # Show progress indicator for first-time users
        if onboarding_state['tooltips_enabled'] and not onboarding_state['onboarding_complete']:
            st.markdown("### Your Workflow")
            render_progress_indicator(
                current_step=1,
                total_steps=4,
                step_labels=["Upload", "Configure", "Process", "Export"]
            )
        
        uploaded_files = render_upload_zone()

    with col2:
        st.markdown("### Actions")
        
        # Show helpful tips for first-time users
        if onboarding_state['tooltips_enabled'] and not onboarding_state['onboarding_complete']:
            render_quick_tip(
                "Upload an image using the zone on the left, then click the button below to generate a depth map!",
                tip_type="info",
                icon="👈"
            )
        
        st.info("Click below to start processing. This may take a while depending on your hardware.")
        
        process_btn = st.button("🚀 Generate Depth Maps", type="primary", disabled=not uploaded_files, use_container_width=True)
        
        result_placeholder = st.empty()

    if process_btn and uploaded_files:
        with st.spinner("Initializing model..."):
            model = load_model(model_type)
        
        if model:
            # Collect visualization settings for processing
            processing_params = {
                "colormap": colormap,
                "invert_depth": invert_depth,
                "near_distance": near_distance,
                "far_distance": far_distance,
                "output_formats": output_formats
            }
            process_batch(uploaded_files, model, result_placeholder, settings, processing_params, history_manager, model_type)

    render_footer()

def process_batch(files, model, placeholder, settings, processing_params, history_manager, model_type):
    """Process batch of images with live preview and visualization options.
    
    Args:
        files: List of uploaded files
        model: Loaded depth model
        placeholder: Streamlit container for results
        settings: User settings dict
        processing_params: Dict with colormap, invert_depth, near_distance, far_distance, output_formats
        history_manager: HistoryManager instance
        model_type: Selected model type
    """
    colormap = processing_params.get("colormap", "grayscale")
    invert_depth = processing_params.get("invert_depth", False)
    near_distance = processing_params.get("near_distance", 0)
    far_distance = processing_params.get("far_distance", 100)
    output_formats = processing_params.get("output_formats", ["PNG (Depth Map)", "JPEG (3D)"])
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
                    
                    # Infer depth
                    depth = infer_depth(model, image)
                    
                    # Apply depth range adjustment
                    depth_adjusted = adjust_depth_range(depth, near_distance, far_distance)
                    
                    # Normalize depth for saving
                    depth_norm = (depth_adjusted - depth_adjusted.min()) / (depth_adjusted.max() - depth_adjusted.min() + 1e-6)
                    
                    # Apply colormap visualization
                    if colormap == "heatmap":
                        depth_img = create_heatmap_visualization(depth_norm, invert_depth)
                    elif colormap == "edges":
                        depth_img = create_edge_detection_visualization(depth_norm)
                    else:
                        depth_img = apply_colormap(depth_norm, colormap, invert_depth)
                    
                    # Also keep grayscale version for 3D JPEG
                    depth_grayscale = Image.fromarray((depth_norm * 255).astype(np.uint8))
                    
                    # Store for gallery
                    depth_maps.append(depth_img)
                    original_images.append(image)
                    filenames.append(file.name)
                    
                    # Save Depth PNG with selected visualization
                    if "PNG (Depth Map)" in output_formats:
                        depth_bytes = io.BytesIO()
                        depth_img.save(depth_bytes, format="PNG")
                        zip_file.writestr(f"{os.path.splitext(file.name)[0]}_depth.png", depth_bytes.getvalue())
                    
                    # Save 3D JPEG (only if selected)
                    if "JPEG (3D)" in output_formats:
                        # Use grayscale depth for XMP
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
                    continue
                
                # Record in history
                try:
                    w, h = image.size
                    file_size_kb = file.size / 1024
                    history_record = ProcessingHistory(
                        filename=file.name,
                        timestamp=datetime.now().isoformat(),
                        model_type=model_type,
                        colormap=colormap,
                        dimensions=f"{w}x{h}",
                        file_size_kb=file_size_kb
                    )
                    history_manager.add_record(history_record)
                except:
                    pass  # Don't fail if history recording fails
                
                progress_bar.progress((idx + 1) / total)
        
        elapsed_time = time.time() - start_time
        status_text.empty()
        progress_bar.empty()
        
        st.success(f"✅ Processing complete in {elapsed_time:.1f}s!")
    
    with tab2:
        # Show professional results gallery with cards
        render_results_gallery(original_images, depth_maps, filenames)
    
    # Final download section
    with placeholder.container():
        st.divider()
        
        # Show beautiful summary
        render_download_summary(len(depth_maps), elapsed_time, output_formats)
        
        # Download button
        st.download_button(
            label="📦 Download All Results (ZIP)",
            data=zip_buffer.getvalue(),
            file_name="depth_maps.zip",
            mime="application/zip",
            type="primary",
            use_container_width=True
        )

if __name__ == "__main__":
    main()
