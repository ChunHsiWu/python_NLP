### Import models
import ImportFile

### define functions


def main():
    data_path = "../export.xls"
    content = ImportFile.open_file(data_path)

    print(content['19'])

if __name__ == "__main__":
    main()
else:
    print('This file is model')