import pyrebase
from PIL import Image, ImageDraw, ImageFont
import os
import csv
import ast
import re

#### ----- Variables ----- ####
my_stream = None

config = {
	  "apiKey": " AIzaSyB5OEATcLYrle-7-Q3JX2Sai7jp5ja0T5o ",
	  "authDomain": "fyp01-8d888.firebaseapp.com",
	  "databaseURL": "https://fyp01-8d888.firebaseio.com/",
	  "storageBucket": "fyp01-8d888.appspot.com",
	  "serviceAccount": "./fyp_key.json"
	}

firebase = pyrebase.initialize_app(config) #you should add the config as documentation

flag = 0
data_rec = None
data_text = None
data_keyphrase = None

# [('natural text',['keyphrase_00',...,'keypharse_09']), ('natural text',['keyphrase_00',...,'keypharse_09']), ...]
testcases = [("Waiting for the wave to crest [wavelength services]\nWavelength services have been hyped ad nauseam for years. But despite their\nquick turn-up time and impressive margins, such services have yet to\nlive up to the industry's expectations. The reasons for this lukewarm\nreception are many, not the least of which is the confusion that still\nsurrounds the technology, but most industry observers are still\nconvinced that wavelength services with ultimately flourish\n", ['wavelength services', 'fiber optic networks', 'Looking Glass Networks', 'PointEast Research', 'optical fibre networks', 'telecommunication'])]
class res:
	no_words = 0
	no_char = 0
	no_ocr_text_correct = 0
	no_key_correct = 0

	total_no_words = 0
	total_no_char = 0
	total_no_ocr_text_correct = 0
	total_no_key_correct = 0

class myTest:
	init_text = ""
	ocr_text = ""

	init_keyphrases = None
	final_keyphrases = None

	init_no_characters = 0
	init_no_words = 0

	pred_no_char = 0
	pred_no_words = 0

	init_no_keyphrases = 0
	pred_no_keyphrases = 0

	mis_no_char = 0
	mis_no_words = 0
	mis_no_keyphrases = 0

	
	def __init__(self, doc_text, doc_keyphrases):
		self.init_text = doc_text.lower()
		self.init_keyphrases = doc_keyphrases

		self.init_no_characters = len(doc_text) - doc_text.count(' ')
		self.init_no_words = len(doc_text.split(' '))
		self.init_no_keyphrases = len(doc_keyphrases)

	def dump_me(self):
		temp = [str(self.init_text), str(self.ocr_text), str(self.init_keyphrases), str(self.final_keyphrases),
			str(self.init_no_characters), str(self.init_no_words), str(self.init_no_keyphrases),
			str(self.pred_no_char), str(self.pred_no_words), str(self.pred_no_keyphrases),
			str(self.mis_no_char), str(self.mis_no_words), str(self.mis_no_keyphrases)]

		print(temp)
		# name of csv file 
		filename = "data.csv"
  
		# writing to csv file 
		with open(filename, 'a', newline=None) as csvfile:
			csvwriter = csv.writer(csvfile)
			csvwriter.writerow(temp)

#### ---------------------- ####

def text_on_img(filename='tb.png', text="Hello", size=12, color=(0,0,0), bg='red'):
	"Draw a text on an Image, saves it, show it"
	fnt = ImageFont.truetype('arial.ttf', size)
	text_height = text.count('\n') * 2 * size + 2
	text_width = 0
	# print(text)

	# create image
	image = Image.new(mode = "RGB", size = (int(size)*50,text_height), color = bg)
	draw = ImageDraw.Draw(image)
	# draw text
	draw.text((10,10), text, font=fnt, fill=(0,0,0))
	# save file
	image.save(filename)
	# show file
	os.system(filename)

def stream_handler(post):
	print(post)
	global flag
	if(post['event']=='patch' and post['path'] == '/' and post['data']['service'] == 5):
		print("Im done")
		global data_rec
		data_rec = post['data']
		flag = 1


		# Download the whole data
		# Compute and update the values

def compare_values(mytest, data):
	# Assign Values to object
	# print(data)
	mytest.ocr_text = data['document_json']
	mytest.final_keyphrases = ast.literal_eval(data['keypharses'])

	init_words = mytest.init_text.split(' ')
	final_words = mytest.ocr_text.split(' ')

	mytest.pred_no_char = len(mytest.ocr_text) - mytest.ocr_text.count(' ')

	mytest.pred_no_words = len(final_words)

	mytest.pred_no_keyphrases = len(mytest.final_keyphrases)
	# print(mytest.final_keyphrases, len(mytest.final_keyphrases))

	w_limit = 0
	if len(init_words) < len(final_words):
		w_limit = len(init_words)
	else:
		w_limit = len(final_words)

	# Character Compare
	
	for i in range(w_limit):
		limit = 0
		if len(init_words[i]) < len(final_words[i]):
			limit = len(init_words[i])
		else:
			limit = len(final_words[i])
		init_word = init_words[i].lower()
		final_word = final_words[i].lower()
		j = 0
		while(j<limit):
			if init_word[j] != final_word[j]:
				mytest.mis_no_char += 1
			j += 1


	# Word Compare
	for i in range(w_limit):
		if init_words[i].lower() != final_words[i].lower():
			mytest.mis_no_words += 1

	# Compare Keyphrases
	for key in mytest.init_keyphrases:
		if key.lower() not in mytest.final_keyphrases and key.lower() in mytest.init_text.lower():
			# Deep Search
			f = 0
			for i_word in key.lower().split(' '):
				for f_key in mytest.final_keyphrases:
					for f_word in f_key.lower().split(' '):
						if i_word == f_word:
							f = 1
			if f == 0:
				mytest.mis_no_keyphrases += 1

def my_init():
	global flag, data, data_text, data_keyphrase
	flag = 0
	data = None
	data_text = None
	data_keyphrase = None

def main_test():
	global firebase
	global my_stream
	global flag
	global data_rec
	global testcases

	storage = firebase.storage()
	db = firebase.database()

	f = open('complied_set.txt', 'r')
	testcases = ast.literal_eval(f.read())
	print(str(testcases))

	# name of csv file 
	# filename = "data.csv"
	# temp = ['Initial Text', 'Ocr Generated Text', 'Initial Keyphrases', 'Generated Keyphrases', 'Init_No_Char', 
	# 	'Init_No_Words', 'Init_No_Keyphrases','Pred_No_Char', 'Pred_No_Words', 'Pred_No_Keyphrases',
	# 	'mis_no_char', 'mis_no_words', 'mis_no_keyphrases']
	
	# # writing to csv file 
	# with open(filename, 'a', newline=None) as csvfile:
	# 	csvwriter = csv.writer(csvfile)
	# 	csvwriter.writerow(temp)

	i = 0

	for doc_text, keypharses in testcases:

		text_on_img(filename='tb.png',text=doc_text, size=14, bg='white')
		text = re.sub('\n+', " ", doc_text)

		mytest = myTest(text, keypharses)

		# as admin
		storage.child("images/test_" + str(i) + ".png").put("tb.png")

		# storage.child("images/test0.jpg").download("downloaded.jpg")
		# # Fetch URL
		url_not_string = storage.child("images/test_" + str(i) + ".png").get_url(None)

		# print(url_not_string)
		# To db -> Insert
		

		data = {
		        "author" : "Lokeshwar",
		        "document_json" : "",
		        "document_name" : "Test Case: " + str(i),
		        "document_path" : str(url_not_string),
		        "keypharses" : "",
		        "service" : 1,
		        "year" : "2020"
		      }

		key = db.child("Requests/Active").push(data)

		# db wait -> logic
		com_path = "Requests/Active/" + str(key['name'])
		my_stream = db.child(com_path).stream(stream_handler, None)
		
		while True:
			if flag == 1:
				my_stream.close()
				print("######-" + str(i) + "-######")
				# print(com_path)
				# print(mytest.init_text)
				compare_values(mytest, data_rec)
				mytest.dump_me()
				print("#######################")
				del mytest
				flag = 0
				break

		i += 1

main_test()