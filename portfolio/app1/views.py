# app1/views.py
from django.shortcuts import render, redirect
from .forms import app1Form


def create_person(request):
    if request.method == "POST":
        form = app1Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = app1Form()
    return render(request, "app1/person_form.html", {"form": form})


def index(request):
    return render(request, "app1/index.html")
