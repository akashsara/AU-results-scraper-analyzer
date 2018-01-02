#!python3
import os
import re
import requests
import csv
import bs4
import analyze

url = r'http://aucoe.annauniv.edu/cgi-bin/result/cgrade.pl?regno='

# Starting and ending register numbers for normal students and lateral entries. A list of debarred students if applicable
start_number = 0
end_number = 0
lateral_start = 0
lateral_end = 0
debar_list = []

subject_list = []
student_data = {}

def scrapeData(reg):
	try:
		# Get page
		response = requests.get(url + str(reg))
		response.raise_for_status()

		# Parse page and get relevant data
		response_data = bs4.BeautifulSoup(response.text, "html.parser")
		student_info = response_data.select('tr td strong')

		# Set up mark list and no. of arrears and begin data collection
		number_of_arrears = 0
		register_number = student_info[0].getText()
		name = student_info[1].getText()
		mark_list = {'Name': name}

		# Get the grade, pass/fail for each subject
		for i in range(6, len(student_info), 3):
			sub = student_info[i].getText()
			grade = student_info[i + 1].getText()
			result = student_info[i + 2].getText().strip()
			mark_list[sub] = grade
			if(result != 'PASS'):
				number_of_arrears += 1
			if sub not in subject_list:
				subject_list.append(sub)
		
		print(register_number + '\t\t' + mark_list['Name'])

		# Add number of arrears to the student's information and add the entire information to student_data
		mark_list['Arrears'] = number_of_arrears
		student_data[register_number] = mark_list
	except TimeoutError:
		print('Could not connect to Anna University server.')
	except Exception as e:
		print(e)

#Remove old data files
if os.path.isfile('AU Results.csv'):
    os.unlink('AU Results.csv')

print("Connecting...")

#Run for normal students
for i in range(start_number, end_number):
    if i in debar_list:
        continue
    scrapeData(i)

#Run for lateral entries
for i in range(lateral_start, lateral_end):
    if i in debar_list:
        continue
    scrapeData(i)

print('Done scraping! Writing to file..')

#Create new file and set up a writer
dataFile = open('AU Results.csv', 'w', newline='')
writer = csv.writer(dataFile)
writer.writerow(['Register Number', 'Name', 'Arrears'] + subject_list)
for data in student_data:
    results_data = []
    for subject in subject_list:
        if subject in student_data[data].keys():
            results_data.append(student_data[data][subject])
        else:
            results_data.append('')
    writer.writerow([data, student_data[data]['Name'], student_data[data]['Arrears']] + results_data)
dataFile.close()

#Analysis
analyze.runAnalysis()
