from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
# from .searchEngine import file_handle, stem


def index(request):
    context = {}
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('document')
        for f in uploaded_files:
            fs = FileSystemStorage()
            fs.save(f.name, f)
        return redirect('search:index')
    else:
        return render(request, "index.html", context)
