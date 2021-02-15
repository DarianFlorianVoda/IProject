import requests
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import csv
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
import os
import shutil

text = []
longitude = []
latitude = []


def getdata():
    url = "https://www.worldometers.info/coronavirus/"
    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')

    filename = 'Covid19Stats.csv'
    csv_writer = csv.writer(open(filename, 'w', encoding='utf8'))

    header = soup.find('thead').text.strip()
    global text
    text = header.split("\n")
    text.remove('')
    text.pop(-1)
    text[-4] = text[-4] + text[-3]
    text.pop(-3)
    text[-5] = 'Tot Cases/1M pop'
    text[1] = 'Country'
    csv_writer.writerow(text)

    # Parse the data from the table only COUNTRIES
    for data in range(9, 228):
        next_data = soup.find_all('tr')[data].text.strip()
        splitter = next_data.split("\n")

        # Put from Blank spaces to 0 and remove first commas and remove from the Total Deaths and Population the spaces
        for index, item in enumerate(splitter):
            if index == 4:
                if item.find(' ') != -1:
                    char = splitter[index].find(' ')
                    splitter[index] = splitter[index][:char] + splitter[index][char + 1:]

            if splitter[index] == splitter[-3]:
                if item.find(' ') != -1:
                    char = splitter[index].find(' ')
                    splitter[index] = splitter[index][:char] + splitter[index][char + 1:]

            if item == '' or item == ' ':
                splitter[index] = 0
            result = isinstance(splitter[index], str)

            if result:
                if item.find(',') != -1:
                    char = splitter[index].find(',')
                    splitter[index] = splitter[index][:char] + splitter[index][char + 1:]

        # Remove second commas
        for index, item in enumerate(splitter):
            result = isinstance(splitter[index], str)
            if result:
                if item.find(',') != -1:
                    char = splitter[index].find(',')
                    splitter[index] = splitter[index][:char] + splitter[index][char + 1:]

        # Eliminate last column
        splitter.pop(-1)

        # Put 0s to those which are not numbered
        if len(splitter) != 16:
            while len(splitter) != 16:
                splitter.append(0)

        # INDIA - Remove last comma
        if data == 10:
            char = splitter[14].find(',')
            splitter[14] = splitter[14][:char] + splitter[14][char + 1:]

        # Put the proper numbering after Bahrain
        if data > 89:
            splitter[0] = str(int(splitter[0]) + 1)

        # Introduce China to number 82
        elif data == 89:
            csv_writer.writerow(splitter)
            last_data = soup.find_all('tr')[228].text.strip()
            splitter = last_data.split("\n")
            splitter.pop(-1)

            splitter[0] = '82'

            # China avoid e+ problem and no value
            if splitter[4].find(' ') != -1:
                char = splitter[4].find(' ')
                splitter[4] = splitter[4][:char] + splitter[4][char + 1:]

            if splitter[-2].find(' ') != -1:
                char = splitter[-2].find(' ')
                splitter[-2] = splitter[-2][:char] + splitter[-2][char + 1:]

            if splitter[5] == '' or splitter[5] == ' ':
                splitter[5] = 0

            # Remove China's commas.
            for index3, k in enumerate(splitter):
                result = isinstance(k, str)
                if result:
                    while splitter[index3].find(',') != -1:
                        if splitter[index3].find(',') != -1:
                            char = splitter[index3].find(',')
                            splitter[index3] = splitter[index3][:char] + splitter[index3][char + 1:]

        # Put the proper Population numbering
        if data == 223:
            splitter[-2] = 1432
            splitter[-1] = 'Europe'
        elif splitter[1] == "Diamond Princess":
            splitter[-2] = 2670
            splitter[-1] = 'Asia'
        csv_writer.writerow(splitter)


def createfolder():
    path = "Covid19Stats"
    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)


def barchart():
    info = pd.read_csv('Covid19Stats.csv')
    plt.figure(figsize=(10, 6))
    plt.title("Total New Cases by Continent")
    plt.bar(info.Continent, info.NewCases, color='midnightblue')
    plt.xlabel('Continent')
    plt.ylabel('Total New Cases')
    plt.ylim(0, 250000)
    name_fig = 'barchart.png'
    plt.savefig(name_fig, bbox_inches='tight')
    plt.show()
    try:
        shutil.move(f"{os.getcwd()}\{name_fig}", f"{os.getcwd()}\Covid19Stats")
    except OSError:
        os.remove(f"{os.getcwd()}\Covid19Stats\{name_fig}")
        plt.figure(figsize=(10, 6))
        plt.title("Total New Cases by Continent")
        plt.bar(info.Continent, info.NewCases, color='midnightblue')
        plt.xlabel('Continent')
        plt.ylabel('Total New Cases')
        plt.ylim(0, 250000)
        name_fig = 'barchart.png'
        plt.savefig(name_fig, bbox_inches='tight')
        shutil.move(f"{os.getcwd()}\{name_fig}", f"{os.getcwd()}\Covid19Stats")
        print("File was overwritten")


def piechart():
    data = pd.read_csv('Covid19Stats.csv')
    df = pd.DataFrame(
        data={'Country': data['Country'], 'value': data['TotalCases']}, ).sort_values('value', ascending=False)

    # top 5
    df2 = df[:5].copy()

    # others
    new_row = pd.DataFrame(
        data={
            'Country': ['others'], 'value': [df['value'][5:].sum()]
        }
    )

    # combine top 5 with others
    df2 = pd.concat([df2, new_row])

    fig, axes = plt.subplots()
    df2.plot(kind='pie', y='value', labels=df2['Country'], ax=axes, legend=None, autopct='%1.0f%%', pctdistance=0.7,
             labeldistance=1.1)
    plt.axis('off')
    axes.set_title('Top 5 countries by Total Cases')
    name_fig = 'piechart.png'
    plt.savefig(name_fig, bbox_inches='tight')
    plt.show()
    try:
        shutil.move(f"{os.getcwd()}\{name_fig}", f"{os.getcwd()}\Covid19Stats")
    except OSError:
        os.remove(f"{os.getcwd()}\Covid19Stats\{name_fig}")
        fig, axes = plt.subplots()
        df2.plot(kind='pie', y='value', labels=df2['Country'], ax=axes, legend=None, autopct='%1.0f%%', pctdistance=0.7,
                 labeldistance=1.1)
        plt.axis('off')
        axes.set_title('Top 5 countries by Total Cases')
        name_fig = 'piechart.png'
        plt.savefig(name_fig, bbox_inches='tight')
        shutil.move(f"{os.getcwd()}\{name_fig}", f"{os.getcwd()}\Covid19Stats")
        print("File was overwritten")


def scatterchart():
    data = pd.read_csv('Covid19Stats.csv')
    plt.scatter(data.TotalDeaths, data.TotalCases)
    plt.ylabel("Total Cases")
    plt.xlabel("Total Deaths")
    plt.title("Scatter Plot about Total Cases and Deaths")
    name_fig = 'scatter.png'
    plt.savefig(name_fig, bbox_inches='tight')
    plt.show()
    try:
        shutil.move(f"{os.getcwd()}\{name_fig}", f"{os.getcwd()}\Covid19Stats")
    except OSError:
        os.remove(f"{os.getcwd()}\Covid19Stats\{name_fig}")
        plt.scatter(data.TotalDeaths, data.TotalCases)
        plt.ylabel("Total Cases")
        plt.xlabel("Total Deaths")
        plt.title("Scatter Plot about Total Cases and Deaths")
        name_fig = 'scatter.png'
        plt.savefig(name_fig, bbox_inches='tight')
        shutil.move(f"{os.getcwd()}\{name_fig}", f"{os.getcwd()}\Covid19Stats")
        print("File was overwritten")


def findGeocode(city):
    try:
        geolocator = Nominatim(user_agent="your_app_name")
        return geolocator.geocode(city)
    except GeocoderTimedOut:
        return findGeocode(city)


def execGeocode():
    data = pd.read_csv('Covid19Stats.csv')
    for i in data['Country']:
        if findGeocode(i) is not None:
            loc = findGeocode(i)
            latitude.append(loc.latitude)
            longitude.append(loc.longitude)
        else:
            latitude.append(np.nan)
            longitude.append(np.nan)
    print(latitude)
    print(longitude)


def checkGeocode():
    k = 0
    for j in range(len(latitude)):
        geolocator = Nominatim(user_agent="your_app_name")
        print(latitude[j], longitude[k])
        location = geolocator.reverse(str(str(latitude[k]) + ', ' + str(longitude[j])))
        print(location.address)
        k = k + 1


getdata()
createfolder()
barchart()
piechart()
scatterchart()
# execGeocode()
# checkGeocode()
