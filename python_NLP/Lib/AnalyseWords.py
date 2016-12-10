### Import models
import nltk
from Lib import ImportFile
from nltk.corpus import movie_reviews
import pickle

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
                state = 1
                pickle_path = "./Doc/Naivebayes.pickle"
                document_path = "./Doc/Movie_review_doc.pickle"
                all_words = []  # all the words from input words
            elif state == 1:
                state = 10

            elif state == 2:
                pass
            # ==== NaiveBayes algorithm ====
            # using own words (haven't ready yet)
            elif state == 10:
                # import doc
                documents = ImportFile.import_pickle(document_path)

                for w in words:
                    all_words.append(w.lower())
                featuresets = [(find_features(rev, all_words), cate) for (rev, cate) in documents]
                state = 14
            # using movie_reviews words
            elif state == 11:
                import random
                # documents of all movie_reviews [(list of words, category)]
                documents = [(list(movie_reviews.words(fileID)), category)
                             for category in movie_reviews.categories()
                             for fileID in movie_reviews.fileids(category)]
                random.shuffle(documents)

                # for w in words:
                for w in movie_reviews.words():
                    all_words.append(w.lower())
                all_words = nltk.FreqDist(all_words)  # list all_words in order
                word_features = list(all_words.keys())[:3000]  # acquire the most frequently used words
                featuresets = [(find_features(rev, word_features), cate) for (rev, cate) in documents]
                state = 12

            # training Naivebayes classifier
            elif state == 12:
                # set that we'll train our classifier with
                training_set = featuresets[:1900]
                # set that we'll test against.
                testing_set = featuresets[1900:]
                classifier = nltk.NaiveBayesClassifier.train(training_set)
                state = 13

                # save Naivebayes classifier
            # export classifier
            elif state == 13:
                ImportFile.export_pickle(pickle_path, classifier)
                ImportFile.export_pickle(document_path, documents)
                state = 15

            # load classifier
            elif state == 14:
                classifier = ImportFile.import_pickle(pickle_path)
                testing_set = featuresets
                state = 15
            # test accuracy
            elif state == 15:
                print("Classifier accuracy percent:", (nltk.classify.accuracy(classifier, testing_set)) * 100)
                classifier.show_most_informative_features(50)
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
    # example_sentence =" hey mate, how's everything going? it's a freakin hot weather today, isnt it?"
    # useful_words = extract_useful_words(example_sentence)
    # print(useful_words)
    pass



def initial():
    pass

if __name__ == "__main__":
    main()
else:
    initial()
    print('using AnalyseWords module')

