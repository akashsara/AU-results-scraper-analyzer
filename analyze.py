#!python3
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def makeBar(data, title):
    print("Generating chart for " + title)
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
		#makeArrearChart(results, titles[0])
		for title in titles:
			makeBar(results, title)
	else:
		print("Error! Could not find results to analyze!")