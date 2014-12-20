import os
import pdb
from collections import Counter
import numpy as np

NGRAMS = [1, 2, 3]

def tokenize(sentence, grams=NGRAMS):
    words = sentence.split()
    tokens = []
    for gram in grams:
        for i in range(len(words) - gram + 1):
            tokens += ["_*_".join(words[i:i+gram])]
    return tokens

def build_dict(file_list):
    dic = Counter()
    for f in file_list:
        for sentence in open(f).xreadlines():
            dic.update(tokenize(sentence))
    return dic

def process_files(file_pos, file_neg, dic, r, outfn):
    output = []
    for beg_line, f in zip([1, -1], [file_pos, file_neg]):
        for l in open(f).xreadlines():
            tokens = tokenize(l)
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

        
if __name__ == "__main__":
    valid = True
    alpha = 1
   
    if not valid:
        train_files = ["train-pos.txt", "train-neg.txt"]
        test_files = ["test-pos.txt", "test-neg.txt"]

        print "counting..."
        poscounts = build_dict(train_files[:1])         
        negcounts = build_dict(train_files[1:])         
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

        print "processing files..."
        process_files(train_files[0], train_files[1], dic, r, "train-nbsvm.txt")
        process_files(test_files[0], test_files[1], dic, r, "test-nbsvm.txt")
       
        os.system("mv train-nbsvm.txt test-nbsvm.txt word2vec") 

        os.chdir("word2vec")
        os.system("./liblinear-1.94/train -s 0 train-nbsvm.txt model.logreg")
        os.system("./liblinear-1.94/predict -b 1 test-nbsvm.txt model.logreg NBSVM-TEST")
        os.chdir("./..")
    else:
        train_files = ["train-pos-small.txt", "train-neg-small.txt"]
        valid_files = ["valid-pos.txt", "valid-neg.txt"]
        test_files = ["test-pos.txt", "test-neg.txt"]

        print "counting..."
        poscounts = build_dict(train_files[:1])         
        negcounts = build_dict(train_files[1:])         
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

        print "processing files..."
        process_files(train_files[0], train_files[1], dic, r, "train-nbsvm.txt")
        process_files(valid_files[0], valid_files[1], dic, r, "valid-nbsvm.txt")
       
        os.system("mv train-nbsvm.txt valid-nbsvm.txt word2vec") 

        os.chdir("word2vec")
        os.system("./liblinear-1.94/train -s 0 train-nbsvm.txt model.logreg")
        os.system("./liblinear-1.94/predict -b 1 valid-nbsvm.txt model.logreg NBSVM-VALID")
        os.chdir("./..")
