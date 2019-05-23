from tkinter import *
from RBTree import RBT
from BSTree import BrokenTreeError
from interaction import Game
from frame import MainFrame
import random




def set_window(root):
    root.title('Red-Black-tree Visualization')
    root.resizable(True, True)


if __name__ == '__main__':

    root = Tk()
    game = Game()
    set_window(root)
    frame = MainFrame(root, game)
    rbt = RBT(root, frame)

    N = 10
    L = list(range(N))
    random.shuffle(L)

    for i in range(N):
        rbt.insert(i, str(i))
        try:
            rbt.verify()
        except BrokenTreeError as e:
            rbt.prefix_traverse(['color'])
            print('Error node:', e.node)
            raise
    rbt.prefix_traverse(['color'])

    root.mainloop()