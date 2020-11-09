from bs4 import BeautifulSoup
import re
def webscrap(filename):
    #Fungsi untuk membaca dokumen html
    #menerima nama file
    #Mengembalikan dokumen bersih bertipe string
    f = open(filename, "r")
    html = f.read()
    soup = BeautifulSoup(html,features="html.parser")
    text = str(soup.get_text()).strip()
    text = re.sub(r'(\n\s*)+\n', '\n\n',text)
    return text

def file_peek(filename):
    #Fungsi untuk membaca judul dan kalimat pertama pada dokumen
    if filename.endswith(".txt"):
        f = open(filename, "r")
        judul = f.readline().rstrip()
        fkal = f.readline()
        while (fkal == '\n'):
            fkal = f.readline()
        fkal = fkal.rstrip()
        fkal = fkal.partition('.'or'!'or'?')[0]
        f.close()
    else:
        f = open(filename, "r")
        html = f.read()
        soup = BeautifulSoup(html, features="html.parser")
        judul = str(soup.find('title'or'h1').get_text())
        fkal = str(soup.find('p').get_text()).partition('.'or'!'or'?')[0]
        f.close()
    return judul, fkal
    

def file_read(filename):
    #Fungsi untuk membaca file txt
    f = open(filename, "r")
    text = f.read()
    f.close()
    return text