import os
import subprocess
from threading import Thread
from tkinter import *
from game import *

class Window(Frame):

    gameThread = None

    def __init__(self, master: Tk):
        Frame.__init__(self, master)
        self.master = master

        form = Frame(master)
        form.grid(column = 0, row = 0)

        widthLabel = Label(form, text = "Width:", font = ("Arial", 14))
        widthLabel.grid(column = 0, row = 0)
        heightLabel = Label(form, text = "Height:", font = ("Arial", 14))
        heightLabel.grid(column = 0, row = 1)

        widthEntry = Entry(form, font = ("Arial", 14))
        widthEntry.grid(column = 1, row = 0)
        heightEntry = Entry(form, font = ("Arial", 14))
        heightEntry.grid(column = 1, row = 1)

        buttons = Frame(master)
        buttons.grid(column = 1, row  = 1)
        startButton = Button(buttons, text = "Start", font = ("Arial", 14), command = self.clickStartButton)
        startButton.grid(column = 0, row  = 0)
        exitButton = Button(buttons, text = "Exit", font = ("Arial", 14), command = self.clickExitButton)
        exitButton.grid(column = 1, row  = 0)

    def clickStartButton(self):
        # env = GameEnv
        game = Game(env)
        root.withdraw()
        game.start()
        exit()

    def clickExitButton(self):
        exit()

root = Tk()
app = Window(root)

root.wm_title("Wallenstein Starter")
root.resizable(0, 0)

root.mainloop()