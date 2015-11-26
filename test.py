from tkinter import *
import constantes

class Test(Tk):
    def __init__(self):
        self.window = Tk()

        background = Canvas(self.window, width=constantes.COTE_FOND, height=constantes.COTE_FOND, background='black')

        pic = PhotoImage(file=constantes.PATH_PIC_PAGES)
        background.create_image(0,0,anchor=NW,image=pic)

        background.pack()

        self.window.mainloop()
    
