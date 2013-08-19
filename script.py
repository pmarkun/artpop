from lxml.html import parse
import urllib2, json, os

url = "http://en.wikipedia.org/wiki/List_of_most_expensive_paintings"

headers = { 'User-Agent' : 'Mozilla/5.0' }
req = urllib2.Request(url, None, headers)
arquivo = urllib2.urlopen(req)
soup = parse(arquivo).getroot()
linhas = soup.cssselect(".wikitable tr")

paintings = []
for linha in linhas[1:]:
    p = {}
    p['name'] = linha.cssselect("td")[1].text_content()
    p['painter'] = linha.cssselect("td")[3].text_content()
    p['year'] = linha.cssselect("td")[4].text_content()
    try:
        p['image_thumb'] = "http:" + linha.cssselect("td")[2].cssselect("img")[0].get("src")
    except:
        print linha.cssselect("td")[2].text_content()
    
    if linha.cssselect("td")[2].cssselect("img"):
        if not os.path.isfile("data/" + p['image'].split("/")[-1]):
            print "Baixando imagem... " + p['name']
            url = "http://en.wikipedia.org" + linha.cssselect("td")[2].cssselect("a")[0].get("href")
            req = urllib2.Request(url, None, headers)
            s = parse(urllib2.urlopen(req)).getroot()
            p['image'] = "http:" + s.cssselect(".fullImageLink img")[0].get("src")
            req = urllib2.Request(p['image'], None, headers)
            img = urllib2.urlopen(req)
            imagem = open("data/" + p['image'].split("/")[-1], "w")
            imagem.write(img.read())
            imagem.close()
    paintings.append(p)

arquivo_final = open("painting.json", "w")
arquivo_final.write(json.dumps(paintings, sort_keys=True, indent=4, separators=(',', ': ')))
arquivo_final.close()