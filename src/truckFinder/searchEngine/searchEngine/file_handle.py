from bs4 import BeautifulSoup
from .stem import stem

def webscrap(filename):
    #Fungsi untuk membaca dokumen html
    #menerima nama file
    #Mengembalikan dokumen bersih bertipe string
    f = open(filename, "r")
    html = f.read()
    soup = BeautifulSoup(html, features="html.parser")
    text = str(soup.get_text)
    f.close()
    return text

def file_peek(filename):
    #Fungsi untuk membaca judul dan kalimat pertama pada dokumen
    f = open(filename, "r")
    judul = f.readline()
    fkal = f.readline()
    while (fkal == '\n'):
        fkal = f.readline()
    f.close()
    return judul, fkal

def file_read(filename):
    #Fungsi untuk membaca file txt
    f = open(filename, "r")
    text = f.read()
    f.close()
    return text

