import pandas as pd
import MySQLdb
import datetime
import os
import shutil
import time
import pathlib
import logging
startProgram = time.time()
print ("--------------------Matching Address STARTED--------------------")

class propsFile:
    host = "localhost"
    username = "admin"
    password = "root"
    db = "database"
    mainFolder = "C:\\testFiles\\"
    logsFolder = "C:\\Users\\Desktop\\Logs\\"
    logFile = "test.log"
    dbColumns = ['Billing Account Description', 'Product Instance', 'Ordered for', 'Matching address', 'Priority Assist', 'Status', 'UNI-D UNI ID', 'UNI-D Access Service ID']
    pandaChunkSize = 100000
    pollInterval = 10   #Define Polling In Secs


def checkFolder (folderLoc):
    if not os.path.exists(folderLoc):
        os.makedirs(folderLoc)


def createCurrFolder():
    now = datetime.datetime.now()
    year = str(now.year)
    month = now.strftime('%m')
    day = now.strftime('%d')
    strCurrFolder = year+month+day
    return strCurrFolder


def delTable (tableName):
    #Connect to DB
    connection = MySQLdb.connect (host=propsFile.host, user = propsFile.username, passwd = propsFile.password, db = propsFile.db)

    #Query
    sqlQuery = "Delete from " + tableName + ";"
    print(sqlQuery)
    start = time.time()
    print ("Start executing Delete Query at:" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + "\n")

    cursor = connection.cursor()
    cursor.execute(sqlQuery)    
    connection.commit()

    #Close Connection
    connection.close()

    end = time.time()
    print ("Time elapsed to run Delete query:")
    print (str((end - start)*1000) + ' ms')
  

def loadCSVFile(sourceCSV):
    sourceCSV = sourceCSV.replace("\\", "\\\\")

    print(sourceCSV)
    start = time.time()
    print ("Start executing: " + sourceCSV + " at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + "\n")
    sqlLoadFile = ("LOAD DATA LOW_PRIORITY LOCAL INFILE\n" + 
                "'" + sourceCSV + "'\n" + 
                "REPLACE INTO TABLE `copper_rehab`.`tbltest`\n" +
                "FIELDS TERMINATED BY ','\n"
                "OPTIONALLY ENCLOSED BY '\"'\n" +
                "LINES TERMINATED BY '\\r\\n'" + "\n" +
                "IGNORE 1 LINES (`BILLING_ACCOUNT_DESCRIPTION`, `PRODUCT_INSTANCE`, `ORDERED_FOR`, `MATCHING_ADDRESS`, `PRIORITY_ASSIST`, `STATUS`, `UNI_ID`, `ACCESS_SERVICE_ID`);"
    )
    print(sqlLoadFile)

    #Connect to DB
    connection = MySQLdb.connect (host=propsFile.host, user = propsFile.username, passwd = propsFile.password, db = propsFile.db)

    cursor = connection.cursor()
    cursor.execute(sqlLoadFile)    
    connection.commit()

    #Close Connection
    connection.close()
    
    end = time.time()
    print ("Time elapsed to run the query:")
    print (str((end - start)*1000) + ' ms')
   


def spliceCSVandLoadDB (inputFile, columns, chunkSize, counter, opFilesLoc):
    for chunck_df in pd.read_csv(inputFile, skip_blank_lines=True, skipinitialspace=True, chunksize=chunkSize, header=0, usecols=columns):
        print (chunck_df.shape)
        counter = counter+1
        print(counter)
        opChunkFilesLoc = opFilesLoc+str(counter)+".csv"
        chunck_df.to_csv(opChunkFilesLoc, sep = ",", index=False)
        print("Splicing Ends")
        #LoadFile
        #loadCSVFile(opChunkFilesLoc)


def delFolder(folderPath):
    shutil.rmtree(folderPath)


def main():
    #Current Date Folder
    currFolder = createCurrFolder()
    print(currFolder)

    #Paths
    rootFolder = propsFile.mainFolder
    fbFile = rootFolder+currFolder+"\\"+"folder1"+currFolder+".csv"
    print(fbFile)
    fnFile = rootFolder+currFolder+"\\"+"folder2"+currFolder+".csv"
    print(fnFile)
    chunkFilesLoc = rootFolder+currFolder+"\\ChunkFiles\\"
    print(chunkFilesLoc)

    #Empty Table and create ChunkFiles Folder
    if os.path.exists(rootFolder+currFolder):
        #delTable("tbltest")
        #Check Folder
        checkFolder(chunkFilesLoc)

    #Variables
    cols = propsFile.dbColumns
    chunkSz = propsFile.pandaChunkSize

    #Dummy -- Split CSV and Load Data
    print("Dummy - Split CSV and Load Data")   
    outputFileLoc = chunkFilesLoc+"fold1"+currFolder+"_"
    filename = fbFile
    if os.path.exists(filename):
        spliceCSVandLoadDB(fbFile,cols,chunkSz,0,outputFileLoc)
    else:
        print ("Dummy File doesn't exist for Today's Date")
        logger.info("Dummy File doesn't exist for Today's Date")

    #Dummy1 -- Split CSV and Load Data
    print("Dummy1 - Split CSV and Load Data")
    filename = fnFile
    outputFileLoc = chunkFilesLoc+"AVC_Dummy1_"+currFolder+"_"
    if os.path.exists(filename):
        spliceCSVandLoadDB(fnFile,cols,chunkSz,0,outputFileLoc)
    else:
        print ("Dummy1 File doesn't exist for Today's Date")
        logger.info("Dummy1 File doesn't exist for Today's Date")

    #Remove ChunkFile Folder
    # if os.path.exists(chunkFilesLoc):
    #     delFolder(chunkFilesLoc)
    
   
if __name__ == "__main__":
    #Set Logging
    #Check Logs Folder
    checkFolder(propsFile.logsFolder)
    logsLocation = propsFile.logsFolder+propsFile.logFile
    print (logsLocation)

    logger = logging.getLogger("matching_address")
    logger.setLevel(logging.INFO)

    # create a file handler
    handler = logging.FileHandler(logsLocation)
    handler.setLevel(logging.INFO)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)

    logger.info("***********************Matching Address STARTED*************************")
    main()
    print ("--------------------Matching Address COMPLETED--------------------")
    endProgram = time.time()
    print ("Time elapsed to compelete activity: ")
    print(str(endProgram - startProgram) + " secs")
    print ("------------------------------------------------------------------\n\n\n\n")
    logger.info("***********************Matching Address COMPLETED*************************")
    logger.info("Time elapsed to compelete activity: ")
    logger.info(str(endProgram - startProgram) + " secs")        
        
