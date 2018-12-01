#### analyzeText.py ####
#this python file contains all the not-really-computational-linguistics garbage for annotating a given essay prompt.

import csv
from collections import Counter

articles = {"the","a"}

conjunctions = {"for","and", "nor", "but", "or", "yet", "so"}

questionWords = {"who", "what", "when", "where", "why", "how"}

#to be continued but w/e
punct = {",",".","?","!",";",":"}

with open('wordlist.csv',newline="") as CSVfile:
    file = list(csv.reader(CSVfile, delimiter=','))
    prepositions = set(file[0])
    #prepositions = set(list(csv.reader(CSVfile, delimiter=','))[0]) #imports a set(list) of prepositions from a .csv file (MS Excel)
    essayVerbs = set(file[1]) #again, but with essay verbs
    ingVerbs = set()
    for infinitiveVerb in essayVerbs:
        if infinitiveVerb.endswith("e"):
            ingVerbs.add(infinitiveVerb[:len(infinitiveVerb)-1]+"ing")
        else:
            ingVerbs.add(infinitiveVerb+"ing")
    essayVerbs = essayVerbs | ingVerbs
    commonWords = set(file[2])

## example prompts just for testing with ##
ex1 = "Evaluate the relative importance of different causes for the expanding role of the United States in the world in the period from 1865 to 1910."

ex2 = "For the period before 1750, analyze the ways in which Britain's policy of salutary neglect influenced the development of American society."

ex3 = "Write a well-developed essay analyzing the complex nature of the gift and how the gift contributes to the meaning of the work as a whole."

ex4 = "The lessons we take from obstacles we encounter can be fundamental to later success. Recount a time when you faced a challenge, setback, or failure. How did it affect you, and what did you learn from the experience?"


#### short ####

def divideToSentences(prompt):
    #This helper function converts a string input into a list of list of words, where each upper-level list item is a sentence or sentence equivalent.
    #e.g. "The quick brown fox jumps over the lazy dog. Also, I recently developed anxiety." becomes [["The","quick",...],["Also,","I","recently",...]]
    sentences = prompt.replace(";",".").split(".") #since ; phrases are independent, for our purposes it'll be treated as such. 
    #because of .split, the very last sentence won't have a period at the end, but since it's the last sentence we can safely assume that there's supposed to be a period.
    result = []
    for sentenceString in sentences:
        sentenceString = sentenceString.strip() 
        sentenceString = list(sentenceString.split(" "))
        if sentenceString != [""]:
            result.append(sentenceString)
    return result

#The function(sentence) parameter for the following functions refers to a single sentence in the form of a list of words (which are strings).

def getPrepPhrases(sentence):
    #This helper function returns a list of lists of words that make up detected prepositional phrases.
    myPrepPhrases = []
    for i in range(len(sentence)):
        if sentence[i] in prepositions and sentence[i+1] not in articles:
            myPrepPhrases.append((sentence[i:i+2])) #because splicing is exclusive...
        elif sentence[i] in prepositions and sentence[i+1] in articles:
            myPrepPhrases.append(sentence[i:i+3])    
    return myPrepPhrases

def getEssayVerbs(sentence):
    #This helper function returns a set of detected common essay verbs.
    myEssayVerbs = set() #using set due to the nature of essay verbs as single words that are important regardless of repetition
    for word in sentence:
        if word.lower() in essayVerbs:
            myEssayVerbs.add(word)
    return myEssayVerbs

def getQuestions(sentence):
    #This helper function returns a list of lists of words that make up questions (note that a single sentence may ask more than one question).
    myQuestions = []
    '''Sometimes, question words are not used for questions. If one is being used to ask a question, it fulfills BOTH these criteria:
        - the end of the sentence it is in ends in a question mark
        - it is capitalized i.e. starts the sentence OR is preceded by a punctuation OR preceded by a conjunction.
        e.g. "John, who was in the kitchen, says no. Given where it happened, who did it, and how was it done?"
        Despite the use of "who" and "where", the only questions asked are "who did it" and "how was it done?"
    '''
    for i in range(len(sentence)):
        if sentence[i].lower() in questionWords:
            if sentence[len(sentence)-1].endswith("?") and (sentence[i] in [Q.title() for Q in questionWords] or any(sentence[i-1].endswith(x) for x in punct) or sentence[i-1] in conjunctions):
                #parse the rest of the sentence UNTIL it runs into a punctuation/conjunction, because that's where the question phrase ends.
                for j in range(i,len(sentence)): #i.e. the rest of the sentence
                    if sentence[j] not in conjunctions and not(any(sentence[j].endswith(x) for x in punct)):
                        #looking at a word that is NOT a conjunction and does NOT end in any punctuation, in which case it is part of the question.
                        pass
                    else:
                        myQuestions.append(sentence[i:j+1])
                        break
                
    return myQuestions

#TODO: find a way to detect proper nouns. Differentiate between capitalized first word of a sentence and proper nouns and multi-word proper nouns, e.g. United States

promptPrepPhrases = []
promptEssayVerbs = set()
promptQuestions = []

def analyzePrompt(prompt):
    global promptPrepPhrases
    global promptEssayVerbs
    global promptQuestions
    sentenceList = divideToSentences(prompt)
    for sentence in sentenceList:
        promptPrepPhrases.extend(getPrepPhrases(sentence))
        promptEssayVerbs = promptEssayVerbs | getEssayVerbs(sentence)
        promptQuestions.extend(getQuestions(sentence))
    return None

#### long ####

def getKeywordLarge(corpus):
    #given a big string, find important terms
    
    #Important terms are scored based on repetition
    #some words will be used but are not important, they will be blacklisted.
    #Such words include prepositions, articles, conjunctions, parts of speech kind of thing
    blacklist = prepositions | articles | conjunctions | commonWords | questionWords
    
    text = corpus.lower().split(" ")
    numWords = len(corpus)
    freq = Counter(x for x in text if x not in blacklist)

    minSize = min(10, len(freq))  # get first 10
    keywords = {x: y for x, y in freq.most_common(minSize)}  # recreate a dict

    for k in keywords:
        articleScore = keywords[k]*1.0 / numWords
        keywords[k] = articleScore * 1.5 + 1

    return keywords