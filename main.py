import pytesseract
from PIL import Image 
import json
import re

def extract_text(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)

    return text


def convert_to_json(text):

    result = {
        "invoice_no": "",
        "invoice_type": "",
        "seller": {
            "name": "",
            "address": "",
            "gstin": "",
            "state": {
                "name": "",
                "code": ""
            }
        },
        "buyer": {
            "name": "",
            "gstin": "",
            "state": {
                "name": "",
                "code": ""
            }
        },
        "invoice_details": {
            "number": "",
            "date": "",
            "reference_number": "",
            "reference_date": "",
            "buyer_order_no": "",
            "dispatch_document_no": "",
            "dispatch_date": "",
            "dispatched_through": "",
            "destination": "",
            "terms_of_payment": ""
        },
        "items": [],
        "tax_details": {
            "taxable_value": 0,
            "cgst": {
                "rate": 0,
                "amount": 0
            },
            "sgst": {
                "rate": 0,
                "amount": 0
            },
            "cess": {
                "on_quantity": 0,
                "on_value": 0,
                "amount": 0
            },
            "total_tax_amount": 0
        },
        "total_amount": 0,
        "amount_in_words": "",
        "declaration": "",
        "signature": ""
    }

        # Split text into lines for processing
    lines = text.split('\n')
    
    # Process each line to extract information
    for i, line in enumerate(lines):
        line = line.strip()
        print(f"line: {line}")

        # Extract invoice type 
        if "Tax Invoice" in line and not result["invoice_no"]:
            result["invoice_no"] = f"{i}"

        # Extract seller name 
        if not result["seller"]["name"] and i < 10:
            pass


    return json.dumps(result, indent=2)

        

    #     
        
        



if __name__ == "__main__":
    image_path = "/home/manish/Desktop/projects/etfp/temp/image_19.png"
    # image_path = ""
    text = extract_text(image_path)
    json_format = convert_to_json(text)
    print(json_format)

