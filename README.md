# Anna University Results Scraper/Analyzer

## What is it?

It's a script that scrapes the results of all students in the given range of register numbers and analyzes it to display graphs of the results on a per-subject basis.

## Setup & Usage:

_Requires Python3 and the following libraries: pandas, matplotlib, BeautifulSoup4 and Requests_

1. Edit `scrape.py` with the starting and ending register numbers as well as the subjects to scrape. Make sure that the subjects are in the same order as the results.

2. Run the script.

3. A `data.csv` file, a `Arrears.jpg` file and a number of images corresponding to each subject will appear in the directory from which the script is run.

## Screenshots:

![Subject Graph](https://i.imgur.com/sHZ7B8B.jpg)

![Arrear Pie Chart](https://i.imgur.com/aJSNY9W.jpg)
