import bitly_api
import sys
import pandas as pd
import csv
import time

USER = str(input('USER:'))
KEY = str(input ('KEY:'))
b = bitly_api.Connection(USER, KEY)

output_file_name = "RAN_CJ.csv"

def main():
    df = pd.read_csv("repertoriul_cluj_coord.csv")
    urls = []
    for link in df["link_harta"]:
        try:
            url = shorten(link)
        except:
            url = "ERROR" + shorten(link)
        print(url)
        urls.append(url)
        time.sleep(1)
        
    df["link_harta"] = urls
    df.to_csv(output_file_name, index = False)


def shorten(link):
    response = b.shorten(uri = link)
    return(response["url"])

if __name__ == "__main__":
    main()