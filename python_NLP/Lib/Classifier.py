### Import models
import nltk

#from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
# from nltk import classify
from Lib import FileInteraction
from Lib import Features
from sklearn.naive_bayes import MultinomialNB, BernoulliNB  # including GaussianNB, BaseDiscreteNB, MultinomialNB,BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC

from nltk.classify import ClassifierI
from statistics import mode
import os

#
class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf


# def find_features(document_words, raw_words):
#     words = set(document_words)
#     features = {}  # create dictionary
#     for w in raw_words:
#         features[w] = (w in words)
#     return features


def train_classifier(input, load_mode = 1):
    state = 0
    list_index = 0
    classifier_dict = {}
    classifier_path_dict = {}
    while isinstance(input, (list, str)) and list_index < len(input):
        try:
            if state == 0:
                print("Classifier step: ", state)
                document_path = current_path + "/Doc/Movie_review_doc.pickle"
                training_features_path = current_path + "/Doc/Training_Features.pickle"
                word_features_path = current_path + "/Doc/Word_Features.pickle"

                Naivebayes_classifier_path = current_path + "/Doc/Naivebayes.pickle"
                BernoulliNB_classifer_path = current_path + "/Doc/BernoulliNB.pickle"
                MultinomialNB_classifer_path = current_path + "/Doc/MultinomialNB.pickle"
                LogisticRegression_classifer_path = current_path + "/Doc/LogisticRegression.pickle"
                SGDClassifier_classifer_path = current_path + "/Doc/SGDClassifier.pickle"
                LinearSVC_classifer_path = current_path + "/Doc/LinearSVC.pickle"
                NuSVC_classifer_path = current_path + "/Doc/NuSVC.pickle"
                Doc_dict = {}
                all_words = []  # all the words from input words
                featuresets =[]
                documents = []
                if load_mode == 1:
                    state = 12
                else:
                    state = 10

            # create training documents
            elif state == 10:
                print("Classifier step: ", state)
                Doc_dict = Features.word_features(6000)
                featuresets = [(Features.find_features(rev, Doc_dict['word_features']), cate) for (rev, cate) in Doc_dict['document']]
                print(len(featuresets))
                print(featuresets[1])
                # import random
                # # documents of all movie_reviews [(list of words, category)]
                # documents = [(list(movie_reviews.words(fileID)), category)
                #              for category in movie_reviews.categories()
                #              for fileID in movie_reviews.fileids(category)]
                # random.shuffle(documents)
                #
                # for w in movie_reviews.words():
                #     all_words.append(w.lower())
                # all_words = nltk.FreqDist(all_words)  # list all_words in order
                # word_features = list(all_words.keys())[:6000]  # acquire the most frequently used words
                # featuresets = [(find_features(rev, word_features), cate) for (rev, cate) in documents]
                state = 11
            # save document & featuresets
            elif state == 11:
                print("Classifier step: ", state)
                FileInteraction.export_pickle(document_path, Doc_dict['document'])
                FileInteraction.export_pickle(word_features_path, Doc_dict['word_features'])
                FileInteraction.export_pickle(training_features_path, featuresets)

                state = 20

            # load document
            elif state == 12:
                print("Classifier step: ", state)
                Doc_dict['document'] = FileInteraction.import_pickle(document_path)
                Doc_dict['word_features'] = FileInteraction.import_pickle(word_features_path)
                # featuresets = FileInteraction.import_pickle(training_features_path)
                state = 20
            # ==== Training algorithm ====
            # identify classifier
            elif state == 20:
                print("Classifier step: ", state)
                if load_mode ==0:   # saving
                    training_set = featuresets[:12000]
                    testing_set = featuresets[12000:]
                    state = 21
                else:
                    state = 23

                if isinstance(input, list):
                    input_classifier = input[list_index]
                else:
                    input_classifier = input
                if input_classifier == 'Naivebayes':
                    classifier = nltk.NaiveBayesClassifier

                elif input_classifier == 'MultinomialNB':
                    classifier = SklearnClassifier(MultinomialNB())

                elif input_classifier == 'BernoulliNB':
                    classifier = SklearnClassifier(BernoulliNB())

                elif input_classifier == 'LogisticRegression':
                    classifier = SklearnClassifier(LogisticRegression())

                elif input_classifier == 'SGDClassifier':
                    classifier = SklearnClassifier(SGDClassifier())

                elif input_classifier == 'SVC':
                    classifier = SklearnClassifier(SVC())

                elif input_classifier == 'LinearSVC':
                    classifier = SklearnClassifier(LinearSVC())

                elif input_classifier == 'NuSVC':
                    classifier = SklearnClassifier(NuSVC())

                elif input_classifier == 'Combination_Classifier':
                    if load_mode == 0:  # saving
                        state = 22
                        Naivebayes_classifer = FileInteraction.import_pickle(Naivebayes_classifier_path)
                        BernoulliNB_classifer = FileInteraction.import_pickle(BernoulliNB_classifer_path)
                        MultinomialNB_classifer = FileInteraction.import_pickle(MultinomialNB_classifer_path)
                        LogisticRegression_classifer = FileInteraction.import_pickle(LogisticRegression_classifer_path)
                        SGDClassifier_classifer = FileInteraction.import_pickle(SGDClassifier_classifer_path)
                        LinearSVC_classifer = FileInteraction.import_pickle(LinearSVC_classifer_path)
                        NuSVC_classifer = FileInteraction.import_pickle(NuSVC_classifer_path)
                        classifier = VoteClassifier(Naivebayes_classifer,
                                                          BernoulliNB_classifer,
                                                          MultinomialNB_classifer,
                                                          LogisticRegression_classifer,
                                                          SGDClassifier_classifer,
                                                          LinearSVC_classifer,
                                                          NuSVC_classifer)
                        trained_classifer = classifier
                        print("classifier '", input_classifier, "' accuracy percent:",
                              (nltk.classify.accuracy(trained_classifer, testing_set)) * 100)

                else:
                    print(input_classifier, "is not a valid classifer in ClassifierTraining")
                    state = -999

            # training classifier
            elif state == 21:
                print("Classifier step: ", state)
                print(len(training_set))
                print(training_set[1])
                trained_classifer = classifier.train(training_set)
                print("classifier '", input_classifier , "' accuracy percent:",
                      (nltk.classify.accuracy(trained_classifer, testing_set)) * 100)
                state = 22
            # pickling trained classifier
            elif state == 22:
                print("Classifier step: ", state)
                classifer_path = current_path + '/Doc/' + input_classifier + '.pickle'
                FileInteraction.export_pickle(classifer_path, trained_classifer)
                state = 24

            # load trained classifier
            elif state == 23:
                print("Classifier step: ", state)
                # classifer_path = '../Doc/'+ input_classifier + '.pickle'
                classifer_path = current_path + '/Doc/' + input_classifier + '.pickle'
                trained_classifer = FileInteraction.import_pickle(classifer_path)
                state = 24

            # set classifier dictionary for list
            elif state == 24:
                print("Classifier step: ", state)
                classifier_dict[input_classifier] = trained_classifer
                if isinstance(input, list):
                    classifier_path_dict[input_classifier] = classifer_path
                    list_index += 1
                    state = 20
                else:
                    state = 30

            # test combination classifier
            elif state == 40:
                pass

            else:
                state = 0
                list_index = 0
                return classifier_dict
                print("End training test")
                break
        except:
            print("Unexpect error occured while training classifier words...")
            break
    return classifier_dict

def main():
    classifier_dict = {}
    # input = ['Naivebayes', 'MultinomialNB', 'BernoulliNB', 'LogisticRegression', 'SGDClassifier', 'SVC', 'LinearSVC', 'NuSVC', 'Combination_Classifier']
    # classifier_dict = train_classifier(input, 0)
    classifier_dict = train_classifier('Combination_Classifier', 1)


current_path = os.getcwd()
if __name__ == "__main__":
    current_path = os.path.abspath(os.path.join(current_path, os.pardir))
    print(current_path)
    main()
else:
    print('using Classifier module')