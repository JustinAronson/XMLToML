'''
Created on July 22, 2020

@author: justi
'''

if __name__ == '__main__':
    import csv
    import shlex
    import datetime
    
    #Incoming header list
    uniqueColumns = {}
    
    numberOfColumns = 0
    
    allColumns = []
    
    with open('e:\\columnTable.csv') as headersFP:
        columnHeaderLine = headersFP.readline()
        columnHeaderSplitter = shlex.shlex(columnHeaderLine)
        columnHeaderSplitter.whitespace = ','
        columnHeaderSplitter.whitespace_split = True
        allColumns = list(columnHeaderSplitter)
        numberOfColumns = len(allColumns)    
        allColumns[numberOfColumns-1] = allColumns[numberOfColumns-1].rstrip()
        
        columnIndex = 0
        for column in allColumns:
            columnHasNumeric = False
            charCounter = 0
            
            while charCounter < len(column) and columnHasNumeric == False:
                if column[charCounter].isdigit():
                    columnHasNumeric = True
                    
                charCounter += 1
            
            if columnHasNumeric == False:
                uniqueColumns.update({column: columnIndex})
                columnIndex += 1
                
        for key in uniqueColumns:
            
            #Boolean, false if column appears multiple times in file.  Use this to get rid of columns that go in higher table
            columnOnlyAppearsOnce = True
            columnCounter = 0
            
            while columnOnlyAppearsOnce == True and columnCounter < len(allColumns):
                
                if len(allColumns[columnCounter]) != len(key):
                    columnOnlyAppearsOnce = False
                    
                columnCounter += 1
                    
            if columnOnlyAppearsOnce == True:
                uniqueColumns.pop(key)
        
    with open('e:\\csvFile202050000.csv', encoding="utf-8") as csvFile:
        
        writeFile = open(r"E:\\SQLReadyFile.csv", 'w+', newline="", encoding = "utf-8")
        writer = csv.writer(writeFile)
        writer.writerows([uniqueColumns,])
                
        csv_reader = csv.reader(csvFile, delimiter=',')
        lCount = 0
        
        for csvRow in csv_reader:

            newRows = []
            
            #Holds the tag indexes that have appeared in each row
            indexesEncountered = []
            
            #Use submission ID as key for each SQL row
#           subID = csvRow[uniqueColumns["ReleaseSet~ClinVarSet~ClinVarAssertion~ClinVarSubmissionID"]]
            subID = csvRow[uniqueColumns["ReleaseSet~ClinVarSet:a:ID"]]
            
            for column in allColumns:
                
                columnCounter = 0
                indexFound = False
                characterCounter = -1
                
                index = 0
                
                if column[-1].isdigit():
                    while indexFound is False:
                        characterCounter -= 1
                        
                        if not column[characterCounter:].isdigit():
                            #If column is the first instance, index will be 0
                            index = int(column[characterCounter + 1:])
                        
                            indexFound = True
                
                if index not in indexesEncountered:
                    newRows.append([])
                    indexesEncountered.append(index)
                    newRows[index].append(subID)
                    
                if column[:characterCounter] in uniqueColumns:
                    cindex = uniqueColumns[column[:characterCounter]]
                    newRows[index][cindex] = csvRow[columnCounter]
                
                columnCounter += 1
                           
            writer.writerow(newRows)

            lCount += 1

            if lCount % 1000 == 0:
                print(str(lCount) + ': ' + str(datetime.datetime.now()))
                break

    
        writeFile.close()
        
        print("Done!")
