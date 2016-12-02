### Import models
import xlrd

### define functions

def open_file(file_location, length = -1):
    dict = {}

    workbook = xlrd.open_workbook(file_location)
    sheet = workbook.sheet_by_index(0)  # extract the first sheet
    if not isinstance(length, int):
        length = -999
    if length == -1:
        rows = sheet.nrows
    elif length > 0:
        rows = length
    else:
        rows = 0
        print('Error length input')

    for ID in range(rows):
        productID = sheet.cell_value(ID+1,1)    # row, col
        helpness = sheet.cell_value(ID+1, 6)    # row, col
        score = sheet.cell_value(ID+1, 7)       # row, col
        summary = sheet.cell_value(ID+1, 9)     # row, col
        description = sheet.cell_value(ID+1, 10)    # row, col
        dict[str(ID)] = [productID, helpness, score, summary, description]
    return dict

def main():
    pass

if __name__ == "__main__":
    main()
else:
    print('using ImportFile module')