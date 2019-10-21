from tkinter import filedialog
from tkinter import *
import g_code_generator
import globals
import window


def main():
    if globals.DEBUG > 0:
        g_code_generator.generate_debug_patterns()
    else:
        root = Tk()
        w = window.Window(root)
        #size of the window
        root.geometry("1200x1000")
        root.title("converter")
        #root.configure(background='#CCCCFF')
        root.mainloop()

if __name__ == "__main__": main()