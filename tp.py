#wowow the style is pretty horrible...things besides style aren't too hot either........but I hacked this together v quick, I promise it won't be this bad in the final product! Still working on refining it, esp because trying to do redrawAll with tkinter's text widget is proving to be quite difficult

import analyzeSentence #a .py file with all of the text analyzing stuff

from tkinter import *

#draw functions taken from 112 website

def init(data):
    data.text = ""

def redrawAll(canvas,data):
    canvas.create_rectangle(0,0,data.width,data.height,fill="yellow")
    canvas.create_text(data.width//2,50,text="M V P",font="Arial 24")
    canvas.create_text(data.width//2,100,text="can i get uhhhhhhhhh computational linguistics",font="Arial 12",width=data.width//1.1)
    textBox(canvas,data)

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
    analyzeSentence.analyzePrompt(text) #running this function gives us the prompt verbs/phrases/questions to work with.
    
    #after getting the text from the text box, adds tags to the text
    verbIndex = []
    for verb in analyzeSentence.promptEssayVerbs:
        data.text.tag_add("verb",1.0+text.find(verb)/10,1.0+len(verb)/10) 
    data.text.tag_config("verb",background="yellow")
def strIndToChr(word):
    #tkinter's text box's way of finding a character is in the format "#.#" where the first number is line number (starts from 1) and the second is column number (starts from 0).
    #this function takes a number in string index format and converts it to a line/column index format.
    wordStartInd = text.find(word) 
    wordEndInd = wordStartInd + len(word)

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
    
    #root.bind("<Button-1>", lambda event:mousePressedWrapper(event, canvas, data))
    
    redrawAll(canvas, data)
    button1 = Button(root,text="Wiki",command=None)
    button2 = Button(root,text="Analyze Text",command=lambda:basicHighlight(data,data.text.get(1.0,END))) #upon pressing the button...
    button1.pack()
    button2.pack()
    root.mainloop()
    print("bye!")

runDrawing()