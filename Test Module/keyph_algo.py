from keyph import position_rank as p
from keyph import tokenizer as t

doc_text = "Unsupervisied Keyphrase Extraction. Unsupervisied Keyphrase. Keyphrase Extraction. ".lower()
tokenizer = t.StanfordCoreNlpTokenizer("http://localhost", port = 9000)
pos_rank, pos_c_rank, res = p.position_rank(doc_text, tokenizer)

print(pos_rank, pos_c_rank, res)