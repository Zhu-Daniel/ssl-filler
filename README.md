# ssl-filler
A tool to take an Excel file of Tacy Foundation volunteer logs and put the information in a signed pdf + event log

## Instructions for use
1. Clone this repository to wherever you want. To do this, go to your terminal, navigate to the desired directory, and run the 'git clone *webURL*', where *webURL* is the link obtained from the top-right **Code** dropdown under "HTTPS"
2. Populate the directories with the respective files that are needed:
  * blank SSL forms should be placed in **SSLForms**
  * Excel spreadsheet with data should be put into **SSLSheets**
3. Install Docker at [https://docs.docker.com/engine/install/], following the instructions there 
4. Pull the Docker image: ```docker push danmartmi/ssl-filler```
5. Run the Docker command to run the code: 
   * Mac: ```docker run --rm -it -v $(pwd):/mnt -w /mnt danmartmi/ssl-filler```
   * Windows: ```docker run --rm -it -v %cd%:/mnt -w /mnt danmartmi/ssl-filler```
   * Powershell: ```docker run --rm -it -v ${PWD}:/mnt -w /mnt danmartmi/ssl-filler```
6. Filled SSL forms will be outputted to **FilledSSL**, event logs will be outputted to **SSLEventLogs**, and processed Excel sheets will be outputted to **SSLSheets**
