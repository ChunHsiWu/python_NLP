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

POS tag list:
Symbol	Function
CC	    coordinating conjunction
CD	    cardinal digit
DT	    determiner
EX  	existential there (like: "there is" ... think of it like "there exists")
FW  	foreign word
IN  	preposition/subordinating conjunction
JJ	    adjective	'big'
JJR 	adjective, comparative	'bigger'
JJS 	adjective, superlative	'biggest'
LS  	list marker	1)
MD  	modal	could, will
NN  	noun, singular 'desk'
NNS 	noun plural	'desks'
NNP 	proper noun, singular	'Harrison'
NNPS   	proper noun, plural	'Americans'
PDT 	predeterminer	'all the kids'
POS	    possessive ending	parent's
PRP 	personal pronoun	I, he, she
PRP$	possessive pronoun	my, his, hers
RB  	adverb	very, silently,
RBR 	adverb, comparative	better
RBS 	adverb, superlative	best
RP  	particle	give up
TO  	to	go 'to' the store.
UH  	interjection	errrrrrrrm
VB  	verb, base form	take
VBD 	verb, past tense	took
VBG 	verb, gerund/present participle	taking
VBN 	verb, past participle	taken
VBP 	verb, sing. present, non-3d	take
VBZ 	verb, 3rd person sing. present	takes
WDT 	wh-determiner	which
WP  	wh-pronoun	who, what
WP$ 	possessive wh-pronoun	whose
WRB 	wh-abverb	where, when
'''


### Import models
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer, PunktSentenceTokenizer
from nltk.corpus import stopwords


### Initial setting
stop_words = stop_words = set(stopwords.words("english"))  # build the stopword list

### define functions

'''
take off punctuation from words
eg.
    '%', '&', '@', '#', '$'
'''
def takeoff_punctuation(words):
    pun_filter = RegexpTokenizer(r'\w+')
    pure_words = pun_filter.tokenize(words)  # take off all the punctuation in the sentences
    return pure_words

'''
take off unmeaningful words
eg.
    the, it, I, and
'''
def takeoff_stopwords(words, stop_words):
    filter_words = [w for w in words if w not in stop_words]  # take off un-meaningful words
    return filter_words

'''
Categorize words
eg.
[('PRESIDENT', 'NNP'), ('GEORGE', 'NNP'), ('W.', 'NNP'), ('BUSH', 'NNP')]
'''
def categorize_words(words):
    POS_words = nltk.pos_tag(words)
    return POS_words

'''
Take off un-useful categorized words
eg.
    'NNP', 'PRP'
'''
def takeoff_unuseful_categorized_words(words):
    unused_words = ['PRP', 'NNP']
    filter_words = [w for w in words if w[1] not in unused_words]
    return filter_words

def chunking_words(words):
    try:
        tagged = nltk.pos_tag(words)
        chunkGram = r"""Chunk: {<RB.?>*<VB.?>*<NNP>+<NN>?}""" # chunking all types of adv, V, prop N and N
        chunkParser = nltk.RegexpParser(chunkGram)
        chunked = chunkParser.parse(tagged)
        # chunked.draw()
        print(chunked)
    except TypeError:
        print("input type should be lists")
    except Exception as e:
        print(str(e))

def analysing_words(words):
    state = 0
    while True:
        try:
            if state == 0:
                categorized_words = []
                analysed_words = []
                state = 1

            elif state == 1:
                state = 70

            elif state == 2:
                pass
            elif state == 70:
                categorized_words = categorize_words(words)
                state=71
            elif state == 71:
                analysed_words = takeoff_unuseful_categorized_words(categorized_words)
                state = 79

            # lemmatize using to find synonym
            elif state == 80:
                from nltk.stem import WordNetLemmatizer
                lemmatizer = WordNetLemmatizer()
                print(lemmatizer.lemmatize("better", pos="a"))
                state = 89

            # chunking algorithm
            elif state == 90:
                analysed_words = chunking_words(words)  # chunk same POS together
                state = 99

            else:  # End process
                # print("Extracting useful words...")
                return analysed_words
                break

        except:
            print("Unexpect error occured while analysing words...")
            break


def extract_useful_words(words):
    state = 0
    while True:
        try:
            if state == 0:
                process_words = []
                state = 1

            elif state == 1:
                process_words = takeoff_punctuation(words)
                state = 2

            elif state == 2:
                process_words = takeoff_stopwords(process_words, stop_words)
                state = 9
            else:    #  End process
                # print("Extracting useful words...")
                return process_words
                break

        except:
            print("Unexpect error occured while extracting useful words...")
            break




def main():
    example_sentence =" hey mate, how's everything going? it's a freakin hot weather today, isnt it?"
    # useful_words = extract_useful_words(example_sentence)
    # print(useful_words)

    tokenized = sent_tokenize(example_sentence)

    chunking_words(tokenized)

def initial():
    stop_words.remove("but")  # "but" should be still important

if __name__ == "__main__":
    main()
else:
    initial()
    print('using ExtractWords module')

