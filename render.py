"""
File with functions to render and update aquarium state
"""

from fish import Fish
from Tkinter import *


tk = Tk()
canvas = Canvas(tk, width=1000, height=500, bd=0)

#pack method tells Tk to fit the size of the window to the given text.
canvas.pack()

fish = Fish(canvas)
fish.move()

tk.mainloop()

# CREATE APP VIA CLASS

# from Tkinter import *
#
# class App(Frame):
#     def __init__(self, master=None):
#         Frame.__init__(self, master)
#         self.pack()
#         self.canvas = Canvas(master, )
# # create the application
# myapp = App(root)
#
# #
# # here are method calls to the window manager class
# #
# myapp.master.title("My Do-Nothing Application")
# myapp.master.maxsize(1000, 400)
#
# # start the program
# myapp.mainloop()

# app = Application(master=root)
# DIFFERENT WAY TO CREATE APP
# class Application(Frame):
#     def createWidgets(self):
#         self.QUIT = Button(self)
#         self.QUIT["text"] = "QUIT"
#         self.QUIT["fg"]   = "red"
#         self.QUIT["command"] =  self.quit
#         self.QUIT.pack({"side": "left"})
#
#         self.canvas = Canvas(self)
#         self.canvas["width"] = 1000
#         self.canvas["height"] = 500
#         self.canvas["bg"] = "white"
#         self.canvas.pack()
#
#     def createFish(self):
#         a = Fish(self.canvas)
#
#     def __init__(self, master=None):
#         Frame.__init__(self, master)
#         self.pack()
#         self.createWidgets()
#         self.createFish()