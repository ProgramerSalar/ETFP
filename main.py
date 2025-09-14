import pytesseract
from PIL import Image 


def extract_text(image_path):
    img = Image.open(image_path)
    et = pytesseract.image_to_string(img)

    return et 



# if __name__ == "__main__":
#     text = extract_text(image_path="/home/manish/Desktop/projects/etfp/data/WhatsApp Image 2025-09-13 at 19.01.52.jpeg")
#     print(text)

