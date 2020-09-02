from keyph import position_rank as p
from keyph import tokenizer as t
import ast
import time
import csv

flag = 0
run = 0
def dump_to_csv(text_search_time, pos_search_time, pos_c_search_time):
	filename = "time_of_search.csv"
	with open(filename, 'a', newline=None) as csvfile:
		csvwriter = csv.writer(csvfile)
		global flag
		if flag == 0:
			csvwriter.writerow(['text_search_time', 'pos_search_time', 'pos_c_search_time'])
			flag = 1
		csvwriter.writerow([text_search_time, pos_search_time, pos_c_search_time])


def main_test_for_search():
	f = open('complied_set.txt', 'r')
	testcases = ast.literal_eval(f.read())
	new_dump = list()
	print("Hello")
	global run
	for doc_text, keypharses in testcases[29:]:
		try:
			print("##  " + str(run) + "  ##")
			run += 1
			tokenizer = t.StanfordCoreNlpTokenizer("http://localhost", port = 9000)
			pos_rank, pos_c_rank, res = p.position_rank(doc_text, tokenizer)
			
			new_pos_rank, new_pos_c_rank = list(), list()
			if res == 1:
				# Clean up
				for i in range(10):
					temp = pos_rank[i]
					temp = " ".join(temp.lower().split('_'))
					new_pos_rank.append(temp)

					temp = pos_c_rank[i].lower()
					new_pos_c_rank.append(temp)

				# Search timings
				text_search_time, pos_search_time, pos_c_search_time = [list() for i in range(3)]


				for i in range(3):
					temp = new_pos_c_rank[i]
					#search through text
					st = time.time()
					if doc_text.lower().find(temp) != -1:
						et = time.time()
					text_search_time.append(et-st)
					#search through pos_rank
					st = time.time()
					for key in new_pos_rank:
						if key == temp:
							et = time.time()
							break
					pos_search_time.append(et-st)

					#search through new_pos_rank

					st = time.time()
					for key in new_pos_c_rank:
						if key == temp:
							et = time.time()
							break
					pos_c_search_time.append(et-st)

				dump_to_csv(sum(text_search_time)/3, sum(pos_search_time)/3, sum(pos_c_search_time)/3)
				text_search_time, pos_search_time, pos_c_search_time = [None for i in range(3)]
		except:
			print("error : " + str(run-1))
			continue


main_test_for_search()