import pyrebase
import re
from crnn import t01
from Dictionary_FYP import dict_using_spellchecker
from Keyphrase_FYP import test

# from crnn.eval import ocr_event_trigger

# from crnn.utils import pad_image, resize_image, create_result_subdir
# from crnn.STN.spatial_transformer import SpatialTransformer

import urllib.request
import random

# from crnn.models import CRNN, CRNN_STN


config = {
  "apiKey": " AIzaSyB5OEATcLYrle-7-Q3JX2Sai7jp5ja0T5o ",
  "authDomain": "fyp01-8d888.firebaseapp.com",
  "databaseURL": "https://fyp01-8d888.firebaseio.com/",
  "storageBucket": "fyp01-8d888.appspot.com",
  "serviceAccount": "./fyp_key.json"
}

firebase = pyrebase.initialize_app(config)
print(firebase)

db = firebase.database()
com_path = "Requests/Active"

iter_db_hits = 0
iter_proc_starts = 0
def some_rnd_func(path, data, key = ''):
	global iter_proc_starts
	iter_proc_starts += 1
	print("----------------------------------------------------------Starting Some rnd func: ", str(iter_proc_starts))
	print("#################### Data Received ####################")
	print("Path: ", path)
	print("key: ", key)
	print("data received: ", data)
	# Download The File


	url = data['document_path']
	print("URL: ", url)

	name = random.randrange(1,100)
	fullname = "crnn/Images/" + str(name)+".jpg"
	urllib.request.urlretrieve(url,fullname)

	#process data.
	data['document_json'] = str(t01.segment_process(fullname)).strip()

	c_s = dict_using_spellchecker.spell_check_me(data['document_json'])

	f_s = test.new(c_s)

	data['keypharses'] = str(f_s) # can directly use list within it as well instead

	#call fyp_modules

	#commit the returned data using the path + key explicitly. Do not change service variable.

	print("----------------------------------------------------------Completed: some rnd func ")
	return data


def stream_handler(post):
	# print(post)
	global iter_db_hits
	iter_db_hits += 1
	print(str(iter_db_hits))
	#Initial Iterator through the whole Matching JSON. Pending Operations are done first.
	if(post['path']=='/'):
		data = post['data']
		keys = list(data.keys())
		# print(keys)
		for key in keys:
			# print(key)
			# print(data[key])
			if(data[key]['service'] == 1):#check only service
				print("Initial Pendings")
				data[key] = some_rnd_func(post['path'], data[key], key)
				if data[key] != None:
					data[key]['service'] = 5
					db.child(com_path).child(key).update(data[key])
	
	# Not so important for app perspective
	# we change directly using web console.
	elif(re.match('/.+/service', post['path']) and post['event'] == 'put'):
		#when we change directly using web console.
		path = post['path'].split('/')
		path = '/'.join(path[:-1])
		# print("ps")
		data = db.child(com_path + path).get()
		# print(data.val())
		data = data.val()
		if(data['service'] == 1):#check changes only to service
			print("PUT event, due to change made in web console @", path)
			data = some_rnd_func(path, data)
			if data != None:
				data['service'] = 5
				db.child(com_path + path).update(data)

	#Any new changes or adds into the db from the specified path
	elif(re.match('/.+', post['path']) and (post['event'] == 'patch' or post['event']=='put')):
		#when patch. We need to use the full path to fetch the whole object. Before we can check the service variable and update.
		# Usually this is the most called/accessed part, as we update the whole data in update(data). So we'll have not have service
		# variable in path due to db new enteries from the app or updates from the initial service update of Pending request.
		path = post['path']
		data = db.child(com_path + path).get()
		data = data.val()
		if(data['service'] == 1):#check changes only to service
			# print("Patch event @ ", post['path'])
			print("NewEntry or changes to service: ", data)
			data = some_rnd_func(path, data)
			if data != None:
				data['service'] = 5
				db.child(com_path + path).update(data)

print(db)

#for listening to event changes.
my_stream = db.child(com_path).stream(stream_handler, None)
