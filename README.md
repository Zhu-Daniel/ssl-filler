# ssl-filler
A tool to take an Excel file of Tacy Foundation volunteer logs and put the information in a signed pdf + event log

## Instructions for use
1. Clone this repository to wherever you want. To do this, go to your terminal, navigate to the desired directory, and run the 'git clone *webURL*', where *webURL* is the link obtained from the top-right **Code** dropdown under "HTTPS"
2. In the root directory of the repo, create a .env file with the following fields:
    * FILE_PATH: path for the Excel sheet with the volunteer logs (input)
    * FILE: name of the Excel sheet itself (input)
      * This will be the one field you update each time the code is ran
    * SHEET: name of the sheet within the Excel file that the volunteer logs are stored on (input)
    * MONTGOMERY_SSL: path to the empty Montgomery County SSL pdf that will be filled for the volunteers (input)
    * SSL_PATH: path to where the outputted filled SSL forms will be stored by the program (output)
    * LOGS_PATH: path to where the outputted event logs for each volunteer will be stored by the program (output)

Example contents:
```
FILE_PATH="/path/to/folder/TacyFoundationSSL/SSLSheets/"
FILE="Tacy_Foundation_SSL_Hours_041324.xlsx"
SHEET="Form Responses 1"
MONTGOMERY_SSL="/path/to/folder/TacyFoundationSSL/SSLForms/montgomerySSLsigned.pdf"
SSL_PATH="/path/to/folder/TacyFoundationSSL/FilledSSL/"
LOGS_PATH="/path/to/folder/TacyFoundationSSL/SSLEventLogs/"
```
To get the path of a directory, navigate to the desired directory in your terminal and use the command 'pwd'. Be sure to add the appending '/'

3. Populate the directories with the respective files that are needed
   * blank SSL forms for MONTGOMERY_SSL
   * Excel spreadsheet for FILE_PATH, FILE, and SHEET
4. Go to root of this project and run "python sslPDF.py"