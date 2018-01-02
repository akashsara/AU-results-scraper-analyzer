#!python3
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    data = data[title].sort_values()
    #Using seaborn for plotting
    ax = sns.countplot(x=data.index, data=data)
    #To get absolute values for each grade

    for p in ax.patches:
        height = p.get_height()
        ax.text(p.get_x() + p.get_width()/2.,
                height + 0.5,
                '{:1}'.format(int(height)),
                ha="center")

    plt.tight_layout()
    plt.savefig(title + '.jpg')
    plt.close()

def runAnalysis():
	if os.path.isfile('AU Results.csv'):
		results = pd.read_csv('AU Results.csv')
		#Ignores register no. and name columns
		results = results.iloc[:, 2:]
		titles = list(results)
	else:
		print("Error! Could not find results to analyze!")