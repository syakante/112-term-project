#### wiki.py ####
#this python file manages the wikipedia API: taking an input, finding a usable wiki page, then taking the relevant text from that page.
import wikipedia

def wikiTest(text):
    keywords = ""
    trainer = wikipedia.search(text)
    #can't do much with this yet
    print("work in progress")