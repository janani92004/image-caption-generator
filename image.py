import streamlit as st
from PIL import Image
import google.generativeai as genai
import io

# Set up the Google Gemini API key
genai.configure(api_key="")

def generate_caption(image_bytes):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        # Pass the image data as a blob directly
        response = model.generate_content([{"mime_type": "image/png", "data": image_bytes}])
        return response.text
    except Exception as e:
        return f"Error: {e}"

def main():
    st.title("🖼️ Image Caption Generator with Google Gemini")
    st.write("Upload an image, and I'll generate a caption for you!")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Convert the image to bytes for the Gemini model
        img_bytes = io.BytesIO()
        image.save(img_bytes, format="PNG")
        img_bytes = img_bytes.getvalue()

        if st.button("Generate Caption"):
            with st.spinner("Generating caption..."):
                caption = generate_caption(img_bytes)
                if "Error" not in caption:
                    st.success("**Generated Caption:**")
                    st.write(caption)
                else:
                    st.error(caption)

if __name__ == "__main__":
    main()
