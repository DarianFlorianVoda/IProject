from matplotlib import pyplot as plt
import pandas as pd
import os
import shutil


def barchart():
    info = pd.read_csv('../Covid19Stats.csv')
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
    data = pd.read_csv('../Covid19Stats.csv')
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
    data = pd.read_csv('../Covid19Stats.csv')
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