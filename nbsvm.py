import os
import pdb
from collections import Counter
import numpy as np

def tokenize(sentence, grams):
    words = sentence.split()
    tokens = []
    for gram in grams:
        for i in range(len(words) - gram + 1):
            tokens += ["_*_".join(words[i:i+gram])]
    return tokens

def build_dict(f, grams):
    dic = Counter()
    for sentence in open(f).xreadlines():
        dic.update(tokenize(sentence, grams))
    return dic

def process_files(file_pos, file_neg, dic, r, outfn, grams):
    output = []
    for beg_line, f in zip([1, -1], [file_pos, file_neg]):
        for l in open(f).xreadlines():
            tokens = tokenize(l, grams)
            indexes = []
            for t in tokens:
                try:
                    indexes += [dic[t]]
                except KeyError:
                    pass
            indexes = list(set(indexes))
            indexes.sort()
            line = [beg_line]
            for i in indexes:
                line += ["%i:%f" % (i + 1, r[i])]
            output += [" ".join(line)]
    output = "\n".join(output)
    f = open(outfn, "w")
    f.writelines(output)
    f.close()

def compute_ratio(poscounts, negcounts, alpha=1):
    alltokens = list(set(poscounts.keys() + negcounts.keys()))
    dic = dict((t, i) for i, t in enumerate(alltokens))
    d = len(dic)
    print "computing r..."
    p, q = np.ones(d) * alpha , np.ones(d) * alpha
    for t in alltokens:
        p[dic[t]] += poscounts[t]
        q[dic[t]] += negcounts[t]
    p /= abs(p).sum()
    q /= abs(q).sum()
    r = np.log(p/q)
    return dic, r
        
if __name__ == "__main__":
    grams = [1, 2, 3] 
    # liblinear PATH
    # train pos file + NEG same for valid
    train_neg = "train-neg.txt"
    train_pos = "train-pos.txt"
    test_neg = "test-neg.txt"
    test_pos = "test-pos.txt"

    print "counting..."
    poscounts = build_dict(train_pos, grams)         
    negcounts = build_dict(train_neg, grams)         
    
    dic, r = compute_ratio(poscounts, negcounts)
    print "processing files..."
    process_files(train_pos, train_neg, dic, r, "train-nbsvm.txt", grams)
    process_files(test_pos, test_neg, dic, r, "test-nbsvm.txt", grams)
   
    os.system("mv train-nbsvm.txt test-nbsvm.txt word2vec") 

    os.chdir("word2vec")
    os.system("./liblinear-1.94/train -s 0 train-nbsvm.txt model.logreg")
    os.system("./liblinear-1.94/predict -b 1 test-nbsvm.txt model.logreg NBSVM-TEST")
    os.chdir("./..")

