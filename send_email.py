#!/usr/bin/python
 
# Import smtplib for the actual sending function
import smtplib
 
# For guessing MIME type
import mimetypes
 
# Import the email modules we'll need
import email
import email.mime.application
 
#Import sys to deal with command line arguments
import sys

import os
import time

import shutil
import datetime

from time import gmtime, strftime

now = strftime("%Y-%m-%d_%H.%M.%S", gmtime())
new_folder = "/home/pi/webcam/archiv"
dest = new_folder + '/' + str(now) + '.jpg'

shutil.copy('/home/pi/webcam/cam-email-old.jpg', dest)

dest = new_folder + '/' + str(now) + '-diff.jpg'

shutil.copy('/home/pi/webcam/cam-email-diff.jpg', dest)

time.sleep(1)

os.system("mv /home/pi/webcam/cam-email-new.jpg /home/pi/webcam/cam-email-old.jpg")

time.sleep(1)

os.system("fswebcam -r 1280x720 /home/pi/webcam/cam-email-new.jpg")

time.sleep(1)

cmd = "convert /home/pi/webcam/cam-email-new.jpg /home/pi/webcam/cam-email-old.jpg -compose difference -composite -evaluate Pow 2 -evaluate divide 3 -separate -evaluate-sequence Add -evaluate Pow 0.5 /home/pi/webcam/cam-email-diff.jpg"
os.system(cmd)

time.sleep(1)

os.system("convert /home/pi/webcam/*.jpg /home/pi/webcam/compare-webcam-result.pdf")

time.sleep(1)
 
# Create a text/plain message
msg = email.mime.Multipart.MIMEMultipart()
msg['Subject'] = 'raspberry webcam snapshot'
msg['From'] = 'your-email@gmail.com'
msg['To'] = 'example@gmail.com'
 
# The main body is just another attachment
body = email.mime.Text.MIMEText("""Hi, hier ein neues Bild von meiner webcam!""")
msg.attach(body)
 
# PDF attachment block code
 
directory='/home/pi/webcam/compare-webcam-result.pdf'
 
# Split de directory into fields separated by / to substract filename
 
spl_dir=directory.split('/')
 
# We attach the name of the file to filename by taking the last
# position of the fragmented string, which is, indeed, the name
# of the file we've selected
 
filename=spl_dir[len(spl_dir)-1]
 
# We'll do the same but this time to extract the file format (pdf, epub, docx...)
 
spl_type=directory.split('.')
 
type=spl_type[len(spl_type)-1]
 
fp=open(directory,'rb')
att = email.mime.application.MIMEApplication(fp.read(),_subtype=type)
fp.close()
att.add_header('Content-Disposition','attachment',filename=filename)
msg.attach(att)
 
# send via Gmail server
# NOTE: my ISP, Centurylink, seems to be automatically rewriting
# port 25 packets to be port 587 and it is trashing port 587 packets.
# So, I use the default port 25, but I authenticate.
s = smtplib.SMTP('smtp.gmail.com:587')
s.starttls()
s.login('example@gmail.com','PASSWORD')
s.sendmail('test@gmail.com',['example@gmail.com'], msg.as_string())
s.quit()
