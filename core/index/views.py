from django.shortcuts import render

from .models import Developer

def index(request):
    developers = Developer.objects.all()
    return render(request, 'index.html', {'developers': developers})
