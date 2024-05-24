import fillpdf
from fillpdf import fillpdfs # for filling pdfs

import numpy as np
import pandas as pd # for data manipulation

from datetime import datetime
from dateutil.rrule import *
from dateutil.relativedelta import * # for determining relevant dates for the SSL forms (Montgomery)

import matplotlib.pyplot as plt 
from matplotlib.backends.backend_pdf import PdfPages # for creating the event logs pdf

import yaml # for loading the configurations related to the locations of the template pdfs

import os
from dotenv import load_dotenv  # for accessing environment variables

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
import email
from email.message import EmailMessage
from email.mime.application import MIMEApplication
from email.utils import make_msgid

# Security for email - TLS encryption
import ssl

# For emailing files
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# For copy pasting the SSL forms to save them
import shutil

# for testing out other pdf editors that can save the pdf generated
from pypdf import PdfReader
from pypdf import PdfWriter

load_dotenv() # load environment variables

with open('config.yaml', 'r') as file: # load configurations
    config_params = yaml.safe_load(file)

def _draw_as_table(df, pagesize, title):
    alternating_colors = [['white'] * len(df.columns), ['lightgray'] * len(df.columns)] * len(df)
    alternating_colors = alternating_colors[:len(df)]
    fig, ax = plt.subplots(figsize=pagesize)
    ax.axis('tight')
    ax.axis('off')
    ax.set_title(title)
    the_table = ax.table(cellText=df.values,
                        colLabels=df.columns,
                        colColours=['lightblue']*len(df.columns),
                        cellColours=alternating_colors,
                        loc='center')
    return fig
  

def dataframe_to_pdf(df, filename, title, numpages=(1, 1), pagesize=(11, 8.5)):
  with PdfPages(filename) as pdf:
    nh, nv = numpages
    rows_per_page = len(df) // nh
    cols_per_page = len(df.columns) // nv
    for i in range(0, nh):
        for j in range(0, nv):
            page = df.iloc[(i*rows_per_page):min((i+1)*rows_per_page, len(df)),
                           (j*cols_per_page):min((j+1)*cols_per_page, len(df.columns))]
            fig = _draw_as_table(page, pagesize, title)
            if nh > 1 or nv > 1:
                # Add a part/page number at bottom-center of page
                fig.text(0.5, 0.5/pagesize[0],
                         "Part-{}x{}: Page-{}".format(i+1, j+1, i*nv + j + 1),
                         ha='center', fontsize=8)
            pdf.savefig(fig, bbox_inches='tight')
            
            plt.close()

### SSL FORMS FOR DIFFERENT COUNTIES:

## Maryland:
# Montgomery:
# Required section is 14-39 + Supervisor Signature
moco_form = {
             # Section I
             # Student Name (Last, First, Middle)
             '2': '', 
             # Student ID
             '3': '', 
             # School
             #'ALL SCHOOLS EXCEPT ELEMENTARY 8/2023': '-- Choose One --', 
             # First Period Teacher
             '5': '', 
             # Grade
             '4': '',
             # E-mail 
             '6': '',
             # Parent/Guardian Name 
             '7': '', 
             # Phone: Home or Cell (1)
             '8': '', 
             # Phone: Home or Cell (2)
             '9': '', 
             # Phone: Home or Cell (3)
             '10': '', 
             # Other (1)
             '11': '', 
             # Other (2)
             '12': '', 
             # Other (3)
             '13': '', 
             # Section II
             # Organization
             '14': 'The Tacy Foundation', 
             # Federal Employer Identification # (1)
             '15': '2', 
             # Federal Employer Identification # (2)
             '16': '6', 
             # Federal Employer Identification # (3)
             '17': '3', 
             # Federal Employer Identification # (4)
             '18': '7', 
             # Federal Employer Identification # (5)
             '19': '1', 
             # Federal Employer Identification # (6)
             '20': '5', 
             # Federal Employer Identification # (7)
             '21': '6', 
             # Federal Employer Identification # (8)
             '22': '6', 
             # Federal Employer Identification # (9)
             '23': '3', 
             # Phone (1)
             '24': '301', 
             # Phone (2)
             '25': '916', 
             # Phone (3)
             '26': '1439', 
             # Address
             '27': 'P.O. Box 2334, Germantown, MD 20875', 
             # E-mail
             '28': 'thetacyfoundation@gmail.com', 
             # Described Activity (performed)
             '29': 'Engage with hospital patients, veterans, first responders, seniors through music/art, mentor youth & seniors', 
             # Date From
             '30': '',
             # Date To 
             '31': '',
             # # Days of Service 
             '32': '', 
             # # Hours Per Day (8 in a 24 hourperiod maximum)
             '33': 'various', 
             # Total # Hours Completed (award 1 SSL hour for every hour of service)
             '34': '', 
             # Supervisor Name (print)
             '35': 'Charlotte Holliday', 
             # Title
             '36': 'Founder and Executive Director', 
             # Date (1)
             '37': '', 
             # Date (2)
             '38': '', 
             # Date (3)
             '39': '', 
             # Section III: Student reflection
             '40': ''
            }
# Howard:
fillpdfs.print_form_fields(config_params['HOWARD_SSL'])
how_form = {'Name': '',
    'School': '',
    'Grade': '',
    'Activity': '',
    'Check Box187': '',
    'Check Box188': '',
    'Check Box189': '',
    'StartDate': '',
    'FinishDate': '',
    'SponsoringClassOrganization': ('The Tacy Foundation', '/Ff', 8),
    'AdultSiteProjectSupervisor': ('Charlotte Holliday', '/Ff', 8),
    'Phone': ('301-916-1439', '/Ff', 8),
    'Service Hours': '',
    'd plan serviceactivities': '',
    'Text181': '',
    'Advocacyprojectsrequire studentstolendtheirvoicesand talentsand isthe workofcitizenship': '',
    'Check Box184': '',
    'Check Box185': '',
    'Check Box186': '',
    'Text182': '',
    'manyforms from essaystosmallgroupdiscussions': '',
    'Text183': '',
    'StudentSignature': '',
    'Date': '',
    'AdultSiteProjectSupervisorSignature': '',
    'Date_2': '',
    'PrincipalDesigneeSignature': '',
    'Date_3': ''}
# Georgetown Day School:

# Carroll: No need to do extra, just send volunteer logs to students for them to enter via the online SSL form submitter: https://ext.carrollk12.org/SLHExt/Default.aspx

## Virginia:
# Fairfax: 
# Loudoun:
#exit()


# Load the Excel file that holds the SSL information
dataframe = pd.read_excel(config_params['FILE_PATH']+'/'+config_params['FILE'], sheet_name=config_params['SHEET'])
print(dataframe)
#dataframe['Timestamp'] = dataframe['Timestamp'].apply(datetime.strptime, '%m/%d/%y %H:%M:%S')
dataframe['Confirmed'] = dataframe['Confirmed'].astype(str)
dataframe.loc[dataframe.Confirmed == "nan", 'Confirmed'] = ""
dataframe['Hours'] = round(dataframe['Hours'], 2)
print(dataframe)
print(dataframe.dtypes)


# TODO: grabbing only the SSL hours within the recommended time frame, or grab all eligible hours?
# Important dates: Last Friday of September, First Friday of January, First Friday of April, Last Friday of May (first Friday of June?)

# Get important dates, as well as the data that corresponds to the important dates
# TODO: Figure out if dates have to follow MCPS deadline days or if there are some flexibility
today = datetime.today()
base_year = ''
if today < datetime(today.year, 6, 1):
    base_year = today.year-1
else:
    base_year = today.year
# June 1 - August 31
# get the starting month/day - June 1
summer = list(rrule(freq=YEARLY, dtstart=datetime(base_year, 6, 1), bymonth=6, bymonthday=1))[0]
print('Summer: ', summer)
# end month - August 31
summer_end = list(rrule(freq=YEARLY, dtstart=datetime(base_year, 6, 1), bymonth=8, bymonthday=31))[0]
print('End of Summer: ', summer_end)

# September 1 - December 31
new_year = list(rrule(freq=YEARLY, dtstart=datetime(base_year, 6, 1), bymonth=12, bymonthday=31))[0]
print('New Year: ',new_year)
# January 1 - First Friday of April (March 31?)
certificate = list(rrule(freq=YEARLY, dtstart=datetime(base_year, 6, 1), bymonth=3, bymonthday=31))[0]
print('Certificate deadline: ', certificate)
# First Friday of April (March 31) - May 31
school_year = list(rrule(freq=YEARLY, dtstart=datetime(base_year, 6, 1), bymonth=5, bymonthday=31))[0]
print('End of School Year: ', school_year)


v_emails = dataframe['Email'].unique()
# Column where the "Confirmed" column is - for tracking what has been signed or not
confirmed_col = 12

# TODO: How should we name differently when volunteers have the same name? Just use email for the output pdfs?

# Use emails as the partition key
for e in v_emails:
    print(f"Processing {e}")
    email_df = dataframe.loc[(dataframe['Email']==e) & (dataframe['SSL eligible?'] == True) & (dataframe['Confirmed']=="")]
    rows = email_df.index
    eligible = email_df.loc[:,'SSL eligible?'].to_numpy()
    # Checks to see if the student is ever eligible or becomes eligible
    # Commented section for case where individual student wants an SSL form, but you don't want to run the program for everyone
    if True in eligible:
        print(f"Creating SSL form for {e}")
        # TODO: only add up the hours which SSL is applicable and not confirmed
        total_ssl = round(email_df.loc[:, 'Hours'].sum(), 2)
        f_name = email_df.loc[:,'First Name'].to_numpy()[0]
        l_name = email_df.loc[:,'Last Name'].to_numpy()[0]
        print(f"Total SSL for {f_name} {l_name}: {total_ssl}")
        # Get number of days student volunteered
        nbr_days = np.unique(email_df.loc[:, 'Start Date'].to_numpy()).size
        # date_format = ["%m/%d/%y %H:%M:%S" for x in email_df.loc[:,'Start Date/Time'].size()]
        # TODO: what if student moves to a different county but still works with the Foundation? Just check last location?
        location = email_df.loc[:,'County'].iloc[-1]
        output_pdf = config_params['SSL_PATH']+'/'+f'{e}SSL.pdf'
        print("Location: ", location)
        if location == "Montgomery":
            input_pdf = config_params['MONTGOMERY_SSL']
            
            # Add in the students' name
            moco_form['2'] = f'{l_name}, {f_name}'

            # Calculate which time period this form will be - uses current date along with deadlines
            
            start_date=""
            end_date=""
            if today <= summer_end:
                start_date = summer.strftime("%m/%d/%Y")
                end_date = summer_end.strftime("%m/%d/%Y")
            elif today <= new_year:
                start_date = (summer_end+relativedelta(days=1)).strftime("%m/%d/%Y")
                end_date = new_year.strftime("%m/%d/%Y")
            elif today <= certificate:
                start_date = (new_year+relativedelta(days=1)).strftime("%m/%d/%Y")
                end_date = certificate.strftime("%m/%d/%Y")
            elif today <= school_year:
                start_date = (certificate+relativedelta(days=1)).strftime("%m/%d/%Y")
                end_date = school_year.strftime("%m/%d/%Y")
            else:
                print("Current date not before any listed date...")
            print(f'Start date: {start_date}')
            print(f'End_date: {end_date}')
            moco_form['30'] = start_date
            moco_form['31'] = end_date
            # Enter the number of days
            moco_form['32'] = nbr_days
            # Enter the number of hours earned
            moco_form['34'] = total_ssl
            # Enter today's date
            moco_form['37'] = today.month
            moco_form['38'] = today.day
            moco_form['39'] = today.year
            # fillpdfs.write_fillable_pdf(input_pdf,output_pdf,moco_form)

            # Generate the PDFs
            reader = PdfReader(input_pdf)
            writer = PdfWriter()

            page = reader.pages[0]
            fields = reader.get_fields()

            writer.append(reader)

            writer.update_page_form_field_values(
                writer.pages[0],
                moco_form,
                auto_regenerate=False,
            )

            with open(output_pdf, "wb") as output_stream:
                writer.write(output_stream)
            
            print(f"SSL PDF for {f_name} {l_name} from Montgomery created")
        elif location == "Howard":
            
            input_pdf = config_params['HOWARD_SSL']

            # Add in the students' name
            how_form['Name'] = tuple((f'{f_name} {l_name}', '/Ff', 8))

            # calculate start date based on the earliest date in the list
            vol_dates = [x.strftime("%m/%d/%Y") for x in email_df['Start Date']]

            start_date=min(vol_dates)
            end_date=today.strftime("%m/%d/%Y")
            how_form['StartDate'] = tuple((start_date, '/Ff', 8))
            how_form['FinishDate'] = tuple((end_date, '/Ff', 8))
            print(isinstance(how_form['FinishDate'], tuple))
            # Enter the number of hours earned
            how_form['Service Hours'] = tuple((total_ssl, '/Ff', 8))
            # Enter today's date
            how_form['Date_2'] = tuple((today.strftime("%m/%d/%Y"), '/Ff', 8))
            # fillpdfs.write_fillable_pdf(input_pdf,output_pdf,how_form)

            reader = PdfReader(input_pdf)
            writer = PdfWriter()

            page = reader.pages[0]
            fields = reader.get_fields()
            print(fields)

            writer.append(reader)

            writer.update_page_form_field_values(
                writer.pages[0],
                how_form,
                auto_regenerate=False,
            )

            with open(output_pdf, "wb") as output_stream:
                writer.write(output_stream)
            
            print(f"SSL PDF for {f_name} {l_name} from Howard created")
        else:
            print(f"Don't have SSL PDF creation set up for {location}")
        
        # Edits spreadsheet - marks all the rows used in the calculation with "signed"
        for r in rows:
            dataframe.at[r, "Confirmed"]="signed"
        
        # Create PDF with table of all the events attended by the individual
        export_df = email_df[['Location','Start Date','Sign In', 'Sign Out', 'Hours']]
        log_name = config_params['LOGS_PATH']+'/'+f'{e}EventLog.pdf'
        dataframe_to_pdf(export_df, log_name, f'Logs of Events attended by {f_name} {l_name} - {total_ssl} Hours of Service')
        
        # Define values to be used in email
        text = f"""
        Hi {f_name} {l_name},

        Here are your SSL hours. If you have any questions about them, please contact the Tacy Foundation.

        Best,

        SSL Manager
        """
        sender = "bernardhardy365@gmail.com"
        password = os.getenv('PASSWORD')
        receiver = e

        # Setting up the message
        msg = MIMEMultipart()

        msg['Subject'] = f'Tacy Foundation SSL Hours'
        msg['From'] = sender
        msg['To'] = receiver
        msg['Bcc'] = receiver
        msg['Message-ID'] = make_msgid()

        msg.attach(MIMEText(text, "plain"))

        ssl_form = output_pdf
        
        ssl_logs = log_name

        files = [ssl_form, ssl_logs]
        # Loop through files to include in the email
        for f in files:
            # Open PDF file in binary mode
            with open(f, "rb") as attachment:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            # Encode file in ASCII characters to send by email    
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {output_pdf}",
            )

            # Add attachment to message and convert message to string
            msg.attach(part)

        context = ssl.create_default_context()

        # Send the message via our own SMTP server.
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender, password)
            smtp.sendmail(sender, receiver, msg.as_string())
            smtp.quit()

        

print(dataframe)
# Create excel file to confirm which ones have been processed or not
dataframe.to_excel(config_params['FILE_PATH']+'/'+config_params['FILE'].split('.')[0]+'_PROCESSED.xlsx', sheet_name=config_params['SHEET'])
