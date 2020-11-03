from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from . import stem

def index(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('document')
        for f in uploaded_files:
            fs = FileSystemStorage()
            fs.save(f.name, f)
        return redirect('index')
    else:
        context = {}
        return render(request,"index.html",context)