import streamlit as st
import pandas as pd
from PIL import Image
import os

# Paths
PROJECT_DIR = os.path.dirname(__file__)
IMAGE_DIR = os.path.join(PROJECT_DIR, "images")
CSV_PATH = os.path.join(PROJECT_DIR, "yoruba_gold_200.csv")

# Make sure images folder exists
os.makedirs(IMAGE_DIR, exist_ok=True)

# Load dataset
df = pd.read_csv(CSV_PATH)
df = df.rename(columns={"Unnamed: 2": "yoruba_caption"})

st.title("Bilingual Image Captioning (English–Yoruba)")
st.write("Course Project Demo")

# ------------------------------------------
# Section 1: Upload new image + captions
# ------------------------------------------
st.subheader("Upload a new image and captions")
uploaded_file = st.file_uploader("Choose an image to add to the dataset", type=["jpg", "jpeg", "png"], key="new")
english_caption = st.text_input("English Caption", key="new_en")
yoruba_caption = st.text_input("Yoruba Caption", key="new_yo")

if uploaded_file and english_caption and yoruba_caption:
    image_name = uploaded_file.name
    image_path = os.path.join(IMAGE_DIR, image_name)

    if not os.path.exists(image_path):
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        # Update CSV
        new_row = {"image_name": image_name,
                   "english_caption": english_caption,
                   "yoruba_caption": yoruba_caption}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(CSV_PATH, index=False)
        st.success(f"Image '{image_name}' and captions added successfully!")
    else:
        st.warning("This image already exists in the dataset.")

# ------------------------------------------
# Section 2: Display existing images
# ------------------------------------------
st.subheader("View existing images from dataset")
image_name = st.selectbox("Select an image from the dataset", df["image_name"].tolist(), key="select")
row = df[df["image_name"] == image_name].iloc[0]
image_path = os.path.join(IMAGE_DIR, image_name)
image = Image.open(image_path)
st.image(image, caption=image_name, use_column_width=True)
st.write("**English Caption:**", row["english_caption"])
st.write("**Yoruba Caption:**", row["yoruba_caption"])

# ------------------------------------------
# Section 3: Upload an existing image to see captions only
# ------------------------------------------
st.subheader("Upload an existing image to see captions (without saving)")
uploaded_existing = st.file_uploader("Choose an image to view captions", type=["jpg", "jpeg", "png"], key="existing")

if uploaded_existing:
    image_name = uploaded_existing.name
    st.image(uploaded_existing, caption=image_name, use_column_width=True)
    # Look up in CSV
    if image_name in df["image_name"].values:
        row = df[df["image_name"] == image_name].iloc[0]
        st.write("**English Caption:**", row["english_caption"])
        st.write("**Yoruba Caption:**", row["yoruba_caption"])
    else:
        st.warning("This image is not in the dataset.")
