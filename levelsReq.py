# Import necessary packages
from bs4 import BeautifulSoup
import requests
import re
import sys


def company_levels():
	try:
		company = None
		# Get the company name from the command line if available
		if len(sys.argv) == 2:
			company = sys.argv[1]
		# Otherwise ask the user for the company name through prompt
		else:
			company = input("Enter company name: ")
		# Declare url
		URL = f'https://www.levels.fyi/company/{company}/salaries/Software-Engineer/'
		# Declare Browser
		user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.27 Safari/537.36"
		headers = {'User-Agent': user_agent}
		# Get the page
		page = requests.get(URL, headers=headers)
		# Use BeautifulSoup package to parse as html
		soup = BeautifulSoup(page.content, 'html.parser')
		# Find the table containing the level information
		result = str(soup.find('table', class_='table salary-by-level-table'))
		# Find the names of the levels
		levels = re.findall(rf'(?<=style="text-decoration:none">)\S+(?=</a)', result)
		if len(levels) == 0:
			raise ValueError(f'{company} not found')
		# Find the compensations of the levels
		compensation = []
		for i in result.split('>'):
			if '$' in i:
				compensation.append(i.strip('</p'))
		assembled_levels = {}
		# Assemble the levels and their compensations into a dictionary
		for i in range(len(levels)):
			total, base, stock_yr, bonus = compensation.pop(0), compensation.pop(0), compensation.pop(0), compensation.pop(0)
			assembled_levels[levels[i]] = {'Total': total, 'Base': base, 'Stock (/yr)': stock_yr, 'Bonus': bonus}
		return assembled_levels
	except ValueError:
		if len(sys.argv) == 2:
			print(f'Company "{company}" not found')
			exit()
		print("Error: Invalid company name")
		return company_levels()


def makeHtml(data):
	with open("output.html", "w") as f:
		f.write('<!DOCTYPE html><html><head><style>')
		f.write('body {background-color: #fafafa;}')
		f.write('table, td, th {border: 1px solid black;}')
		f.write('table {border-collapse: collapse; width: 100%;}')
		f.write('th, td {text-align: left; padding: 8px;}')
		f.write(f'</style></head><body>')
		f.write('<table>')
		f.write('<tr><td>Level</td><td>Total</td><td>Base</td><td>Stock (&sol;yr)</td><td>Bonus</td></tr>')
		for row in data:
			total, base, stock_yr, bonus = data[row]['Total'], data[row]['Base'], data[row]['Stock (/yr)'], data[row]['Bonus']
			f.write('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (row, total, base, stock_yr, bonus))
		f.write('</table>')
		f.write('</body></html>')


levels_compensation = company_levels()
print(levels_compensation)
makeHtml(levels_compensation)
