import os
import zipfile
from PIL import Image
from django.shortcuts import render, redirect
from .models import Project, Task
from .forms import ProjectForm, TaskForm
from django.http import HttpResponse
from .models import Project
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from docx import Document
from pdfdocument.document import PDFDocument
from docx2pdf import convert
from django.shortcuts import render, redirect
from docx2pdf import convert
import tempfile
from io import BytesIO
import zipfile
import pythoncom
from pdfdocument.document import PDFDocument
import pandas as pd
import pythoncom
import win32com.client
from django.http import FileResponse
import comtypes.client
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import pythoncom
import chardet
import zipfile
from google.cloud import speech_v1
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from google.cloud import speech_v1
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
import speech_recognition as sr
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import io
from django.http import HttpResponseRedirect
from django.urls import reverse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import speech_recognition as sr
import win32com.client as win32
import pythoncom
import pandas as pd

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_list.html', {'projects': projects})

def project_detail(request, pk):
    project = Project.objects.get(pk=pk)
    return render(request, 'project_detail.html', {'project': project})

def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'project_form.html', {'form': form})

def project_edit(request, pk):
    project = Project.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'project_form.html', {'form': form})

def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form})

def task_edit(request, pk):
    task = Task.objects.get(pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', pk=pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form})

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

def task_detail(request, pk):
    task = Task.objects.get(pk=pk)
    return render(request, 'task_detail.html', {'task': task})

def project_report(request, pk):
    project = Project.objects.get(pk=pk)
    tasks = project.task_set.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{project.name} Report.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(f'{project.name} Report', styles['Title']))
    elements.append(Spacer(1, 0.25 * inch))

    elements.append(Paragraph('Tasks', styles['Heading2']))
    for task in tasks:
        elements.append(Paragraph(f'{task.title}: {task.description}', styles['Normal']))
        elements.append(Spacer(1, 0.25 * inch))

    doc.build(elements)

    return response


def convert_file(request):
    if request.method == 'POST':
        file = request.FILES['file']
        image = Image.open(file)
        pdf = image.convert('RGB')
        pdf_size = image.size
        pdf_page = Image.new('RGB', pdf_size, (255, 255, 255))
        pdf_page.paste(image)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{file.name}.pdf"'
        # Crea un archivo en memoria
        buffer = BytesIO()
        # Guarda el objeto PDF en el archivo en memoria
        pdf_page.save(buffer, 'PDF')
        # Escribe el contenido del archivo en memoria en la respuesta
        response.write(buffer.getvalue())
        return response
    return render(request, 'convert_file.html')


def convert_fileword(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        if not files:
            # No se cargaron archivos
            # Mostrar un mensaje de error al usuario
            return render(request, 'convert_fileword.html', {'error': 'Debes cargar al menos un archivo.'})
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="archivosconvertidos.zip"'
        buffer = BytesIO()
        with zipfile.ZipFile(buffer, 'w') as zip_file:
            for file in files:
                # Verificar la extensión del archivo
                if not file.name.endswith('.docx'):
                    # El archivo no es de formato .docx
                    # Mostrar un mensaje de error al usuario
                    return render(request, 'convert_fileword.html', {'error': 'Debes cargar solo archivos de formato .docx.'})
                temp_file = os.path.join(tempfile.gettempdir(), file.name)
                with open(temp_file, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                pythoncom.CoInitialize()
                pdf_file = os.path.splitext(temp_file)[0] + '.pdf'
                convert(temp_file, pdf_file)
                zip_file.write(pdf_file, os.path.basename(pdf_file))
                os.remove(temp_file)
                os.remove(pdf_file)
        response.write(buffer.getvalue())
        return response
    return render(request, 'convert_fileword.html')


def convert_fileexc(request):
    if request.method == 'POST':
        excel_files = request.FILES.getlist('files')
        print(excel_files)
        output_files = []

        for excel_file in excel_files:
            # Lee el contenido del archivo de Excel en un DataFrame de pandas
            df = pd.read_excel(excel_file)

            # Crea un archivo temporal para guardar el archivo PDF
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                pdf_path = tmp.name

            # Exporta el DataFrame a un archivo PDF
            pdf = PDFDocument(pdf_path)
            pdf.init_report()
            pdf.p(df.to_html(index=False))
            pdf.generate()

            output_files.append(pdf_path)

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for output_file in output_files:
                zip_file.write(output_file, os.path.basename(output_file))

        # Imprime el valor de output_files para verificar si contiene las rutas de los archivos PDF creados
        print(output_files)

        # Envía el archivo zip como una respuesta de descarga
        response = FileResponse(zip_buffer.getvalue(), as_attachment=True, filename='output.zip')
        response['Content-Disposition'] = 'attachment; filename=output.zip'
        return response

    return render(request, 'convert_fileexc.html')



def convert_filetxt(request):
    # Verificar si el formulario ha sido enviado
    if request.method == 'POST':
        # Obtener los archivos de texto del formulario
        txt_files = request.FILES.getlist('files')

        # Crear un archivo ZIP para almacenar los archivos PDF generados
        zip_filename = "output.zip"
        zip_file = zipfile.ZipFile(zip_filename, "w")

        # Procesar cada archivo de texto y generar un archivo PDF
        for txt_file in txt_files:
            # Crear un objeto PDF con ReportLab
            pdf_filename = os.path.splitext(txt_file.name)[0] + ".pdf"
            pdf = SimpleDocTemplate(pdf_filename, pagesize=letter)
            styles = getSampleStyleSheet()
            style = styles["Normal"]

            # Leer el contenido del archivo de texto y agregarlo al PDF
            content = []
            for line in txt_file:
                content.append(Paragraph(line.decode('utf-8'), style))
            pdf.build(content)

            # Agregar el archivo PDF generado al archivo ZIP
            zip_file.write(pdf_filename)

        # Cerrar el archivo ZIP
        zip_file.close()

        # Devolver el archivo ZIP generado como respuesta
        response = FileResponse(open(zip_filename, "rb"), as_attachment=True, filename=zip_filename)
        return response
    else:
        # Renderizar la plantilla HTML con el formulario para cargar archivos
        return render(request, 'convert_filetxt.html')


def inicio(request):
    return render(request, 'inicio.html')

def comofunciona(request):
    return render(request, 'comofunciona.html')

def caracteristicas(request):
    return render(request, 'caracteristicas.html')



def convert_fileppt(request):
    def ppt_to_pdf(input_file_path, output_file_path):
        pythoncom.CoInitialize()
        powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
        powerpoint.Visible = 1
        deck = powerpoint.Presentations.Open(input_file_path)
        deck.SaveAs(output_file_path, 32)
        deck.Close()
        powerpoint.Quit()

    if request.method == 'POST' and request.FILES.getlist('files'):
        pdf_files = []
        for file in request.FILES.getlist('files'):
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            uploaded_file_url = fs.url(filename)
            input_file_path = os.path.join(settings.MEDIA_ROOT, filename)
            output_file_path = os.path.join(settings.MEDIA_ROOT, os.path.splitext(filename)[0] + '.pdf')
            ppt_to_pdf(input_file_path, output_file_path)
            pdf_files.append(output_file_path)

        if len(pdf_files) == 1:
            response = FileResponse(open(pdf_files[0], 'rb'), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_files[0])}"'
            return response
        else:
            zip_filename = 'converted_files.zip'
            zip_file_path = os.path.join(settings.MEDIA_ROOT, zip_filename)
            with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                for pdf_file in pdf_files:
                    zipf.write(pdf_file, arcname=os.path.basename(pdf_file))
            response = FileResponse(open(zip_file_path, 'rb'), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
            return response

    return render(request, 'convert_fileppt.html')


def convert_fileaudio(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        output_files = []
        for file in files:
            r = sr.Recognizer()
            with sr.AudioFile(file) as source:
                audio = r.record(source)
                text = r.recognize_google(audio, language='es-ES')

            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            style = styles["Normal"]
            story = [Paragraph(text, style)]
            doc.build(story)
            pdf = buffer.getvalue()
            buffer.close()

            output_filename = f'{file.name}.pdf'
            output_path = os.path.join(settings.MEDIA_ROOT, output_filename)
            with open(output_path, 'wb') as f:
                f.write(pdf)

            output_files.append(output_path)

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for output_file in output_files:
                zip_file.write(output_file, os.path.basename(output_file))

        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="output.zip"'

        return response

    else:
        return render(request, 'convert_fileaudio.html')

