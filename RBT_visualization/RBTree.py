from BSTree import BSTNode, BST
from frame import MainFrame
import tkinter as tk


class RBTNode(BSTNode):
    __slots__ = tuple(list(BSTNode.__slots__) + ['color', 'x', 'y', 'fig', 'text', 'connect'])

    def __init__(self, key, value, left=None, right=None, parent=None, color='red',
                 x=None, y=None, fig=None, text=None, connect=None):
        super().__init__(key, value, left=left, right=right, parent=parent)
        self.color = color


class RBT(BST):

    def __init__(self):
        super().__init__()
        self.Root = tk.Tk()
        self.frame = MainFrame(self.Root)

    ############################
    # Insertion methods

    def _get_relatives_ins(self, node):
        parent = node.parent
        grandparent = parent.parent
        uncle = grandparent.right if parent.is_left_child() else grandparent.left
        return parent, uncle, grandparent

    def _case_3_ins(self, node):
        parent, uncle, grandparent = self._get_relatives_ins(node)
        grandparent.color = 'red'
        parent.color = 'black'
        uncle.color = 'black'
        self._retrace_insert(grandparent)

    def _case_4_ins(self, node):
        parent = node.parent
        if parent.is_left_child() ^ node.is_left_child():
            self._subcase_4_1_ins(node)
        else:
            self._subcase_4_2_ins(node)

    def _subcase_4_1_ins(self, node):
        parent = node.parent
        if node.is_left_child():
            self._rotate_right(parent)
        else:
            self._rotate_left(parent)
        self._subcase_4_2_ins(parent)

    def _subcase_4_2_ins(self, node):
        parent, uncle, grandparent = self._get_relatives_ins(node)
        if node.is_left_child():
            self._rotate_right(grandparent)
        else:
            self._rotate_left(grandparent)
        parent.color = 'black'
        grandparent.color = 'red'

    def _retrace_insert(self, node):
        if node.parent is not None:
            if node.parent.parent is not None:
                parent, uncle, grandparent = self._get_relatives_ins(node)

        if node.parent is None:
            # case 1
            node.color = 'black'
            self.frame.recolor_node(node, 'black')
        elif node.parent.color == 'black':
            # case 2
            # no need to do anything
            node.color = 'red'
        elif parent.color == 'red' and uncle is not None and uncle.color == 'red':
            self._case_3_ins(node)
        elif parent.color == 'red' and (uncle is None or uncle.color == 'black'):
            self._case_4_ins(node)
        else:
            assert False, (
                "unexpected coloring,\nnode={}\nparent={}"
                "\nuncle={}\ngrandparent={}".format(
                    node,
                    parent,
                    uncle,
                    grandparent,
                )
            )

    def _insert(self, key, value, root):
        if key == root.key:
            root.value = value
        elif key < root.key:
            if root.left is None:
                root.left = RBTNode(key, value, parent=root)
                self.frame.draw_node(root.left, root, 'left')
                self._retrace_insert(root.left)
            else:
                self._insert(key, value, root.left)
        else:
            if root.right is None:
                root.right = RBTNode(key, value, parent=root)
                self.frame.draw_node(root.right, root, 'right')
                self._retrace_insert(root.right)
            else:
                self._insert(key, value, root.right)

    def insert(self, key, value):
        if self.root is None:
            self.root = RBTNode(key, value)
            # Draw root node
            self.frame.draw_node(self.root)
            self._retrace_insert(self.root)
        else:
            self._insert(key, value, self.root)

    ############################
    # Removal methods

    def _get_relatives_rem(self, parent, node_is_left_child):
        sibling = parent.right if node_is_left_child else parent.left
        return sibling, sibling.left, sibling.right

    def _2nd_cond_rem(self, p, node_is_left_child):
        s, sl, sr = self._get_relatives_rem(p, node_is_left_child)
        return (p.color == 'black' and
                s.color == 'black' and
                (sl is None or sl.color == 'black') and
                (sr is None or sr.color == 'black'))

    def _3rd_cond_rem(self, p, node_is_left_child):
        s, _, _ = self._get_relatives_rem(p, node_is_left_child)
        return s.color == 'red'

    def _4th_cond_rem(self, p, node_is_left_child):
        pass  # TODO

    def _5th_cond_rem(self, p, node_is_left_child):
        pass  # TODO

    def _6th_cond_rem(self, p, node_is_left_child):
        pass  # TODO

    def _case_2_rem(self, parent, node_is_left_child):
        sibling, _, _ = self._get_relatives_rem(parent, node_is_left_child)
        sibling.color = 'red'
        self._retrace_remove(parent.parent, parent.is_left_child())

    def _case_3_rem(self, parent, node_is_left_child):
        if node_is_left_child:
            sibling = parent.right
            self._rotate_left(parent)
        else:
            sibling = parent.left
            self._rotate_right(parent)
        parent.color = 'red'
        sibling.color = 'black'
        self._cases_4_5_6_rem(parent, node_is_left_child)

    def _case_4_rem(self, parent, node_is_left_child):
        pass  # TODO

    def _case_5_rem(self, parent, node_is_left_child):
        pass  # TODO

    def _case_6_rem(self, parent, node_is_left_child):
        pass  # TODO

    def _cases_4_5_6_rem(self, parent, node_is_left_child):
        pass  # TODO

    def _retrace_remove(self, parent, node_is_left_child):
        if parent is None:
            pass  # case 1

        elif self._2nd_cond_rem(parent, node_is_left_child):
            self._case_2_rem(parent, node_is_left_child)

        elif self._3rd_cond_rem(parent, node_is_left_child):
            self._case_3_rem(parent, node_is_left_child)

        else:
            self._cases_4_5_6_rem(parent, node_is_left_child)

    def _replace(self, node, successor):
        if node.color == 'red':
            # both children are NIL
            assert successor is None, \
                ("broken RBT: there is non NIL child of "
                 "the red node which other child is NIL")
            self._set_links_with_parent_for_node_replacement(node, successor)
        elif successor is None:
            node_is_left_child = node.is_left_child()
            self._set_links_with_parent_for_node_replacement(node, successor)
            self._retrace_remove(node.parent, node_is_left_child)
        else:
            assert successor.color == 'red', \
                "broken RBT: the only non NIL child is black"
            self._set_links_with_parent_for_node_replacement(node, successor)
            successor.color = 'black'

    def _remove(self, key, root):
        node = self._find(key, root)
        if node is not None:
            if node.left is None:
                self._replace(node, node.right)
            elif node.right is None:
                self._replace(node, node.left)
            else:
                successor = self._find_min_in_subtree(key, node.right).copy()
                node.key = successor.key
                node.value = successor.value
                self._remove(successor.key, node.right)
        else:
            raise KeyError("node with key {} is not found in RBT".format(repr(key)))

    def remove(self, key):
        self._remove(key, self.root)

    ############################
    # Verification methods

    def _check_for_red_red_link(self, node):
        if node.color == 'red':
            if node.left is not None:
                if node.left.color == 'red':
                    raise BrokenTreeError(
                        "the left child with key {} of "
                        "the red node with key {} is red".format(
                            repr(node.left.key), repr(node.key)),
                        node,
                        2
                    )
            if node.right is not None:
                if node.right.color == 'red':
                    raise BrokenTreeError(
                        "the right child with key {} of the red node"
                        " with key {} is red".format(
                            repr(node.right.key), repr(node.key)),
                        node,
                        2
                    )

    def _verify(self, root):
        if root is None:
            return 1
        self._check_for_red_red_link(root)
        right_black_height = self._verify(root.right)
        left_black_height = self._verify(root.left)
        if left_black_height != right_black_height:
            raise BrokenTreeError(
                "left and right black heights are not equal for node with key {}"
                "\nleft_black_height={}\nright_black_height={}".format(
                    repr(root.key), left_black_height, right_black_height),
                root,
                None
            )
        if root.color == 'red':
            return left_black_height
        return left_black_height + 1

    def verify(self):
        """Verifies that red-black tree properties"""

        super().verify()
        if self.root is not None and self.root.color == 'red':
            raise BrokenTreeError("color of the tree root is red", self.root, 1)
        _ = self._verify(self.root)