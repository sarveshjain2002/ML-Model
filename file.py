from PyPDF2 import PdfReader
from PIL import Image
from io import BytesIO
import os
import tkinter as tk
from tkinter import filedialog

def extract_text_and_images(pdf_path, output_file="output.txt", image_folder="images"):
    text_content = ""

    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            
            # Extract text
            text_content += page.extract_text()

            # Extract images
            images = extract_images_from_page(page, page_num, image_folder)
            
            for img_index, image in enumerate(images):
                img_index_str = f"{page_num + 1}_{img_index + 1}"
                image_path = os.path.join(image_folder, f"image_{img_index_str}.png")
                image.save(image_path)

    # Save text and image information to a single text file
    with open(output_file, 'w', encoding='utf-8') as output_file:
        output_file.write("Text Content:\n")
        output_file.write(text_content)
        output_file.write("\n\nImage Information:\n")
        for page_num in range(len(pdf_reader.pages)):
            images = extract_images_from_page(pdf_reader.pages[page_num], page_num, image_folder)
            for img_index in range(len(images)):
                img_index_str = f"{page_num + 1}_{img_index + 1}"
                image_path = os.path.join(image_folder, f"image_{img_index_str}.png")
                output_file.write(f"Page {page_num + 1}, Image {img_index + 1}:\n")
                output_file.write(f"Image Path: {image_path}\n\n")

def extract_images_from_page(page, page_num, image_folder):
    images = []
    if '/Resources' in page and '/XObject' in page['/Resources']:
        x_objects = page['/Resources']['/XObject'].getObject()
        for obj_name in x_objects:
            image = x_objects[obj_name]
            if image['/Subtype'] == '/Image':
                try:
                    image_data = image._data
                    image_stream = BytesIO(image_data)
                    image = Image.open(image_stream)
                    images.append(image)
                except Exception as e:
                    print(f"Error processing image on Page {page_num + 1}, Object {obj_name}: {e}")
    return images

def browse_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        output_file = "output.txt"
        image_folder = "images"
        os.makedirs(image_folder, exist_ok=True)
        extract_text_and_images(file_path, output_file, image_folder)
        print(f"Text content and image information saved to: {output_file}")

# Create a simple GUI for browsing the PDF file
root = tk.Tk()
root.withdraw()  # Hide the main window

# Call the function to browse and process the selected PDF file
browse_pdf()
