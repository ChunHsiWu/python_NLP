### Import models
from Lib import FileInteraction
from Lib import ExtractWords
from Lib import AnalyseWords
from nltk.tokenize import word_tokenize
#from Lib.Classifier import VoteClassifier  <- keep observe

### define functions

#### ==== Optimize list ====
# replace import nltk to certain modules only <- increase loading speed, memory use
# optimization of features
# add more documents
# classifier change (ML)
# stemming and lemmatizing
# textBlob ?? (spell correction)

### note
# Polarity analysis takes into account the amount of positive or negative terms that appear in a given sentence. (not enough for us)
# subjectivity
# opinion mining



def main():
    state = 0

    while True:
        try:
            if state == 0:      # initial state
                dict = {}
                input_words = []
                ID = 0
                data_path = "../export.xls"
                pickle_path = "../filtered_export.pickle"
                test_ID = '0'
                state = 1
            elif state == 1:    # user input
                user_input = input("Import dataset(Y/N)?")
                if (user_input=='Y') or (user_input == 'y'):
                    state = 13
                elif (user_input=='N') or (user_input == 'n'):
                    state = 10
                else:
                    print('Error input')
                    state = 1

            elif state == 10:    # import datasets
                file_content = FileInteraction.open_file(data_path)  # file path, length
                print("successfully import raw dataset")
                state = 11

            elif state == 11:
                for _ in file_content:
                    # extract data from description part
                    #dict[str(ID)] = ExtractWords.extract_useful_words(file_content[str(ID)][4])
                    dict[str(ID)] = word_tokenize(file_content[str(ID)][4])
                    ID += 1
                state = 12
            elif state == 12:   # export refined dataset
                FileInteraction.export_pickle(pickle_path, dict)
                user_input = input("Start doing sentiment analysis (Y/N)?")
                if (user_input=='Y') or (user_input == 'y'):
                    state = 13
                elif (user_input=='N') or (user_input == 'n'):
                    state = 19
                else:
                    print('Error input, end of program')
                    state = 19

            elif state == 13:   # import pickled dataset
                dict = FileInteraction.import_pickle(pickle_path)
                state = 30

            elif state == 30:     # sentiment analysis
                # for i in range(len(dict)):
                #     input_words += dict[str(i)]
                # analysed_words = AnalyseWords.analysing_words(set(input_words))


                # test_content = FileInteraction.open_file(data_path)  # file path, length
                # print(test_content[str(ID)][4])Combination_Classifier
                # analysed_words = AnalyseWords.analysing_words(test_content[test_ID][4])
                print(dict[test_ID])
                for i in range(12):
                    analysed_words = AnalyseWords.analysing_words(dict[test_ID],0, i+1)
                # print(analysed_words)
                state = 40

            elif state == 40:    # print out results
                print(dict[test_ID])
                state = 50

            else:
                print("End of program")
                state = 0
                break


        except:
            print("Error occurred")
            break

global current_path
if __name__ == "__main__":
    main()
else:
    print('This file is a model')