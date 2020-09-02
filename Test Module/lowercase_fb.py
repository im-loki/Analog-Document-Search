import pyrebase
import re

my_stream = None

config = {
	  "apiKey": " AIzaSyB5OEATcLYrle-7-Q3JX2Sai7jp5ja0T5o ",
	  "authDomain": "fyp01-8d888.firebaseapp.com",
	  "databaseURL": "https://fyp01-8d888.firebaseio.com/",
	  "storageBucket": "fyp01-8d888.appspot.com",
	  "serviceAccount": "./fyp_key.json"
	}

firebase = pyrebase.initialize_app(config) #you should add the config as documentation

db = firebase.database()
print(db)
com_path = "Requests/Active"

iter = 0

def some_rnd_func(path, data, key = ''):
	global iter
	iter += 1
	print("----------------------------------------------------------Starting Some rnd func - " + str(iter))
	print("#################### Data Received ####################")
	print("Path: ", path)
	print("key: ", key)
	print("data received: ", data)
	# Download The File
	if( iter != 0):
		text = data['document_json']
		doc_string = text.lower()
		doc_string = [s.strip() for s in re.split("[();\/:\.+=\-?,]", doc_string)]
		doc_string = " ".join(doc_string)

		key_text = data['keypharses']
		key_text = key_text.lower()
		key_text = re.sub('[();\/:\.+=\-?,]', " ", key_text)
		print(doc_string, key_text)
		data['document_json'] = doc_string
		data['keypharses'] = key_text
	#commit the returned data using the path + key explicitly. Do not change service variable.

	print("----------------------------------------------------------Completed: some rnd func ")
	return data

def stream_handler(post):
	# print(post)
	print("hit")

	#Initial Iterator through the whole Matching JSON. Pending Operations are done first.
	if(post['path']=='/'):
		data = post['data']
		keys = list(data.keys())
		# print(keys)
		for key in keys:
			# print(key)
			# print(data[key])
			if(data[key]['service'] == 5):#check only service
				print("Initial Pendings")
				data[key] = some_rnd_func(post['path'], data[key], key)
				if data[key] != None:
					data[key]['service'] = 5
					db.child(com_path).child(key).update(data[key])


my_stream = db.child(com_path).stream(stream_handler)