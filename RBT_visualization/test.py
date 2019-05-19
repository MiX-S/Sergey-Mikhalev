from frame import MainFrame
import tkinter as tk


class Node:

    def __init__(self, value):
        self.value = value


node = Node(5)
# print(node.value)

root = tk.Tk()
frame = MainFrame(root)
frame.draw_node(node)

root.mainloop()