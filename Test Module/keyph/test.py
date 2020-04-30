import position_rank as p
import tokenizer as t
# from p import position_rank
# from tokenizer import StanfordCoreNlpTokenizer

#title = "PositionRank: An Unsupervised Approach to Keyphrase Extraction from Scholarly Documents. "
#abstract = "The large and growing amounts of online scholarly data present both challenges and opportunities to enhance knowledge discovery."
# title = ""
# abstract = "optical character recognition from wikipedia the free encyclopedia optical character recognition dr optical character reader or s the electronic dr mechanical conversion of mage of typed handwritten d printed text into machineencoded text whether from a scanned document a phot of a document a scenephoto for example the tex dt signs an billboard sum a landscape photo dr from subtle text superimposed dt a image for example from a television broadcast widely used as a form d data entry from printed pape data records ae whether passport documents unvoices dank statements computerized receipts business cards mail printout so fstaticdata dr any suitable documentation se t s a common metho of digitizing printed texts so that they can ge electronically edited searched stored ore compactly displayed online and used n machine processes such a aconitine computing machine translation extracted texttospeech key data and tex mining oc is a felt of research n pattern recognition artificial intelligence and compute vision"
# print("length of title + abstract: ", len(title + abstract))

def new(text):
	tokenizer = t.StanfordCoreNlpTokenizer("http://localhost", port = 9000)
	temp = p.position_rank(text, tokenizer)
	print("Keyphrase Module: ", temp)
	return temp
