from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import SignUpForm, ProfileForm
from .decorators import unauthenticated_user
from django.http import HttpResponseRedirect
from blog.models import Author
from django.contrib import messages


def index(request):
    return render(request, "index.html")

# account management


@unauthenticated_user
def loginViews(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.info(request, 'Username atau password salah')

    return render(request, "login.html")


@login_required(login_url="login")
def logoutViews(request):
    logout(request)
    return redirect('index')


@unauthenticated_user
def signUpViews(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            form = SignUpForm(request.POST)
            user = form.save()
            Author.objects.create(
                user=user,
                name=user.first_name + " " + user.last_name,
                email=user.email
            )

            return redirect("login")

    context = {'form': form}
    return render(request, 'signup.html', context)


@login_required(login_url="login")
def profile(request, username):
    if request.user.username != username:
        return redirect('index')
    return render(request, "profile.html")


@login_required(login_url="login")
def profile_form(request, name):
    author = Author.objects.get(name=name)
    if author != request.user.author:
        redirect('index')
    else:
        prof_form = ProfileForm(request.POST or None, instance=author)
        if request.POST:
            username = request.POST.get('username')
            prof_form = ProfileForm(
                request.POST, request.FILES, instance=author)
            if prof_form.is_valid():
                author_update = prof_form.save()
                print(author_update)
                fname = author_update.name.split(" ")[0]
                lname = author_update.name.split(" ")[1]
                user = User.objects.filter(author=author.id).update(
                    first_name=fname, last_name=lname, username=username, email=author_update.email)
                return redirect("index")

    context = {'form': prof_form}
    return render(request, "profile_form.html", context)
