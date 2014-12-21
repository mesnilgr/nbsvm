import os
import pdb
import numpy as np
import argparse
from collections import Counter

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
    for beg_line, f in zip(["1", "-1"], [file_pos, file_neg]):
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
 
def main(ptrain, ntrain, ptest, ntest, out, liblinear, ngram):
    ngram = [int(i) for i in ngram]
    print "counting..."
    poscounts = build_dict(ntrain, ngram)         
    negcounts = build_dict(ptrain, ngram)         
    
    dic, r = compute_ratio(poscounts, negcounts)
    print "processing files..."
    process_files(ptrain, ntrain, dic, r, "train-nbsvm.txt", ngram)
    process_files(ptest, ntest, dic, r, "test-nbsvm.txt", ngram)
    
    trainsvm = os.path.join(liblinear, "train") 
    predictsvm = os.path.join(liblinear, "predict") 
    os.system(trainsvm + " -s 0 train-nbsvm.txt model.logreg")
    os.system(predictsvm + " -b 1 test-nbsvm.txt model.logreg " + out)
    os.system("rm model.logreg train-nbsvm.txt test-nbsvm.txt")
        
if __name__ == "__main__":
    """
    Usage :

    python nbsvm.py --liblinear /PATH/liblinear-1.96\
        --ptrain /PATH/data/full-train-pos.txt\
        --ntrain /PATH/data/full-train-neg.txt\
        --ptest /PATH/data/test-pos.txt\
        --ntest /PATH/data/test-neg.txt\
         --ngram 123 --out TEST-SCORE
    """

    parser = argparse.ArgumentParser(description='Run NB-SVM on some text files.')
    parser.add_argument('--liblinear', help='path of liblinear install e.g. */liblinear-1.96')
    parser.add_argument('--ptrain', help='path of the text file TRAIN POSITIVE')
    parser.add_argument('--ntrain', help='path of the text file TRAIN NEGATIVE')
    parser.add_argument('--ptest', help='path of the text file TEST POSITIVE')
    parser.add_argument('--ntest', help='path of the text file TEST NEGATIVE')
    parser.add_argument('--out', help='path and fileename for score output')
    parser.add_argument('--ngram', help='N-grams considered e.g. 123 is uni+bi+tri-grams')
    args = vars(parser.parse_args())

    main(**args)
