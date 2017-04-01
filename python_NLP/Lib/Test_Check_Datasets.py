from Lib import FileInteraction
from Lib import ExtractWords
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.classify import accuracy
import xlrd
from Lib import Classifier
from Lib import Features
import os
current_path = os.getcwd()

def check_reliable_dataset(dataset={}):
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
                state = 1
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







            # haven't add weight of summary (polarity check)
            elif state == 10:  # import datasets
                print('step', state)
                #dict[str(ID)] = [productID, helpness, score, summary, description]
                for k,v in dataset.items():
                    if float(v[2]) == 5:  # users satisfy products
                        x, y = v[1].split("/")
                        if float(x) > 3 and float(x)/float(y) > 0.8: # dataset is reliable
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
                        if float(x) > 3 and float(x)/float(y) > 0.8: # dataset is reliable
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
                '''
                test_freq = all_words.most_common(10)
                print(test_freq)
                for i in test_freq:
                    print('key = ', i[0])
                    print('value = ', i[1])
                '''


                #for k, v in dict.items():
                #    print('ID', k, 'has', v[1], 'meaning')
                state = 21

            else:
                print("End of program")
                state = 0
                return dict
                break


        except:
            print("Error occurred at extract useful dataset")
            break


def check_accuracy(dict={}):
    classifier_dict = {}
    classifier_input = ['Naivebayes', 'LogisticRegression', 'LinearSVC', 'Combination_Classifier']
    for classifier in classifier_input:
        classifer_path = current_path + '/Doc/' + classifier + '.pickle'
        trained_classifer = FileInteraction.import_pickle(classifer_path)
        classifier_dict[classifier] = trained_classifer
    '''
    classifier_load = 'LogisticRegression'
    #classifier_load = 'LogisticRegression'
    classifer_path = current_path + '/Doc/' + classifier_load + '.pickle'
    trained_classifer = FileInteraction.import_pickle(classifer_path)
    print('success import pickle')
    '''
    testing_set = [(Features.find_features(rev, dict['word_features']), cate) for (rev, cate) in
                   dict['document']]
    for k, v in classifier_dict.items():
        print("classifier '", k, "' accuracy percent:",
              (accuracy(v, testing_set)) * 100)


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
    data_path = file_path + "/2.xls"
    print(data_path)

    file_content = FileInteraction.open_file(data_path)  # file path, length
    print("successfully import dataset")

    toplist = find_most_product(file_content, 5)

    for i in toplist:
        new_dataset = {}
        for k, v in file_content.items():
            if v[0] == i:
                new_dataset[k] = v
        dataset = new_dataset

        dict = check_reliable_dataset(dataset)
        print('length of useful datasent is ', len(dict['document']), 'sets')
        print(dict['document'][0])
        print('number of all_words is ', len(dict['word_features']), 'words')
        print('load algorithm')
        print("productID:", i)
        check_accuracy(dict)
    '''
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        dict = check_reliable_dataset(file_content)
        print('length of useful datasent is ', len(dict['document']), 'sets')
        print(dict['document'][0])
        print('number of all_words is ', len(dict['word_features']), 'words')
        print('load algorithm')
    
        check_accuracy(dict)
    
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