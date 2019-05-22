from RBTree import RBT
import random



rbt = RBT()

rbt.insert(5, str(5))
rbt.insert(8, str(8))
rbt.insert(2, str(2))
rbt.insert(7, str(7))
rbt.insert(10, str(10))

# rbt.frame.rotate_left(node=rbt.root)
nodes = rbt.frame._get_all_nodes(rbt.root)
# for node in nodes:
    # print(node.value)

# rbt.prefix_traverse()
rbt.frame.rotate_left_redraw_connect(rbt.root)
rbt._rotate_left(rbt.root)
rbt.prefix_traverse()

rbt.frame.rotate_left(rbt.root)

rbt.Root.mainloop()

# rbt.prefix_traverse(['color'])

