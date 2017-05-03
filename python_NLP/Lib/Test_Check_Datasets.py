from Lib import FileInteraction
from Lib import ExtractWords
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.classify import accuracy
from Lib import AnalyseWords
import nltk
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB  # including GaussianNB, BaseDiscreteNB, MultinomialNB,BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
import xlrd
import xlwt
import random
from Lib import Classifier
from Lib import Features
import os
current_path = os.getcwd()
from Lib.Classifier import VoteClassifier

# setup for saving csv
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1")
# establish the csvfile
book_confusion_matrix = xlwt.Workbook(encoding="utf-8")
sheet1_confusion_matrix = book_confusion_matrix.add_sheet("Sheet 1")

def check_reliable_dataset(dataset={}, Doc_dict={}):
    state = 0
    while True:
        try:
            if state == 0:  # initial state
                print('step', state)
                sid = SentimentIntensityAnalyzer()
                dict={}
                documents=[]
                words_array=[]
                all_words=[]
                search_frequent_productID = True
                #classifer_path = current_path + '/Doc/' + 'Combination_Classifier' + '.pickle'
                #classifer = FileInteraction.import_pickle(classifer_path)



                state = 10
                '''
                # test for find specific
                elif state == 1:
                    if(search_frequent_productID):
                        state = 2
                    else:
                        state = 10
                elif state == 2:
                    productID_array=[]
                    productID_dict={}
                    for k, v in dataset.items():
                        if v[0] not in productID_array:
                            productID_array.append(v[0])
                            productID_dict[v[0]]=0
                        else:
                            productID_dict[v[0]] += 1
                    #for i in productID_array:
                    #    print("prodict ID ", i, "has elements =", productID_dict[i])
                    maximum = max(productID_dict, key=productID_dict.get)  # Just use 'min' instead of 'max' for minimum.
                    print(maximum, productID_dict[maximum])
                    top5 = sorted(productID_dict, key=productID_dict.get, reverse=True)[:5]
                    for i in top5:
                        print(i, "has element ", productID_dict[i])
                    state=3
                # modify datasets by specific product ID
                elif state==3:
                    new_dataset = {}
                    for k,v in dataset.items():
                        if v[0] == maximum:
                            new_dataset[k] = v
                    dataset = new_dataset
                    print("only use productID:", maximum)
                    state=10
                '''

            # haven't add weight of summary (polarity check)
            elif state == 10:  # import datasets
                print('step', state)
                #dict[str(ID)] = [productID, helpness, score, summary, description]
                for k,v in dataset.items():
                    if float(v[2]) == 5:  # users satisfy products
                        x, y = v[1].split("/")
                        if (float(x) >= 2 and float(x) / float(y) > 0.7) or (float(x) >= 3 and sid.polarity_scores(v[3].lower())['pos'] > 0):  # dataset is reliable

                            words_array = ExtractWords.extract_useful_words(v[4])

                            useful_words = ' '.join(words_array)
                            #print('ID: ', k, 'has useful words:', useful_words)
                            #print(v[3], 'polarity: pos')
                            #print(sid.polarity_scores(v[3].lower()))
                            #dict[k] = (useful_words, 'pos') # extract useful commend
                            documents.append((word_tokenize(v[4]), 'pos'))
                            for w in words_array:
                                all_words.append(w)
                        else:    # dataset isn't reliable
                            pass

                    elif float(v[2]) < 3: # users don't satisfy products
                        x, y = v[1].split("/")
                        if (float(x) >= 2 and float(x) / float(y) > 0.7) or (float(x) >= 3 and sid.polarity_scores(v[3].lower())['neg'] > 0):  # dataset is reliable
                            words_array = ExtractWords.extract_useful_words(v[4])


                            useful_words = ' '.join(words_array)
                            #print('ID: ', k, 'has useful words:', useful_words)
                            #print(v[3], 'polarity: neg')
                            #print(sid.polarity_scores(v[3].lower()))
                            #dict[k] = (useful_words, 'neg') # extract useful commend
                            documents.append((word_tokenize(v[4]), 'neg'))
                            for w in words_array:
                                all_words.append(w)
                        else:  # dataset isn't reliable
                            pass
                    else:   # dataset isn't reliable
                        pass
                state = 20
            elif state == 20:
                print('step', state)
                dict['document'] = documents
                all_words = FreqDist(all_words)  # list all_words in order
                dict['word_features'] = list(all_words.keys())
                dict['data_pool'] = all_words

                state = 21

            else:
                print("End of program")
                state = 0
                return dict
                break


        except:
            print("Error occurred at extract useful dataset")
            break


def check_in_datapool(all_words={}, data_pool={}):
    data_pool_temp = data_pool.copy()
    for k,v in all_words.items():
        if k in data_pool.keys():
            data_pool_temp[k]= data_pool[k] + v
        else:
            data_pool_temp[k]=v
    return data_pool_temp

def training_classifier(dict={}, classifier_input=[]):
    pass

def build_confusion_matrix(words, count, word_features=[], classifier_input=[]):
    # initia parameters
    classifier_dict = {}

    # load all the classifiers
    for classifier in classifier_input:
        classifer_path = current_path + '/Doc/' + classifier + '_retraining.pickle'
        trained_classifer = FileInteraction.import_pickle(classifer_path)
        classifier_dict[classifier] = trained_classifer
    # create features
    feats = Features.find_features(words, word_features)
    testing_set = feats
    #print('testing_set =', testing_set)
    for k, v in classifier_dict.items():
        prediction = v.classify(testing_set)
        if k is "Naivebayes":
            sheet1_confusion_matrix.write(count, 1, prediction)
        elif k is "MultinomialNB":
            sheet1_confusion_matrix.write(count, 2, prediction)
        elif k is "BernoulliNB":
            sheet1_confusion_matrix.write(count, 3, prediction)
        elif k is "LogisticRegression":
            sheet1_confusion_matrix.write(count, 4, prediction)
        elif k is "SGDClassifier":
            sheet1_confusion_matrix.write(count, 5, prediction)
        elif k is "SVC":
            sheet1_confusion_matrix.write(count, 6, prediction)
        elif k is "LinearSVC":
            sheet1_confusion_matrix.write(count, 7, prediction)
        elif k is "NuSVC":
            sheet1_confusion_matrix.write(count, 8, prediction)
        else:
            sheet1_confusion_matrix.write(count, 9, prediction)
            sheet1_confusion_matrix.write(count, 10, v.confidence(testing_set) * 100)
    #print("classifier", k, "Classification:", v.classify(testing_set))
    #print("with confidence", v.confidence(testing_set) * 100)
    #print("original polarity = ", polarity)

def check_accuracy(dict={}, classifier_input=[], count=0):
    classifier_dict = {}
    test_result = []
    gold_result = []

    for classifier in classifier_input:
        classifer_path = current_path + '/Doc/' + classifier + '.pickle'
        trained_classifer = FileInteraction.import_pickle(classifer_path)
        classifier_dict[classifier] = trained_classifer
    testing_set = [(Features.find_features(rev, dict['word_features']), cate) for (rev, cate) in
                   dict['document']]
    for k, v in classifier_dict.items():
        acc = (accuracy(v, testing_set)) * 100
        print("classifier '", k, "' accuracy percent:", acc)
        for i in range(len(testing_set)):
            test_result.append(v.classify(testing_set[i][0]))
            gold_result.append(testing_set[i][1])
        CM = nltk.ConfusionMatrix(gold_result, test_result)
        print(k, "Classifier: ")
        print(CM)

        # save classifier to csv
        if k is "Naivebayes":
            sheet1.write(count, 1, acc)
        elif k is "MultinomialNB":
            sheet1.write(count, 2, acc)
        elif k is "BernoulliNB":
            sheet1.write(count, 3, acc)
        elif k is "LogisticRegression":
            sheet1.write(count, 4, acc)
        elif k is "SGDClassifier":
            sheet1.write(count, 5, acc)
        elif k is "SVC":
            sheet1.write(count, 6, acc)
        elif k is "LinearSVC":
            sheet1.write(count, 7, acc)
        elif k is "NuSVC":
            sheet1.write(count, 8, acc)
        else:
            sheet1.write(count, 9, acc)


def find_most_product(dict={}, number=1):
    productID_array = []
    productID_dict = {}
    for k, v in dict.items():
        if v[0] not in productID_array:
            productID_array.append(v[0])
            productID_dict[v[0]] = 0
        else:
            productID_dict[v[0]] += 1
    toplist = sorted(productID_dict, key=productID_dict.get, reverse=True)[:number]
    for i in toplist:
        print(i, "has element ", productID_dict[i])
    return toplist


def test(file_path):
    testing_set = []
    classifier_dict = {}
    count = 0
    number_of_products=0

    data_pool_path = current_path + "/Doc/Datapool.pickle"
    document_all_words_path = current_path + "/Doc/Movie_review_all_words.pickle"
    #data_pool = FileInteraction.import_pickle(data_pool_path)
    data_pool={}
    #check_in_datapool(data_pool, data_pool)
    #FileInteraction.export_pickle(data_pool_path, words)
    #data_pool = FileInteraction.import_pickle(data_pool_path)


    sheet1.write(0, 0, "Product ID")
    sheet1.write(0, 1, "Naivebayes")
    sheet1.write(0, 2, "MultinomialNB")
    sheet1.write(0, 3, "BernoulliNB")
    sheet1.write(0, 4, "LogisticRegression")
    sheet1.write(0, 5, "SGDClassifier")
    sheet1.write(0, 6, "SVC")
    sheet1.write(0, 7, "LinearSVC")
    sheet1.write(0, 8, "NuSVC")
    sheet1.write(0, 9, "Combination_Classifier")
    sheet1.write(0, 10, "Total datasets")
    sheet1.write(0, 11, "Effective sets")
    sheet1.write(0, 12, "Number of words")


    data_path = file_path + "/export.xls"
    classifier_input = ['Naivebayes', 'MultinomialNB', 'BernoulliNB', 'LogisticRegression', 'SGDClassifier',
                        'SVC', 'LinearSVC', 'NuSVC', 'Combination_Classifier']
    file_content = FileInteraction.open_file(data_path)  # file path, length
    print("successfully import dataset")

    Doc_dict={}
    document_path = current_path + "/Doc/Movie_review_doc.pickle"
    word_features_path = current_path + "/Doc/Word_Features.pickle"
    Doc_dict['document'] = FileInteraction.import_pickle(document_path)
    Doc_dict['word_features'] = FileInteraction.import_pickle(word_features_path)
    Doc_dict['all_words'] = FileInteraction.import_pickle(document_all_words_path)
    '''
    if(number_of_products > 0):
        toplist = find_most_product(file_content, number_of_products)

        for i in toplist:
            new_dataset = {}
            count += 1
            for k, v in file_content.items():
                if v[0] == i:
                    new_dataset[k] = v
            dataset = new_dataset
            print('length of datasent is ', len(dataset), 'sets')
            sheet1.write(count, 10, len(dataset))
            dict = check_reliable_dataset(dataset, Doc_dict)
            print('length of useful datasent is ', len(dict['document']), 'sets')
            sheet1.write(count, 11, len(dict['document']))
            print('number of all_words is ', len(dict['word_features']), 'words')
            sheet1.write(count, 12, len(dict['word_features']))
            print("productID:", i)
            sheet1.write(count, 0, i)
            check_accuracy(dict, classifier_input, count)

    # testing Amazon review accuracy
    print("testing Amazon review accuracy")
    data_path = file_path + "/export.xls"
    file_content = FileInteraction.open_file(data_path)  # file path, length
    count += 1
    print('length of datasent is ', len(file_content), 'sets')
    sheet1.write(count, 10, len(file_content))
    dict = check_reliable_dataset(file_content, Doc_dict)
    print('length of useful datasent is ', len(dict['document']), 'sets')
    sheet1.write(count, 11, len(dict['document']))
    print('number of all_words is ', len(dict['word_features']), 'words')
    sheet1.write(count, 12, len(dict['word_features']))
    print("productID: All data")
    sheet1.write(count, 0, "All data")

    #check_accuracy(dict, classifier_input, count)

    print("finish original classifier's confusion matrix ")

    
    #=========== for the confusion matrix ==============
    sheet1_confusion_matrix.write(0, 0, "prediction Count")
    sheet1_confusion_matrix.write(0, 1, "Naivebayes")
    sheet1_confusion_matrix.write(0, 2, "MultinomialNB")
    sheet1_confusion_matrix.write(0, 3, "BernoulliNB")
    sheet1_confusion_matrix.write(0, 4, "LogisticRegression")
    sheet1_confusion_matrix.write(0, 5, "SGDClassifier")
    sheet1_confusion_matrix.write(0, 6, "SVC")
    sheet1_confusion_matrix.write(0, 7, "LinearSVC")
    sheet1_confusion_matrix.write(0, 8, "NuSVC")
    sheet1_confusion_matrix.write(0, 9, "Combination_Classifier")
    sheet1_confusion_matrix.write(0, 10, "Confidence")
    sheet1_confusion_matrix.write(0, 11, "Target polarity")
    count_prediction = 1
    docs = dict['document']
    for i in docs:
        sheet1_confusion_matrix.write(count_prediction, 0, count_prediction)
        build_confusion_matrix(i[0], count_prediction, dict['word_features'], classifier_input)
        sheet1_confusion_matrix.write(count_prediction, 11, i[1])
        count_prediction += 1
    csv_path = file_path + '/python_NLP/Doc/exportCSV/prediction_selfTrained.csv'
    book_confusion_matrix.save(csv_path)
    print("success saving prediction.csv")
    '''




    # training new classifier here
    data_path = file_path + "/export.xls"
    #classifier_input = ['Naivebayes', 'LogisticRegression', 'LinearSVC','NuSVC', 'Combination_Classifier']
    #classifier_input = ['NuSVC']
    Naivebayes_classifier_path = current_path + "/Doc/Naivebayes_retraining.pickle"
    BernoulliNB_classifer_path = current_path + "/Doc/BernoulliNB_retraining.pickle"
    MultinomialNB_classifer_path = current_path + "/Doc/MultinomialNB_retraining.pickle"
    LogisticRegression_classifer_path = current_path + "/Doc/LogisticRegression_retraining.pickle"
    SGDClassifier_classifer_path = current_path + "/Doc/SGDClassifier_retraining.pickle"
    LinearSVC_classifer_path = current_path + "/Doc/LinearSVC_retraining.pickle"
    NuSVC_classifer_path = current_path + "/Doc/NuSVC_retraining.pickle"
    file_content = FileInteraction.open_file(data_path)  # file path, length
    dict = check_reliable_dataset(file_content)

    # ===========   test retraining algorithm   ============

    # only for the first time, will change to upload by file in the future
    data_pool['all_words'] = Doc_dict['all_words']
    docs = Doc_dict['document']
    for i in dict['document']:
        docs.append(i)
    random.shuffle(docs)
    data_pool['document'] = docs[:2000]

    print("start testing re-traing")
    data_pool_all_words = check_in_datapool(dict['data_pool'], data_pool['all_words'])
    data_pool_all_words = sorted(data_pool_all_words.items(), key=lambda x: x[1], reverse=True)

    print("most common 20 words in Movie_review")
    print(Doc_dict['all_words'].most_common(20))
    print("most common 20 words in Amazon_review")
    print(dict['data_pool'].most_common(20))
    print("most common 20 words in Movie_review")
    print(data_pool_all_words[:20])


    most_freq = [i[0] for i in data_pool_all_words]
    #most_freq = [i[0] for i in data_pool_all_words.most_common()]
    word_features = most_freq[:2000]


    # ==== havent done yet !!! =====

    print("get new 2000 words")
    featuresets = [(Features.find_features(rev, word_features), cate) for (rev, cate) in
                   data_pool['document']]
    #featuresets = [(Features.find_features(rev, word_features), cate) for (rev, cate) in dict['document']]
    training_set_length = int(len(featuresets) * 2 / 3)
    training_set = featuresets[:training_set_length]
    testing_set = featuresets[training_set_length:]
    print("get new training & testing sets")

    for classifier_name in classifier_input:

        if classifier_name == 'Naivebayes':
            classifier = nltk.NaiveBayesClassifier

        elif classifier_name == 'MultinomialNB':
            classifier = SklearnClassifier(MultinomialNB())

        elif classifier_name == 'BernoulliNB':
            classifier = SklearnClassifier(BernoulliNB())

        elif classifier_name == 'LogisticRegression':
            classifier = SklearnClassifier(LogisticRegression())

        elif classifier_name == 'SGDClassifier':
            classifier = SklearnClassifier(SGDClassifier())

        elif classifier_name == 'SVC':
            classifier = SklearnClassifier(SVC())

        elif classifier_name == 'LinearSVC':
            classifier = SklearnClassifier(LinearSVC())

        elif classifier_name == 'NuSVC':
            classifier = SklearnClassifier(NuSVC(kernel='rbf',nu=0.01))

        elif classifier_name == 'Combination_Classifier':
            Naivebayes_classifer = FileInteraction.import_pickle(Naivebayes_classifier_path)
            #BernoulliNB_classifer = FileInteraction.import_pickle(BernoulliNB_classifer_path)
            #MultinomialNB_classifer = FileInteraction.import_pickle(MultinomialNB_classifer_path)
            LogisticRegression_classifer = FileInteraction.import_pickle(LogisticRegression_classifer_path)
            #SGDClassifier_classifer = FileInteraction.import_pickle(SGDClassifier_classifer_path)
            LinearSVC_classifer = FileInteraction.import_pickle(LinearSVC_classifer_path)
            #NuSVC_classifer = FileInteraction.import_pickle(NuSVC_classifer_path)
            classifier = VoteClassifier(Naivebayes_classifer, LogisticRegression_classifer, LinearSVC_classifer)
            trained_classifer = classifier
        if classifier_name != 'Combination_Classifier':
            trained_classifer = classifier.train(training_set)


        acc = (accuracy(trained_classifer, testing_set)) * 100
        print("classifier '", classifier_name, "' accuracy percent:", acc)
        test_result = []
        gold_result = []
        for i in range(len(testing_set)):
            test_result.append(trained_classifer.classify(testing_set[i][0]))
            gold_result.append(testing_set[i][1])
        CM = nltk.ConfusionMatrix(gold_result, test_result)
        print(classifier_name, "Classifier: ")
        print(CM)
        classifer_path = current_path + '/Doc/' + classifier_name + '_retraining.pickle'
        FileInteraction.export_pickle(classifer_path, trained_classifer)

    '''
    # =========== for the confusion matrix ==============
    count_prediction = 1
    docs = dict['document']
    for i in docs:
        sheet1_confusion_matrix.write(count_prediction, 0, count_prediction)
        build_confusion_matrix(i[0], count_prediction, dict['word_features'], classifier_input)
        sheet1_confusion_matrix.write(count_prediction, 11, i[1])
        count_prediction += 1
    csv_path = file_path + '/python_NLP/Doc/exportCSV/prediction_selftrained.csv'
    book_confusion_matrix.save(csv_path)
    print("success saving prediction.csv")

    csv_path = file_path + '/python_NLP/Doc/exportCSV/Amazon_Review.csv'
    book.save(csv_path)
    '''
    training_features_path = current_path + "/Doc/Training_Features.pickle"
    #for (rev, cate) in dict['document']:
    #    testing_set.append((Features.find_features(rev, dict['word_features']), cate))





if __name__ == "__main__":
    current_path = os.path.abspath(os.path.join(current_path, os.pardir))
    file_path = os.path.abspath(os.path.join(current_path, os.pardir))
    print(current_path)
    test(file_path)
else:
    print('This file is a model')