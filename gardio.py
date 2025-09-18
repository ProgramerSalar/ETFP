import gradio as gr
from PIL import Image
import pytesseract

custom_css = """
    .big-font textarea {
        font-size: 20px !important;
    }
"""


from PIL import Image
import io 

def image_format(image_path):
    
    # Open the image file using Pillow
        img = Image.open(image_path)
        
        print(img)
        
        # Create a BytesIO object to store the image in memory
        img_byte_arr = io.BytesIO()
        
        # Save the image to the BytesIO object. The format is inferred from the original file extension.
        # You can specify the format like: img.save(img_byte_arr, format='PNG')
        img.save(img_byte_arr, format=img.format)
        
        # Get the byte data from the BytesIO object
        image_bytes = img_byte_arr.getvalue()
        
        # Return the data in the specified list of dictionaries format
        image_parts = [
            {
                "mime_type": "image/png",
                "data": image_bytes
            }
        ]
        
        return image_parts




def extract_text(image_path):
    
    output = image_format(image_path)
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