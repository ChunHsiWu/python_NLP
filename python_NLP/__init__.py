### Import models
from Lib import ImportFile

from Lib import ExtractWords

import nltk
### define functions


def main():
    state = 0

    while True:
        try:
            if state == 0:      # initial state
                dict = {}
                ID = 0
                data_path = "../export.xls"
                state = 1

            elif state == 1:    # import datasets
                file_content = ImportFile.open_file(data_path, 10)  # file path, length
                state = 2

            elif state == 2:
                for _ in file_content:
                    dict[str(ID)] = ExtractWords.extract_useful_words(file_content[str(ID)][4])  # extract description
                    ID += 1
                state = 3

            elif state == 3:     # analysing dataset

                print(dict['0'])
                analysed_words = ExtractWords.analysing_words(dict['0'])
                print(analysed_words)
                state = 5

            elif state == 4:    # print out results
                print(file_content['0'][4])
                print(dict['0'])

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