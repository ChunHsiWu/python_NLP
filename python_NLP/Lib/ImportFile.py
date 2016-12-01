### Import models
import xlrd

### define functions

def open_file(file_location):
    dict = {}

    workbook = xlrd.open_workbook(file_location)
    sheet = workbook.sheet_by_index(0)  # extract the first sheet

    # for ID in range(sheet.nrows-1):
    for ID in range(20 - 1):
        productID = sheet.cell_value(ID+1,1).lower()    # row, col
        helpness = sheet.cell_value(ID+1, 6).lower()    # row, col
        score = sheet.cell_value(ID+1, 7).lower()    # row, col
        summary = sheet.cell_value(ID+1, 9).lower()    # row, col
        description = sheet.cell_value(ID+1, 10).lower()    # row, col
        dict[str(ID)] = [productID, helpness, score, summary, description]
    return dict

def main():
    pass

if __name__ == "__main__":
    main()
else:
    print('using ImportFile module')