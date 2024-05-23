# ssl-filler
A tool to take an Excel file of Tacy Foundation volunteer logs and put the information in a signed pdf + event log and email the information to the respective volunteers

## Instructions for use
1. Clone this repository to wherever you want. To do this, go to your terminal, navigate to the desired directory, and run the 'git clone *webURL*', where *webURL* is the link obtained from the top-right **Code** dropdown under "HTTPS"
2. Populate the directories with the respective files that are needed:
   * blank SSL forms should be placed in **SSLForms**
   * Excel spreadsheet with data should be put into **SSLSheets**
3. Set up the email account that will be sending the emails to the volunteers. This instruction assumes you are using a GMail account
   * From your GMail, click on the top right profile and then select "Manage your Google Account"
   * A new tab will appear - click on Security -> enable 2-step Verification
   * Go to the top search bar and search for "App Passwords", clicking on the first result
   * Create a new app password and copy the 16-digit code that is shown.
   * Go back to the root directory of this project, create a file called ".env"
   * In the newly created file, add the line ```PASSWORD={code}```, where ```{code}``` represents the 16-digit code you copied earlier
   * save the file
4. Install Docker at https://docs.docker.com/engine/install/, following the instructions there 
5. Pull the Docker image: ```docker pull danmartmi/ssl-filler```
6. Run the Docker command to run the code: 
   * Mac: ```docker run --rm -it -v $(pwd):/mnt -w /mnt danmartmi/ssl-filler```
   * Windows: ```docker run --rm -it -v %cd%:/mnt -w /mnt danmartmi/ssl-filler```
   * Powershell: ```docker run --rm -it -v ${PWD}:/mnt -w /mnt danmartmi/ssl-filler```
7. Filled SSL forms will be outputted to **FilledSSL**, event logs will be outputted to **SSLEventLogs**, and processed Excel sheets will be outputted to **SSLSheets**
