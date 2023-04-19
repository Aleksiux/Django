from django.shortcuts import render
from django.http import HttpResponse



def index(request):
    return HttpResponse('Nice!')
# Create your views here.
