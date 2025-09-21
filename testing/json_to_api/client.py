import requests
import json



def process_receipt_api(image_paths, api_url="http://localhost:8000/process-receipt/"):

    results = []
    for image_path in image_paths:
        try:

            with open(image_path, 'rb') as file:
                files = {'file': file}
                response = requests.post(api_url, files=files)
                
            
            if response.status_code == 200:
                result = response.json()
                result['image_path'] = image_path
                results.append(result)

            else:
                return {"error": f"API request failed with status {response.status_code}"}
            
        except Exception as e:
            error_result = {
                "image_path": image_path,
                "error": f"Exception occured: {str(e)}"
            }
            results.append(error_result)
        
    return results



if __name__ == "__main__":
    # Usage

    image_paths = [
    "/home/manish/Desktop/projects/etfp/temp/image_19.png",
    "/home/manish/Desktop/projects/etfp/temp/Bill Image_Receipt.png",
    "/home/manish/Desktop/projects/etfp/temp/good-hand-written-bill.jpg",
    "/home/manish/Desktop/projects/etfp/temp/image_20.png"
    ]

    result = process_receipt_api(image_paths=image_paths)
    print(result)
    # print(f"output have client: {json.dumps(result, indent=2)}")