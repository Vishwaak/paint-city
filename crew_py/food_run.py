import streamlit as st

from PIL import Image
import numpy as np
from io import BytesIO
import base64
import os
import traceback
import time
import json
from crew_py import run_agents
st.set_page_config(layout="wide", page_title="Image Background Remover")

st.write("Check it's an option to order food or cook at home")
st.write(
    "Try uploading an image of a food item to see the magic of agent-based deciosn making!"
)
st.sidebar.write("## Upload and download :gear:")

# Increased file size limit
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Max dimensions for processing
MAX_IMAGE_SIZE = 2000  # pixels

# Download the fixed image

counter = 0
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

# Resize image while maintaining aspect ratio
def resize_image(image, max_size):
    width, height = image.size
    if width <= max_size and height <= max_size:
        return image
    
    if width > height:
        new_width = max_size
        new_height = int(height * (max_size / width))
    else:
        new_height = max_size
        new_width = int(width * (max_size / height))
    
    return image.resize((new_width, new_height), Image.LANCZOS)



def fix_image(upload):
    try:
        start_time = time.time()
        progress_bar = st.sidebar.progress(0)
        status_text = st.sidebar.empty()
        
        status_text.text("Loading image...")
        progress_bar.progress(10)
        
        # Read image bytes
        if isinstance(upload, str):
            # Default image path
            if not os.path.exists(upload):
                st.error(f"Default image not found at path: {upload}")
                return
            with open(upload, "rb") as f:
                image_bytes = f.read()
        else:
            # Uploaded file
            image_bytes = upload.getvalue()
        
        status_text.text("Processing image...")
        progress_bar.progress(30)
        
        
        image = resize_image(Image.open(BytesIO(image_bytes)), MAX_IMAGE_SIZE)
        
        if image is None:
            return
      
        global counter
        
        image.save(f"food_images/food_item_{counter}.png")
        image_path = f"food_images/food_item_{counter}.png"

        counter += 1   
        runner = run_agents()

        food_name = runner.get_food_name(image_path)
        status_text.text(f"Identified food: {food_name}")
        print(f"Identified food: {food_name}")

        progress_bar.progress(60)
        status_text.text(f"Running agents to decide wheather you should eat {food_name}...")
        decision_data = runner.run_agents(food_name)


        progress_bar.progress(90)
        status_text.text("Parsing Results...")
        
        
        # Parse decision JSON for reason and best option
        try:
            print(decision_data)
            reason = decision_data.get("reason", "No reason provided.")
            best_option = decision_data.get("best_option", "No option selected.")
        except Exception:
            reason = "Could not parse decision data."
            best_option = "Unknown"

        col1.write(f"**Best Option:** {best_option}")
        col1.write(f"**Reason:** {reason}")
        

        
        progress_bar.progress(100)
        processing_time = time.time() - start_time
        status_text.text(f"Completed in {processing_time:.2f} seconds")
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.sidebar.error("Failed to process image")
        # Log the full error for debugging
        print(f"Error in fix_image: {traceback.format_exc()}")

# UI Layout
col1, col2 = st.columns(2)
my_upload = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Information about limitations
with st.sidebar.expander("ℹ️ Image Guidelines"):
    st.write("""
    - Maximum file size: 10MB
    - Large images will be automatically resized
    - Supported formats: PNG, JPG, JPEG
    - Processing time depends on image size
    """)

# Process the image
if my_upload is not None:
    if my_upload.size > MAX_FILE_SIZE:
        st.error(f"The uploaded file is too large. Please upload an image smaller than {MAX_FILE_SIZE/1024/1024:.1f}MB.")
    else:
        fix_image(upload=my_upload)
else:
    # Try default images in order of preference
    default_images = ["./zebra.jpg", "./wallaby.png"]
    for img_path in default_images:
        if os.path.exists(img_path):
            fix_image(img_path)
            break
    else:
        st.info("Please upload an image to get started!")