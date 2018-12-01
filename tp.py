#wowow the style is pretty horrible...things besides style aren't too hot either........but I hacked this together v quick, I promise it won't be this bad in the final product! Still working on refining it, esp because trying to do redrawAll with tkinter's text widget is proving to be quite difficult

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

from tkinter import *

#draw functions taken from 112 website

def init(data):
    data.text = ""
    data.mouseX = -1

def textBox(canvas,data):
    #draws a text box.
    #1 char is ~3pixels
    boxW = data.width//12
    boxH = data.height//32
    data.text= Text(canvas,width=boxW,height=boxH) #creates a text widget box. the value of data.text becomes w/e is in that text box.
    #note that width/height is in chars, not pixels, unlike canvas.
    canvas.create_window((data.width//6,data.height//4),window=data.text, anchor="nw") #draws the text box in the tkinter canvas
    data.text.insert("end","Evaluate the relative importance of different causes for the expanding role of the United States in the world in the period from 1865 to 1910.")

def basicHighlight(data,text):
    analyzeText.analyzePrompt(text) #running this function gives us the prompt verbs/phrases/questions to work with.
    
    #after getting the text from the text box, adds tags to the text
    verbIndex = []
    for verb in analyzeText.promptEssayVerbs:
        data.text.tag_add("verb",1.0+text.find(verb)/10,1.0+len(verb)/10) 
    data.text.tag_config("verb",background="yellow")
    
def strIndToChr(word):
    #tkinter's text box's way of finding a character is in the format "#.#" where the first number is line number (starts from 1) and the second is column number (starts from 0).
    #this function takes a number in string index format and converts it to a line/column index format.
    wordStartInd = text.find(word) 
    wordEndInd = wordStartInd + len(word)

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
    
    splash(root,canvas,data)

    root.mainloop()
    print("bye!")

runDrawing()


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
