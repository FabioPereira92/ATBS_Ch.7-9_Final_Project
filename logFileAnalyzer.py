#! python3

"""logFileAnalyzer - A program that scans a folder selected by the user for .txt and .log
files. It finds dates, emails, warning and error messages, creates a summary file for each
scanned file and places all summary files in a processed files .zip. It also allows the user
to copy or move the processed .zip files to an archived files .zip and prints a final
summary of finds across all files in the console. It also creates a .txt file with a final
summary added each time the program is run"""

import re, os, shutil, shelve, zipfile

# Counting the run with a shelfFile
shelfFile = shelve.open('run_counter')
if shelfFile == {}:
    shelfFile['runCounter'] = 1
else:
    shelfFile['runCounter'] += 1

# Starting the finds counters
fileCounter = 0
fileCounter2 = 0
emailCounter = 0
dateCounter = 0
warningCounter = 0
errorCounter = 0

# Email regex
emailRegex = re.compile(r"""
                        [a-zA-Z0-9._%+-]+    # before @ part
                        @                    # @ character
                        [a-zA-Z0-9.-]+       # domain
                        \.[a-zA-Z]{2,4}      # top level domain
                        """, re.VERBOSE)

# Date regex
while True:
    print('Insert date format (yyyy-mm-dd/dd-mm-yyyy):')
    dateInput = input()
    if dateInput == 'yyyy-mm-dd':
        date = r'\d{4}-\d{2}-\d{2}'
        break
    elif dateInput == 'dd-mm-yyyy':
        date = r'\d{2}-\d{2}-\d{4}'
        break
    else:
        print('Invalid input!')
dateRegex = re.compile(date + r'(\s\d{2}:\d{2}:\d{2})?')     

# Error regex
errorRegex = re.compile(r'^.+ERROR.+$')

# Warning regex
warningRegex = re.compile(r'^.+WARNING.+$')

# Asking the user for a folder path
print('Insert a folder path:')
folderPath = os.path.abspath(input())

# Creating a processed_logs folder:
os.chdir(folderPath)
os.makedirs(os.path.join('..', 'processed_logs_' + str(shelfFile['runCounter'])))
os.chdir(os.path.join('..', 'processed_logs_' + str(shelfFile['runCounter'])))

files = []

# Walking through all .txt and .log files in folder path
for foldername, subfolders, filenames in os.walk(folderPath):
    for file in filenames:       

        # Opening .txt and .log files
        if file[-4:] == '.txt' or file[-4:] == '.log':
            fileCounter += 1
            fileObj = open(foldername + '\\' + file)
            content = fileObj.readlines()
            fileObj.close()

            # Finding matches in the files
            emailList = []
            dateList = []
            errorList = []
            warningList = []
            for i in range(len(content)):
                moEmail = emailRegex.search(content[i])
                if moEmail != None:
                    emailCounter += 1
                    emailList.append(moEmail.group())
                moDate = dateRegex.search(content[i])
                if moDate != None:
                    dateCounter += 1
                    dateList.append(moDate.group())             
                moError = errorRegex.search(content[i])
                if moError != None:
                    errorCounter += 1
                    errorList.append(moError.group())
                moWarning = warningRegex.search(content[i])    
                if moWarning != None:
                    warningCounter += 1
                    warningList.append(moWarning.group())

            # Creating and writing the summary files
            for i in range(len(files)):
                if files[i] == file:
                    fileCounter2 += 1
            if fileCounter2 == 0:
                fileObj = open('summary_' + file, 'w')
                fileObj.write('SUMMARY REPORT FOR: ' + file + '\n\n')
                fileObj.write('\nFILE PATH\n\n')
                fileObj.write(os.path.join(foldername, file) + '\n\n')
            else:
                file2 = file[:-4] + '(' + str(fileCounter2)  + ')' + file[-4:]
                fileObj = open('summary_' + file2, 'w')
                fileObj.write('SUMMARY REPORT FOR: ' + file2 + '\n\n')
                fileObj.write('\nFILE PATH\n\n')
                fileObj.write(os.path.join(foldername, file2) + '\n\n')
            fileObj.write('\nTOTAL LINES SCANNED\n\n')
            fileObj.write(str(len(content)) + '\n')
            if dateList != []:
                fileObj.write('\n\nDATES FOUND\n\n')
                for i in dateList:
                    fileObj.write(i + '\n')
            if emailList != []:
                fileObj.write('\n\nEMAILS FOUND\n\n')
                for j in emailList:
                    fileObj.write(j + '\n')
            if warningList != []:
                fileObj.write('\n\nWARNINGS\n\n')
                for k in warningList:
                    fileObj.write(k + '\n')
            if errorList != []:
                fileObj.write('\n\nERRORS\n\n')
                for l in errorList:
                    fileObj.write(l + '\n')
            fileObj.write('\n\nSUMMARY COUNTS\n\n')
            fileObj.write('Dates found: ' + str(len(dateList)) + '\n')
            fileObj.write('Emails found: ' + str(len(emailList)) + '\n')
            fileObj.write('Warnings found: ' + str(len(warningList)) + '\n')
            fileObj.write('Errors found: ' + str(len(errorList)) + '\n\n')
            fileObj.write('\nProcessed by: logFileAnalyzer.py')
            fileObj.close()
            files.append(file)
            fileCounter2 = 0

os.chdir('..')

# Optionally moving or copying the processed files into archived_Logs
while True:
    print('Move or copy processed files into archived_logs(move/copy/no): ')
    choice = input().lower().strip()
    
    if choice == 'move':
        print('Insert a folder path:')
        folderPath2 = os.path.abspath(input())
        shutil.move(os.path.join('.', 'processed_logs_' +
                                    str(shelfFile['runCounter'])), os.path.join(
                    folderPath2, 'archived_logs_' + str(shelfFile['runCounter'])))
        
        # Creating an archived files zip
        zipFileObj = zipfile.ZipFile(os.path.join(folderPath2, 'archived_logs_' +
                                     str(shelfFile['runCounter']) + '.zip'), 'a')
        for i in os.listdir(os.path.join(folderPath2, 'archived_logs_' +
                                         str(shelfFile['runCounter']))):
            zipFileObj.write('archived_logs_' +
                             str(shelfFile['runCounter']) + '\\' + i,
                             compress_type=zipfile.ZIP_DEFLATED)
        zipFileObj.close()
        
        # Deleting archived_logs
        shutil.rmtree(os.path.join(folderPath2, 'archived_logs_' +
                                   str(shelfFile['runCounter'])))       
        break
    
    elif choice == 'copy':
        print('Insert a folder path:')
        folderPath2 = os.path.abspath(input())
        shutil.copytree(os.path.join('.', 'processed_logs_' +
                                        str(shelfFile['runCounter'])), os.path.join(
                        folderPath2, 'archived_logs_' + str(shelfFile['runCounter'])))
        # Creating an archived files zip
        zipFileObj = zipfile.ZipFile(os.path.join(folderPath2, 'archived_logs_' +
                                     str(shelfFile['runCounter']) + '.zip'), 'a')
        for i in os.listdir(os.path.join(folderPath2, 'archived_logs_' +
                                         str(shelfFile['runCounter']))):
            zipFileObj.write(os.path.join('archived_logs_' +
                             str(shelfFile['runCounter']), i),
                             compress_type=zipfile.ZIP_DEFLATED)
        zipFileObj.close()
        
        # Deleting archived_logs
        shutil.rmtree(os.path.join(folderPath2, 'archived_logs_' +
                                   str(shelfFile['runCounter'])))       
        break
    
    elif choice == 'no':
        break
    else:
        print('Invalid input!')

# Creating a processed files zip
if os.path.exists('processed_logs_' + str(shelfFile['runCounter'])):
    zipFileObj = zipfile.ZipFile('processed_logs_' + str(shelfFile['runCounter']) +
                                 '.zip', 'a')
    for i in os.listdir(os.path.join('.', 'processed_logs_' +
                                        str(shelfFile['runCounter']))):
        zipFileObj.write(os.path.join('processed_logs_' +
                         str(shelfFile['runCounter']), i),
                         compress_type=zipfile.ZIP_DEFLATED)
    zipFileObj.close()
    
    # Deleting processed_logs
    shutil.rmtree('processed_logs_' + str(shelfFile['runCounter']))

# Printing a final summary in the console
fileObj = open('master_summary.txt', 'a')
fileObj.write('SUMMARY - RUN ' + str(shelfFile['runCounter']) + '\n') 
print('\nTotal files processed: ' + str(fileCounter))
fileObj.write('Total files processed: ' + str(fileCounter))
print('\nTotal dates found: ' + str(dateCounter))
fileObj.write('\nTotal dates found: ' + str(dateCounter))
print('\nTotal emails found: ' + str(emailCounter))
fileObj.write('\nTotal emails found: ' + str(emailCounter))
print('\nTotal warnings found: ' + str(warningCounter))
fileObj.write('\nTotal warnings found: ' + str(warningCounter))
print('\nTotal errors found: ' + str(errorCounter))
fileObj.write('\nTotal errors found: ' + str(errorCounter) + '\n\n\n')
fileObj.close()
shelfFile.close()
