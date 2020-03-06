from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import re
import pandas as pd
import csv

### main function
def main():
    for i in range(26,27):   # counties are numbered 1 to 42
        input_file_name = "RAN_judetul" + str(i) + ".csv"
        output_file_name = "RAN_coord_judetul" + str(i) + ".csv"

        df = pd.read_csv(input_file_name)
        x_field, y_field = [], []
        counter = 1

        for link in df["link_harta"]:
            try:
                coord = get_coordinates(link)
            except:
                coord = "Null : Null"

            xy = coord.split(" : ")
            y = xy[0]
            x = xy[1]
            print("judetul " + str(i) + " - " + str(counter) + " - " + x + ": " + y)
            x_field.append(x)
            y_field.append(y)
            counter += 1

        df["x_field"] = x_field
        df["y_field"] = y_field
        df.to_csv(output_file_name, index = False)

     
def get_coordinates(link):
    browser = webdriver.Firefox()
    browser.get(link)
    browser.maximize_window()

    elem = browser.find_element_by_id("divHarta")

    actions = ActionChains(browser)
    actions.move_to_element(elem).perform()
    actions.click()

    coordinates = browser.find_element_by_class_name("leaflet-control-mouseposition").text

    browser.quit()
    return coordinates

if __name__ == "__main__":
    main()