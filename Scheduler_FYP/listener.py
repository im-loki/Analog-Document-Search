import pyrebase
import re

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

def some_rnd_func(path, data, key = ''):
	print("Starting Some rnd func")
	# print("Path: ", path)
	# print("key: ", key)
	# print("data received: ", data)

	#commit any new data into db explicitly here. Do not change service variable here, though.
	
	#process data.

	#call fyp_modules

	#commit the returned data using the path + key explicitly. Do not change service variable.

	#return 1. if successful. Else -1. Service variable will be updated depending on the type.

	print("Completed: some rnd func ")
	return 1


def stream_handler(post):
	# print(post)

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
				if some_rnd_func(post['path'], data[key], key)==1:
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
			if some_rnd_func(path, data) == 1:
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
			if some_rnd_func(path, data) == 1:
				data['service'] = 5
				db.child(com_path + path).update(data)

print(db)
#for listening to event changes.
my_stream = db.child(com_path).stream(stream_handler, None)