### Name: Jazzbear
### Version: 202605291011

### import librarys 
import hashlib
import json
import datetime

### Function to produce hash as required
def produce_hash(string_to_hash):
    hashed_object = hashlib.sha256(string_to_hash.encode('utf-8')) ## defining the type of hash to create
    return hashed_object.hexdigest()
print("Welcome to The Checker of Bad Passwords!!\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~") ##welcome messege

###define variables
logSwitch = False ##so an empty log file isn't created
user_wants_to_continue = True ##loop variable
bruteDict = {}
resultList = [] ##saved data
print("Loading...") ##messege to let the user know it's running
try: ##try to open the "bad" passwords list
    passList = open("rockyou.txt","r", encoding="latin-1") ##open the list file
    pWL = passList.read() ##save the list temp
    passList.close()  ## close the file
    

except: ##if can't find the list tell the user then exit
    print("rockyou.txt can not be found! unable to continue!")
    exit

### go through list of passwords and save them with their hash values
for password in pWL.splitlines(): ##go through line by line
    rockHash = produce_hash(password) ##hashing the line
    bruteDict[rockHash] = password ##saving info
print("Complete!\n") ## tell user the previous is done



### Main loop
while user_wants_to_continue:
    ## prompt for filepath from user
    userInput = input('Enter the file path of your passwords file(JSON) or type "e" to Exit:')
    
    if userInput.upper() == "E" or userInput.upper() == "EXIT": ## check if user wants to exit
        print("Exiting...") ## print messege to user
        user_wants_to_continue = False ##exit loop
    else: ##user doesn't want to exit
        print("Searching for File...\n") ##tell user the script is looking for their file path
        try:
            infoFile = open(userInput,"r") ##try open the file
            userJs = infoFile.read() ##save the files contents
            infoFile.close() ##close the file
            print("File Loaded!") ##messege so the user knows the file was correctly read
            logSwitch = True
        except:
            print("File Path could not be found! Please try again.") ## tell user the file path can't be found
            continue
        userInfo = (json.loads(userJs)) ##convert the json format to list of dicts to be easier to work with
        ### check if the users password has a match with "bad" password list
        for user in userInfo:
            if user["user_password"] in bruteDict: ##if the password is in the list
                resultList.append({"username":user["user_name"], "password":bruteDict[user["user_password"]],"password_found": True})
            else: ##if the password isn't in the list
                resultList.append({"username":user["user_name"], "password":"","password_found": False})
###make sure a log file isn't created if no passwords were checked
if logSwitch == True:
    ###get local system date and time for log file naming
    stringDate = str(datetime.datetime.now()) ##get date and time as string
    removeMilSec = stringDate[:-7] ##remove milliseconds from the string
    timeStamp = removeMilSec.replace(":", "-") ##remove invalid charecters for file naming
    ### save data to a log file in JSON format
    logFile = open(f'log{timeStamp}.json','w') ## create the file with the date and time in the name
    json.dump(resultList,logFile,indent=2) ## put the gatherd info in the JSON file
    logFile.close()## close the file
    print("Log file saved! \n")
    

### print final messege to user before exiting
print("Goodbye")
        
        
    
