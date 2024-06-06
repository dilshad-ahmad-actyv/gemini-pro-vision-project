import os
import streamlit as st
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

google_api_key = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=google_api_key)

## function to load gemini pro vision model and get response

def get_gemini_response(input, image, prompt):
    # load the gemini model
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:

        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]

        return image_parts
    else:
        raise FileNotFoundError("No file uploaded!")


## Initialize our streamlit app

st.set_page_config(page_title="Invoice Extractor")
input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])

image = ''

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the invoice")

input_prompt = """
    You are and expert in understanding invoices.
    You will receive input images as as invoies and 
    your job is to answer the questions based on the input image.
"""

# if submit button is clicked

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)

    st.subheader("The Response is")
    st.write(response)