### Import models
from Lib import ImportFile

from Lib import ExtractWords


### define functions


def main():
    state = 0

    while True:
        try:
            if state == 0:      # initial state
                dict = {}
                ID = 0
                data_path = "../export.xls"

            elif state == 1:    # import datasets
                file_content = ImportFile.open_file(data_path)

            elif state == 2:    # analysing dataset
                for _ in file_content:
                    dict[str(ID)] = ExtractWords.extract_useful_words(file_content[str(ID)][4])  # extract description
                    ID += 1

            elif state == 3:    # print out results
                print(file_content['1'][4])
                print(dict['1'])

            else:
                print("End of program")
                state = 0
                break

            state += 1
        except:
            print("Error occurred")
            break



if __name__ == "__main__":
    main()
else:
    print('This file is a model')