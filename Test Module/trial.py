import os

list_text = list()

for root, dirs, files in os.walk("./Inspec/text/"):
    for filename in files:
        list_text.append(str(filename).split('.')[0])
print(len(list_text))
print(list_text[4])