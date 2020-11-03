from django.shortcuts import render

def index(request):
    context = {
        'konteks1': "Ai",
        'konteks2': "Hayasaka",
        'nuclear_code': 267980,
    }
    return render(request,"index.html",context)