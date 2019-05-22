from frame import MainFrame
import tkinter as tk


class Node:

    def __init__(self, value):
        self.value = value


node1 = Node(5)
node2 = Node(10)
node3 = Node(15)
node4 = Node(2)

# print(node.value)

root = tk.Tk()
frame = MainFrame(root)
frame.draw_node(node1)
frame.draw_node(node2, node1, 'right')
frame.draw_node(node3, node2, 'right')
frame.draw_node(node4, node2, 'left')


#frame.flip_nodes(node2, node3)

root.mainloop()