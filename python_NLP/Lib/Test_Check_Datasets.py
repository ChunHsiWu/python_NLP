from Lib import FileInteraction
from Lib import ExtractWords
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.classify import accuracy
from Lib import AnalyseWords

import xlrd
import xlwt
from Lib import Classifier
from Lib import Features
import os
current_path = os.getcwd()

# setup for saving csv
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1")

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
                        if (float(x) >= 2 and float(x) / float(y) > 0.7) or (float(x) >= 2 and sid.polarity_scores(v[3].lower())['pos'] > 0) :  # dataset is reliable

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
                        if (float(x) >= 2 and float(x) / float(y) > 0.7) or (float(x) >= 2 and sid.polarity_scores(v[3].lower())['neg'] > 0) :  # dataset is reliable
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
                dict['word_features'] = all_words

                state = 21

            else:
                print("End of program")
                state = 0
                return dict
                break


        except:
            print("Error occurred at extract useful dataset")
            break
def getFeatures(words, Doc_dict={}):
    feats = Features.find_features(words, Doc_dict['word_features'])
    return feats

def check_accuracy(dict={}, classifier_input=[], count=0):
    classifier_dict = {}
    for classifier in classifier_input:
        classifer_path = current_path + '/Doc/' + classifier + '.pickle'
        trained_classifer = FileInteraction.import_pickle(classifer_path)
        classifier_dict[classifier] = trained_classifer
    testing_set = [(Features.find_features(rev, dict['word_features']), cate) for (rev, cate) in
                   dict['document']]
    for k, v in classifier_dict.items():
        acc = (accuracy(v, testing_set)) * 100
        print("classifier '", k, "' accuracy percent:", acc)
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


    data_path = file_path + "/2.xls"
    classifier_input = ['Naivebayes', 'MultinomialNB', 'BernoulliNB', 'LogisticRegression', 'SGDClassifier',
                        'SVC', 'LinearSVC', 'NuSVC', 'Combination_Classifier']
    file_content = FileInteraction.open_file(data_path)  # file path, length
    print("successfully import dataset")

    Doc_dict={}
    document_path = current_path + "/Doc/Movie_review_doc.pickle"
    word_features_path = current_path + "/Doc/Word_Features.pickle"
    Doc_dict['document'] = FileInteraction.import_pickle(document_path)
    Doc_dict['word_features'] = FileInteraction.import_pickle(word_features_path)

    toplist = find_most_product(file_content, 10)

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
    check_accuracy(dict, classifier_input, count)

    csv_path = file_path + '/python_NLP/Doc/exportCSV/Amazon_Review.csv'
    book.save(csv_path)

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