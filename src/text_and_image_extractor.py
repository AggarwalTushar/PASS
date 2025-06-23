from docx import Document
import zipfile
import os
from docx import Document
from io import BytesIO
from PIL import Image
import argparse



def extracted_text_from_docx(file_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    doc = Document(file_path)
    data = ""
    for para in doc.paragraphs:
        print(para.text)
        data+=para.text + "\n"
    with open(os.path.join(output_dir, "file.txt"), "w") as f:
        f.write(data)
    
    
def extract_images_from_docx(docx_file, output_dir):

    
    os.makedirs(output_dir, exist_ok=True)

    with zipfile.ZipFile(docx_file, 'r') as docx:
        for file in docx.namelist():
            if file.startswith('word/media/'):
                img_data = docx.read(file)
                
                img_name = file.split('/')[-1]
                img_path = os.path.join(output_dir, img_name) 
                with open(img_path, 'wb') as img_file:
                    img_file.write(img_data)
                print(f"Image saved: {img_path}")


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--input_file", type=str, required=True, help="Path to the input document file")
    argparser.add_argument("--output_dir", type=str, required=True, help="Path to the output directory")
    args = argparser.parse_args()
    extract_images_from_docx(args.input_file, os.path.join(args.output_dir, "images"))
    extracted_text_from_docx(args.input_file, args.output_dir)
