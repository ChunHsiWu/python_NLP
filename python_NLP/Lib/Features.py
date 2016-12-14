# "Features" are also known as predictors, inputs, or attributes.
### Import models
from nltk.corpus import movie_reviews
import nltk
# from nltk.tokenize import word_tokenize
import random
import os
### define functions
from Lib import FileInteraction



def find_features(document_words, word_features):
    words = set(document_words) #<- change to feature words
    features = {}  # create dictionary
    for w in word_features:
        features[w] = (w in words)
    return features

def word_features(frequency):   # return documents & word_features
    state = 0
    while isinstance(frequency, int):
        try:
            if state == 0:
                documents = []
                all_words = []  # all the words from input words
                dict = {}
                state = 10
            # load document and all words from NLTK movie review
            elif state == 10:
                documents = [(list(movie_reviews.words(fileID)), category)
                             for category in movie_reviews.categories()
                             for fileID in movie_reviews.fileids(category)]
                # documents[:1000]  # neg
                # documents[1000:]  # pos
                for w in movie_reviews.words():
                    all_words.append(w.lower())
                state = 11
            # load document and all words from https://pythonprogramming.net/static/downloads/short_reviews/
            elif state == 11:
                pos_doc_path = current_path + "/Doc/positive.csv"
                neg_doc_path = current_path + "/Doc//negative.csv"
                pos_doc = FileInteraction.import_file(pos_doc_path)
                neg_doc = FileInteraction.import_file(neg_doc_path)
                for r in pos_doc.split('\n'):
                    documents.append((nltk.word_tokenize(r), "pos"))

                for r in neg_doc.split('\n'):
                    documents.append((nltk.word_tokenize(r), "neg"))

                for w in nltk.word_tokenize(pos_doc):
                    all_words.append(w.lower())
                for w in nltk.word_tokenize(neg_doc):
                    all_words.append(w.lower())
                state = 12
            # load document and all words from https://github.com/jeffreybreen/twitter-sentiment-analysis-tutorial-201107/tree/master/data/opinion-lexicon-English
            elif state == 12:
                pos_doc_path = current_path + "/Doc/positive-words.csv"
                neg_doc_path = current_path + "/Doc//negative-words.csv"
                pos_doc = FileInteraction.import_file(pos_doc_path)
                neg_doc = FileInteraction.import_file(neg_doc_path)
                documents.append((list(nltk.word_tokenize(pos_doc)), "pos"))
                documents.append((list(nltk.word_tokenize(neg_doc)), "neg"))
                for w in nltk.word_tokenize(pos_doc):
                    all_words.append(w.lower())
                for w in nltk.word_tokenize(neg_doc):
                    all_words.append(w.lower())
                state = 20
            elif state == 20:
                random.shuffle(documents)
                dict['document'] = documents
                state = 21
            # return
            elif state == 21:
                all_words = nltk.FreqDist(all_words)  # list all_words in order
                word_features = list(all_words.keys())[:frequency]  # acquire the most frequently used words
                dict['word_features'] = word_features
                state = 999
            else:
                return dict

        except:
            print("Unexpect error occured while loading review documents ...")
            break


def main():
    Doc_dict={}
    document_path = current_path + "/Doc/Movie_review_doc.pickle"
    training_features_path = current_path + "/Doc/Training_Features.pickle"
    word_features_path = current_path + "/Doc/Word_Features.pickle"
    Doc_dict['document'] = FileInteraction.import_pickle(document_path)
    Doc_dict['word_features'] = FileInteraction.import_pickle(word_features_path)
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