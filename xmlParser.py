
'''
Created on Jun 30, 2019

@author: justi
'''
import xml.sax
import csv
import os
import time

#if __name__ == '__main__':
    
class TableCreatorHandler( xml.sax.ContentHandler ):
    def __init__(self):    
        print("Initializing Parser")
        
        #current tag depth
        self.depth = 0    
        
        #maximum tag depth encountered thus far        
        self.maxDepth = 0        
        
        #dictionary mapping tags to columns
        self.tagColumn = {}
        
        #the csv table
        self.csvTable = []
        
        #A stack of current x path
        self.xPath = []
        
        #number of rows processed
        self.rowCounter = -1
        
        #buffer for accummulating characters between start and end tags
        self._charBuffer = []
        self.charString = ""
        
        self.varID = "unset"
        
        #dictionary containing the max number of appearances 
        #that a tag has had in single row
        self.tagMaxAppearance = {}
        
        #dictionary containing the max number of appearances 
        #that a tag has had in single row
        self.tagAppearanceOnThisRow = {}
        
        #Flags whether the parser is on the first row.  Changed to 1 after first row processed
        self.firstRowPastFlag = False
        
        self.itemCount = {}
        
#        os.chmod(r"C:\Users\justi\Documents\csvFile.csv", 0o777)
        
        self.writeFile = open(r"e:\csvFileUniProt.csv", 'w+', newline="", encoding = "utf-8")
        self.writer = csv.writer(self.writeFile)

#        os.chmod(r"C:\Users\justi\Documents\columnTable.csv", 0o777)
        self.writeColumnTable = open(r"e:\columnTableUniProt.csv", 'w+', newline="", encoding = "utf-8")
        self.writerForCT = csv.writer(self.writeColumnTable)
        
        self.writeColumnCount = open(r"e:\columnCountUniProt.csv", 'w+', newline="", encoding = "utf-8")
        self.writerForCC = csv.writer(self.writeColumnCount)
            
    def closeFile(self):
#        os.chmod("csvFile.csv", 0o777)
        self.writeFile.close()
        
#        os.chmod("columnTable.csv", 0o777)
        self.writerForCT.writerows([self.tagColumn])
        self.writeColumnTable.close()
        
        self.writerForCC.writerows(self.itemCount.items())
        
        self.writeColumnCount.close()
        
    def startElement(self, tag, attributes):
        
        self.xPath.append(tag)
        
        tagPath = '~'.join(self.xPath)
        
#        if 'VariationID' in attributes:
#            self.varID = attributes.get('VariationID')
            
#        print("VarID: " + self.varID + "In startElement tag:" + tag)
        
        #if we have reached a new depth, increment max depth
        if self.depth > self.maxDepth : self.maxDepth = self.depth
        
        #depth 1 indicates the start of a row so reach appropriately
        if self.depth == 1:
            self.rowCounter += 1
            if self.firstRowPastFlag == True:
                self.writer.writerows([self.csvTable])
            else:
                self.firstRowPastFlag = True
            self.csvTable = []
            self.tagAppearanceOnThisRow = {}
        
        if self.depth != 0:  
            self.processStartElement(tagPath, attributes)
        self.depth += 1
        
    def processStartElement(self, tagPath, attributes):
        indexedTag = self.processItems(tagPath)
        for key, value in attributes.items():
            attributeTag = indexedTag + ":a:" + key
            self.processItems(attributeTag)
            tagIndex = self.getTagIndex(attributeTag)
            self.csvTable[tagIndex] = value
        
        
    def processItems(self, tagPath):
        if tagPath not in self.tagColumn:
            self.newTagInit(tagPath)
                            
        currentAppearance = 0
        if tagPath not in self.tagAppearanceOnThisRow:
            newEntryForFirstAppearance = {tagPath: 0}
            self.tagAppearanceOnThisRow.update(newEntryForFirstAppearance)
            currentAppearance = 0
        else:
            currentAppearance = self.tagAppearanceOnThisRow.get(tagPath)
            currentAppearance = currentAppearance + 1
            updatedAppearance = {tagPath: currentAppearance}
            self.tagAppearanceOnThisRow.update(updatedAppearance)
        
        if currentAppearance != 0:    
            indexedTag = tagPath + str(currentAppearance)
        else:
            indexedTag = tagPath
            
        if currentAppearance > self.tagMaxAppearance.get(tagPath):
            newMaxAppearance = {tagPath: currentAppearance}
            self.tagMaxAppearance.update(newMaxAppearance)
            newEntry = {indexedTag: len(self.tagColumn)}
            self.tagColumn.update(newEntry)        
            
        if indexedTag in self.itemCount:
            newCount = self.itemCount.get(indexedTag) + 1
        else:
            newCount = 1
            
        updatedItemCount = {indexedTag: newCount}
        self.itemCount.update(updatedItemCount)
        
        return indexedTag
            
    def newTagInit(self, tagPath):
            newEntry = {tagPath: len(self.tagColumn)}
            self.tagColumn.update(newEntry)
            newMaxAppearance = {tagPath: 0}
            self.tagMaxAppearance.update(newMaxAppearance)
            
            newItemCount = {tagPath: 0}
            self.itemCount.update(newItemCount)        
    
    def characters(self, data):
        if data != "\n" or data != "\"" or data != '\'':
            self._charBuffer.append(data)
        for i in range(0, len(self._charBuffer)):
            if self._charBuffer[i] == "\n" or self._charBuffer[i] == "\r" or self._charBuffer[i] == "\"" or self._charBuffer[i] == '\'':
                self._charBuffer[i] = ""    
            
    def getTagIndex(self, tagPath):
        tagIndex = 0
        
        if self.tagAppearanceOnThisRow.get(tagPath) != 0:
            tagIndex = self.tagColumn.get(tagPath + str(self.tagAppearanceOnThisRow.get(tagPath)))
        else:
            tagIndex = self.tagColumn.get(tagPath)
            
        while len(self.csvTable) < tagIndex + 1:
            self.csvTable.append("")
            
        return tagIndex
            
    def endElement(self, tag):
 #       if self.rowCounter > 1307:
 #           self.closeFile()
 #           quit()          
        
        tagPath = '~'.join(self.xPath)
        
        self.depth -= 1
        if self.depth != 0:
            
            #put into called methods
            tagIndex = self.getTagIndex(tagPath)
                    
            #Convert from CharList to String and strip whitespace    
            self.csvTable[tagIndex] = ''.join(self._charBuffer).strip()
            
            #Delete this line?
            if self._charBuffer == []:
                self.csvTable[tagIndex] = ""
            
            self.charString = ""
            self._charBuffer= []      
            
        self.xPath.pop()
        
    def printParser(self):
        
        #Add column headers
        
        for i in range(0, self.csvTable.__len__()):
            print(self.csvTable[i], end="")
            print("\r")
    
parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces, 0)

Handler = TableCreatorHandler()
parser.setContentHandler( Handler )

parser.parse("E:\\uniprot_sprot.xml")

print(Handler.csvTable)

print("---------------------")
Handler.printParser()
print("Done")
Handler.closeFile()
