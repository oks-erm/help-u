from django.shortcuts import render
from django.contrib import messages


def home_page(request):
    return render(request, 'index.html')
