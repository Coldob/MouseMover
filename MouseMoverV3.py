import pandas as pd
import numpy as np
import datetime
import time

MouzMovers = True

data=pd.read_excel(io='MouseColony.xlsx' ,sheet_name='MouseDetailedInfo' ,dtype={'cages. MousePerDOB. Gender. DOB. TotalMice. BelongsTo.':object});
def help():
	print(commands)
def findahome():
	owner = True
	gender = True
	DOBV = True
	while owner==True:
		Towner = input('Whos Colony is it?   ').lower()
		if Towner in MouseData:
			owner = Towner
		else:
			if Towner == "quit":
				return()
			print("Sorry we dont not have a record of that person.")
			print("if you would like to return to the main menu type 'quit'.")
	while gender==True:
		tgender = input('Whats the Gender of the mouse?	  ').lower()
		if (tgender == "m") or (tgender == "f") or (tgender =="male") or (tgender == "female"):
			if (tgender == "male"):
				gender = "m"
			if (tgender == "female"):
				gender = "f"
			if (tgender == "f") or (tgender == "m"):
				gender = tgender
		else:
			if tgender == "quit":
				return()
			print("if you arent sure you can use 'quit' and come back later : )")
	while DOBV==True:
		year = str(input("year of birth? four or two digits only...   "))
		if len(year) == 2:
			year = ("20"+year)
		if year == "quit":
			return()
		month = str(input("month of birth?"))
		if month == "quit":
			return()
		day = str(input("day of birth?"))
		if day == "quit":
			return()
		if (year.isnumeric()) and month.isnumeric() and day.isnumeric():
			if (0 < int(month) < 13) and (int(day) < 32 and (len(year)==4)):
				DOBV = (year+"-"+month+"-"+day)
			else:
				print("sorry but we cant have any months higher than 12, days highter than 31, or years with 3 or greater than 4 digits type 'quit' to return to menu")			
		else:
			print("only numbers please 'quit' to return to menu or try again?")
	print(FindaHomecalc(owner, gender, DOBV))
	
def FindaHomecalc(owner, gender, DOBV):
	Youngest = 2704980236
	epochTimeDOB = time.mktime(time.strptime(str(DOBV), '%Y-%m-%d'))
	DOBTop = epochTimeDOB + 2678400
	DOBBottom = epochTimeDOB - 2678400
	temp = MouseData.pop(owner)
	cageList = []
	for cages in temp:
		cageList.append(cages)
	for cages in cageList:
		if not (gender == temp[cages]['Gender']) or (5 == temp[cages]['TotalMice']):
			del temp[cages]
		else:
			for dob in temp[cages]['DOB']:
				Youngest = 2704980236
				epochTime = time.mktime(time.strptime(str(dob),'%Y-%m-%d %H:%M:%S'))
				if epochTime < Youngest:
					Youngest = epochTime
			if not ((DOBBottom <= Youngest) and (DOBTop >= Youngest)):
				del temp[cages]
	for Results in temp:
		cageID = Results
		totalMice = temp[Results]['TotalMice']
		print('~~~~~~~~~~~~~~~~~~~~~')
		print('Cage ID: ' + str(Results))
		print('Total Mice: ' + str(totalMice))
		for RDOB in temp[Results]['DOB']:
			EDOB = str(RDOB)
			print('DOB: ' + str(EDOB))
		print('~~~~~~~~~~~~~~~~~~~~~')
	
	temp.clear()

def export():
	FileName = input("Name of File: ")
	SheetName = input("Name of Sheet: ")
	DataFrame = []
	DataLine = 0
	for x in MouseData:
		for cage in MouseData[x]:
			date = str(MouseData[x][cage]['DOB'][0])
			year = date[0:4]
			month = date[5:7]
			day = date[8:10]
			DataFrame.append(["#" + str(cage)[0:3], MouseData[x][cage]['Gender'], day +'/'+ month +'/'+ year, x, '19'])
			y = 1
			if not MouseData[x][cage]['TotalMice'] == 1:
				F=0
				for d in MouseData[x][cage]['MPDOB']:
					E=0
					while E < d:
						date = str(MouseData[x][cage]['DOB'][F])
						year = date[0:4]
						month = date[5:7]
						day = date[8:10]
						if not y == 1:
							DataFrame.append(["", MouseData[x][cage]['Gender'], day +'/'+ month +'/'+ year,])
							E += 1
						else:
							y = "not 1"
							E+= 1
					F += 1
			DataFrame.append([])
	df = pd.DataFrame(DataFrame)
	df.to_excel(FileName + '.xlsx', sheet_name=SheetName, index=False)	
	print("Exported, Thanks Come again!")

MouseData = {}
def DataGen():
	MouseData.clear()
	for x in range(len(data)):

		person = str(data.loc[x].Belongsto).lower()
		if not (data.isnull().loc[x].Cages):
			if (person not in MouseData):
				MouseData[person]= {}
			cage = str(data.loc[x].Cages)
			MouseData[person][cage]= {'Gender': str(data.loc[x].Gender).lower(), 'TotalMice': int(data.loc[x].TotalMice), 'DOB': [], 'MPDOB':[]}
		
			DOB = data.loc[x].DOB
			MouseData[person][cage]['DOB'].append(DOB)
			MPDOB = data.loc[x].MousePerDOB
			MouseData[person][cage]['MPDOB'].append(MPDOB)
			check = True
			while check == True:
				try:
					x +=1
					if (data.isnull().loc[x].Cages):
						DOB = data.loc[x].DOB
						MouseData[person][cage]['DOB'].append(DOB)
						MPDOB = data.loc[x].MousePerDOB
						MouseData[person][cage]['MPDOB'].append(MPDOB)
					else:
						check = False

				except:
					check = False	

print("'help' for options")
commands = ['quit','help','findahome','export']
while MouzMovers:
	DataGen()
	command = input("1-800MouzMvr How may we assist you today?").lower()
	if command in commands:
		if not command  == 'quit':
			eval(command + "()")
		else:
			print("Thank you, I hope you will consider MouzMvrs Again.")
			MouzMovers = False
	else:
		print("Sorry my tiny ears didnt get that please try again.")
