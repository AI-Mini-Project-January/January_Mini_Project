from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse

# Create your views here.

def home(request):
    return render(request, 'hometemplate/index.html')