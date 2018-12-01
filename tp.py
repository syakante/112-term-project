#wowow the style is pretty horrible...things besides style aren't too hot either........but I hacked this together v quick, I promise it won't be this bad in the final product! Still working on refining it, esp because trying to do redrawAll with tkinter's text widget is proving to be quite difficult
<<<<<<< HEAD

import analyzeText #a .py file with all of the text analyzing stuff
import autocomplete
import wiki

#### buttons because buttons suck in tkinter, aaaaaaaa aaaaaa ####

allButtons = []

class myButton():
    def __init__(self,root,text,function):
        self.text = text
        self.function = function
        self.root = root
        self.button = Button(self.root,text=self.text,command=lambda:self.function)
    
    def generate(self):
        self.button.pack()
        allButtons.append(self.button)
    
    def kill(self):
        self.button.destroy()
        allButtons.remove(self.button)

#### draw stuff ####
=======
    
#### computational linguistics, but not really ####

## example prompts just for testing with ##
ex1 = "Evaluate the relative importance of different causes for the expanding role of the United States in the world in the period from 1865 to 1910."

ex2 = "For the period before 1750, analyze the ways in which Britain's policy of salutary neglect influenced the development of American society."

ex3 = "Write a well-developed essay analyzing the complex nature of the gift and how the gift contributes to the meaning of the work as a whole."

ex4 = "The lessons we take from obstacles we encounter can be fundamental to later success. Recount a time when you faced a challenge, setback, or failure. How did it affect you, and what did you learn from the experience?"

## setting up lists of word types ##

import csv

with open('prepositions.csv',newline="") as prepCSV:
    prepositions = csv.reader(prepCSV, delimiter=',') #imports a list of prepositions from a .csv file (MS Excel)

myPrepPhrases = []
myEssayVerbs = set()
#due to the nature of essayVerbs as single words that are important regardless of repetition, I'm using set
myQuestions = []

def complTest(prompt):
    
    essayVerbs = {"Analyze","Compare","Contrast","Criticize","Criticise","Define","Describe","Discuss","Evaluate","Examine"}
    #to be continued but w/e
    
    articles = {"the","a"}
    
    conjunctions = {"for","and", "nor", "but", "or", "yet", "so"}
    
    questions = {"who", "what", "when", "where", "why", "how"}
    
    punct = {",",".","?","!",";",":"}
    
    global myPrepPhrases
    global myEssayVerbs
    global myQuestions
    
    sentences = prompt.replace(";",".").split(".") #since ; phrases can stand as sentences, for our purposes it'll be treated as such. 
    for sentence in sentences:
        if sentence == "" or sentence == "/n":
            continue
        promptList = sentence.split(" ")
        for i in range(len(promptList)):
            #prepositional phrases
            if promptList[i] in prepositions and promptList[i+1] not in articles:
                myPrepPhrases.append((promptList[i-1:i+1]))
            elif promptList[i] in prepositions and promptList[i+1] in articles:
                myPrepPhrases.append(promptList[i-1:i+2])
            
            #proper nouns
            '''if promptList[i].capitalize() == promptList[i]:
                print("proper noun/first word ig")
                print(promptList[i])'''
            
            #question-types
            #sometimes question words are not used in questions. If it is being used to ask a question, it fulfills BOTH these criteria:
            #the end of the sentence it is in ends in a question mark
            #it is capitalized i.e. starts the sentence OR is preceded by a punctuation OR preceded by a conjunction.
            #e.g. "John, who was in the kitchen, says no. Given where it happened, who did it, and how was it done?"
            
            if promptList[i].lower() in questions:
                if sentence.endswith("?") and (promptList[i] in [Q.title() for Q in questions] or any(promptList[i-1].endswith(x) for x in punct) or promptList[i-1] in conjunctions):
                    print("found question",promptList[i])
                    #so what I want to do eventually highlight until the end of this phrase (till next punctuation), so record the exact phrase
            
            #essay verbs
            if promptList[i] in essayVerbs:
                myEssayVerbs.add(promptList[i])
    return None
                
def findPhrase():
    #given a sentence, 
    pass
    


#### tkinter text editor ####
>>>>>>> 2ced2a2c49041570dad9c8f3d8805aeccd6d4be1

from tkinter import *

#draw functions taken from 112 website

def init(data):
<<<<<<< HEAD
    data.text = ""
    data.mouseX = -1
=======
    data.text = "temporary temporary"

'''def mousePressed(event,data):
    print("h")
'''
def redrawAll(canvas,data):
    canvas.create_rectangle(0,0,data.width,data.height,fill="yellow")
    canvas.create_text(data.width//2,50,text="darn its incomplete",font="Arial 24")
    canvas.create_text(data.width//2,100,text="at the moment you can try putting in generic essay prompts in the text box and click 'analyze' and it will highlight the verb, the code does other stuff but yet to highlight it",font="Arial 12",width=data.width//1.1)
    textBox(canvas,data)
>>>>>>> 2ced2a2c49041570dad9c8f3d8805aeccd6d4be1

def textBox(canvas,data):
    #draws a text box.
    #1 char is ~3pixels
    boxW = data.width//12
    boxH = data.height//32
<<<<<<< HEAD
    data.text= Text(canvas,width=boxW,height=boxH) #creates a text widget box. the value of data.text becomes w/e is in that text box.
=======
    data.text= Text(canvas,width=boxW,height=boxH) #creates a text widget box
>>>>>>> 2ced2a2c49041570dad9c8f3d8805aeccd6d4be1
    #note that width/height is in chars, not pixels, unlike canvas.
    canvas.create_window((data.width//6,data.height//4),window=data.text, anchor="nw") #draws the text box in the tkinter canvas
    data.text.insert("end","Evaluate the relative importance of different causes for the expanding role of the United States in the world in the period from 1865 to 1910.")

<<<<<<< HEAD
def basicHighlight(data,text):
    analyzeText.analyzePrompt(text) #running this function gives us the prompt verbs/phrases/questions to work with.
    
    #after getting the text from the text box, adds tags to the text
    verbIndex = []
    for verb in analyzeText.promptEssayVerbs:
        data.text.tag_add("verb",1.0+text.find(verb)/10,1.0+len(verb)/10) 
    data.text.tag_config("verb",background="yellow")
    
=======
def basicHighlight(text):
    #after getting the text from the text box, adds tags to the text etc using the global variables from earlier
    
    #highlight single verbs
    strung = text.get(1.0,END)
    verbIndex = []
    for verb in myEssayVerbs:
        text.tag_add("verb",1.0+strung.find(verb)/10,1.0+len(verb)/10)
    
    
    text.tag_add("verb",1.10,1.20)    
    text.tag_config("verb",background="yellow")
>>>>>>> 2ced2a2c49041570dad9c8f3d8805aeccd6d4be1
def strIndToChr(word):
    #tkinter's text box's way of finding a character is in the format "#.#" where the first number is line number (starts from 1) and the second is column number (starts from 0).
    #this function takes a number in string index format and converts it to a line/column index format.
    wordStartInd = text.find(word) 
    wordEndInd = wordStartInd + len(word)

<<<<<<< HEAD
def redrawAll(root,canvas,data):
    canvas.delete(ALL)
    [x.kill() for x in allButtons]
    canvas.update()

def splash(root,canvas,data):
    canvas.create_rectangle(0,0,data.width,data.height,fill="white")
    canvas.create_text(data.width//2,data.height//2,text="start screen",font="Arial 24")
    startButton = myButton(root,"Start",textBoxScreen(root,canvas,data))

def textBoxScreen(root,canvas,data):
    redrawAll(root,canvas,data)
    canvas.create_rectangle(0,0,data.width,data.height,fill="yellow")
    canvas.create_text(data.width//2,50,text="M V P",font="Arial 24")
    canvas.create_text(data.width//2,100,text="kiughgjdts",font="Arial 12",width=data.width//1.1)
    textBox(canvas,data)
    button1 = myButton(root,"Wiki",None)
    button2 = myButton(root,"Analyze Text",basicHighlight(data,data.text.get(1.0,END))) #upon pressing the button...
    button1.generate()
    button2.generate()

def runDrawing(width=500, height=500):    
=======
def runDrawing(width=500, height=500):
    
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    '''def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)
    '''

>>>>>>> 2ced2a2c49041570dad9c8f3d8805aeccd6d4be1
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.text = ""
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    canvas = Canvas(root, width=width, height=height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    
<<<<<<< HEAD
    splash(root,canvas,data)

=======
    #root.bind("<Button-1>", lambda event:mousePressedWrapper(event, canvas, data))
    
    redrawAll(canvas, data)
    button1 = Button(root,text="Wiki",command=lambda:wikiTest(data.text.get("1.0",END)))
    button2 = Button(root,text="Analyze Text",command=lambda:[complTest(data.text.get("1.0",END)),basicHighlight(data.text)])
    button1.pack()
    button2.pack()
>>>>>>> 2ced2a2c49041570dad9c8f3d8805aeccd6d4be1
    root.mainloop()
    print("bye!")

runDrawing()


<<<<<<< HEAD
#### demo ####

def demo():
    keyword = str(input("Keyword:"))
    a = wiki.getWiki(keyword)
    autocomplete.trainer(a)
    n = int(input("Length:"))
    print(autocomplete.chainDemo(n))
    print("enter autocomplete.chainDemo(n) to try again with same keyword")

#citation w/ webscraping and/or wikipedia api (post MVP)
#TODO: finish this by 6pm :):):):)
=======
#### wiki ####

import wikipedia

def wikiTest(text):
    keywords = ""
    trainer = wikipedia.search(text)
    #can't do much with this yet
    print("work in progress")
>>>>>>> 2ced2a2c49041570dad9c8f3d8805aeccd6d4be1
