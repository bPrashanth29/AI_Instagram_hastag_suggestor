import streamlit as st
import os
import shutil

st.title("📸 AI Instagram Hashtag Suggester")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Save the uploaded image to the expected path
    save_path = "images/uploaded_image.jpg"
    with open(save_path, "wb") as f:
        f.write(uploaded_file.read())
    
    st.image(save_path, caption="Uploaded Image", use_column_width=True)
    st.success("Image uploaded successfully!")

    if st.button("Generate Hashtags"):
        with st.spinner("Generating hashtags..."):
            # Option 1: Run the existing script using system call
            os.system("python main.py")

            # Option 2 (cleaner): If you refactor `main.py` into functions, import and call directly
            # from main import generate_hashtags_for_image
            # generate_hashtags_for_image() 

        # Read and display hashtags
        try:
            with open("output/hashtags.txt", "r") as f:
                hashtags = f.read()
            st.subheader("📌 Suggested Hashtags")
            st.code(hashtags)
        except FileNotFoundError:
            st.error("Hashtags file not found. Something went wrong.")
