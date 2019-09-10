'''
Created on Aug 30, 2019

@author: justi
'''

if __name__ == '__main__':
    import csv
    import shlex
    import datetime
    
    #Incoming header list
    columnHeaderList = []
    
    #Counts of Entries Per Column
    columnCounts = {}
    
    #List that will contain booleans indicating whether a column index
    #should be prepresented in the output
    columnShouldTransfer = []
    
    #Min number of values in a column for it to transfer
    minColumnEntries = 0
    
    #Index of Max column that makes the minColumnEntries threshold
    maxColumnsToCheck = 0
    
    numberOfColumns = 0
    
    with open('e:\\columnTable.csv') as headersFP:
        columnHeaderLine = headersFP.readline()
        columnHeaderSplitter = shlex.shlex(columnHeaderLine)
        columnHeaderSplitter.whitespace = ','
        columnHeaderSplitter.whitespace_split = True
        columnHeaderList = list(columnHeaderSplitter)
        numberOfColumns = len(columnHeaderList)    
        columnHeaderList[numberOfColumns-1] = columnHeaderList[numberOfColumns-1].rstrip()    
    
    with open('e:\\columnCount.csv') as columnCountCSV:
        csv_reader = csv.reader(columnCountCSV, delimiter=',')
        for csvRow in csv_reader:
            columnCounts[csvRow[0]] = int(csvRow[1])
            
    for i in range(numberOfColumns):
        if columnCounts[columnHeaderList[i]] >= minColumnEntries:
            maxColumnsToCheck = i
            columnShouldTransfer.append(True)
        else:
            columnShouldTransfer.append(False)
            
        
            
        
    with open('e:\\csvFile.csv', encoding="utf-8") as csvFile:
        
        writeFile = open(r"E:\\csvFileWithHeaders.csv", 'w+', newline="", encoding = "utf-8")
        writer = csv.writer(writeFile)
        writer.writerows([columnHeaderList,])
                
        csv_reader = csv.reader(csvFile, delimiter=',')
        lCount = 0
        
        for csvRow in csv_reader:
            
            newRow = []
            
            for i in range(maxColumnsToCheck):
                if i < len(csvRow):
                    if columnShouldTransfer[i]:
                        newRow.append(csvRow[i])
                    else:
                        newRow.append('')
            writer.writerows([newRow,])
            if lCount % 1000 == 0:
                print(str(lCount) + ': ' + str(datetime.datetime.now()))

            lCount += 1

    
        writeFile.close()
        
        print("Done!")