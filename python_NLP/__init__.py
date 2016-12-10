### Import models
from Lib import ImportFile
from Lib import ExtractWords
from Lib import AnalyseWords

import nltk
### define functions


def main():
    state = 0

    while True:
        try:
            if state == 0:      # initial state
                dict = {}
                input_words = []
                ID = 0
                data_path = "../export.xls"
                pickle_path= "../export.pickle"
                test_ID = '20'
                state = 20

            elif state == 10:    # import datasets
                file_content = ImportFile.open_file(data_path)  # file path, length
                print("successfully import dataset")
                state = 11

            elif state == 11:
                for _ in file_content:
                    dict[str(ID)] = ExtractWords.extract_useful_words(file_content[str(ID)][4])  # extract description
                    ID += 1
                state = 12
            elif state == 12:   # export refined dataset
                ImportFile.export_pickle(pickle_path, dict)
                state = 30

            elif state == 20:   # import pickled dataset
                dict = ImportFile.import_pickle(pickle_path)
                state = 30

            elif state == 30:     # analysing dataset
                # for i in range(len(dict)):
                #     input_words += dict[str(i)]
                # analysed_words = AnalyseWords.analysing_words(set(input_words))
                analysed_words = AnalyseWords.analysing_words(dict[test_ID])
                print(analysed_words)
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



if __name__ == "__main__":
    main()
else:
    print('This file is a model')