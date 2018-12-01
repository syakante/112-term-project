#### wiki.py ####
#this python file manages the wikipedia API: taking an input, finding a usable wiki page, then taking the relevant text from that page.

import wikipedia

def getWiki(topic):
    #get wikipedia article text with API. Return as a string.
    relevant = wikipedia.search(topic)[0]
    article = wikipedia.page(relevant)
    #article is an object. article.content gives the article text.
    #some parts of the article we won't need, such as headers and some escape characters.
    #headers have \n== preceding and ==\n after.
    #\n is not needed
    #everything after "See Also" and/or "References" is not needed.
    text = article.content
    text = text.replace("\n","")
    if "= References =" in text:
        start = text.find("= References =")
        sub = text[start:]
        text = text.replace(sub,"")
    #Text in between == are either topics (important), labels e.g. "History" (not really important), or wikipedia formatting e.g. "References" (not needed)
    #For now I'll just remove any text in between ==.
    while text.find("==") != -1:
        firstInst = text.find("==")
        toNext = text.find("==",firstInst + 1)
        if toNext != -1:
            #we want to remove the substring of text[firstInst:toNext+2] (the +2 accounts for the ending ==)
            sub = text[firstInst:toNext+2]
        else:
            #uneven number of == or something
            sub = text[firstInst:firstInst+2]
        text = text.replace(sub,"")
    return text
