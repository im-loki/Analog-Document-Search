from position_rank import position_rank
from tokenizer import StanfordCoreNlpTokenizer

title = "PositionRank: An Unsupervised Approach to Keyphrase Extraction from Scholarly Documents. "
abstract = "The large and growing amounts of online scholarly data present both challenges and opportunities to enhance knowledge discovery."

print("length of title + abstract: ", len(title + abstract))

tokenizer = StanfordCoreNlpTokenizer("http://localhost", port = 9000)
print(position_rank(title + abstract, tokenizer))