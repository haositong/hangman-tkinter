from tkinter import *
from tkinter import messagebox
import csv, random, sys, turtle

file = open('word_list.csv','r')
reader = csv.reader(file)
word_list = []
for row in reader:
    word_list.append(row[0])
file.close()

#global variables
word = ''
lives = 10
word_guessed = ''
letters_guessed = []
drawing = False

#functions
def drawLine():
    global drawing
    drawing = True
    if lives == 10:
        p.up()
        p.goto(-150,-150)
        p.down()
        p.fd(300)
    elif lives == 9:
        p.up()
        p.bk(300)
        p.lt(90)
        p.down()
        p.fd(300)
    elif lives == 8:
        p.rt(90)
        p.fd(150)
    elif lives == 7:
        p.rt(90)
        p.fd(50)
    elif lives == 6:
        p.rt(90)
        p.circle(25)
    elif lives == 5:
        p.up()
        p.lt(90)
        p.fd(50)
        p.down()
        p.fd(75)
    elif lives == 4:
        p.up()
        p.bk(50)
        p.rt(60)
        p.down()
        p.fd(35)
    elif lives == 3:
        p.up()
        p.bk(35)
        p.lt(60)
        p.lt(60)
        p.down()
        p.fd(35)
    elif lives == 2:
        p.up()
        p.bk(35)
        p.rt(60)
        p.fd(50)
        p.rt(60)
        p.down()
        p.fd(35)
    elif lives == 1:
        p.up()
        p.bk(35)
        p.lt(120)
        p.down()
        p.fd(35)
    drawing = False

def spaceOut(string):
    new_string = ''
    for letter in string:
        new_string = new_string + letter + ' '
    return new_string[:-1]


def updateWordGuessedText():
    word_guessed_text.set(spaceOut(word_guessed))

def over():
    if messagebox.askyesno('Restart','Restart?'):
        reset()
    else:
        tk.destroy()
        sys.exit()

def reset():
    global word, lives, word_guessed
    word = random.choice(word_list)
    lives = 10
    word_guessed = '_' * len(word)
    updateWordGuessedText()
    message_text.set('')
    p.clear()
    p.reset()
    p.pensize(5)

def keyPress(event):
    check()

def check():
    global lives, word_guessed
    if drawing == True:
        return
    guess = entry.get()
    guess = guess.lower()
    entry.delete(0,END)

    if guess not in 'abcdefghijklmnopqrstuvwxyz' or len(guess) != 1:
        message_text.set("That's not a letter")
        return

    if guess in letters_guessed:
        message_text.set('Already tried that letter')
        return
    else:
        message_text.set('')
        letters_guessed.append(guess)
    
    if guess in word:
        new_word_guessed = ''
        for i in range(len(word)): #for every letter in word:
            if guess == word[i]: #if it is the letter guessed,
                new_word_guessed += word[i] #add this letter to new_
            else: #else
                new_word_guessed += word_guessed[i] #keep the letter
        word_guessed = new_word_guessed
        message_text.set('Correct!')
        updateWordGuessedText()
    else:
        message_text.set('Incorrect!')
        drawLine()
        lives -= 1

    if word_guessed == word:
        message_text.set('You win! You have guessed the word')
        over()
    if lives == 0:
        message_text.set('Game over. The word is '+word)
        over()

#tkinter stuff
tk = Tk()
tk.title('Hangman')

canvas = Canvas(master=tk,width=500,height=500)
canvas.grid(row=1,column=1,columnspan=2)
p = turtle.RawTurtle(canvas)

word_guessed_text = StringVar()
l = Label(tk, textvariable=word_guessed_text,font=('Consolas',15))
l.grid(row=2, column=1, columnspan=2)

message_text = StringVar()
Label(tk, textvariable=message_text,font=('Consolas',15)).grid(row=3, column=1, columnspan=2)

entry = Entry(tk,width=3,font=('Consolas',15))
entry.grid(row=4,column=1,sticky=E)

Button(tk,text='Enter',command=check).grid(row=4,column=2,sticky=W)

tk.bind('<Return>',keyPress)

reset()

tk.mainloop()

