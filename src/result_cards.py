"""Result card components for displaying processed depth maps."""

import streamlit as st
from PIL import Image
import io
import base64


def image_to_base64(image):
    """Convert PIL Image to base64 string for embedding in HTML."""
    if isinstance(image, Image.Image):
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"
    return None


def render_result_card(original_image, depth_image, filename, index=0):
    """Render a beautiful result card with comparison slider.
    
    Args:
        original_image: PIL Image (original)
        depth_image: PIL Image (depth map)
        filename: String filename for the image
        index: Integer for unique key generation
    """
    orig_b64 = image_to_base64(original_image)
    depth_b64 = image_to_base64(depth_image)
    
    if not orig_b64 or not depth_b64:
        st.error(f"Failed to process {filename}")
        return
    
    # HTML/CSS card with interactive comparison slider
    card_html = f"""
    <div class="result-card" style="margin-bottom: 2rem;">
        <div class="card-header">
            <h3 class="card-title">{filename}</h3>
            <span class="card-status">Processed</span>
        </div>
        
        <div class="comparison-slider-container">
            <img src="{orig_b64}" alt="Original" class="comparison-img original-img">
            <img src="{depth_b64}" alt="Depth Map" class="comparison-img depth-img">
            <input type="range" min="0" max="100" value="50" class="comparison-slider" id="slider-{index}">
            <div class="comparison-labels">
                <span class="label-left">Original</span>
                <span class="label-right">Depth Map</span>
            </div>
        </div>
        
        <div class="card-actions">
            <button class="action-btn btn-download" onclick="downloadImage('{filename}', 'depth')">
                Download Depth
            </button>
            <button class="action-btn btn-copy" onclick="copyToClipboard('{index}')">
                Copy Image
            </button>
            <button class="action-btn btn-view" onclick="viewFullSize('{index}')">
                View Full
            </button>
        </div>
    </div>
    
    <style>
        .result-card {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: var(--radius-lg);
            padding: var(--space-xl);
            box-shadow: var(--shadow-md);
            transition: all var(--transition-base);
        }}
        
        .result-card:hover {{
            border-color: var(--primary);
            box-shadow: var(--shadow-lg);
            transform: translateY(-2px);
        }}
        
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: var(--space-lg);
            padding-bottom: var(--space-md);
            border-bottom: 1px solid var(--card-border);
        }}
        
        .card-title {{
            font-size: 1.125rem;
            font-weight: 700;
            color: var(--text-primary);
            margin: 0;
            word-break: break-word;
        }}
        
        .card-status {{
            display: inline-block;
            padding: var(--space-xs) var(--space-md);
            background: rgba(16, 185, 129, 0.2);
            color: #10b981;
            border-radius: var(--radius-full);
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
        }}
        
        .comparison-slider-container {{
            position: relative;
            width: 100%;
            overflow: hidden;
            border-radius: var(--radius-md);
            margin-bottom: var(--space-lg);
            aspect-ratio: 16/9;
            background: var(--bg-secondary);
        }}
        
        .comparison-img {{
            position: absolute;
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        
        .original-img {{
            left: 0;
        }}
        
        .depth-img {{
            right: 0;
            clip-path: inset(0 0 0 50%);
            transition: clip-path var(--transition-fast);
        }}
        
        .comparison-slider {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0;
            cursor: col-resize;
            z-index: 5;
        }}
        
        .comparison-slider::-webkit-slider-thumb {{
            -webkit-appearance: none;
            appearance: none;
            width: 4px;
            height: 100%;
            background: var(--primary);
            cursor: col-resize;
            box-shadow: -2px 0 8px rgba(0, 0, 0, 0.3);
        }}
        
        .comparison-slider::-moz-range-thumb {{
            width: 4px;
            height: 100%;
            background: var(--primary);
            cursor: col-resize;
            border: none;
            border-radius: 0;
            box-shadow: -2px 0 8px rgba(0, 0, 0, 0.3);
        }}
        
        .comparison-labels {{
            position: absolute;
            top: var(--space-md);
            left: 0;
            right: 0;
            display: flex;
            justify-content: space-between;
            padding: 0 var(--space-lg);
            font-size: 0.875rem;
            font-weight: 600;
            z-index: 4;
            pointer-events: none;
        }}
        
        .label-left {{
            color: white;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
        }}
        
        .label-right {{
            color: white;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
        }}
        
        .card-actions {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: var(--space-md);
        }}
        
        .action-btn {{
            padding: var(--space-md) var(--space-lg);
            border: none;
            border-radius: var(--radius-md);
            font-weight: 600;
            font-size: 0.875rem;
            cursor: pointer;
            transition: all var(--transition-fast);
            text-align: center;
            text-decoration: none;
        }}
        
        .btn-download {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            box-shadow: var(--shadow-sm);
        }}
        
        .btn-download:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }}
        
        .btn-copy {{
            background: var(--card-border);
            color: var(--text-primary);
            box-shadow: var(--shadow-sm);
        }}
        
        .btn-copy:hover {{
            background: var(--primary);
            color: white;
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }}
        
        .btn-view {{
            background: transparent;
            border: 2px solid var(--primary);
            color: var(--primary);
        }}
        
        .btn-view:hover {{
            background: var(--primary);
            color: white;
            transform: translateY(-2px);
        }}
        
        @media (max-width: 768px) {{
            .result-card {{
                padding: var(--space-lg);
                margin-bottom: 1.5rem;
            }}
            
            .card-header {{
                flex-direction: column;
                align-items: flex-start;
                gap: var(--space-md);
            }}
            
            .card-title {{
                font-size: 1rem;
            }}
            
            .comparison-slider-container {{
                aspect-ratio: 4/3;
                margin-bottom: var(--space-lg);
            }}
            
            .card-actions {{
                grid-template-columns: 1fr;
                gap: var(--space-md);
            }}
            
            .action-btn {{
                padding: var(--space-md) var(--space-lg);
                font-size: 0.85rem;
                min-height: 44px;
            }}
            
            .comparison-labels {{
                font-size: 0.7rem;
                padding: 0 var(--space-md);
            }}
        }}
        
        @media (max-width: 480px) {{
            .result-card {{
                padding: var(--space-md);
            }}
            
            .card-header {{
                margin-bottom: var(--space-md);
            }}
            
            .card-title {{
                font-size: 0.95rem;
                word-break: break-word;
            }}
            
            .card-status {{
                font-size: 0.65rem;
                padding: var(--space-xs) var(--space-sm);
            }}
            
            .comparison-slider-container {{
                aspect-ratio: 3/2;
                margin-bottom: var(--space-md);
            }}
            
            .comparison-labels {{
                font-size: 0.65rem;
                padding: 0 var(--space-sm);
            }}
            
            .card-actions {{
                grid-template-columns: 1fr;
                gap: 0.5rem;
            }}
            
            .action-btn {{
                padding: 0.6rem 0.8rem;
                font-size: 0.8rem;
                min-height: 40px;
                width: 100%;
            }}
        }}
    </style>
    
    <script>
        (function() {{
            const slider = document.getElementById('slider-{index}');
            const depthImg = slider.parentElement.querySelector('.depth-img');
            
            if (slider && depthImg) {{
                slider.addEventListener('input', function() {{
                    const percentage = this.value;
                    depthImg.style.clipPath = `inset(0 0 0 ${{100 - percentage}}%)`;
                }});
                
                // Touch support for mobile
                slider.addEventListener('touchmove', function(e) {{
                    e.preventDefault();
                    const container = slider.parentElement;
                    const rect = container.getBoundingClientRect();
                    const x = e.touches[0].clientX - rect.left;
                    const percentage = (x / rect.width) * 100;
                    slider.value = Math.max(0, Math.min(100, percentage));
                    const event = new Event('input', {{ bubbles: true }});
                    slider.dispatchEvent(event);
                }});
                
                // Initialize
                const percentage = slider.value;
                depthImg.style.clipPath = `inset(0 0 0 ${{100 - percentage}}%)`;
            }}
        }})();
    </script>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)


def render_results_gallery(original_images, depth_images, filenames):
    """Render a full gallery of result cards.
    
    Args:
        original_images: List of PIL Images
        depth_images: List of PIL Images (depth maps)
        filenames: List of filenames
    """
    st.markdown("## Results Gallery")
    
    if not original_images:
        st.info("No results to display")
        return
    
    st.caption(f"Showing {len(original_images)} processed image(s)")
    
    # Render each result as a card
    for idx, (orig, depth, filename) in enumerate(zip(original_images, depth_images, filenames)):
        render_result_card(orig, depth, filename, index=idx)


def render_download_summary(total_files, elapsed_time, output_formats):
    """Render a professional summary before download.
    
    Args:
        total_files: Number of files processed
        elapsed_time: Processing time in seconds
        output_formats: List of output format strings
    """
    summary_html = f"""
    <div class="summary-card">
        <div class="summary-header">
            <h2>Processing Complete!</h2>
        </div>
        
        <div class="summary-stats">
            <div class="summary-stat">
                <span class="stat-icon"></span>
                <span class="stat-label">Files Processed</span>
                <span class="stat-value">{total_files}</span>
            </div>
            <div class="summary-stat">
                <span class="stat-icon"></span>
                <span class="stat-label">Processing Time</span>
                <span class="stat-value">{elapsed_time:.1f}s</span>
            </div>
            <div class="summary-stat">
                <span class="stat-icon"></span>
                <span class="stat-label">Output Formats</span>
                <span class="stat-value">{len(output_formats)}</span>
            </div>
        </div>
        
        <p class="summary-message">Your depth maps have been generated successfully. Download the complete package below or select individual images from the gallery above.</p>
    </div>
    
    <style>
        .summary-card {{
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            border: 2px solid var(--primary);
            border-radius: var(--radius-lg);
            padding: var(--space-xl);
            margin: var(--space-xl) 0;
        }}
        
        .summary-header {{
            text-align: center;
            margin-bottom: var(--space-lg);
        }}
        
        .summary-header h2 {{
            font-size: 1.75rem;
            margin: 0;
            color: var(--primary);
        }}
        
        .summary-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: var(--space-lg);
            margin-bottom: var(--space-lg);
        }}
        
        .summary-stat {{
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: var(--space-lg);
            background: var(--card-bg);
            border-radius: var(--radius-md);
            border: 1px solid var(--card-border);
        }}
        
        .stat-icon {{
            font-size: 2rem;
            margin-bottom: var(--space-sm);
        }}
        
        .stat-label {{
            font-size: 0.875rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: var(--space-xs);
        }}
        
        .stat-value {{
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary);
        }}
        
        .summary-message {{
            text-align: center;
            color: var(--text-secondary);
            font-size: 0.95rem;
            margin: 0;
        }}
        
        @media (max-width: 768px) {{
            .summary-card {{
                padding: var(--space-lg);
                margin: var(--space-lg) 0;
            }}
            
            .summary-header h2 {{
                font-size: 1.5rem;
            }}
            
            .summary-stats {{
                grid-template-columns: 1fr;
                gap: var(--space-md);
            }}
            
            .summary-stat {{
                padding: var(--space-lg);
            }}
            
            .stat-icon {{
                font-size: 1.75rem;
            }}
            
            .stat-value {{
                font-size: 1.25rem;
            }}
            
            .summary-message {{
                font-size: 0.9rem;
                line-height: 1.5;
            }}
        }}
        
        @media (max-width: 480px) {{
            .summary-card {{
                padding: var(--space-md);
                margin: var(--space-md) 0;
                border-radius: var(--radius-md);
            }}
            
            .summary-header h2 {{
                font-size: 1.3rem;
            }}
            
            .summary-stats {{
                gap: var(--space-sm);
            }}
            
            .summary-stat {{
                padding: var(--space-md);
            }}
            
            .stat-icon {{
                font-size: 1.5rem;
                margin-bottom: var(--space-xs);
            }}
            
            .stat-label {{
                font-size: 0.75rem;
            }}
            
            .stat-value {{
                font-size: 1.1rem;
            }}
        }}
    </style>
    """
    
    st.markdown(summary_html, unsafe_allow_html=True)
