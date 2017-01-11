from Lib import FileInteraction
from Lib import ExtractWords
import os
current_path = os.getcwd()

def check_reliable_dataset(dataset={}):
    state = 0
    while True:
        try:
            if state == 0:  # initial state
                print('step', state)
                dict={}
                words_array=[]
                all_words=[]
                state = 10
            # haven't add weight of summary
            elif state == 10:  # import datasets
                print('step', state)
                #dict[str(ID)] = [productID, helpness, score, summary, description]
                for k,v in dataset.items():
                    if float(v[2]) == 5:  # users satisfy products
                        x, y = v[1].split("/")
                        if float(x) > 3 and float(x)/float(y) > 0.8: # dataset is reliable
                            words_array = ExtractWords.extract_useful_words(v[4])
                            useful_words = ' '.join(words_array)
                            print('ID: ', k, 'has useful words:', useful_words)
                            dict[k] = (useful_words, 'pos') # extract useful commend
                            for w in words_array:
                                all_words.append(w)
                        else:    # dataset isn't reliable
                            pass

                    elif float(v[2]) < 3: # users don't satisfy products
                        x, y = v[1].split("/")
                        if float(x) > 3 and float(x)/float(y) > 0.8: # dataset is reliable
                            words_array = ExtractWords.extract_useful_words(v[4])
                            useful_words = ' '.join(words_array)
                            print('ID: ', k, 'has useful words:', useful_words)
                            dict[k] = (useful_words, 'neg') # extract useful commend
                            for w in words_array:
                                all_words.append(w)
                        else:  # dataset isn't reliable
                            pass
                    else:   # dataset isn't reliable
                        pass
                state = 20
            elif state == 20:
                print('step', state)
                for k, v in dict.items():
                    print('ID', k, 'has', v[1], 'meaning')
                state = 21

            else:
                print("End of program")
                state = 0
                return dict, all_words
                break


        except:
            print("Error occurred at extract useful dataset")
            break


def test():
    data_path = current_path + "/export.xls"
    print(data_path)
    file_content = FileInteraction.open_file(data_path)  # file path, length
    print("successfully import dataset")
    dict, all_words = check_reliable_dataset(file_content)
    print('length of useful datasent is ', len(dict), 'sets' )
    print('number of all_words is ', len(all_words), 'words')


if __name__ == "__main__":
    current_path = os.path.abspath(os.path.join(current_path, os.pardir))
    current_path = os.path.abspath(os.path.join(current_path, os.pardir))
    print(current_path)
    test()
else:
    print('This file is a model')