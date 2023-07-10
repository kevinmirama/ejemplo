
from django.urls import path

from . import views

urlpatterns = [
    path('projects/', views.project_list, name='project_list'),
    path('project_create/', views.project_create, name='project_create'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/new/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('projects/<int:pk>/report/', views.project_report, name='project_report'),
    path('convert/', views.convert_file, name='convert_file'),
   path('convert_fileword/', views.convert_fileword, name='convert_fileword'),
    path('inicio/', views.inicio, name='inicio'),
    path('comofunciona/', views.comofunciona, name='comofunciona'),
    path('convert_fileexc/', views.convert_fileexc, name='convert_fileexc'),
    path('convert_file/', views.convert_file, name='convert_file'),
    path('convert_filetxt/', views.convert_filetxt, name='convert_filetxt'),
    path('convert_fileppt/', views.convert_fileppt, name='convert_fileppt'),
    path('convert_fileaudio/', views.convert_fileaudio, name='convert_fileaudio'),
    path('caracteristicas/', views.caracteristicas, name='caracteristicas'),
]

