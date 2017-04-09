### Import models
import xlrd
import pickle
import os

### define functions

def import_pickle(pickle_path):
    pickle_in = open(pickle_path, "rb")
    data = pickle.load(pickle_in)
    pickle_in.close()
    return data

def export_pickle(pickle_path, data):
    pickle_out = open(pickle_path, "wb")
    pickle.dump(data, pickle_out)
    pickle_out.close()

def import_file(path):
    file_in = open(path, "r", encoding='utf-8')
    data = file_in.read()
    file_in.close()
    return data
def export_file(path, content):
    file_out = open(path, "w", encoding='utf-8')
    file_out.write(content)
    file_out.close()

def open_file(file_location='../export.xls',length=-1):
    dict = {}
    workbook = xlrd.open_workbook(file_location)
    sheet = workbook.sheet_by_index(0)  # extract the first sheet
    if not isinstance(length, int):
        length = -999
    if length == -1:
        rows = sheet.nrows-1
    elif length > 0:
        rows = length
    else:
        rows = 0
    for ID in range(rows):
        productID = sheet.cell_value(ID+1,1)    # row, col
        helpness = sheet.cell_value(ID+1, 6)    # row, col
        score = sheet.cell_value(ID+1, 7)       # row, col
        summary = sheet.cell_value(ID+1, 9)     # row, col
        description = sheet.cell_value(ID+1, 10)    # row, col
        dict[str(ID)] = [productID, helpness, score, summary, description]
    return dict

def main():
    data_path = "../../export.xls"
    dict = open_file(data_path)
    print(dict['5993'][4])

current_path = os.getcwd()
if __name__ == "__main__":
    main()
else:
    print('using ImportFile module at ', current_path)