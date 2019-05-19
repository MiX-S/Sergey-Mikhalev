from tkinter import *
from BSTree import BST, BSTNode
import random




def set_window(root):
    root.title('Red-Black-tree')
    root.geometry('400x400+200+200')
    root.resizable(True, True)

def visualize(root, tree):

    canvas = Canvas(root)
    canvas.grid(column=0, row=0)
    set_window(root)

    max_nodes = 10
    window_x = 310
    window_y = 310
    ind = 0
    coord = [(200, 100), (100, 200), (300, 200)]
    while ind < 3:
        x0, y0 = 100, 100
        d = 50
        canvas.create_oval(coord[ind][0], coord[ind][1], coord[ind][0] + d, coord[ind][1] + d,
                           outline="black")
        canvas.create_text(coord[ind][0] + d/2, coord[ind][1] + d/2, text=str(ind), fill='black',
                           font=('Helvetica', '16'))
        # root.update()
        ind += 1


    root.mainloop()


root = Tk()
visualize(root, None)

N = 3
L = list(range(N))
random.shuffle(L)

bst = BST()
for i in L:
    bst.insert(i, str(i))
    bst.verify()
# bst.traverse()
# bst.prefix_traverse()