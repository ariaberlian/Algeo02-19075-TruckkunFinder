from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re
import string
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import nltk
# nltk.download()

def stem(dokumen):

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
    token = nltk.tokenize.word_tokenize(hasil_stem)

    return token

