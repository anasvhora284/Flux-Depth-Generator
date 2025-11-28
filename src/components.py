"""Reusable UI components for the application."""

import streamlit as st
from PIL import Image
import numpy as np


def render_comparison_slider(original_image, depth_image, title="Comparison"):
    """Render an interactive before/after comparison slider.
    
    Args:
        original_image: PIL Image or numpy array (original)
        depth_image: PIL Image or numpy array (depth map)
        title: Title for the comparison
    """
    # Convert to numpy if needed
    if isinstance(original_image, Image.Image):
        orig_array = np.array(original_image)
    else:
        orig_array = original_image
    
    if isinstance(depth_image, Image.Image):
        depth_array = np.array(depth_image)
    else:
        depth_array = depth_image
    
    # Ensure same size
    if orig_array.shape != depth_array.shape:
        # Resize depth to match original
        depth_image = Image.fromarray(depth_array).resize((orig_array.shape[1], orig_array.shape[0]))
        depth_array = np.array(depth_image)
    
    st.markdown(f"### {title}")
    
    # Use slider to control blend
    slider_value = st.slider(
        "Drag to compare",
        min_value=0,
        max_value=100,
        value=50,
        key=f"comparison_{id(original_image)}"
    )
    
    # Create blended image
    blend_ratio = slider_value / 100.0
    if len(orig_array.shape) == 2:  # Grayscale
        combined = (orig_array * (1 - blend_ratio) + depth_array * blend_ratio).astype(np.uint8)
    else:  # RGB
        combined = (orig_array * (1 - blend_ratio) + depth_array[:, :, :3] * blend_ratio).astype(np.uint8)
    
    # Create side-by-side view with overlay indicator
    st.image(combined, use_column_width=True)
    
    # Show labels
    col1, col2 = st.columns(2)
    with col1:
        st.caption("← Original")
    with col2:
        st.caption("Depth Map →")


def render_preview_gallery(images, titles=None, columns=4):
    """Render a grid gallery of images.
    
    Args:
        images: List of PIL Images or numpy arrays
        titles: Optional list of titles for each image
        columns: Number of columns in grid
    """
    st.markdown("### Results Gallery")
    
    if not images:
        st.info("No images to display")
        return
    
    cols = st.columns(columns)
    for idx, image in enumerate(images):
        with cols[idx % columns]:
            st.image(image, use_column_width=True)
            if titles and idx < len(titles):
                st.caption(titles[idx])


def render_upload_zone():
    """Render an enhanced upload zone with better feedback."""
    st.markdown("### 📤 Upload Images")
    st.markdown("*Drag and drop your images here or click to select*")
    
    uploaded_files = st.file_uploader(
        "Choose images",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    
    if uploaded_files:
        # Show summary
        total_size = sum(f.size for f in uploaded_files) / (1024 * 1024)  # MB
        st.success(f"✅ {len(uploaded_files)} file(s) selected • {total_size:.2f} MB")
        
        # Show quick preview
        st.markdown("**Preview:**")
        cols = st.columns(min(4, len(uploaded_files)))
        for i, file in enumerate(uploaded_files[:4]):
            with cols[i % 4]:
                from PIL import Image
                image = Image.open(file)
                st.image(image, use_column_width=True, caption=file.name)
        
        if len(uploaded_files) > 4:
            st.caption(f"...and {len(uploaded_files) - 4} more")
    
    return uploaded_files


def render_processing_progress(current, total, current_filename=""):
    """Render a beautiful progress indicator.
    
    Args:
        current: Current item number (0-indexed)
        total: Total items
        current_filename: Current file being processed
    """
    progress = current / total if total > 0 else 0
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.progress(progress)
    with col2:
        st.metric("Progress", f"{int(progress*100)}%")
    
    if current_filename:
        st.caption(f"Processing: {current_filename}")


def render_results_summary(total_files, processing_time, output_formats):
    """Render a summary of processing results.
    
    Args:
        total_files: Number of files processed
        processing_time: Total processing time in seconds
        output_formats: List of output format strings
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Files Processed", total_files)
    
    with col2:
        st.metric("Processing Time", f"{processing_time:.1f}s")
    
    with col3:
        st.metric("Output Formats", len(output_formats))


def render_depth_options():
    """Render controls for depth visualization options."""
    st.markdown("### 🎨 Depth Visualization")
    
    col1, col2 = st.columns(2)
    
    with col1:
        colormap = st.selectbox(
            "Colormap",
            ["grayscale", "viridis", "plasma", "inferno", "turbo", "jet", "heatmap", "edges"],
            help="Select how depth is visualized"
        )
    
    with col2:
        invert_depth = st.checkbox("Invert Depth", help="Swap near/far colors")
    
    return colormap, invert_depth


def render_batch_settings():
    """Render batch processing settings."""
    st.markdown("### ⚙️ Batch Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        model_preset = st.selectbox(
            "Model Preset",
            ["vits (Fast)", "vitb (Balanced)", "vitl (Quality)"],
            help="Choose speed vs accuracy tradeoff"
        )
    
    with col2:
        output_format = st.selectbox(
            "Output Format",
            ["Both (PNG + JPEG)", "Depth Only (PNG)", "3D Only (JPEG)"],
            help="What to generate"
        )
    
    return model_preset, output_format


def render_depth_range_sliders():
    """Render depth range adjustment sliders."""
    st.markdown("### 📏 Depth Range Adjustment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        near = st.slider(
            "Near Distance",
            0, 100, 0,
            help="Exclude closer objects (percentage)"
        )
    
    with col2:
        far = st.slider(
            "Far Distance", 
            0, 100, 100,
            help="Exclude distant objects (percentage)"
        )
    
    return near, far