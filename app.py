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

st.subheader("Yoruba Caption (Reference)")
st.write(row["yoruba_caption"])
