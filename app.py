import streamlit as st
import pandas as pd
from PIL import Image
import os

# Paths 
PROJECT_DIR = os.path.dirname(__file__)  # folder where app.py is
IMAGE_DIR = os.path.join(PROJECT_DIR, "images")  # folder for images
CSV_PATH = os.path.join(PROJECT_DIR, "yoruba_gold_200.csv")

# Make sure the images folder exists
os.makedirs(IMAGE_DIR, exist_ok=True)

# Load data
df = pd.read_csv(CSV_PATH)

# Rename Yoruba column
df = df.rename(columns={"Unnamed: 2": "yoruba_caption"})

st.title("Bilingual Image Captioning (English–Yoruba)")
st.write("Course Project Demo")

st.subheader("Upload a new image and captions")

# Upload new image
uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

# Input captions
english_caption = st.text_input("English Caption")
yoruba_caption = st.text_input("Yoruba Caption")

if uploaded_file and english_caption and yoruba_caption:
    # Save image to images folder
    image_name = uploaded_file.name
    image_path = os.path.join(IMAGE_DIR, image_name)

    if not os.path.exists(image_path):
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Add new row to dataframe
        new_row = {"image_name": image_name,
                   "english_caption": english_caption,
                   "yoruba_caption": yoruba_caption}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        # Save updated CSV
        df.to_csv(CSV_PATH, index=False)

        st.success(f"Image '{image_name}' and captions added successfully!")
    else:
        st.warning("This image already exists in the dataset.")

# Image selector
image_name = st.selectbox("Select an image", df["image_name"].tolist())

# Get row
row = df[df["image_name"] == image_name].iloc[0]

# Load image
image_path = os.path.join(IMAGE_DIR, image_name)
image = Image.open(image_path)

# Display image
st.image(image, caption=image_name, use_column_width=True)

# Display captions
st.subheader("English Caption")
st.write(row["english_caption"])

st.subheader("Yoruba Caption")
st.write(row["yoruba_caption"])

