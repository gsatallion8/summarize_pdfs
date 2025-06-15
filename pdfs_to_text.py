import os
import fitz  # PyMuPDF
import pytesseract
from pathlib import Path
from PIL import Image
import io

DPI_VALUE = 300  # DPI for image extraction

def pdf_to_text(pdf_path: Path, output_dir: Path):
    """
    Performs OCR on a single PDF and writes the result to a .txt file.
    """
    doc = fitz.open(pdf_path)
    text_output = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=300)  # High resolution for OCR
        image = Image.open(io.BytesIO(pix.tobytes("png")))
        text = pytesseract.image_to_string(image)
        text_output.append(f"\n\n--- Page {page_num + 1} ---\n{text.strip()}")

    output_text_file = output_dir / f"{pdf_path.stem}.txt"
    with open(output_text_file, "w", encoding="utf-8") as f:
        f.write("\n".join(text_output))

    print(f"Processed: {pdf_path.name}")

def pdfs_to_text(input_folder: str, output_folder: str):
    """
    Processes all PDFs in the input folder using OCR and writes .txt outputs.
    """
    input_dir = Path(input_folder)
    output_dir = Path(output_folder)
    output_dir.mkdir(parents=True, exist_ok=True)

    pdf_files = list(input_dir.glob("*.pdf"))
    if not pdf_files:
        print("No PDF files found.")
        return

    for pdf_file in pdf_files:
        pdf_to_text(pdf_file, output_dir)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Perform OCR on all PDFs in a folder.")
    parser.add_argument("input_folder", help="Path to folder containing PDF files")
    parser.add_argument("output_folder", help="Path to folder for output text files")

    args = parser.parse_args()
    pdfs_to_text(args.input_folder, args.output_folder)
