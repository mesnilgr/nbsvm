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
git clone git@github.com:mesnilgr/nbsvm.git
cd nbsvm; chmod +x oh_my_go.sh
./oh_my_go.sh
```

End to end (downloading the data, tokenizing, training the models), this will
take 68 mins. Note that most of the time is spent dowloading and tokenizing.
Once the data has been downloaded and tokenized, training an NB-SVM only takes
~2 mins for uni+bigrams and <5 mins for uni+bi+trigrams.

<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">Naive Bayes SVM</span> by <span xmlns:cc="http://creativecommons.org/ns#" property="cc:attributionName">Grégoire Mesnil</span> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.<br />Based on a work at <a xmlns:dct="http://purl.org/dc/terms/" href="https://github.com/mesnilgr/nbsvm" rel="dct:source">https://github.com/mesnilgr/nbsvm</a>.
