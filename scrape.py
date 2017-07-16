#!python3
import os, re, requests, csv, bs4, analyze

url = r'http://aucoe.annauniv.edu/cgi-bin/result/cgrade.pl?regno='

#Starting and ending register numbers for normal students and lateral entries. A list of debarred students if applicable
startNo = 0
endNo = 0
latStart = 0
latEnd = 0
debarList = [0,0,0]
#Subjects for the semester. Make sure this is in the order in which the results are announced.
subjectCodes = ['CS6401', 'CS6402', 'CS6403', 'CS6411', 'CS6412', 'CS6413', 'CS6551', 'EC6504', 'MA6453']
#This is for the title of columns in the csv and the title of each chart. You can rename it as you like
subjectList = ['CS6401 - Operating Systems', 'CS6402 - Design & Analysis of Algorithms', 'CS6403 - Software Engineering', 'CS6411 - Networks Laboratory', 'CS6412 - Microprocessor & Microcontroller Laboratory', 'CS6413 - Operating Systems Laboratory', 'CS6551 - Computer Networks', 'EC6504 - Microprocessor & Microcontroller', 'MA6453 - Probability & Queueing Theory']

def scrapeData(reg):
    #Get page
    try:
        response = requests.get(url + str(reg))
        response.raise_for_status()
        print('Scraping %s.' %reg)

        #Parse page and get relevant data
        data = bs4.BeautifulSoup(response.text, "html.parser")
        studentInfo = data.select('tr td strong')

        #Set up mark list and no. of arrears and begin data collection
        markList = []
        noArrears = 0
        regNo = studentInfo[0].getText()
        name = studentInfo[1].getText()

        for i in range(6, len(studentInfo), 3):
            sub = studentInfo[i].getText()
            if sub in subjectCodes:
                grade = studentInfo[i + 1].getText()
                result = studentInfo[i + 2].getText().strip()
                if(result != 'PASS'):
                    noArrears += 1
                markList.append(grade)
        writer.writerow([regNo, name, noArrears] + markList)
    except TimeoutError:
        print('Could not connect to Anna University server.')

#Remove old data files
if os.path.isfile('data.csv'):
    os.unlink('data.csv')

#Create new file and set up a writer
dataFile = open('data.csv', 'w', newline='')
writer = csv.writer(dataFile)
writer.writerow(['Register No.', 'Name', 'Arrears'] + subjectList)

#Run for normal students
for i in range(startNo, endNo):
    if i in debarList:
        continue
    scrapeData(i)

#Run for lateral entries
for i in range(latStart, latEnd):
    if i in debarList:
        continue
    scrapeData(i)

print('Done!')
dataFile.close()

#Analysis
analyze.runAnalysis()
