import gradio as gr
import requests
import json
import tempfile
import os

def process_receipt_api(image):
    """
    Process a single receipt image using the FastAPI server
    """
    # Extract file path from tuple if needed
    if isinstance(image, tuple):
        image_path = image[0]  # Get the file path from the tuple
    else:
        image_path = image
    
    # Create a temporary file to save the image
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        # Convert the image if it's in numpy array format (from Gradio)
        if hasattr(image_path, 'shape'):  # It's a numpy array
            from PIL import Image
            pil_img = Image.fromarray(image_path)
            pil_img.save(temp_file.name)
        else:  # It's already a file path
            with open(image_path, 'rb') as f:
                temp_file.write(f.read())
        
        temp_file_path = temp_file.name
    
    # Send the image to the FastAPI server
    api_url = "http://localhost:8000/process-receipt/"
    with open(temp_file_path, 'rb') as file:
        files = {'file': file}
        response = requests.post(api_url, files=files)
    
    # Clean up
    os.unlink(temp_file_path)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            try:
                # Try to parse the JSON data if it's a string
                data = result['data']
                if isinstance(data, str):
                    data = json.loads(data)
                return data
            except json.JSONDecodeError:
                return result['data']
        else:
            return f"Error: {result.get('error', 'Unknown error')}"
    else:
        return f"API request failed with status {response.status_code}"

def process_multiple_receipts(images):
    """
    Process multiple receipt images
    """
    results = []
    for image in images:
        result = process_receipt_api(image)
        results.append(result)
    return results

# Create the Gradio interface
with gr.Blocks(title="Receipt Processor") as demo:
    gr.Markdown("# Receipt Processing App")
    gr.Markdown("Upload receipt images to extract data in JSON format")
    
    with gr.Tab("Single Receipt"):
        with gr.Row():
            with gr.Column():
                image_input = gr.Image(label="Upload Receipt", type="filepath")
                process_btn = gr.Button("Process Receipt")
            with gr.Column():
                json_output = gr.JSON(label="Extracted Data")
        
        process_btn.click(
            fn=process_receipt_api,
            inputs=image_input,
            outputs=json_output
        )
    
    with gr.Tab("Multiple Receipts"):
        with gr.Row():
            with gr.Column():
                gallery_input = gr.Gallery(
                    label="Upload Multiple Receipts",
                    type="filepath"
                )
                process_multiple_btn = gr.Button("Process All Receipts")
            with gr.Column():
                multiple_json_output = gr.JSON(label="Extracted Data from All Receipts")
        
        process_multiple_btn.click(
            fn=process_multiple_receipts,
            inputs=gallery_input,
            outputs=multiple_json_output
        )

if __name__ == "__main__":
    # Start the Gradio app
    demo.launch(server_name="0.0.0.0", server_port=7860)