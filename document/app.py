import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

# 1. Setup Environment
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# 2. Page Configuration (Matching your project guide)
st.set_page_config(page_title="Civil Engineering Insight Studio")
st.header("🏗️ Civil Engineering Insight Studio")

# 3. Input Prompt (The missing field you mentioned)
input_text = st.text_input("Input Prompt: ", key="input", placeholder="e.g., Focus on the structural integrity of the beams")

# 4. File Uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_container_width=True)

submit = st.button("Describe Structure")

# 5. Professional Instruction (The 'Brain' of the project)
input_prompt = """
You are a civil engineer. Please describe the structure in the image and provide details such as its type.
1. Type of structure - Description
2. Materials used - Description
Additionally, provide a detailed breakdown of each item with its respective count if applicable.
"""

# 6. Helper Functions (Updated to Gemini 2.5 to fix 404 error)
def get_gemini_response(input_text, image_parts, prompt):
    # 'gemini-2.5-flash' is the stable version for image analysis in 2026
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content([input_text, image_parts[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# 7. Execution Logic
if submit:
    if uploaded_file is not None:
        try:
            image_data = input_image_setup(uploaded_file)
            # The actual AI call
            response = get_gemini_response(input_prompt, image_data, input_text)
            
            st.subheader("Description of the Civil Engineering Structure:")
            
            # This creates the clean "Boxed" output like in your instruction images
            st.info(response) 
            
        except Exception as e:
            st.error(f"Error: {e}. If you see a 404, try updating your API key or checking your internet.")
    else:
        st.warning("Please upload an image first!")