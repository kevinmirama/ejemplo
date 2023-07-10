import pythoncom
from docx2pdf import convert

def convert_word_to_pdf(word_file, pdf_file):
    pythoncom.CoInitialize()
    convert(word_file, pdf_file)
