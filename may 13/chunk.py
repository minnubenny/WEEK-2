import PyPDF2

def extract_text_from_pdf(file_path):
    """Extracts all text from a PDF file."""
    reader = PyPDF2.PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def chunk_text_simple(text, chunk_size=1000):
    """Splits text into chunks of fixed size (characters)."""
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def chunk_pdf_text(file_path, chunk_size=1000):
    """Extracts and chunks text from a PDF."""
    full_text = extract_text_from_pdf(file_path)
    return chunk_text_simple(full_text, chunk_size)

# Example usage:
if __name__ == "__main__":
    pdf_path = "/home/minnu/Desktop/week 2/may 13/aiml_short_notes.pdf"  # Replace with your actual file
    chunks = chunk_pdf_text(pdf_path, chunk_size=800)

    for i, chunk in enumerate(chunks):
        print(f"\n--- Chunk {i+1} ---\n{chunk}")
