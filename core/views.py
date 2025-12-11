from django.shortcuts import render
from .models import Students, Subjects, Exams

def home(request):
    context = {
        'students': Students.objects.all(),
        'subjects': Subjects.objects.all(),
        'exams': Exams.objects.all(),
    }
    return render(request, 'index.html', context)