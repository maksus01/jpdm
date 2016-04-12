#!/usr/bin/python

# from dataset import Dataset

##########################################################################
# Function for reading data files.
# Builds a list of dataset objects from the input files that are read.
##########################################################################

import dataset
import sys, os

class Read:
   verbose = False
   fileRange = []
   skipFiles = []
   dataSets = [] # List of dataset objects, each representing the data from one input file (corresponding to one set of excel data)


   def __init__(self, verbose):
      verbose = False
      dir = os.path.dirname(sys.argv[0])
      listDirPath  =  os.path.join(dir, "../../data/FormattedDataFiles/")
      nFiles = len(os.listdir(listDirPath))
      print nFiles
      self.fileRange = [0, nFiles];

      for i in range(self.fileRange[0], self.fileRange[1]):
         # print "READING...", i
         if i in self.skipFiles:
            continue
         
         # print "DIR", dir
         filePath =  os.path.join(dir, "../../data/FormattedDataFiles/T"+str(i)+".txt")
         self.dataSets.append(self.readFile(filePath, i)) # Read and store data as Dataset object
         

      if verbose:
         for d in self.dataSets:
            print "-----------------------TITLES:", d.getTitles()
            print d.toString(),"\n"

   
   def readFile(self, filePath, datasetID):
      # print "IN READ FUNCTION", datasetID
      f = open(filePath,'r')
      title = ""
      subtitle = ""
      columnRange = ""
      dataDictionary = {}
      line = f.readline()

      if "<TITLE>" in line:
         line = f.readline() 
         while not "<SUBTITLE>" in line:
            title += line
            line = f.readline()

      if "<SUBTITLE>" in line:
         line = f.readline() 
         while not "<EXCEL COLUMN RANGE>" in line:
            subtitle += line
            line = f.readline()

      if "<EXCEL COLUMN RANGE>" in line:
         line = f.readline() 
         while not "<VECTOR LABELS>" in line:
            columnRange+=line
            line = f.readline()

      labels = []
      if "<VECTOR LABELS>" in line:
         line = f.readline()
         while not "<DATA>" in line:
            labels.append(line)
            line = f.readline()

      labelIndex = 0

      if "<DATA>" in line:
         line = f.readline()
         while not (line == "" or line=="\n"):
            line = line.strip()
            lineSplit = line.split() # Split on white space
            dataVector = []
            for s in lineSplit:
               dataVector.append(self.parseNumber(s))
            # print "DATASET ID", datasetID
            # print "LABEL INDEX", labelIndex
            L=labels[labelIndex]
            dataDictionary["T"+str(datasetID)+"-"+L]=dataVector
            labelIndex+=1
            line = f.readline()

      if not (len(dataDictionary)==len(labels)):
         print "ERROR 1"

      f.close()
      # Finally, make Dataset object
      # print "LEAVING READ FUNCTION"
      return dataset.Dataset(title, subtitle, columnRange, dataDictionary)


   def parseNumber(self, s):
      number = 0
      try:
         number = float(s)
         return number
      except:
         try: # Try removing a comma
            number = float(s.replace(",",""))
            return number
         except:
            return -1.0

   def getDataSets(self):
      return self.dataSets