#autocomplete.py

test = "Solomon is a pedestrian. Everything is close enough in Sugar Land, simple, Texas-big, benign and plodding, so he walks everywhere without rush. He does not jaywalk, he does not go on red lights, and he is a law-abiding citizen who waits his turn at the crosswalks. He waits on a Thursday afternoon at the intersection next to his school. The sun is out, but the air is cool and restless. Solomon remembers reading somewhere about fronts and El Niño, an explanation for southern weather oddities. He closes his eyes and feels the bright cold air nipping at his nose. When he opens his eyes he sees Ji next to him. Ji, the girl in his grade that he always observes from a distance, as if any move he makes will send her fluttering from him like papers caught by wind. Ji bikes to and from school, and today is no exception to the rule. She stands on her bike, poised for the light to change with one foot pressing on the pedal. She has tall, athletic legs, and Solomon takes a moment to admire them before it occurs to him to have conversation. Solomon has set guidelines for dialogue. Interaction is better than no interaction. The driest conversation is better than awkward silence. Don't be afraid to initiate. Don't talk about yourself. Don't insult or offend, subtly or explicitly or otherwise. They talk briefly. CompSci. Club activities. SAT. She doesn't speak loud enough and her voice gets covered by the roar of passing cars. He's a little tired from waking up early to finish Physics. And neither of them are good conversationalists. It doesn't take long for the conversation to die into silence. Waiting for the cross light to change, tell them to go. He wonders when they will cross the invisible threshold where he can share whatever he thinks, about everything and nothing like how the cold front air prickles over his arms, leaving him wishing he wore a hoodie, how his impending job interview plants a lump in his throat, or maybe that’s just Ji, tasting stillborn words and sorry about being awkward I just wish I wasn't thinking about everything and nothing, the school's reel through the electronic sign and the fringe of Ji’s blue shorts and how they match the sky like she had planned it. Solomon sets guidelines for himself. But in the end, I wish I knew what to say"

from collections import Counter
'''
def load():
    """load the classic Norvig big.txt corpus"""
    print("training!")

    load_models()

    print("done training!")

    return True
'''
#### helpers.py ####
"""
helpers.py
This file contains a collection of useful and concise functions gathered
from across the Web"""

import re

def norm_rsplit(text,n):
    return text.lower().rsplit(' ', n)[-n:]

#http://norvig.com/spell-correct.html
def re_split(text):
    return re.findall('[a-z]+', text.lower())

#http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
#https://github.com/rrenaud/Gibberish-Detector/blob/master/gib_detect_train.py#L16
def chunks(l, n):
    for i in range(0, len(l) - n + 1):
        yield l[i:i+n]

#### models.py ####
"""
AUTOCOMPLETE -
This file contains the process where we train our predictive models, Also
helpful are the load_models and save_models functions.
"""

import os

import collections

#import pickle

WORDS = []

WORD_TUPLES = []

WORDS_MODEL = {}

WORD_TUPLES_MODEL = {}

#This step is where we transform "raw" data
# into some sort of probabilistic model(s)
def train_models(corpus, model_name="models_compressed.pkl"):
    """Takes in a preferably long string (corpus/training data),
    split that string into a list, we \"chunkify\" resulting in
    a list of 2-elem list. Finally we create a dictionary,
    where each key = first elem and each value = Counter([second elems])
    Will save/pickle model by default ('models_compressed.pkl').
    Set second argument to false if you wish to not save the models.
    """

    # "preperation" step
    # word is in WORDS
    global WORDS
    WORDS = re_split(corpus)

    # first model -> P(word)
    global WORDS_MODEL
    WORDS_MODEL = collections.Counter(WORDS)

    # another preperation step
    # wordA, wordB are in WORDS
    global WORD_TUPLES
    WORD_TUPLES = list(chunks(WORDS, 2))

    # second model -> P(wordA|wordB)
    global WORD_TUPLES_MODEL
    WORD_TUPLES_MODEL = {first:collections.Counter()
                         for first, second in WORD_TUPLES}

    for tup in WORD_TUPLES:
        try:
            WORD_TUPLES_MODEL[tup[0]].update([tup[1]])
        except:
            # hack-y fix for uneven # of elements in WORD_TUPLES
            pass

    '''if model_name:
        save_models(os.path.join(os.path.dirname(__file__), model_name))
    '''

'''
def save_models(path=None):
    """Save models to 'path'. If 'path' not specified,
    save to module's folder under name 'models_compressed.pkl'"""

    if path == None:
        path = os.path.join(os.path.dirname(__file__), 'models_compressed.pkl')

    print("saving to:", path)
    #save for next use. pickle format: (key=model name, value=model)
    pickle.dump({'words_model': WORDS_MODEL,
                 'word_tuples_model': WORD_TUPLES_MODEL},
                open(path, 'wb'),
                protocol=2)


def load_models(load_path=None):
    """Load autocomplete's built-in model (uses Norvig's big.txt). Optionally
    provide the path to Python pickle object."""

    if load_path is None:
        load_path = os.path.join(os.path.dirname(__file__),
                                 'models_compressed.pkl')
    try:
        models = pickle.load(open(load_path,'rb'))

        global WORDS_MODEL
        WORDS_MODEL = models['words_model']

        global WORD_TUPLES_MODEL
        WORD_TUPLES_MODEL = models['word_tuples_model']

        print("successfully loaded: models_compressed.pkl")
    except IOError:
        print("Error in opening pickle object. Training on default corpus text.")
        train_bigtxt()
    except KeyError:
        print("Error in loading both predictve models.\
              Training on default corpus text.")
        train_bigtxt()
    except ValueError:
        print("Corrupted pickle string.\
              Training on default corpus text (big.txt)")
        train_bigtxt()
'''
#the so called "Hidden" step, thus allowing this module to be
#a "Hidden Markov Model"... Whatever that means...
NEARBY_KEYS = {
    'a': 'qwsz',
    'b': 'vghn',
    'c': 'xdfv',
    'd': 'erfcxs',
    'e': 'rdsw',
    'f': 'rtgvcd',
    'g': 'tyhbvf',
    'h': 'yujnbg',
    'j': 'uikmnh',
    'k': 'iolmj',
    'l': 'opk',
    'm': 'njk',
    'n': 'bhjm',
    'o': 'iklp',
    'p': 'ol',
    'q': 'wa',
    'r': 'edft',
    's': 'wedxza',
    't': 'rfgy',
    'u': 'yhji',
    'v': 'cfgb',
    'w': 'qase',
    'x': 'zsdc',
    'y': 'tghu',
    'z': 'asx'
    }


def this_word(word, top_n=10):
    """given an incomplete word, return top n suggestions based off
    frequency of words prefixed by said input word"""
    try:
        return [(k, v) for k, v in WORDS_MODEL.most_common()
                if k.startswith(word)][:top_n]
    except:
        raise Exception("Please load predictive models. Run:\
                        \n\tautocomplete.load()")


predict_currword = this_word


def this_word_given_last(first_word, second_word, top_n=10):
    """given a word, return top n suggestions determined by the frequency of
    words prefixed by the input GIVEN the occurence of the last word"""

    #Hidden step
    possible_second_words = [second_word[:-1]+char
                             for char in NEARBY_KEYS[second_word[-1]]
                             if len(second_word) > 2]

    possible_second_words.append(second_word)

    probable_words = {w:c for w, c in
                      WORD_TUPLES_MODEL[first_word.lower()].items()
                      for sec_word in possible_second_words
                      if w.startswith(sec_word)}

    return Counter(probable_words).most_common(top_n)


predict_currword_given_lastword = this_word_given_last


def predict(first_word, second_word, top_n=10):
    """given the last word and the current word to complete, we call
    predict_currword or predict_currword_given_lastword to retrive most n
    probable suggestions.
    """

    try:
        if first_word and second_word:
            return predict_currword_given_lastword(first_word,
                                                   second_word,
                                                   top_n=top_n)
        else:
            return predict_currword(first_word, top_n)
    except KeyError:
        raise Exception("Please load predictive models. Run:\
                        \n\tautocomplete.load()")


def split_predict(text, top_n=10):
    """takes in string and will right split accordingly.
    Optionally, you can provide keyword argument "top_n" for
    choosing the number of suggestions to return (default is 10)"""
    text = norm_rsplit(text, 2)
    return predict(*text, top_n=top_n)
