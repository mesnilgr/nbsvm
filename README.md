Naive Bayes SVM (NB-SVM)
========================

This code reproduces performance of the NB-SVM on the IMDB reviews from the
paper:

Sida Wang and Christopher D. Manning: Baselines and Bigrams: Simple, Good Sentiment and Topic Classification; ACL 2012.
http://nlp.stanford.edu/pubs/sidaw12_simple_sentiment.pdf

They obtain 91.22% while this code obtains 91.55% with bigrams and 91.82% with trigrams.
Little improvements (+0.33% with bigrams and +0.6% with unigrams) versus the paper.

To reproduce the results:

```
chmod +x go.sh
./go.sh
```

End to end (downloading the data, tokenizing, training the models), this will
take 68 mins. Note that most of the time is spent dowloading and tokenizing.
Once the data has been downloaded and tokenized, training an NB-SVM only takes
~2 mins for uni+bigrams and <5 mins for uni+bi+trigrams.
