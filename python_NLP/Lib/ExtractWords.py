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

from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer, PunktSentenceTokenizer
from nltk.tag import pos_tag
from nltk.corpus import stopwords
import os
from Lib import FileInteraction
from nltk.tag import StanfordPOSTagger, StanfordNERTagger
from nltk.stem import WordNetLemmatizer
#from autocorrect import spell
from nltk.stem import PorterStemmer
### Initial setting
stop_words = set(stopwords.words("english"))  # build the stopword list
current_path = os.getcwd()
# stop_words = list(word_tokenize(FileInteraction.import_file(current_path+'/Doc/stopwords_en.txt')))  # build the stopword list

### define functions
def spellingcorrector(words):
    suggestions = []
    for w in words:
        suggestions.append(spell(w))
    return suggestions
def os_time():
    return os.times()[4]



def lemmatizing_words(words):
    lema_words=[]
    lemmatizer = WordNetLemmatizer()
    for w in words:
        lema_words.append(lemmatizer.lemmatize(w))
    return lema_words



def stemming_words(words):
    stem_words = []
    ps = PorterStemmer()
    for w in words:
        stem_words.append(ps.stem(w))
    return stem_words
'''
Categorize words
eg.
[('PRESIDENT', 'NNP'), ('GEORGE', 'NNP'), ('W.', 'NNP'), ('BUSH', 'NNP')]
'''
def categorize_words(words):
    # jar_path = '/usr/local/share/nltk_data/stanford-postagger/stanford-postagger-3.6.0.jar'
    # tag_path = '/usr/local/share/nltk_data/stanford-postagger/models/english-bidirectional-distsim.tagger'
    # st = StanfordPOSTagger(tag_path, jar_path, encoding='utf-8')
    # POS_words = st.tag(words)
    POS_words = pos_tag(words)
    return POS_words

#  j is adject, r is adverb, and v is verb
def categorized_words_filter(words):
    filter_words = []
    allowed_word_types = ["JJ", "JJR", "JJS", "RB", "RBR", "RBS", "VB", "VBP", "VBD", "VBG", "VBN", "VBZ"]
    for w in words:
        if w[1] in allowed_word_types:
            filter_words.append(w[0].lower())

    return filter_words

'''
take off punctuation from words
eg.
    '%', '&', '@', '#', '$'
'''
def takeoff_punctuation(words):
    # pun_filter = RegexpTokenizer(r'[\'\w\-]+|[A-Z]{2,}(?![a-z])|[^a-z]')
    pun_filter = RegexpTokenizer(r'\w+\-\w+|\w+\'\w|[A-Z]{2,}(?![a-z])|[a-zA-Z]\w+')
    # \w+ all word character
    # \w+\-\w+, \w+\'\w words which may contain ' and -
    # [A-Z]{2,}(?![a-z]) words with all letters capital
    # [a-z] only for small letter words
    # [a-zA-Z]\w+ all words except single letter word
    # \w+\-\w+|[a-z]\w+\'\w|[A-Z]{2,}(?![a-z])|\b[a-z]\w+

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
# '''
# Take off un-useful categorized words
# eg.
#     'NNP', 'PRP'
# '''
# def chunking_words(words):
#     try:
#         tagged = nltk.pos_tag(words)
#         chunkGram = r"""Chunk: {<RB.?>*<VB.?>*<NNP>+<NN>?}""" # chunking all types of adv, V, prop N and N
#         chunkParser = nltk.RegexpParser(chunkGram)
#         chunked = chunkParser.parse(tagged)
#         # chunked.draw()
#         print(chunked)
#     except TypeError:
#         print("input type should be lists")
#     except Exception as e:
#         print(str(e))

def extract_useful_words(words):
    state = 0
    while True:
        try:
            if state == 0:
                input_words = words # lower case for all words
                processd_words = []
                # process_time0 = os_time()
                state = 1

            elif state == 1:
                processd_words = takeoff_punctuation(input_words)
                input_words = processd_words
                state = 2

            elif state == 2:
                processd_words = takeoff_stopwords(input_words, stop_words)
                input_words = processd_words
                state = 61

            # correct spelling
            # currently not in the pipeline cuz it takes too much time
            elif state == 50:
                processd_words = spellingcorrector(input_words)
                input_words = processd_words
                state = 61
            # stemming words
            # currently not in the pipeline cuz it's inappropriate
            # we can try but not sure!!
            elif state == 60:
                processd_words = stemming_words(input_words)
                input_words = processd_words
                # print(lemmatizer.lemmatize("better", pos="a"))
                state = 69
            # lemmatize using to find synonym
            elif state == 61:
                processd_words = lemmatizing_words(input_words)
                input_words = processd_words
                # print(lemmatizer.lemmatize("better", pos="a"))
                state = 70
            # words filter
            elif state == 70:
                categorized_words = categorize_words(input_words)
                state = 71
            elif state == 71:
                processd_words = categorized_words_filter(categorized_words)
                input_words = processd_words
                state = 79

            # currently we dont use chunking cuz it takes time
            # # chunking algorithm
            # elif state == 90:
            #     analysed_words = chunking_words(words)  # chunk same POS together
            #     state = 99

            else:    #  End process
                # # print("Extracting useful words...")
                # process_time1 = os_time()
                # print('total process time: ', process_time1 - process_time0)
                return processd_words
                break

        except:
            print("Unexpect error occured while extracting useful words...")
            break


def main():
    # example_sentence =" hey mate, how's everything going? it's a freakin hot weather today, isnt it?"
    # useful_words = extract_useful_words(example_sentence)
    # print(useful_words)
    pass



def initial():
    stop_words.remove("but")  # "but" should be still important
    # pass
if __name__ == "__main__":
    current_path = os.path.abspath(os.path.join(current_path, os.pardir))
    print(current_path)
    main()
else:
    initial()
    print('using ExtractWords module at ', current_path)

