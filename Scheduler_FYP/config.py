import pyrebase

config = {
  "apiKey": " AIzaSyB5OEATcLYrle-7-Q3JX2Sai7jp5ja0T5o ",
  "authDomain": "fyp01-8d888.firebaseapp.com",
  "databaseURL": "https://fyp01-8d888.firebaseio.com/",
  "storageBucket": "fyp01-8d888.appspot.com",
  "serviceAccount": "./fyp_key.json"
}

firebase = pyrebase.initialize_app(config) #you should add the config as documentation
print(firebase)

db = firebase.database()

# database path always changes, with respect to this
# db.child("loki").child("loki01")

data = {
        "author" : "Lokeshwar1",
        "document_json" : "",
        "document_name" : "Living Room1",
        "document_path" : "https://firebasestorage.googleapis.com/v0/b/fyp01-8d888.appspot.com/o/images%2FWed%20Jan%2029%2022%3A41%3A56%20GMT%2B05%3A30%202020.jpg?alt=media&token=c75d2cd1-5c75-4bde-b7d6-dd09abcad516",
        "keypharses" : "",
        "service" : 1,
        "year" : "2020"
      }

db.child("Requests/Active").push(data)