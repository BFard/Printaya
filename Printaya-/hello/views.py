import requests
import os
import time
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from hello.models import Greeting
from hello.models import Print, Restriction
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm
import datetime

test = Print.objects.filter(title = "test")
daily = Restriction.objects.filter(title = "DailyPrints")
today = Print.objects.filter(title = "Today")
printsToday = Print.objects.filter(title = "PrintsToday")
printLog = Print.objects.filter(title = "PrintLog")
date = Print.objects.get(title="Today").status
year = int(date[0:4])
month = int(date[4:6])
day = int(date[6:8])
newToday = datetime.date(year, month, day)

def upDate():
    if newToday < datetime.datetime.date(datetime.datetime.now()):
        newYear = str(datetime.datetime.now().year)
        newMonth = str(datetime.datetime.now().month)
        if len(newMonth) == 1:
            newMonth = "0" + newMonth
        newDay = str(datetime.datetime.now().day)
        if len(newDay) == 1:
               newDay = "0" + newDay
        newDate = newYear + newMonth + newDay
        today.update(status = newDate)
        printsToday.update(status = "0")

 #Create your views here.
def index(request):
    if request.user.is_authenticated():
        role = request.user.first_name
        if role == "Student":
            return redirect("student")
        elif role == "Teacher":
            return redirect("teacher")
    return render(request, 'index.html')

def queue(request):
    return HttpResponse(Print.objects.get(title = "test").status)

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

def UserFormView(request):
    form_class = UserForm
    template = "hello/registration.html"
    if request.method == "GET":
        form = form_class(None)
        return render(request, "registration.html", {"form": form})
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            first_name = form.cleaned_data["first_name"]
            user.backend = "django.contrib.auth.backends.ModelBackend"
            user.set_password(password)
            user.save()
            login(request, user)
            if user.first_name == "Student":
                return redirect("student")
            elif user.first_name == "Teacher":
                return redirect("teacher")
    return render(request, "registration.html", {"form": form})

def Student(request):
    if request.method == "GET":
        upDate()
    if request.method == "POST" and request.FILES["file"]:
        soFar = int(Print.objects.get(title="PrintsToday").status)
        perDay = int(Restriction.objects.get(title="DailyPrints").perday)
        if soFar < perDay:
            printJob = request.FILES["file"]
            fs = FileSystemStorage()
            filename = fs.save(printJob.name, printJob)
            print_job_url = fs.url(filename)
            test.update(status = filename)
            time.sleep(3)
            test.update(status = "stop")
            printsToday.update(status = str(soFar + 1))
            currentLog = Print.objects.get(title="PrintLog").status
            newLog = currentLog + "\n" + request.user.username + "\n" + datetime.datetime.now().ctime() + "\n" + filename
            printLog.update(status = newLog)
    role = None
    if request.user.is_authenticated():
        role = request.user.first_name
    if role == "Student":
        return render(request, "student.html")
    else:
        return render(request, "index.html")

def Teacher(request):
    if request.method == "POST":
        newPerday = request.POST.get("perday")
        if newPerday != "":
            daily.update(perday = newPerday)    
    role = None
    if request.user.is_authenticated():
        role = request.user.first_name
    if role == "Teacher":
        currentLog = Print.objects.get(title="PrintLog").status
        rows = int((currentLog.count("\n") + 1) / 3)
        data = []
        for i in range (0, rows):
            currentRow = []
            currentRow.append(currentLog.splitlines()[3*i])
            currentRow.append(currentLog.splitlines()[3*i+1])
            currentRow.append(currentLog.splitlines()[3*i+2])
            data.append(currentRow)
        print(data)
        return render(request, "teacher.html", {"rows": rows, "data": data})
    else:
        return render(request, "index.html")
