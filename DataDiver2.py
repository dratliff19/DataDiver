##Dylan Ratliff

import nltk
import csv
import sys
import os

masterFile = ""
headersglobal = []

##creates new file, appends to file if already exist##
def saveNewFile(dataToWrite):
    nameOfNewFile = input("Enter a name for prepared file: ")
    if os.path.exists(nameOfNewFile):
        append_write = 'a'  # append if already exists
    else:
        append_write = 'w'  # make a new file if not
    try:
        with open(nameOfNewFile, append_write, newline='', encoding='utf-8') as csv_file2:
            writer2 = csv.writer(csv_file2)

            try:
                num = int(input("Enter a number for classification: "))#the class for the data. Must be a number. (Lucy edition)
                try:
                    column = int(input("Enter number of cloumn to write: "))  ##number of the column you wish to write
                    writeData = []
                    for row in dataToWrite:
                        writeData.append((num, row[column]))  # Write rows to file.
                    writer2.writerows(writeData)
                    csv_file2.close()
                    takecmd(dataToWrite)
                except ValueError:
                    print("Must be an integer!")
            except ValueError:
                print("Must be an integer!")
    except IOError:
        print("File name not valid!")
        saveNewFile(dataToWrite)


def printHeaders(headers): #print headers
    count = 0
    print("<+> Search bank headers <+>")  # list the headers
    for columns in headers:
        print("[" + str(count) + "]" + " " + columns)
        count += 1


def openFile(fileToOpen):
    global masterFile
    global headersglobal
    masterFile = fileToOpen
    try:
        with open(fileToOpen, encoding='utf-8') as file: #try and except block for opening the file here

            reader = csv.reader(file)
            headers = next(reader) #gets the headers for later listing
            headersglobal = headers
            rest = [row for row in reader] #get the rest of the rows here
            count = 0
            for rr in rest: #counts how many rows
                count += 1
            print('Number of rows in document: ' + str(count))  #prints number of rows
            printHeaders(headers)
            print("Successfully opened " + str(fileToOpen))
            return rest
    except IOError:
        print("\nFile not found or open in another location!")
        mainmenu()


def drillDown(restPassed):

    try:
        mineByInt = int(input("Enter Column number to drill down by:>> "))
        count = 0
        uniques = []

        for current in restPassed:
            if current[mineByInt] not in uniques:
                uniques.append(current[mineByInt])  # gets the unique values of the column selected and numbers them
        print("\nUnique Values: ")

        for unique in uniques:
            print("[" + str(count) + "]" + unique)  # prints
            count += 1

        terms = input("Parse By(number key or --back):>> ")  # if the user wants to parse by a value, take that here.
        if terms == '--back':  # otherwise go back using --back
            takecmd(restPassed)
        try:
            termsIntval = int(terms)

        except ValueError:
            print("Not an integer Input")
            drillDown(restPassed)

        count = 0
        drilledDown = []
        for current in restPassed:
            if current[mineByInt] == uniques[termsIntval]:  # creates new sliced data type
                count += 1
                drilledDown.append(current)

        totalRowsDrilled = 0
        for cc in restPassed:
            totalRowsDrilled += 1  # determines original and new counts and displays them.

        print("Drilled down to: " + str(count) + "/" + str(totalRowsDrilled) + " rows")
        takecmd(drilledDown)
    except ValueError:
        print("Must enter a number or out of range!")
        drillDown(restPassed)


def takecmd(data):
    global headersglobal
    cmd = input("DataDiver>>")
    if cmd == "create": ##create data set
        saveNewFile(data)
    elif cmd == "drill": ##drill down by column
        drillDown(data)
    elif cmd == "headers": ##list headers from file
        printHeaders(headersglobal)
        takecmd(data)
    else:
        takecmd(data)


#--Main menu of the program. Can be accessed when the user closes a file.--#
def mainmenu(): #the main menu of the program.
    file = input("Enter the name of the file to mine:>> ")
    filedata = openFile(file) #call to open file
    takecmd(filedata)

#end

def main():
    print("<+> Welcome to Data Diver by DCRDevelopments <+> ")
    mainmenu()

main()