import gradio as gr
from PIL import Image
import pytesseract
import json 

import google.generativeai as genai 
google_api = 'AIzaSyAMlYqwvuQgekl8nlqc56XTqJVBufszrBU'
genai.configure(api_key=google_api)
from pathlib import Path
from IPython.display import Markdown




from PIL import Image
import io 




# Model Configuration
MODEL_CONFIG = {
  "temperature": 0.2,
  "top_p": 1,
  "top_k": 32,
  "max_output_tokens": 4096,
}

## Safety Settings of Model
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  }
]

model = genai.GenerativeModel(model_name='gemini-2.5-flash',
                              generation_config=MODEL_CONFIG,
                              safety_settings=safety_settings)


def gemini_output(image_path,
                  system_prompt,
                  user_prompt):
    
    
    input_prompt = [system_prompt, image_path, user_prompt]
    response = model.generate_content(input_prompt)

    return response.text




custom_css = """
    .big-font textarea {
        font-size: 20px !important;
    }
"""

def extract_text(image_path):
   
    system_prompt = """
               You are a specialist in comprehending receipts.
               Input images in the form of receipts will be provided to you,
               and your task is to respond to questions based on the content of the input image.
               """
    
    user_prompt = "Convert Invoice data into json format with appropriate json tags as required for the data in image "
    output = gemini_output(image_path, system_prompt, user_prompt)

    

    output = output.replace("```json", "")
    output = output.replace("```", "")
    

    print(f">>>>>>> {output}")
    
    


    return output


# Create the Gradio interface
iface = gr.Interface(
    fn=extract_text,
    inputs=gr.Image(type="pil"),  # Accept PIL images directly
    outputs=gr.Textbox(lines=20,
                       max_lines=10,
                       label='Extracted Text',
                       elem_classes=["big-font"]
                       ),
    title="Text Extraction",
    description="Upload an image to extract text",
    allow_flagging='never',
    css=custom_css
)

# Launch the app
iface.launch()