from card import *
import tkinter as tk

pgWidth = 1220
pgHeight = 1000

root = tk.Tk(baseName='Spider Solitaire')
root.title('Spider Solitaire')
root.geometry(str(pgWidth)+"x"+str(pgHeight))

table = Canvas(root, width=pgWidth, height=pgHeight)
table.configure(bg='darkgreen')
table.pack()

table.create_text(100,100,fill="red",font="Arial 40 bold",
                        text="Click the bubbles that are multiples of two.", anchor=NW)

c2=Card(0,10)

c=Card(3,13)
c3=Card(0,10)
c4=Card(3,13)

a = [1,3,4,[c2,c],True]
b = [1,3,4,[c3,c4], True]
print(a)
print(b)

print(c)
print (a==b)

a = [3,4,5,6,7,9,10]
b = []
b.append(a[1:])
print(b)

img = None
images = []

tmpImg = None

def drag(event):
    global img

    img = images[0]
    table.delete("all")
    table.create_image(event.x,event.y,image=img, anchor = NW)

def turn(event):
    c.turn()

def show(event):
    global img,images
    img = c.getImg()
    table.create_image(250, 250, image=img, anchor=NW)
    images = [img]


root.bind('<B1-Motion>', drag)
root.bind('<Button 3>', turn)
root.bind('<Button 1>', show)
root.mainloop()
