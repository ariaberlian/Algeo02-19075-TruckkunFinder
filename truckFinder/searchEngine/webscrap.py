from bs4 import BeautifulSoup

def webscrap(lokasi):
    f = open(lokasi, "r")
    html = f.read()
    soup = BeautifulSoup(html, features="html.parser")
    text = str(soup.get_text)
    f.close()
    return text
