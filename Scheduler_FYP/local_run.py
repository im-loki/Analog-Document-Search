from crnn import t01
from Dictionary_FYP import dict_using_spellchecker
from Keyphrase_FYP import test
import os
import pyrebase

document = {
'author': 'Local', 'document_json': '', 'document_name': 'Demo', 
'document_path': 'NA', 'keypharses': '', 'service': 5, 'year': '2020'}

def main():
	# User Input
	os.system('clear')
	print("######################################################################################################################################################")
	print("FYP-Local Digitizer Module")
	print(">>")
	file = input("Enter the path relative to this file (./path_to_file) :: ")
	filename = file.split('/')[-1]

	# Call Modules
	print("-- --Debug Information Starting")
	document['document_json'] = str(t01.segment_process(file)).strip()

	c_s = dict_using_spellchecker.spell_check_me(document['document_json'])

	f_s = test.new(c_s)

	document['keypharses'] = str(f_s)

	print("-- --Debug Information Ending\n\n")

	# User Output
	print("> Module Ouput")
	print("OCR Detected Text: ")
	print(document['document_json'] + '\n')
	print("Spell Corrcted Text: ")
	print(c_s + '\n')
	print("Document Keyphrase: ")
	print(document['keypharses'])
	print(">")
	if (str(input("Document Dump? (Y|N):: ")).upper() == 'Y'):
		print("Document Object::")
		print(document)

	# try to upload to firebase
	print(">>")
	if (str(input("Document Upload to firebase? (Y|N):: ")).upper() == 'Y'):
		config = {
		  "apiKey": " AIzaSyB5OEATcLYrle-7-Q3JX2Sai7jp5ja0T5o ",
		  "authDomain": "fyp01-8d888.firebaseapp.com",
		  "databaseURL": "https://fyp01-8d888.firebaseio.com/",
		  "storageBucket": "fyp01-8d888.appspot.com",
		  "serviceAccount": "./fyp_key.json"
		}

		firebase = pyrebase.initialize_app(config)
		print("> Firebase Configuration Initialized")
		print(firebase)

		# Storage
		storage = firebase.storage()
		storage.child("images/local.png").put(filename)
		url_not_string = storage.child("images/local.png").get_url(None)
		document['document_path'] = str(url_not_string)
		print("> Image Uploaded")
		print(str(url_not_string))

		# DB
		db = firebase.database()
		key = db.child("Requests/Active").push(document)
		print("> Committed to Database")
		print(str(key))

		print()
main()