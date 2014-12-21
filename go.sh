#this function will convert text to lowercase and will disconnect punctuation and special symbols from words
function normalize_text {
  awk '{print tolower($0);}' < $1 | sed -e 's/\./ \. /g' -e 's/<br \/>/ /g' -e 's/"/ " /g' \
  -e 's/,/ , /g' -e 's/(/ ( /g' -e 's/)/ ) /g' -e 's/\!/ \! /g' -e 's/\?/ \? /g' \
  -e 's/\;/ \; /g' -e 's/\:/ \: /g' > $1-norm
}

mkdir nbsvm_run; cd nbsvm_run

wget http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz
tar -xvf aclImdb_v1.tar.gz

for j in train/pos train/neg test/pos test/neg train/unsup; do
  for i in `ls aclImdb/$j`; do cat aclImdb/$j/$i >> temp; awk 'BEGIN{print;}' >> temp; done
  normalize_text temp
  mv temp-norm aclImdb/$j/norm.txt
  rm temp
done

mkdir data
mv aclImdb/train/pos/norm.txt data/train-pos.txt
mv aclImdb/train/neg/norm.txt data/train-neg.txt
mv aclImdb/test/pos/norm.txt data/test-pos.txt
mv aclImdb/test/neg/norm.txt data/test-neg.txt
cd ..

python nbsvm.py --liblinear ../liblinear-1.96 --ptrain ../data/train-pos.txt --ntrain ../data/train-neg.txt --ptest ../data/test-pos.txt --ntest ../data/test-neg.txt --ngram 123 --out ../scores/NBSVM-TEST
cd ..
