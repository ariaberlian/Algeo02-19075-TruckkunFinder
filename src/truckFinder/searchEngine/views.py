from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .searchEngine.truckFinder import truckFinder


def index(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('document')
        for f in uploaded_files:
            fs = FileSystemStorage()
            fs.save(f.name, f)
        return redirect('search:index')
    else:
        query = request.GET.get('q', '')
        listDok, termArray, vektorQuery, vektorDokumen, tabelFrekuensi = truckFinder(query)

        print(listDok[0])
        context = {
            'List': listDok,
            'Terms': termArray,
            'VektorQuery': vektorQuery,
            'VektorDokumen': vektorDokumen,
            'Table':tabelFrekuensi,
        }
        return render(request, "index.html", context)

def about(request):
    return render(request, "about.html")

def concept(request):
    return render(request, "concept.html")
    
def how_to_use(request):
    return render(request, "howto.html")


