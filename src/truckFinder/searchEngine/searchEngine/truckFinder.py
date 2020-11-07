from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os
from bs4 import BeautifulSoup
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re
import string
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# from .stem import stemming
# from .file_handle import webscrap,file_peek,file_read

# nltk.download()

folderDokumen = '../../media/'


def webscrap(filename):
    # Fungsi untuk membaca dokumen html
    # menerima nama file
    # Mengembalikan dokumen bersih bertipe string
    f = open(folderDokumen + filename, "r")
    html = f.read()
    soup = BeautifulSoup(html, features="html.parser")
    text = str(soup.get_text)
    f.close()
    return text


def file_peek(filename):
    # Fungsi untuk membaca judul dan kalimat pertama pada dokumen
    f = open(folderDokumen + filename, "r")
    judul = f.readline()
    fkal = f.readline()
    while (fkal == '\n'):
        fkal = f.readline()
    f.close()
    return judul, fkal


def file_read(filename):
    # Fungsi untuk membaca file txt
    f = open(filename, "r")
    text = f.read()
    f.close()
    return text


def stemming(dokumen):
    # Fungsi untuk membersihkan dokumen
    # Menerima dokumen bertipe string
    # Mengembalikan array hasil filter,stemming dan tokenizing

    factory = StopWordRemoverFactory()
    stopword = factory.create_stop_word_remover()
    stemmer = StemmerFactory().create_stemmer()

    # 1.Case Folding
    dokumen = dokumen.translate(str.maketrans(
        "", "", string.punctuation)).lower().strip()
    dokumen = re.sub(r"\d+", "", dokumen)
    # 2.Filtering stopword
    stop = stopword.remove(dokumen)
    # 3.Stemming
    hasil_stem = stemmer.stem(stop)
    # 4.Tokenizing
    token = word_tokenize(hasil_stem)
    return token


def truckFinder(string):
    # menerima input string kata-kata(query)
    # output tupple: <listDok, termArray, vektorQuery, vectorDokumen>
    # listDok[0 sampai n-1 buah file][0-2; 0: nama file, 1: list isi dari dokumen yang tertoken, 2: kosinus similarity]
    # termArray[0 sampai k-1 buah semua kata dari seluruh dokumen]
    # vektorQuery: vektor yang berisi sebanyak k buah elemen yang masing masing memiliki nilai = jumlah pengulangan semua di query relatif terhadap term
    # vektorDokumen[0 sampai n-1 buah file]: vektor yang berisi sebanyak k buah elemen yang masing masing memiliki nilai = jumlah pengulangan semua kata di dokumen relatif terhadap term

    totalFiles = 0
  
    query = stemming(string)
    print(query)

    listDok = []

    for filename in os.listdir(folderDokumen):
        if filename.endswith(".txt") or filename.endswith(".html"):
            listDok.append([])
            listDok[totalFiles].append(filename)  # listDok[i][0]

            if filename.endswith(".txt"):
                # Membuka dokemen
                file = open(folderDokumen + filename)
                dokumen = file.read().replace("\n", " ").lower()
                file.close()
            else:
                dokumen = webscrap(filename)

            # Menambahkan dan menToken isi file (line) kedalam array
            stemDok = stemming(dokumen)
            listDok[totalFiles].append(stemDok)  # listDok[i][1]

            print(listDok[totalFiles][1])
     
            totalFiles += 1
        else:
            continue

    vectorDokumen = []
    vektorQuery = []

    termArray = query
    for i in range(totalFiles):
        vectorDokumen.append([])
        termArray = sorted(list(set(termArray) | set(listDok[i][1])))

    kamus = {}
    for i in range(len(termArray)):
        kamus[termArray[i]] = i

    for i in range(totalFiles):

        tempL1 = [0 for j in range(len(termArray))]
        tempL2 = [0 for j in range(len(termArray))]

        for w in listDok[i][1]:
            tempL1[kamus[w]] += 1  # menginkremen vektor dengan indeks dari dictionary
        for w in query:
            tempL2[kamus[w]] += 1

        vectorDokumen[i] = tempL1.copy()
        vektorQuery = tempL2.copy()

        c = 0

        for j in range(len(termArray)):
            c += vectorDokumen[i][j] * vektorQuery[j]
            tempL1[j] = tempL1[j] ** 2
            tempL2[j] = tempL2[j] ** 2

        cosine = c / float((sum(tempL1) * sum(tempL2)) ** 0.5)

        listDok[i].append(cosine)  # listDok[i][2]

    return listDok, termArray, vektorQuery, vectorDokumen


