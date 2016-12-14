### Import models

import nltk
from Lib import FileInteraction
from Lib import Classifier
from Lib import Features
from Lib.Classifier import VoteClassifier
from nltk.corpus import movie_reviews
import os


### define functions
'''
Categorize words
eg.
[('PRESIDENT', 'NNP'), ('GEORGE', 'NNP'), ('W.', 'NNP'), ('BUSH', 'NNP')]
'''
def categorize_words(words):
    POS_words = nltk.pos_tag(words)
    return POS_words

'''
Take off un-useful categorized words
eg.
    'NNP', 'PRP'
'''
def takeoff_unuseful_categorized_words(words):
    unused_words = ['PRP', 'NNP']
    filter_words = [w for w in words if w[1] not in unused_words]
    return filter_words
def chunking_words(words):
    try:
        tagged = nltk.pos_tag(words)
        chunkGram = r"""Chunk: {<RB.?>*<VB.?>*<NNP>+<NN>?}""" # chunking all types of adv, V, prop N and N
        chunkParser = nltk.RegexpParser(chunkGram)
        chunked = chunkParser.parse(tagged)
        # chunked.draw()
        print(chunked)
    except TypeError:
        print("input type should be lists")
    except Exception as e:
        print(str(e))

def find_features(document_words, raw_words):
    words = set(document_words)
    features = {}  # create dictionary
    for w in raw_words:
        features[w] = (w in words)
    return features

def analysing_words(words = []):
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
                load_mode = 1  # 1 = loading
                state = 10

            # create test sets
            elif state == 10:
                if load_mode == 0:
                    featuresets = FileInteraction.import_pickle(training_features_path)
                    state = 11
                else:
                    Doc_dict = {}
                    document_path = current_path + "/Doc/Movie_review_doc.pickle"
                    word_features_path = current_path + "/Doc/Word_Features.pickle"
                    Doc_dict['document'] = FileInteraction.import_pickle(document_path)
                    Doc_dict['word_features'] = FileInteraction.import_pickle(word_features_path)
                    feats = Features.find_features(words, Doc_dict['word_features'])
                    state = 12

            # training algorithm
            elif state == 11:

                print('train algorithm')
                classifier_input = ['Naivebayes', 'MultinomialNB', 'BernoulliNB', 'LogisticRegression', 'SGDClassifier', 'SVC',
                         'LinearSVC', 'NuSVC', 'Combination_Classifier']
                classifier_dict = Classifier.train_classifier(classifier_input, load_mode) # save mode
                state = 15
            # load classifiers
            elif state == 12:
                print('load algorithm')
                # classifier_load = ['Naivebayes', 'MultinomialNB', 'BernoulliNB', 'LogisticRegression', 'SGDClassifier',
                #                      'SVC', 'LinearSVC', 'NuSVC', 'Combination_Classifier']
                classifier_load = ['Naivebayes', 'MultinomialNB', 'BernoulliNB', 'LogisticRegression', 'SGDClassifier',
                                   'LinearSVC', 'NuSVC']
                classifier_dict = Classifier.train_classifier(classifier_load, load_mode)  # load mode
                print('loading success')
                state = 15

            # test algorithm accuracy
            elif state == 15:
                if load_mode == 0:
                    testing_set = featuresets[1900:3000]
                    for k, v in classifier_dict.items():
                        print("classifier '", k, "' accuracy percent:",
                              (nltk.classify.accuracy(v, testing_set)) * 100)
                else:

                    testing_set = feats
                    classifier = VoteClassifier(classifier_dict['Naivebayes'],
                                                classifier_dict['MultinomialNB'],
                                                classifier_dict['BernoulliNB'],
                                                classifier_dict['LogisticRegression'],
                                                classifier_dict['SGDClassifier'],
                                                classifier_dict['LinearSVC'],
                                                classifier_dict['NuSVC'])
                    print("classifier 'Combination_Classifier' Classification:", classifier.classify(testing_set))
                    print("with confidence", classifier.confidence(testing_set)*100 )

                state = 19

            elif state == 70:
                categorized_words = categorize_words(words)
                state=71
            elif state == 71:
                analysed_words = takeoff_unuseful_categorized_words(categorized_words)
                state = 79

            # lemmatize using to find synonym
            elif state == 80:
                from nltk.stem import WordNetLemmatizer
                lemmatizer = WordNetLemmatizer()
                print(lemmatizer.lemmatize("better", pos="a"))
                state = 89

            # chunking algorithm
            elif state == 90:
                analysed_words = chunking_words(words)  # chunk same POS together
                state = 99

            else:  # End process
                # print("Extracting useful words...")
                return analysed_words
                break

        except:
            print("Unexpect error occured while analysing words...")
            break





def main():
    pass

def initial():
    pass

current_path = os.getcwd()
if __name__ == "__main__":
    current_path = os.path.abspath(os.path.join(current_path, os.pardir))
    print(current_path)
    main()
else:
    initial()
    print('using AnalyseWords module')

