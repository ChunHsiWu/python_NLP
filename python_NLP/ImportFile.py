### Import models
import xlrd

### define functions

def open_file(file_location):
    dict = {}


    workbook = xlrd.open_workbook(file_location)
    sheet = workbook.sheet_by_index(0)  # extract the first sheet
    for ID in range(sheet.nrows-1):
        productID = sheet.cell_value(ID+1,1)    # row, col
        helpness = sheet.cell_value(ID+1, 6)    # row, col
        score = sheet.cell_value(ID+1, 7)    # row, col
        summary = sheet.cell_value(ID+1, 9)    # row, col
        description = sheet.cell_value(ID+1, 10)    # row, col
        dict[str(ID)] = [productID, helpness, score, summary, description]
    return dict
