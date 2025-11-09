from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.user.is_authenticated:
        return redirect("users:profile")
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("login")
    return render(request, "registration/signup.html", {"form": form})

@login_required
def profile(request):
    return render(request, "users/profile.html")
