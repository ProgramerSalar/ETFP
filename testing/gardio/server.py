import json
import google.generativeai as genai 
from pathlib import Path
import requests

from datetime import datetime, timezone

import os 
from pymongo import MongoClient
from datetime import datetime
import bson.json_util as json_util 
import json

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import tempfile, os 

import certifi
from pymongo.server_api import ServerApi


google_api = 'AIzaSyDwJYGjq4gC-weKuTcR7jlEd5q1GDzsDZE'
genai.configure(api_key=google_api)

MONGODB_URI = "mongodb://localhost:27017"
DB_NAME = "receipt_processor"
COLLECTION_NAME = "processed_receipts"


# try:
#     client = MongoClient(MONGODB_URI)
    
    
#     db = client[DB_NAME]
#     collection = db[COLLECTION_NAME]
#     print("Connected to mongodb successfully...")

# except Exception as e:
#     print(f"Error connecting to MongoDB: {e}")
#     client = None
#     collection = None
    

app = FastAPI(title="Testing api working or not ...")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# Model Configuration
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
)

def gemini_output(image_path, system_prompt, user_prompt):
    image_info = image_format(image_path)
    input_prompt = [system_prompt, image_info[0], user_prompt]
    response = model.generate_content(input_prompt)

    return response.text

    
    
    
def image_format(image_path):
    img = Path(image_path)
    if not img.exists():
        raise FileNotFoundError(f"Could not find image: {img}")
    
    image_parts = [
        {
            "mime_type": "image/png",
            "data": img.read_bytes()
        }
    ]
    return image_parts






# def save_to_mongodb(data, filename=None):

#     """Save processed receipt data to mongodb"""

#     if not client:
#         print("Mongdb client not initialized.")
#         return None
    
#     try:
#         document = {
#             "data": data,
#             "filename": filename,
#             "processed_at": datetime.now(timezone.utc),
#             "status": "processed"
#         }
#         print(f"document: {document}")

#         # Insert into mongodb 
#         result = collection.insert_one(document)
#         print(f"Data saved to MOngodb with ID: {result.inserted_id}")
#         return result.inserted_id
    
#     except Exception as e:
#         print(f"Error saving to MongoDB: {e}")
#         return None
    
    

    



@app.get("/")
async def root():
    return {"message": "Receipt Processing API is running."}



from fastapi import File, UploadFile
import requests

@app.post("/process-receipt/")
async def process_receipt(file: UploadFile = File(...)):

    try:
        # save uploded file temporarily 
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name 

            system_prompt = """You are a specialist in comprehending receipts.
            Input images in the form of receipts will be provided to you,
            and your task is to respond to questions based on the content of the input image."""

            user_prompt = "Convert Invoice data into json format with appropriate json tags as required for the data in image"


            result = gemini_output(image_path=temp_file_path,
                                system_prompt=system_prompt,
                                user_prompt=user_prompt)
            
            # print(f"result: >>>>>>>>> {result}")
            
            

            # json_data = process_receipt_api(image_path="/home/manish/Desktop/projects/etfp/bill_image_receipt.png")
            # print(f"json_data is working >>>>>>>> {json_data}")
            json_data = result.strip('```json\n').strip('```').strip()
            print(f"result: >>>>>>>>> {json_data}")

            try:
                json_data = json.loads(json_data)
            except json.JSONDecodeError:
                json_data = {"row_output": json_data}

            


            # Save to MongoDB 
            # db_id = save_to_mongodb(json_data, filename=file.filename)
            # print(f"result: >>>>>>>>> {db_id}")


            # clean up temporary file 
            os.unlink(temp_file_path)

            # return {"success": True,
            #         "data": json_data,
            #         "mongodb_id": str(db_id) if db_id else None}
        
            return {"success": True,
                    "data": json_data,
                    }
        

    except Exception as e:
        return {"success": False, "error": str(e)}
    


        
        
        




if __name__ == "__main__":

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

  


