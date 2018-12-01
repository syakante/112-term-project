#autocomplete.py
#### helpers ####
"""
helper functions sourced from online
"""
#TODO: why the heck apostrophes break code

import re

def norm_rsplit(text,n):
    #rsplit is basically a more refined .split()
    return text.lower().rsplit(' ', n)[-n:]

#http://norvig.com/spell-correct.html
def re_split(text):
    return re.findall('[a-z]+', text.lower())

#http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
#https://github.com/rrenaud/Gibberish-Detector/blob/master/gib_detect_train.py#L16
def chunks(L, n):
    #generates sub-lists from L of length n
    #e.g. chunks([0,1,2,3],2) yields [0,1] [1,2] [2,3]
    for i in range(0, len(L) - n + 1):
        yield L[i:i+n]

## sample text for testing purposes

#readFile from 112 website
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

test = readFile("sampleText.txt")

#### autocomplete ####

from collections import Counter
#collections is a module that comes with python, like random or math.
#specifically using the Counter function, which creates a dictionary where the key's value is its number of occurences.

words = []

wordsTuples = []

wordsModel = {}

wordsTuplesModel = {}

def trainer(text):
    """howitworks
    0.Input string text.
    1. split that string into a list of words. 
    2. Chunk that list of words into a list of 2-elem lists.
    3. create a dictionary, where key = first elem and value = Counter([second elems])
    This creates our Markov Chain dictionary of unique words:words that occur after it
    """

    # step 0
    global words
    words = re_split(text)

    global wordsModel
    wordsModel = Counter(words)
    #wordsModel is a dictionary of word:its occurences, so we can easily find Probability(any one word).
    
    global wordsTuples
    wordsTuples = list(chunks(words, 2))
    #wordsTuples is a list of consecutive word combinations as tuples.
    # e.g. "The quick brown fox" --> [(The,quick),(quick,brown),(brown,fox)]

    #using wordTuples, we can find out the most probable following word given a first word.
    #i.e. conditional probability.
    #P(A and B) = P(A|B) * P(A)

    global wordsTuplesModel
    wordsTuplesModel = {first:Counter()
                         for first, second in wordsTuples}

    for tup in wordsTuples:
        try:
            wordsTuplesModel[tup[0]].update([tup[1]])
        except:
            # hack-y fix for uneven # of elements in wordsTuples
            pass

#temporary
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


def thisWord(word, top_n=10):
    """given an incomplete word, return top n suggestions based off
    frequency of words prefixed by said input word"""
    try:
        return [(k, v) for k, v in wordsModel.most_common()
                if k.startswith(word)][:top_n]
    except:
        raise Exception("code machine broke")


def thisWordGivenLast(firstWord, nextWord, top_n=10):
    """given a word, return top n suggestions determined by the frequency of
    words prefixed by the input GIVEN the occurence of the last word"""

    #Hidden step
    possible_nextWords = [nextWord[:-1]+char
                             for char in NEARBY_KEYS[nextWord[-1]]
                             if len(nextWord) > 2]

    possible_nextWords.append(nextWord)

    probable_words = {w:c for w, c in
                      wordsTuplesModel[firstWord.lower()].items()
                      for sec_word in possible_nextWords
                      if w.startswith(sec_word)}

    return Counter(probable_words).most_common(top_n)



def predict(firstWord, nextWord, top_n=10):
    """given the last word and the current word to complete, we call
    thisWord or thisWordGivenLast to retrive most n
    probable suggestions.
    """

    try:
        if firstWord and nextWord:
            return thisWordGivenLast(firstWord,
                                                   nextWord,
                                                   top_n=top_n)
        else:
            return thisWord(firstWord, top_n)
    except KeyError:
        raise Exception("code machine broke")
                        

import random
def chainDemo(n):
    #just a test function to show it chains. n is the length of your "sentence"
    #step 0: run trainer(test)
    #step 1: start with most probable word overall
    start = random.choice(list(words))
    #TODO: random.choice from words that start sentences, not just words.
    result = start.capitalize()
    while len(result.split(" ")) < n:
        nextChoice = nextWordList(start)
        next = random.choice(nextChoice)
        start = next
        result += " " + next
    return result

def nextWordList(word):
    #converts the value of a word from wordsTuplesModel into a list where the word occurs the number of times 
    L = []
    occur = wordsTuplesModel[word]
    for key in occur:
        times = occur[key]
        for i in range(times):
            L.append(key)
    return L
