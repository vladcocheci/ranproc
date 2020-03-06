import urllib.request
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import csv
import time
from yelp_uri.encoding import recode_uri
from random import randrange
import os.path
from os import path

exceptions_file_name = "exceptions.txt"     # exceptions file

### main function
def main():
    for i in range(2,6):   # counties are numbered 1 to 42
        output_file_name1 = "RAN_judetul" + str(i) + ".csv"
        output_file_name2 = "DESCOPERIRI_judetul" + str(i) + ".csv"

        list_base_link = "http://ran.cimec.ro/sel.asp?jud=" + str(i) + "&Lang=RO&crsl=2&csel=2&clst=1&lpag=20&campsel=jud&nr="
        n = get_pages_no(list_base_link)
        while n == None:
            time.sleep(1 + randrange(3))
            n = get_pages_no(list_base_link)
        print(n)
        
        link_list = list_generator(list_base_link, n)
    
        to_scan_list = []
        while link_list:
            link_list, to_scan = RAN_scraper(link_list)
            to_scan_list.extend(to_scan)
        print(to_scan_list)
        print(len(to_scan_list))

        while to_scan_list: 
            to_scan_list = scraper(to_scan_list, output_file_name1, output_file_name2)

    
# function that returns the number of RAN pages
def get_pages_no(base_link):
    try:
        req = urllib.request.Request(
            base_link + "1",
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0'
            }
        )
        f = urllib.request.urlopen(req)
        soup = bs(f.read().decode('utf-8'))

        try:
            pages_no_string = soup.find("font", class_ = "Verdana2").contents[0].split(" ")[2]
            pages_no = int(pages_no_string)
            return pages_no
        except:
            print("error")

    except Exception as e:
        exceptions_file = open(exceptions_file_name,'a')
        exceptions_file.write(str(e) + ": " + base_link + "\n")
        exceptions_file.close()


# function generating the list of links for all RAN pages
def list_generator(base_link, n):
    link_list = []  # a list containing all the links to the RAN site pages
    for i in range(1, n+1):   # there are n pages of containing maximum 20 records/page
        url = base_link + str(i)
        link_list.append(url)
    return link_list


# RAN scraper function -returns a list of links to all records
def RAN_scraper(link_list):
    cod_RAN_list = []
    error_links = []
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
                    print("http://ran.cimec.ro/" + href)
        
        except Exception as e:
            exceptions_file = open(exceptions_file_name,'a')
            exceptions_file.write("!!!" + str(e) + ": " + url + "\n")
            exceptions_file.close()
            error_links.append(url)

        time.sleep(randrange(3))
    return error_links, cod_RAN_list


# content scraper function -scraps relevant content from each page and saves it to .csv files
def scraper(link_list, output_file_name1, output_file_name2):
    rec = []    # stores general information from all tables
    disc = []   # stores discovery information from all tables
    error_links = []    # stores links that raised errors when trying to open
    count = 0

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
            count += 1

            ### Archeological Site Info
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
                cod_RAN = str(soup.find("td", string = "Cod RAN").find_next_sibling("td").contents[0])
            except:
                cod_RAN = "lipsa cod"
            print(cod_RAN)
            regex = re.compile(r"\.[0-9]*")
            siruta = re.sub(regex, '', cod_RAN)
        
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

            ### Bibliography
            biblio = ""
            try:
                tr_biblio_list = soup.find(string = "Bibliografie").find_parent("tr").find_next_siblings("tr")
                for tr in tr_biblio_list:
                    biblio = biblio + tr.find("td").contents[0] + "\n"
            except:
                biblio = "lipsa bibliografie"
            print(biblio)

            rec.append([siruta, link_harta, cod_LMI, cod_RAN, nume, judet, uat, localitate, punct, reper, categorie, tip, data_modif, biblio])

            ### Discoveries
            try:
                tr_disc_list = soup.find("td", string = "Categorie/ Tip").find_parent("tr").find_next_siblings("tr")
                for tr in tr_disc_list:
                    td_list = tr.findChildren("td")
                    td_record = []
                    td_record.append(siruta)
                    td_record.append(cod_RAN)
                    for td in td_list:
                        td_record.append(re.sub('(\n|\r|\t|\xa0)', '', td.contents[0])) # removing escape characters
                    print(str(td_record))
                    disc.append(td_record)
            except:
                disc.append([siruta, cod_RAN, '', '', '', '', ''])
            
            print("__________________________________________________________________________________________________________")    
        
        except Exception as e:
            exceptions_file = open(exceptions_file_name,'a')
            exceptions_file.write(str(e) + ": " + url + "\n")
            exceptions_file.close()
            error_links.append(url)

        time.sleep(1 + randrange(3))
        if count % 10 == 0:
            print("sleeping 5")
            time.sleep(5)

    df = pd.DataFrame(rec, columns = ['siruta', 'link_harta', 'cod_LMI', 'cod_RAN', 'nume', 'judet', 'uat', 'localitate', 'punct', 'reper', 'categorie', 'tip', 'data_modif', 'bibliografie'])
    df.to_csv(output_file_name1, mode = 'a', header = not(path.exists(output_file_name1)), index = False)

    dfd = pd.DataFrame(disc, columns = ['siruta', 'cod_RAN', 'categorie', 'epoca', 'cultura', 'descriere', 'cod_LMI'])
    dfd.to_csv(output_file_name2, mode = 'a', header = not(path.exists(output_file_name2)), index = False)

    exceptions_file = open(exceptions_file_name,'a')
    exceptions_file.write("________________________________________________________________" + "\n")
    return error_links


# calling the main function
if __name__ == "__main__":
    main()