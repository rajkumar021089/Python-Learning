from pypdf import PdfReader

## Reading a PDF file ##

reader = PdfReader("IntelliStay_RAG_Sample.pdf")

print("Number of pages in the PDF:", len(reader.pages))

## Extractint text from each page of the PDF ##

full_text = ""

for page in reader.pages:
    text = page.extract_text()
    
    if text:
        full_text += text + "\n"


print("Total characters:", len(full_text))




