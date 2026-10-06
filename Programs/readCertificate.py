import pdfReader

print("Reading PDF file...")

data = pdfReader.read_pdf(
    "certificate_of_completion_python.pdf"
)

print(data)