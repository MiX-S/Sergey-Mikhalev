from RBTree import RBT
from frame import MainFrame
from interaction import Game
from tkinter import *
import random
import time

N = 10
L = list(range(N))
random.shuffle(L)

game = Game()
root = Tk()
frame = MainFrame(root, game, speed=10)
rbt = RBT(frame)

for i in range(N):
    rbt.insert(i, str(i))
    try:
        rbt.verify()
    except BrokenTreeError as e:
        rbt.prefix_traverse(['color'])
        print('Error node:', e.node)
        raise
rbt.prefix_traverse(['color'])
time.sleep(1)

print('#######################################')

# L = [0, 4, 3, 6, 5, 9, 8, 2, 1, 7]
random.shuffle(L)
for i in L:
    rbt.remove(i)
    # time.sleep(2)
    # rbt.frame.speed = 1
    try:
        rbt.verify()
    except BrokenTreeError as e:
        rbt.prefix_traverse(['color'])
        print('Error node:', e.node)
        raise
rbt.prefix_traverse(['color'])


root.mainloop()