import requests
import scrapy
import unidecode


def AddNumbersToList(year,file):
    f = open(file,"r")
    liste= f.readlines()
    f.close()
    listeRes = []
    for element in liste:
        pointsBefore = None
        pointsAfter = None
        print(element)
        element = element.split(",")
        link=element[1]
        link = fromNomPrenomtoPrenomNomPlusOnEnleveLesAccents(link)
        url = "https://www.procyclingstats.com/rider/"+link

        response = requests.get(url)

        if response.status_code == 200:
            source = response.text

        if source:
            selector = scrapy.Selector(text=source)
            years = selector.css("table.basic tbody > tr")
            for x in years:
                if x.css("td.season::text").extract_first() == year:
                    pointsAfter = x.css("td.bar div.barCont > span::text").extract_first()
                if x.css("td.season::text").extract_first() == str(int(year)-1):
                    pointsBefore = x.css("td.bar div.barCont > span::text").extract_first()
            if pointsAfter and pointsBefore:
                listeRes.append([element[1].replace("\n",""),element[2].replace("\n",""),element[3].replace("\n",""),pointsBefore.replace("\n",""),pointsAfter.replace("\n","")])
    return listeRes


def fromNomPrenomtoPrenomNomPlusOnEnleveLesAccents(NOMPrenom):
    ALPHABET = "AZERTYUIOPQSDFGHJKLMWXCVBN"
    NOMPrenom = NOMPrenom.split(" ")
    prenom_nom=""

    for i,x in enumerate(NOMPrenom):
        prenom = None
        for k in x:
            if k not in ALPHABET:
                prenom = i
                break
        if prenom:
            break

    for x in NOMPrenom[prenom:]:
        prenom_nom+=x.lower()
        prenom_nom+="-"

    for x in NOMPrenom[:prenom]:
        prenom_nom += x.lower()
        prenom_nom += "-"

    prenom_nom = prenom_nom[:-1]
    prenom_nom = unidecode.unidecode(prenom_nom)

    return prenom_nom





def getMVdP():
    url = "https://www.procyclingstats.com/rider/mathieu-van-der-poel"

    response = requests.get(url)

    if response.status_code == 200:
        source = response.text

    if source:
        selector = scrapy.Selector(text=source)
        years = selector.css("table.basic tbody > tr")
        for x in years:
            print(x.css("td.season::text").extract_first())
            if x.css("td.season::text").extract_first() == "2019":
                year = x.css("td.bar div.barCont > span::text").extract_first()

    return year

def createCSVtransferts():
    newFile = open("transferts.csv","a+")
    for i in range(2015,2022):
        for k in AddNumbersToList(str(i),str(i)+".txt"):
            newFile.write(str(i)+","+k[0]+","+k[1]+","+k[2]+","+k[3]+","+k[4]+"\n")



if __name__ == "__main__":

    #print(fromNomPrenomtoPrenomNomPlusOnEnleveLesAccents("VAN POPPEL Dànny Pöl"))
    #print(AddNumbersToList("2018","2018.txt"))
    print(createCSVtransferts())
    pass