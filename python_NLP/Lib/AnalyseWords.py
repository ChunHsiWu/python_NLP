### Import models

import nltk
from Lib import FileInteraction
from Lib import Classifier
from Lib import Features
from Lib.Classifier import VoteClassifier
#from nltk.corpus import movie_reviews
import os
from sklearn import metrics
### define functions


#
# def find_features(document_words, raw_words):
#     words = set(document_words)
#     features = {}  # create dictionary
#     for w in raw_words:
#         features[w] = (w in words)
#     return features

def analysing_words(words=[], load_mode=1):
    state = 0
    while True:
        try:
            if state == 0:
                categorized_words = []
                analysed_words = []
                all_words = []  # all the words from input words
                document_path = current_path + "/Doc/Movie_review_doc.pickle"
                training_features_path = current_path + "/Doc/Training_Features.pickle"
                classifier_dict = {}
                #load_mode = 1  # 1 = loading
                state = 10

            # allocate states
            elif state == 10:
                if load_mode == 0:
                    state = 11
                else:
                    state = 12

            # training classifiers
            elif state == 11:

                print('train algorithm')
                classifier_input = ['Naivebayes', 'MultinomialNB', 'BernoulliNB', 'LogisticRegression', 'SGDClassifier',
                                    'SVC', 'LinearSVC', 'NuSVC', 'Combination_Classifier']
                #classifier_input = ['Naivebayes', 'MultinomialNB', 'LogisticRegression', 'LinearSVC', 'Combination_Classifier']
                classifier_dict = Classifier.train_classifier(classifier_input, load_mode) # save mode
                state = 14
            # load classifiers
            elif state == 12:
                print('load algorithm')
                classifier_load = 'Combination_Classifier'

                classifier_dict = Classifier.train_classifier(classifier_load, load_mode)  # load mode
                state = 14

            # create test datasets
            elif state == 14:
                if load_mode == 0:
                    featuresets = FileInteraction.import_pickle(training_features_path)
                else:
                    Doc_dict = {}
                    document_path = current_path + "/Doc/Movie_review_doc.pickle"
                    word_features_path = current_path + "/Doc/Word_Features.pickle"
                    Doc_dict['document'] = FileInteraction.import_pickle(document_path)
                    Doc_dict['word_features'] = FileInteraction.import_pickle(word_features_path)
                    feats = Features.find_features(words, Doc_dict['word_features'])
                state = 15

            # test algorithm accuracy
            elif state == 15:
                if load_mode == 0:
                    testing_set = featuresets[12000:]
                    for k, v in classifier_dict.items():
                        print("classifier '", k, "' accuracy percent:",
                              (nltk.classify.accuracy(v, testing_set)) * 100)
                else:
                    testing_set = feats
                    print('testing_set =', testing_set)
                    for k, v in classifier_dict.items():
                        print("classifier",k , "Classification:", v.classify(testing_set))
                        print("with confidence", v.confidence(testing_set) * 100)

                state = 19


            else:  # End process
                # print("Extracting useful words...")
                return analysed_words
                break

        except:
            print("Unexpect error occured while analysing words...")
            break





def main():
    # training classifier here
    user_input = input("Are you going to start training classifier (Y/N)?")
    if (user_input == 'Y') or (user_input == 'y'):
        analysing_words('',0)
    elif (user_input == 'N') or (user_input == 'n'):
        load_mode = 1
    else:
        print('Error input')

def initial():
    pass

current_path = os.getcwd()
if __name__ == "__main__":
    current_path = os.path.abspath(os.path.join(current_path, os.pardir))
    print('using AnalyseWords module at ', current_path)
    main()
else:
    initial()
    print('using AnalyseWords module at ', current_path)

