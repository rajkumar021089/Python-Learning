from pypdf import PdfReader

def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

data=read_pdf("certificate_of_completion_python.pdf")
print(data)


