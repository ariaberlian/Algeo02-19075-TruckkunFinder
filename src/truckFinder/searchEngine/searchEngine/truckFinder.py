from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os
from bs4 import BeautifulSoup
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re
import string
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from .file_handle import *
from .stem import *
from django.conf import settings

# nltk.download()

# folderDokumen = '../../media/'
folderDokumen = settings.MEDIA_ROOT+'\\'

def truckFinder(string):
    # menerima input string kata-kata(query)
    # output tupple: <listDok, termArray, vektorQuery, vectorDokumen, tableFrekuensi>
    # listDok[0 sampai n-1 buah file][0-3; 0: nama file, 1: jumlah kata, 2:tuple: <judul, kalimat pertama>, 3: list isi dari dokumen yang tertoken, 4: kosinus similarity]
    # termArray[0 sampai k-1 buah semua kata dari seluruh dokumen]
    # vektorQuery: vektor yang berisi sebanyak k buah elemen yang masing masing memiliki nilai = jumlah pengulangan semua di query relatif terhadap term
    # vektorDokumen[0 sampai n-1 buah file]: vektor yang berisi sebanyak k buah elemen yang masing masing memiliki nilai = jumlah pengulangan semua kata di dokumen relatif terhadap term
    # tabelFrekuensi: tabel dengan kolom term, vektorQuery, vektorDokumen
    
    totalFiles = 0
  
    query = stemming(string)

    listDok = []

    for filename in os.listdir(folderDokumen):
        if filename.endswith(".txt") or filename.endswith(".html"):
            listDok.append([])
            listDok[totalFiles].append(filename)  # listDok[i][0]

            if filename.endswith(".txt"):
                # Membuka dokumen
                file = open(folderDokumen + filename)
                dokumen = file.read().replace("\n", " ").lower()
                file.close()
            else:
                dokumen = webscrap(folderDokumen + filename)

            #Menghitung jumlah kata
            lenDok = len(dokumen.split())
            listDok[totalFiles].append(lenDok) #listDok[i][1]

            #Membaca judul dan kalimat pertama file
            peek = file_peek(folderDokumen + filename) #listDok[i][2]
            listDok[totalFiles].append(peek)

            # Menambahkan dan menToken isi file (line) kedalam array
            stemDok = stemming(dokumen)
            listDok[totalFiles].append(stemDok)  # listDok[i][3]

     
            totalFiles += 1
        else:
            continue

    vectorDokumen = []
    vektorQuery = []

    termArray = query.copy()
    for i in range(totalFiles):
        vectorDokumen.append([])
        termArray = sorted(list(set(termArray) | set(listDok[i][3] )))

    kamus = {}
    for i in range(len(termArray)):
        kamus[termArray[i]] = i

    for i in range(totalFiles):

        tempL1 = [0 for j in range(len(termArray))]
        tempL2 = [0 for j in range(len(termArray))]

        for w in listDok[i][3]:
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
        
        if query:
            cosine = c / float((sum(tempL1) * sum(tempL2)) ** 0.5)
            listDok[i].append(cosine)  # listDok[i][4]
            listDok[i].append(vectorDokumen[i])     # listDok[i][5]

    if query:
        listDok = sorted(listDok, key=lambda x: -x[4])
        
    newQuery = list(set(query))  # menghilangkan yang double
    k = 0
    tableFrekuensi = [["" for j in range(totalFiles + 2)] for i in range(len(newQuery))]
    for w in termArray:
        if w in newQuery:
            for j in range(totalFiles+2):
                if j == 0:
                    tableFrekuensi[k][j] = termArray[kamus[w]]
                elif j == 1:
                    tableFrekuensi[k][j] = str(vektorQuery[kamus[w]])
                else:
                    tableFrekuensi[k][j] = str(listDok[j - 2][5][kamus[w]])
            k += 1


    return listDok, termArray, vektorQuery, vectorDokumen, tableFrekuensi


