from dotenv import load_dotenv 
load_dotenv() 

import streamlit as st 
import os 
import google.generativeai as genai 

# Set page configuration - this MUST be the first Streamlit command
st.set_page_config(page_title="SMART_BOT")

# Google Generative AI configuration
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro") 

def my_output(query):
    response = model.generate_content(query) 
    return response.text 

#### UI Development using streamlit 
st.header("SMART_BOT") 
input = st.text_input("Input ", key="input")  
submit = st.button("Ask your query") 

if submit:
    response = my_output(input) 
    st.subheader("The Response is=")
    st.write(response)

#### Add Image Generation Functionality ####

from diffusers import StableDiffusionXLPipeline
import torch
from PIL import Image as PILImage
from io import BytesIO

# Set up the model for image generation
pipe = StableDiffusionXLPipeline.from_pretrained(
    "segmind/SSD-1B",
    torch_dtype=torch.float16,
    use_safetensors=True,
    variant="fp16"
)

# Check if CUDA is available, otherwise use CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
pipe.to(device)

# Prompt and negative prompt for image generation
prompt = "A football player whose name is Ronaldo who is cheering for winning a match"
neg_prompt = "ugly, blurry, poor quality"

# Generate the image when the button is clicked
if submit:
    image = pipe(prompt=prompt, negative_prompt=neg_prompt).images[0]
    
    # Display the image using Streamlit
    st.subheader("Generated Image:")
    st.image(image, caption="Generated by StableDiffusionXLPipeline")
