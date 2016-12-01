'''
Regular Expression Symbols
Symbol	Function
\b	    Word boundary (zero width)
\d	    Any decimal digit (equivalent to [0-9])
\D	    Any non-digit character (equivalent to [^0-9])
\s	    Any whitespace character (equivalent to [ \t\n\r\f\v])
\S	    Any non-whitespace character (equivalent to [^ \t\n\r\f\v])
\w	    Any alphanumeric character (equivalent to [a-zA-Z0-9_])
\W	    Any non-alphanumeric character (equivalent to [^a-zA-Z0-9_])
\t	    The tab character
\n	    The newline character

Regular expression operators
Operator	Effect
.	        Matches any single character.
?	        The preceding item is optional and will be matched, at most, once.
*	        The preceding item will be matched zero or more times.
+	        The preceding item will be matched one or more times.
{N}	        The preceding item is matched exactly N times.
{N,}        The preceding item is matched N or more times.
{N,M}	    The preceding item is matched at least N times, but not more than M times.
-	        represents the range if it's not first or last in a list or the ending point of a range in a list.
^	        Matches the empty string at the beginning of a line; also represents the characters not in the range of a list.
$	        Matches the empty string at the end of a line.
\b	        Matches the empty string at the edge of a word.
\B	        Matches the empty string provided it's not at the edge of a word.
\<	        Match the empty string at the beginning of word.
\>	        Match the empty string at the end of word.

'''

### Import models
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords

### define functions

def takeoff_punctuation(words):
    pun_filter = RegexpTokenizer(r'\w+')
    pure_words = pun_filter.tokenize(words)  # take off all the punctuation in the sentences
    return pure_words

def takeoff_stopwords(words, stop_words):

    filter_words = [w for w in words if w not in stop_words]  # take off un-meaningful words
    return filter_words

def extract_useful_words(words):
    state = 0
    pure_words = []
    filter_words = []

    stop_words = set(stopwords.words("english"))  # build the stopword list
    ###
    stop_words.remove("but")  # "but" should be still important
    ###
    while True:
        try:
            if state == 0:
                pure_words += takeoff_punctuation(words)
            elif state == 1:
                filter_words += takeoff_stopwords(pure_words, stop_words)
            else:    #  End process
                # print("Extracting useful words...")
                return filter_words
                break
            state += 1
        except:
            print("Unexpect error occured while extracting useful words...")
            break

def main():

    example_sentence =" hey mate, how's everything going? it's a freakin hot weather today, isnt it?"
    useful_words = extract_useful_words(example_sentence)
    print(useful_words)

if __name__ == "__main__":
    main()
else:
    print('using ExtractWords module')