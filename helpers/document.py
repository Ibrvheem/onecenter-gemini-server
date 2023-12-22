import PyPDF2
import requests
from io import BytesIO

def read_pdf(pdf_url):
    # Download the PDF file from the URL
    response = requests.get(pdf_url)
    if response.status_code == 200:
        # Open the PDF from the response content
        pdf_file = BytesIO(response.content)

        # Create a PDF object
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Get the number of pages in the PDF
        num_pages = len(pdf_reader.pages)

        # Initialize a variable to store the text from the PDF
        pdf_text = ''

        # Iterate through each page and extract the text
        for page_num in range(num_pages):
            # page = pdf_reader.getPage(page_num)
            page = pdf_reader.pages[page_num]
            pdf_text += page.extract_text()

        # Print the extracted text
        return pdf_text
    else:
        print(f"Failed to download PDF from {pdf_url}. Status code: {response.status_code}")
        return ""
