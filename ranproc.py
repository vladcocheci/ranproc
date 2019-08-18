import urllib.request
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import csv
import time
import sys # for command line arguments
from yelp_uri.encoding import recode_uri

# base link for cluj county
cj_list_base_link = "http://ran.cimec.ro/sel.asp?lpag=100&Lang=RO&layers=&crsl=2&csel=2&clst=1&jud=14&campsel=jud&nr="

cod_RAN_list =[]
exceptions_file_name = "exceptions.txt"
output_file_name = "repertoriul_cluj.csv"

# main function
def main():
    cj_link_list = cj_list_generator(cj_list_base_link)
    RAN_scraper(cj_link_list)
    
    to_scan_list = cod_RAN_list
    scraper(to_scan_list)


# function generating the list of links for cluj county
def cj_list_generator(base_link):
    link_list = []
    for i in range(1, 8):
        url = base_link + str(i)
        link_list.append(url)
    return link_list

# RAN scraper function
def RAN_scraper(link_list):
    for url in link_list:
        try:
            req = urllib.request.Request(
                url, 
                data=None,
                headers={
                    'User-Agent': 'Mozilla/5.0'
                }
            )
            
            f = urllib.request.urlopen(req)
            soup = bs(f.read().decode('utf-8'))
            
            for link in soup.find_all('a'):
                text = link.get_text()
                href = link.get('href')
                if re.match(re.compile(r"[0-9]*\.[0-9]*"),text):
                    cod_RAN_list.append("http://ran.cimec.ro/" + href)
        
        except Exception as e:
            exceptions_file = open(exceptions_file_name,'a')
            exceptions_file.write(str(e) + ": " + url + "\n")
            exceptions_file.close()

        print("http://ran.cimec.ro/" + href)
        time.sleep(1)   

# content scraper function
def scraper(link_list):
    rec = []

    for url in link_list:
        url = recode_uri(url)   # re-encoding potentially poorly encoded urls
        try:
            req = urllib.request.Request(
                url,
                data=None,
                headers={
                    'User-Agent': 'Mozilla/5.0'
                }
            )
            f = urllib.request.urlopen(req)
            soup = bs(f.read().decode('utf-8'))

            try:
                link_harta = soup.find("td", string = "Informaţii despre SIT").find_next_sibling("td").find("a").get('href')
            except:
                link_harta = "lipsa link"
            print(link_harta)

            if soup.find(class_ = "RandHeadNeselectatDetaliuLMI"):
                try:
                    cod_LMI = soup.find(class_ = "RandHeadNeselectatDetaliuLMI").find_next_sibling("td").contents[0]
                except:
                    cod_LMI = "lipsa cod"
            else:
                cod_LMI = "lipsa cod"
            print(cod_LMI)

            try:
                cod_RAN = soup.find("td", string = "Cod RAN").find_next_sibling("td").contents[0]
            except:
                cod_RAN = "lipsa cod"
            print(cod_RAN)
        
            try:
                nume = soup.find("td", string = "Nume").find_next_sibling("td").contents[0]
            except:
                nume = "lipsa nume"
            print(nume)

            try:
                judet = soup.find("td", string = "Județ").find_next_sibling("td").contents[0]
            except:
                judet = "lipsa judet"
            print(judet)

            try:
                uat = soup.find("td", string = "Unitate administrativă").find_next_sibling("td").contents[0]
            except:
                uat = "lipsa uat"
            print(uat)

            try:
                localitate = soup.find("td", string = "Localitate").find_next_sibling("td").contents[0]
            except:
                localitate = "lipsa localitate"
            print(localitate)

            try:
                punct = soup.find("td", string = "Punct").find_next_sibling("td").contents[0]
            except:
                punct = "lipsa punct"
            print(punct)

            try:
                reper = soup.find("td", string = "Reper").find_next_sibling("td").contents[0]
            except:
                reper = "lipsa reper"
            print(reper)

            try:
                categorie = soup.find("td", string = "Categorie").find_next_sibling("td").contents[0]
            except:
                categorie = "lipsa categorie"
            print(categorie)

            try:
                tip = soup.find("td", string = "Tip").find_next_sibling("td").contents[0]
            except:
                tip = "lipsa tip"
            print(tip)

            try:
                data_modif = soup.find("td", string = "Data ultimei modificări a fişei").find_next_sibling("td").contents[0]
            except:
                data_modif = "lipsa data"
            print(data_modif)

            print("__________________________________________________________________________________________________________")
            
            rec += [[link_harta, cod_LMI, cod_RAN, nume, judet, uat, localitate, punct, reper, categorie, tip, data_modif]]
        
        except Exception as e:
            exceptions_file = open(exceptions_file_name,'a')
            exceptions_file.write(str(e) + ": " + url + "\n")
            exceptions_file.close()

        time.sleep(1)

    df = pd.DataFrame(rec, columns = ['link_harta', 'cod_LMI', 'cod_RAN', 'nume', 'judet', 'uat', 'localitate', 'punct', 'reper', 'categorie', 'tip', 'data_modif'])
    df.to_csv(output_file_name, index = False)

# calling the main function
if __name__ == "__main__":
    main()