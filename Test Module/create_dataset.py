import re
import ast
import os

print("Hello")
number_of_instances = int(input("Enter the number of instances: "))
i = 0
list_dataset = []
list_name = []
for root, dirs, files in os.walk("./Inspec/text/"):
    for filename in files:
        list_name.append(str(filename).split('.')[0])
list_name = list_name[:]
while i < number_of_instances:
	file_text = open("Inspec/text/" + list_name[i] + ".txt", "r")
	text = file_text.read()
	text = re.sub('\t+', "", text)
	print("Text",text)
	file_text.close()

	file_key = open("Inspec/keys/" + list_name[i] + ".key", "r")
	key = file_key.read()
	key = re.sub('\t+', '', key)
	key = key.split('\n')
	list_key = []
	for k in key:
		if k == " " or k =='' or k=="\n":
			pass
		else:
			list_key.append(k)

	print(list_key)
	file_key.close()

	list_dataset.append((text, list_key))
	i += 1

print(list_dataset)
f = open("complied_set.txt", "w")
f.write(str(list_dataset))
f.close()
# f = open("complied_set.txt", "r")
# print(str(ast.literal_eval(f.read())))
# f.close()