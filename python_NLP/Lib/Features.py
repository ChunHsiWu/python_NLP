# "Features" are also known as predictors, inputs, or attributes.
### Import models
from nltk.corpus import movie_reviews
import nltk
# from nltk.tokenize import word_tokenize
import random
import os
### define functions
from Lib import FileInteraction



def find_features(document_words, raw_words):
    words = set(document_words)
    features = {}  # create dictionary
    for w in raw_words:
        features[w] = (w in words)
    return features

def get_documents():
    pass


def main():
    documents = []
    all_words = []  # all the words from input words

    documents = [(list(movie_reviews.words(fileID)), category)
                 for category in movie_reviews.categories()
                 for fileID in movie_reviews.fileids(category)]

    # documents[:(len(NLTK_documents)/2)]  # neg
    # documents[(len(NLTK_documents)/2):]  # pos

    pos_doc_path = current_path + "/Doc/positive.csv"
    neg_doc_path = current_path + "/Doc//negative.csv"
    pos_doc = FileInteraction.import_file(pos_doc_path)
    neg_doc = FileInteraction.import_file(neg_doc_path)


    for r in pos_doc.split('\n'):
        documents.append((nltk.word_tokenize(r), "pos"))

    for r in neg_doc.split('\n'):
        documents.append((nltk.word_tokenize(r), "neg"))

    random.shuffle(documents)


    for w in movie_reviews.words():
        all_words.append(w.lower())

    for w in nltk.word_tokenize(pos_doc):
        all_words.append(w.lower())

    for w in nltk.word_tokenize(neg_doc):
        all_words.append(w.lower())


    all_words = nltk.FreqDist(all_words)  # list all_words in order
    word_features = list(all_words.keys())[:6000]  # acquire the most frequently used words
    featuresets = [(find_features(rev, word_features), cate) for (rev, cate) in documents]
    print(len(featuresets))
    training_set = featuresets[:10000]
    testing_set = featuresets[10000:]
    # input_classifier =
    # classifer_path = current_path + '/Doc/' + input_classifier + '.pickle'
    # trained_classifer = FileInteraction.import_pickle(classifer_path)
    input_classifier = 'Naivebayes'
    NBclassifier = nltk.NaiveBayesClassifier

    trained_classifer = NBclassifier.train(training_set)
    print("classifier '", input_classifier, "' accuracy percent:",
          (nltk.classify.accuracy(trained_classifer, testing_set)) * 100)
    classifer_path = current_path + '/Doc/' + input_classifier + '_new.pickle'
    FileInteraction.export_pickle(classifer_path, trained_classifer)


def test():
    pos_doc_path = current_path + "/Doc/positive.csv"
    #neg_doc_path = current_path + "/Doc//negative.txt"
    pos_doc = FileInteraction.import_file(pos_doc_path)
    #neg_doc = FileInteraction.import_file(neg_doc_path)


current_path = os.getcwd()
if __name__ == "__main__":
    current_path = os.path.abspath(os.path.join(current_path, os.pardir))
    print(current_path)
    #test()
    main()
else:
    print('using Features module')