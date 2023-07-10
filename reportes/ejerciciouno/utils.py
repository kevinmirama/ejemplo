from .convert import convert_word_to_pdf

def handle_uploaded_file(f):
    with open('temp.docx', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    convert_word_to_pdf('temp.docx', 'output.pdf')
