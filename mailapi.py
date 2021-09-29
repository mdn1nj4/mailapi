#!/usr/bin/python3
import re
import sys
import requests
from bs4 import BeautifulSoup

def mailcheck(addressToVerify):

	api_url = ""
	
	
	if "" == api_url:
		print("\n\t [-] API url not Found")
		sys.exit(1)

	regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'
	# Syntax check
	match = re.match(regex, addressToVerify)
	if match == None:
		print('Bad Syntax')
		raise ValueError('Bad Syntax')
	api_url = api_url.split("&")
	url = api_url[0]
	try:
		req = requests.get(f"{url}&emailAddress={addressToVerify}",stream=True,timeout=15)
		json = req.json()
		#print(json['ErrorMessage'])
		try:
			if json["smtpCheck"] == "true":
				print(addressToVerify, flush=True)
		except:
			if json["ErrorMessage"]:
				error = str(json["ErrorMessage"])
				if error == "{'Error': 'The email address must be a valid email address.'}":
					pass
				if error == "{'Error': 'You ran out of credits.'}":
					print(f"	\n Last Checked Email : { addressToVerify }\n")
					print(f"	\n[+] API Expired Create a New Account in : https://emailverification.whoisxmlapi.com\n",flush=True)
					raise KeyboardInterrupt

	except (KeyboardInterrupt):
		sys.exit(0)
	except:
		pass

def mobile(addressToVerify):
	try:
		html = requests.get(f"https://domainbigdata.com/email/{ email }").content
		soup=BeautifulSoup(html,"html.parser")
		rgx = str(soup)
		phones = re.findall('<td colspan="2">\+.*.</td>', rgx)
		for phone in phones:
			number = phone.replace("<td colspan="+'"'+'2'+'"'+'>', "").replace("</td>","")
			print(number)
		if len(phones) == 0:
			pass
			print(f"No phone numbers found!\n")
	except:
		print(f"Phone Number Data Error!")



try:

	if sys.argv[1] == "-h":
		print(f"Usage : {sys.argv[0]} adhil.mohamed@gmail.com")
		print(f"	{sys.argv[0]} -f mail.txt")

	if sys.argv[1] == "-f":
		try:
			filepath=sys.argv[2]
			file = open(str(filepath), 'r')
			Lines = file.readlines()
			file.close()
			for email in Lines:
				email = email.rstrip()
				mailcheck(str(email))
				sys.stdout.flush()
		except KeyboardInterrupt:
			sys.exit(0)
			
	else:
		inputAddress = sys.argv[1]
		addressToVerify = str(inputAddress)
		mailcheck(addressToVerify)
		mobile(addressToVerify)
except IndexError:
	print(f"Usage : {sys.argv[0]} adhil.mohamed@gmail.com")
	print(f"	{sys.argv[0]} -f mail.txt")
	#print(f"	{sys.argv[0]} ")
	print(f"	{sys.argv[0]} -h - For Help")

