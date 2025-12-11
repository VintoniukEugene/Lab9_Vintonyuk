from django.contrib import admin
from .models import Students, Subjects, Exams

admin.site.register(Students)
admin.site.register(Subjects)
admin.site.register(Exams)