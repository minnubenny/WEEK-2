import fitz  # This is PyMuPDF

# Open the PDF
doc = fitz.open("/home/minnu/Desktop/week 2/may 12/aiml_short_notes.pdf")  # Replace with your PDF file name

# Go through each page and print the text
for page in doc:
    text = page.get_text()
    print(text)

doc.close()
