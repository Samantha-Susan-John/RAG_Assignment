import os
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """Extract text from a single PDF file."""
    with fitz.open(pdf_path) as pdf:
        text = ""
        for page in pdf:
            text += page.get_text()
    return text

def parse_all_pdfs(pdf_directory):
    """Parse all PDFs in a directory, including subfolders."""
    all_text = ""
    for root, dirs, files in os.walk(pdf_directory):
        for file in files:
            if file.endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                text = extract_text_from_pdf(pdf_path)
                all_text += text + "\n\n"
    return all_text

pdf_directory = 'data/'  
ncert_text = parse_all_pdfs(pdf_directory)
with open('data/ncert_combined_text.txt', 'w') as f:
    f.write(ncert_text)
