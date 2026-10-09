
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def home(request):
    return render(request, "HBase.html")


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("log")
    else:
        form = UserCreationForm()

    return render(request, "Register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect("HBase")
    else:
        form = AuthenticationForm(request)

    return render(request, "log.html", {"form": form})