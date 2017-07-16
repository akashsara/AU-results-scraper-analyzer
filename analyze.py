#!python3
import os
import pandas as pd
import matplotlib.pyplot as plt

def makeArrearChart(data, title):
    #Draw chart
    data = data[title].value_counts()
    data.plot(kind='pie', autopct='%1.0f%%', title=title, shadow=True, startangle=90, labels=None)
    #Remove labels
    plt.axes().set_ylabel('')
    plt.axes().set_xlabel('')
    #Add legend
    labels = [str(i) + ' Arrears: ' + str(data[i]) for i in data.index]
    plt.legend(labels=labels, loc="best")
    #Apply proper spacing and save
    plt.tight_layout()
    plt.savefig(title + '.jpg')
    plt.close()

def makeBar(data, title):
    #Draw chart
    data = data[title].value_counts()
    data.plot(kind='barh', title=title)
    #Add raw values
    for i, v in enumerate(data):
        plt.text(v + 0.5, i - 0.05, str(v), color='black', fontweight='bold', fontsize=12)
    #Apply proper spacing and save
    plt.tight_layout()
    plt.savefig(title + '.jpg')
    plt.close()

def runAnalysis():
    data = pd.read_csv('data.csv')
    #Ignores register no. and name columns
    data = data.iloc[:, 2:]

    titles = list(data)

    print('Generating graph for %s.' %titles[0])
    makeArrearChart(data, titles[0])

    for title in titles[1:]:
        print('Generating graph for %s.' %title)
        makeBar(data, title)
