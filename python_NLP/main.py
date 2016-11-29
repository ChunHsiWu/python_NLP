### Import models

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

### define functions


def main():
    example_sentence = "this is an example showing off stop word filteration"
    stop_words = set(stopwords.words("english"))    # get english stop words
    words = word_tokenize(example_sentence)
    print(stop_words)
    filtered_sentence = [w for w in words if w not in stop_words]

    print(filtered_sentence)


if __name__ == "__main__":
    main()
else:
    print('This file is model')