import requests
import pdfkit
import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from lxml import html
import os

pageNames = ['Representational_state_transfer','List_of_HTTP_status_codes','Hash_function','Cryptographic_hash_function','Key_derivation_function','Collision_(computer_science)','Encryption','Public-key_encryption','Cross-origin_resource_sharing','HTTP_cookie','Content_delivery_network','Cache_(computing)','JSON_Web_Token']

sender_email = input("Type your sender email address and press enter:")
receiver_email = input("Type your receiver email address (like xyz@kindle.com) and press enter:")
password = input("Type your password and press enter:")

for pageName in pageNames:

	subject = pageName
	body = "This is an email with attachment sent from Python: " + pageName

	path = 'div#content'
	r = requests.get('https://en.wikipedia.org/wiki/' + pageName)
	soup = BeautifulSoup(r.text, 'lxml')
	content = soup.select_one(path).encode("utf-8")

	f = open(pageName+".html", "w")
	f.write(str(content)[2:-1].replace('url(\"//','url(\"https://').replace('src=\"/w','src=\"https://en.wikipedia.org/w').replace('srcset=\"//','srcset=\"https://').replace("src=\"//", "src=\"https://").replace("href=\"/wiki","href=\"https://en.wikipedia.org/wiki").replace("\\n",""))
	f.close()

	options = {'page-size': 'A5', 'zoom': '1.5'}

	pdfkit.from_file(pageName + '.html', pageName + '.pdf', options)
	os.remove(pageName + ".html");


	# Create a multipart message and set headers
	message = MIMEMultipart()
	message["From"] = sender_email
	message["To"] = receiver_email
	message["Subject"] = subject

	# Add body to email
	message.attach(MIMEText(body, "plain"))

	filename = pageName+".pdf"  # In same directory as script

	# Open PDF file in binary mode
	with open(filename, "rb") as attachment:
		# Add file as application/octet-stream
		# Email client can usually download this automatically as attachment
		part = MIMEBase("application", "octet-stream")
		part.set_payload(attachment.read())

	# Encode file in ASCII characters to send by email    
	encoders.encode_base64(part)

	# Add header as key/value pair to attachment part
	part.add_header(
		"Content-Disposition",
		f"attachment; filename= {filename}",
	)

	# Add attachment to message and convert message to string
	message.attach(part)
	text = message.as_string()

	# Log in to server using secure context and send email
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
		server.login(sender_email, password)
		server.sendmail(sender_email, receiver_email, text)

	os.remove(pageName + ".pdf")