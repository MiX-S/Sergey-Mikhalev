from tkinter import *
from BSTree import BST
import random


N = 10
L = list(range(N))
random.shuffle(L)

bst = BST()
for i in L:
    bst.insert(i, str(i))
    bst.verify()
bst.traverse()
bst.prefix_traverse()



def set_window(root):
    root.title('Red-Black-tree')
    root.geometry('310x310+200+200')
    root.resizable(True, True)


if __name__ == '__main__':

    root = Tk()

    #canvas = Canvas(root)
    #canvas.grid(column=0, row=0)
    #set_window(root)

    root.mainloop()