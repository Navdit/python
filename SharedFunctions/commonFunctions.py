import os

##################################################################################################################
# Function Name: searchFile
# Description  : Traverses the directory and search the file 
# @param       : Directory, which you would like to traverse
# @param       : File, which you would like to search
# @return      : List of the File Location(s)
##################################################################################################################

def searchFile(Directory, FileNameOrExtenstion):
    #Initilise List
    fileLocationList = []

    extension = FileNameOrExtenstion.lower()

    for dirpath, dirnames, files in os.walk(Directory):
        for name in files:
            if extension and name.endswith(FileNameOrExtenstion):
                # print(os.path.join(dirpath, name))
                fileLocationList.append(os.path.join(dirpath, name))
                return fileLocationList

            elif not extension:
                # print(os.path.join(dirpath, name))
                fileLocationList.append(os.path.join(dirpath, name))
                return fileLocationList
            
##################################################################################################################



##################################################################################################################
# Function Name: stripList
# Description  : Take a list of string objects and return the same list stripped of extra whitespace.
# @param       : List which needs to be stripped of the extra white spaces
# @return      : The same list, which was given as input but stripped of whitespaces
##################################################################################################################
def stripList(listInput):
    return([x.strip() for x in listInput])

##################################################################################################################


##################################################################################################################
# Function Name: dropEvenOrOddElmentsOfList
# Description  : Deletes the nth element of the list
# @param       : List
# @param       : Argument as Even or Odd. Zero is considered even
# @return      : The same list, with dropped indexes
##################################################################################################################
def dropEvenOrOddElmentsOfList(list, EvenOrOdd):
    finalList = []
    if(EvenOrOdd == "Even"):
        finalList = [item for index, item in enumerate(list) if index % 2 == 0]
    elif (EvenOrOdd == "Odd"):
        finalList = [item for index, item in enumerate(list) if index % 2 != 0]
    else:
        raise Exception("Custom Error: Argument can only be Even or Odd")

    return finalList

##################################################################################################################



##################################################################################################################
# Function Name: checkFolder
# Description  : Checks if the given folder exists, if not then creates a new one
# @param       : Folder Location along with Folder Name.
##################################################################################################################
def checkFolder (folderLoc):
    if not os.path.exists(folderLoc):
        os.makedirs(folderLoc)
        
##################################################################################################################



##################################################################################################################
# Function Name: createCurrDateFolderName
# Description  : Creates a Folder Name of Current Date in format YYYYMMDD
# @return      : String of CurrentDate Folder Name
##################################################################################################################
def createCurrDateFolderName():
    now = datetime.datetime.now()
    year = str(now.year)
    month = now.strftime('%m')
    day = now.strftime('%d')
    strCurrFolder = year+month+day
    return strCurrFolder
        
##################################################################################################################
