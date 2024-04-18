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
FILE_PATH="SSLSheets"
FILE="Tacy_Foundation_SSL_Hours_041324.xlsx"
SHEET="Form Responses 1"
MONTGOMERY_SSL="SSLForms/montgomerySSLsigned.pdf"
SSL_PATH="FilledSSL"
LOGS_PATH="SSLEventLogs"
```
You can copy the contents to your own .env file, but if you use different folder names or folders in different locations, you will need to update this.
Otherwise, include the different names in the .gitignore to avoid pushing extra files into the repository.

3. Populate the directories with the respective files that are needed
  * blank SSL forms for MONTGOMERY_SSL
  * Excel spreadsheet for FILE_PATH, FILE, and SHEET
4. If you do not have python installed, install it from this link: [https://www.python.org/downloads/]
  * Click on the big yellow button near the top of the page
5. Go to root of this project and run the following commands to install dependencies and then run the program:
```
pip install -r requirements.txt
python sslPDF.py
```
