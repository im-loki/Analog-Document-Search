# coding:utf-8
import math
import stemming.porter2 as porter
import numpy as np
import copy
from collections import Counter
import re

def position_rank(sentence, tokenizer, alpha=0.85, window_size=6, num_keyphrase=10, lang="en"):
    """Compute position rank score.

    Position rank is a method for extracting keyphrase from sentence.
    This method is allowed any language if you provide tokenizer
    that tokenize language you wanna apply position rank.
    In the oroginal paper, authors used 'title' and 'abstract' of scholarly documents.
    Original paper is here: http://aclweb.org/anthology/P/P17/P17-1102.pdf

    Args:
      sentence: Text concatenated title and abstract.
      tokenizer: Object that tokenize sentence.
        Tokenizer must has tokenize(), tokenize() receive sentence and return token list
        and phrase list. See tokenizer.py and class of tokenizer for detail.
      alpha: Damping parameter. This allows 'teleport' operation into another node in the graph.
      window_size: Size of woindow for co-occurece word.
      num_keyphrase: Number of keyphrase which method will return.
      lang: Target language.

    Returns:
      Keyphrase list. Length of list is decided by 'num_keyphrase' param.

    """
    if lang == "en":
        stem = porter.stem
        print("Stem: ", stem)
    else:
        stem = lambda word: word
    # origial words(=no stemming) and phrase list
    original_words, phrases = tokenizer.tokenize(sentence)

    print("Original words: ", original_words, len(original_words))
    print("Phrases: ", phrases, len(phrases))

    # stemmed words
    stemmed_word = [stem(word) for word in original_words]
    print("Stemmed: ",stemmed_word, len(stemmed_word))

    unique_word_list = set([word for word in stemmed_word])
    n = len(unique_word_list)
    # print("\nunique_word_list: ",unique_word_list, n)

    adjancency_matrix = np.zeros((n, n))
    word2idx = {w: i for i, w in enumerate(unique_word_list)}
    p_vec = np.zeros(n)
    # store co-occurence words
    co_occ_dict = {w: [] for w in unique_word_list}
    # print(adjancency_matrix, word2idx, p_vec, co_occ_dict)

    # 1. initialize  probability vector
    for i, w in enumerate(stemmed_word):
        print("i, w:", i, w)
        # add position score
        p_vec[word2idx[w]] += float(1 / (i+1))
        print(p_vec)
        for window_idx in range(1, math.ceil(window_size / 2)+1):
            if i - window_idx >= 0:
                co_list = co_occ_dict[w]
                co_list.append(stemmed_word[i - window_idx])
                co_occ_dict[w] = co_list

            if i + window_idx < len(stemmed_word):
                co_list = co_occ_dict[w]
                co_list.append(stemmed_word[i + window_idx])
                co_occ_dict[w] = co_list
            print(w, ": ", co_occ_dict[w])

    print("\np_vec: ", p_vec)
    print("co_occ_dict", co_occ_dict)

    print("\n Adj Matrix: \n")
    # 2. create adjancency matrix from co-occurence word. Just static weights
    for w, co_list in co_occ_dict.items():
        print(w, co_list)
        cnt = Counter(co_list)
        print("--> ", cnt)
        for co_word, freq in cnt.most_common():
            print("<:::>", co_word, freq)
            adjancency_matrix[word2idx[w]][word2idx[co_word]] = freq
            print("$$$::\n",adjancency_matrix)

    print("Final Matrix: \n", adjancency_matrix, adjancency_matrix.sum(axis=0))
    #Incoming Edges relative-weights
    adjancency_matrix = adjancency_matrix / adjancency_matrix.sum(axis=0)
    print("Final relative-weights Matrix: ", adjancency_matrix)

    print("Initial P_vec:, ", p_vec, p_vec.sum())
    p_vec = p_vec / p_vec.sum()
    print("After relative p_vec: ", p_vec, p_vec.sum())
    # principal eigenvector s
    s_vec = np.ones(n) / n
    print("s_vec: ", s_vec)

    # threshold
    lambda_val = 1.0
    loop = 0

    # compute final principal eigenvector
    while lambda_val > 0.001:
        next_s_vec = copy.deepcopy(s_vec)
        print("next_s_vec: ", next_s_vec)
        for i, (p, s) in enumerate(zip(p_vec, s_vec)):
            print(lambda_val, ":", i, "->", (p,s))
            #computation
            next_s = (1 - alpha) * p + alpha * (weight_total(adjancency_matrix, i, s_vec))
            next_s_vec[i] = next_s
            if(i==0):
                print("next_s_vec[",i,"]=", next_s)

        print(next_s_vec)
        lambda_val = np.linalg.norm(next_s_vec - s_vec)
        print("Lambda val after iter: ",lambda_val)
        s_vec = next_s_vec
        loop += 1
        if loop > 100:
            break

    print(s_vec.sum(), len(s_vec))

    # score original words and phrases
    word_with_score_list = [(word, s_vec[word2idx[stem(word)]]) for word in original_words]
    print("Initial word score and list", word_with_score_list, len(word_with_score_list))
    print("Pharses: ", phrases, len(phrases))
    for phrase in phrases:
        print(phrase)
        total_score = sum([s_vec[word2idx[stem(word)]] for word in phrase.split("_")])
        word_with_score_list.append((phrase, total_score))

    print(word_with_score_list, len(word_with_score_list))

    sort_list = np.argsort([t[1] for t in word_with_score_list])
    print("Sort List: ", sort_list)
    keyphrase_list = []
    # if not check stemmed keyphrase, there are similar phrases in keyphrase list
    # i.e. "neural network" and "neural networks" in list
    stemmed_keyphrase_list = []
    for idx in reversed(sort_list):
        keyphrase = word_with_score_list[idx][0]
        print(idx, keyphrase)
        stemmed_keyphrase = " ".join([stem(word) for word in keyphrase.split("_")])
        if not stemmed_keyphrase in stemmed_keyphrase_list:
            keyphrase_list.append(keyphrase)
            stemmed_keyphrase_list.append(stemmed_keyphrase)
        if len(keyphrase_list) >= num_keyphrase:
            break
    print(keyphrase_list)

    c_instance = c_method(keyphrase_list, sentence)
    print("After Position Rank: ", keyphrase_list)
    print("C-value reranking:")
    return c_instance.c_value()


    # C-value method to rerank the keyphrases.

class c_method:

    text = ""
    keyphrase_list = []
    new_keyphrase_list = []

    def __init__(self, keyphrase_list, text):
        self.text = text
        self.keyphrase_list = []
        self.new_keyphrase_list = []
        
        for keyphrase in keyphrase_list:
            temp = keyphrase.split("_")
            # print(temp)
            self.keyphrase_list.append(" ".join(temp))

        print(self.keyphrase_list)

    def c_value(self):
        keyphrase_dict = []
        for keyphrase in self.keyphrase_list:
            keyphrase_dict.append((self.final_Score(keyphrase), keyphrase))

        #re-arrange
        keyphrase_dict.sort(reverse = True)
        # print(keyphrase_dict)
        new_keyphrase_list = [keyphrase for val, keyphrase in keyphrase_dict]
        return new_keyphrase_list

    def score(self, keyphrase):
        # print(len(re.findall(keyphrase, self.text, re.IGNORECASE)))
        return len(re.findall(keyphrase, self.text, re.IGNORECASE))


    def final_Score(self, keyphrase):
        N = -1
        repeat = []
        repeat_score = 0
        # print("\nKEY-> ", keyphrase, end=" ")
        for beta_key in self.keyphrase_list:
            # print("Beta: ",beta_key,end = " ")
            if re.search(keyphrase, beta_key, re.IGNORECASE):
                N += 1
                # print("keyphrase: ", keyphrase, N, "\n")
                repeat.append(beta_key)
                repeat_score += self.score(beta_key)

        # print("repeat_score: ", repeat_score)
        fin_score = self.length(keyphrase) * self.score(keyphrase)

        # self.keyphrase.append(keyphrase)
        # print(N)

        if N>0:
            fin_score -= self.length(keyphrase) * (1/N) * repeat_score

        return fin_score

    def length(self, keyphrase):
        if(len(keyphrase)==1):
            return 0.2
        else:
            return math.log(len(keyphrase),2)

def weight_total(matrix, idx, s_vec):
    """Sum weights of adjacent nodes.

    Choose 'j'th nodes which is adjacent to 'i'th node.
    Sum weight in 'j'th column, then devide wij(weight of index i,j).
    This calculation is applied to all adjacent node, and finally return sum of them.

    """
    return sum([(wij / matrix.sum(axis=0)[j]) * s_vec[j] for j, wij in enumerate(matrix[idx]) if not wij == 0])
