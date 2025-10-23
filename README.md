# Log File Analyzer
A program that scans a folder selected by the user for .txt and .log files. It finds dates, emails, warning and error messages, creates a summary file for each scanned file and places all summary files in a processed files .zip. It also allows the user to copy or move the processed .zip files to an archived files .zip and prints a final summary of finds across all files in the console. It also creates a .txt file with a final summary added each time the program is run

## Features
- Scanning .txt and .log files for dates, emails, warning and error messages in a folder selected by the user.
- Creating a summary file with information about what it found for each scanned file.
- Creating a processed files .zip to place all summary files
- Allowing the user to choose to copy or move the processed files .zip to an archived files .zip
- Printing a final summary of finds across all files in the console
- Adding the final summary to a master summary file each time the program is run
  
## How to run
1. Clone this repository or download the file `logFileAnalyzer.py`.
2. Run in terminal.

## Example Usage
### Folder structure pre run example
![logFileAnalyzer folder structure pre run example](https://github.com/user-attachments/assets/464817ed-cd66-4e7d-ab1c-c8b16543259b)
### Example logs folder content example
![logFileAnalyzer example logs folder content example](https://github.com/user-attachments/assets/74386de1-7b99-4dee-9ea5-d0f0ecb9837c)
### app_log_01 content example
![logFileAnalyzer app_log_01 content example](https://github.com/user-attachments/assets/807cf868-9f8f-41c6-a7a1-c7c9610c53fd)
### Console example
![logFileAnalyzer console example](https://github.com/user-attachments/assets/2dd68501-bc58-4cda-ba17-2af3766b243c)
### Folder structure post run example
![logFileAnalyzer folder structure post run example](https://github.com/user-attachments/assets/b62e99d7-feba-4d5f-98d4-66c23201a9c0)
### Master summary content example
![logFileAnalyzer master summary content example](https://github.com/user-attachments/assets/694c236b-0de0-4067-823c-648e6cac207d)
### Processed logs folder content example
![logFileAnalyzer processed logs folder content example](https://github.com/user-attachments/assets/fd541cf9-d7b1-4970-8ff6-244d1d8e2539)
### Summary_app_log_01 content example
![logFileAnalyzer summary_app_log_01 content example](https://github.com/user-attachments/assets/c64eda1a-03c7-4105-9607-f0454bd12073)

## Tech Stack
- Python 3.13
- Standard library only (re, os, shutil, shelve, zipfile)

## License
MIT
