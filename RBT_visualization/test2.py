from RBTree import RBT
import random



rbt = RBT()

rbt.insert(7, str(7))
rbt.insert(5, str(5))
rbt.insert(10, str(10))
rbt.insert(15, str(15))
rbt.insert(17, str(17))
rbt.insert(8, str(8))


rbt.remove(8)
rbt.remove(10)
#rbt.remove(17)
#rbt.remove(15)
# rbt.remove(5)
# rbt.remove(7)




# rbt.frame.rotate_left(node=rbt.root)
#nodes = rbt.frame._get_all_nodes(rbt.root)
# for node in nodes:
    # print(node.value)

#rbt.frame.rotate_left_redraw_connect(rbt.root.left)
#rbt._rotate_left(rbt.root.left)
#rbt.prefix_traverse(['color'])
#rbt.frame.rotate(rbt.root)

#rbt.frame.rotate_right_redraw_connect(rbt.root)
#rbt._rotate_right(rbt.root)
#rbt.prefix_traverse(['color'])
#rbt.frame.rotate(rbt.root)


rbt.Root.mainloop()

