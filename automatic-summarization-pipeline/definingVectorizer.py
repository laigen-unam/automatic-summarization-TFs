# -*- encoding: utf-8 -*-
from nltk import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

__author__ = 'CMendezC, LAguirreM'

# FUNCIÓN PARA DEFINIR VECTORIZADORES

# While the tf–idf normalization is often very useful, there might be cases where the binary occurrence
# markers might offer better features.
# This can be achieved by using the binary parameter of CountVectorizer. In particular,
# some estimators such as Bernoulli Naive Bayes explicitly model discrete boolean random variables.
# Also, very short texts are likely to have noisy tf–idf values while the binary occurrence info is more stable.

# It is also common among the text processing community to use binary feature values
# (probably to simplify the probabilistic reasoning) even if normalized counts (a.k.a. term frequencies)
# or TF-IDF valued features often perform slightly better in practice.

# The HashingVectorizer also comes with the following limitations:
# it is not possible to invert the model (no inverse_transform method), nor to access the original string representation
# of the features, because of the one-way nature of the hash function that performs the mapping.
# it does not provide IDF weighting as that would introduce statefulness in the model.
# A TfidfTransformer can be appended to it in a pipeline if required.

class truncate(object):
    def __call__(self, doc):
        return [ocur[:6] for ocur in word_tokenize(doc)]

class noTruncate(object):
    def __call__(self, doc):
        return [ocur for ocur in word_tokenize(doc)]

def definingVectorizer(sgram, fgram, vecType, stopWords, stripAccents, truncating, lowerCase):
    vectorizerObje = None
    vectorizerName = ''
    vectorizerDesc = ''

    # token_pattern : string
    #   Regular expression denoting what constitutes a “token”, only used if analyzer == 'word'.
    # The default regexp select tokens of 2 or more alphanumeric characters
    # (punctuation is completely ignored and always treated as a token separator)
    # WE CHANGE FOR (?u)\b\w+\b AND IT WORKS READING PUNCTUATION AND MULTI-WORD TERMS WITH -
    # TO LOOK AT FEATURES OF VECTORIZER:
    # print(vectorizerObje.get_feature_names()) IN trainingTest.py
    # [',', '.', '19', '5-nt', 'ATP-hydrolysis', 'GAFTGA', 'PhoP', 'PhoQ', 'TGGGN', 'XylR', 'a', 'analysis', 'and',
    # 'as', 'associate', 'b1500', 'be', 'bp', 'by', 'change', 'close', 'communicate',
    # 'complex', 'conformational', 'consecutive', 'd-xylose', 'degradation', 'determine', 'direct', 'factor',
    # 'footprinting', 'fur-binding', 'in', 'increase', 'interact', 'involve', 'lead', 'level', 'motif', 'of',
    # 'phosphorylation', 'polymerase', 'previous', 'promoter', 'promoting-open-complex-formation',
    # 'rearrangement', 'region', 'regulator', 'repeat', 'represent', 'rna', 'separate', 'sequence', 'several',
    # 'show', 'site', 'spacer', 'successive', 'that', 'the', 'thereby', 'think', 'three', 'to', 'transcription',
    # 'two', 'which', 'with', 'xylose']


    if stopWords:
        print("   Filtering stop words")
        pf = stopwords.words('english')
    else:
        pf = None
    
    if vecType == 'BINAR':
        if truncating:
            vectorizerObje = CountVectorizer(binary=True, strip_accents=stripAccents, ngram_range=(sgram, fgram), token_pattern='(?u)\b\w+\b', lowercase=lowerCase,
                stop_words=pf, tokenizer=truncate(), analyzer='word')
        else:
            vectorizerObje = CountVectorizer(binary=True, strip_accents=stripAccents, ngram_range=(sgram, fgram), token_pattern='(?u)\b\w+\b', lowercase=lowerCase,
                stop_words=pf, tokenizer=noTruncate(), analyzer='word')

    elif vecType == 'TFIDF':
        if truncating:
            vectorizerObje = TfidfVectorizer(binary=False, strip_accents=stripAccents, ngram_range=(sgram, fgram), token_pattern='(?u)\b\w+\b', lowercase=lowerCase,
                stop_words=pf, tokenizer=truncate(), analyzer='word')
        else:
            vectorizerObje = TfidfVectorizer(binary=False, strip_accents=stripAccents, ngram_range=(sgram, fgram), token_pattern='(?u)\b\w+\b', lowercase=lowerCase,
                stop_words=pf, tokenizer=noTruncate(), analyzer='word')
    elif vecType == 'COUNT':
        if truncating:
            # '(?u)\b\w+\b'
            vectorizerObje = CountVectorizer(binary=False, strip_accents=stripAccents, ngram_range=(sgram, fgram), token_pattern='(?u)\b\w+\b', lowercase=lowerCase,
                stop_words=pf, tokenizer=truncate(), analyzer='word')
        else:
            vectorizerObje = CountVectorizer(binary=False, strip_accents=stripAccents, ngram_range=(sgram, fgram), token_pattern='(?u)\b\w+\b', lowercase=lowerCase,
                stop_words=pf, tokenizer=noTruncate(), analyzer='word')

    vectorizerName = 'vecTipo{}Stop{}Stri{}NgrI{}NgrF{}Trunc{}Lower{}'.format(vecType, stopWords, stripAccents, sgram, fgram, truncating, lowerCase)
    vectorizerDesc = 'Vectorizer {}, stop words {}, stripAccents {}, sngram {} fngram {} truncate {} lowerCase {}'.format(vecType, stopWords, stripAccents, sgram, fgram, truncating, lowerCase)

    return tuple([vectorizerObje, vectorizerName, vectorizerDesc])
