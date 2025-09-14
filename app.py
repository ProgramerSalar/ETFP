import gradio as gr
from PIL import Image
import pytesseract

custom_css = """
    .big-font textarea {
        font-size: 20px !important;
    }
"""

def extract_text(image):
    # Convert the image to text using pytesseract
    text = pytesseract.image_to_string(image)
    return text

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