import requests
import os
import time
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from hello.models import Greeting
from hello.models import Print

test = Print.objects.filter(title = "test")
# Create your views here.
def index(request):
    if request.method == "POST" and request.FILES["file"]:
        printJob = request.FILES["file"]
        fs = FileSystemStorage()
        filename = fs.save(printJob.name, printJob)
        print_job_url = fs.url(filename)
        test.update(status = filename)
        time.sleep(3)
        test.update(status = "stop")
    return render(request, 'index.html')

def queue(request):
    return HttpResponse(Print.objects.get(title = "test").status)

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

