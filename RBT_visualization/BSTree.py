from frame import MainFrame
import tkinter as tk


class BSTNode:
    # Description of __slots__ attribute can be found at
    # https://pythonz.net/references/named/object.__slots__/
    # Here __slots__ is used in __str__() method.
    __slots__ = ('key', 'value', 'left', 'right', 'parent')

    def __init__(self, key, value, left=None, right=None, parent=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent

    def __str__(self):
        print_str = []
        for k in self.__slots__:
            if k in ['left', 'right', 'parent']:
                n = getattr(self, k)
                if n is None:
                    v = None
                else:
                    k += '.key'
                    v = n.key
                print_str.append('{}={}'.format(k, repr(v)))
            else:
                print_str.append('{}={}'.format(k, repr(getattr(self, k))))
        return self.__class__.__name__ + '(' + ', '.join(print_str) + ')'

    def is_left_child(self):
        if self.parent is None:
            return False
        if self is self.parent.left:
            return True
        return False

    def is_right_child(self):
        if self.parent is None:
            return False
        if self is self.parent.right:
            return True
        return False

    def get_attribute_values_string(self, attributes):
        """Returns a string with names and values of
        specified attributes. Used in Tree.prefix_traverse()
        method for optional demostration of node contents."""

        values = [getattr(self, attr) for attr in attributes]
        attr_strings = ['{}={}'.format(attr, repr(v)) for attr, v in zip(attributes, values)]
        return ' '.join(attr_strings)

    def _get_slots_attributes(self):
        attributes = {}
        for attr in self.__slots__:
            attributes[attr] = getattr(self, attr)
        return attributes

    def copy(self):
        kwargs = self._get_slots_attributes()
        return self.__class__(**kwargs)


class BrokenTreeError(Exception):
    def __init__(self, message, node, notional_depth=None):
        super().__init__(message)
        self.node = node
        self.notional_depth = notional_depth


class BST:
    def __init__(self):
        self.root = None

    ############################
    # Traverse methods

    def _traverse(self, root):
        if root is not None:
            print(root.key, root.value)
            self._traverse(root.left)
            self._traverse(root.right)

    def traverse(self):
        """Infix traverse"""
        self._traverse(self.root)

    @staticmethod
    def _get_connection_lines_for_children(connections):
        connections = connections.copy()
        if len(connections) == 0:
            return connections
        if connections[-1] == '├':
            connections[-1] = '│'
        elif connections[-1] == '└':
            connections[-1] = ' '
        else:
            raise ValueError('no connection to current node')
        return connections

    @staticmethod
    def _print_connections(connections):
        connections_str = ''
        for c in connections:
            if c == ' ':
                connections_str += c * 4
            elif c == '│':
                connections_str += c + ' ' * 3
            elif c in '├└':
                connections_str += c + '─' * 2 + ' '
            else:
                raise ValueError("unknown character '{}' in connections list".format(c))
        print(connections_str, end='')

    def _prefix_traverse(self, root, connections, attributes):
        self._print_connections(connections)
        connections = self._get_connection_lines_for_children(connections)
        if root is not None:
            print(root.key, root.get_attribute_values_string(attributes))
            connections_right = connections.copy()
            connections_right.append('├')
            self._prefix_traverse(root.right, connections_right, attributes)
            connections_left = connections.copy()
            connections_left.append('└')
            self._prefix_traverse(root.left, connections_left, attributes)
        else:
            print('-')

    def prefix_traverse(self, attributes=()):
        """Prefix traverse which draws connections between nodes.
        `attributes` is a tuple containing names of attributes
        of tree node which will be printed during traversing.
        For instance if you need to print values in nodes you
        may use
        ```python
        import random
        for _ in range(5):
            key = random.randint(0, 5)
            bst.insert(key, str(key))
        bst.prefix_traverse(('value',))
        ```
        The output will look similar to
        ```
        8 value='8'
        ├── 12 value='12'
        │   ├── 13 value='13'
        │   │   ├── -
        │   │   └── -
        │   └── 9 value='9'
        │       ├── -
        │       └── -
        └── 3 value='3'
            ├── -
            └── -
        ```
        By default only keys of the node are printed.
        The right subtree is printed before the left subtree.
        If a node has no child, hyphen is printed instead of
        child's key.
        Args:
            attributes: a tuple of strings

        Returns:
            None
        """
        self._prefix_traverse(self.root, [], attributes)

    ##################################
    # Insertion methods

    def _insert(self, key, value, root):
        if key == root.key:
            root.value = value
        elif key < root.key:
            if root.left is None:
                root.left = BSTNode(key, value, parent=root)
            else:
                self._insert(key, value, root.left)
        else:
            if root.right is None:
                root.right = BSTNode(key, value, parent=root)
            else:
                self._insert(key, value, root.right)

    def insert(self, key, value):
        if self.root is None:
            self.root = BSTNode(key, value)
        else:
            self._insert(key, value, self.root)

    ###################################
    # Search and removal methods

    def _find(self, key, root):
        if root is None:
            return None
        if key == root.key:
            return root  # ATTENTION changed from root.value
        elif key < root.key:
            return self._find(key, root.left)
        else:
            return self._find(key, root.right)

    def _remove(self, key, root):
        node = self._find(key, root)
        if node is not None:
            if node.left is None:
                successor = node.right
                self._set_links_with_parent_for_node_replacement(node, successor)
            elif node.right is None:
                successor = node.left
                self._set_links_with_parent_for_node_replacement(node, successor)
            else:
                successor = self._find_min_in_subtree(key, node.right).copy()
                node.key = successor.key
                node.value = successor.value
                self._remove(successor.key, node.right)
        else:
            raise KeyError("node with key {} is not found in BST".format(repr(key)))

    def _find_min_in_subtree(self, key, root):
        if root.left is None:
            return root
        else:
            return self._find_min_in_subtree(key, root.left)

    def _set_links_with_parent_for_node_replacement(self, node, successor):
        parent = node.parent
        if parent is None:
            self.root = successor
        else:
            if node.is_left_child():
                parent.left = successor
            else:
                parent.right = successor
        if successor is not None:
            successor.parent = parent

    def remove(self, key):
        self._remove(key, self.root)

    def find(self, key):
        return self._find(key, self.root).value

    ###################################
    # Rotation methods

    def _rotate_left(self, node):
        """Left rotation of subtree with root at `node`.
            node                 B
           /    \               / \
          A      B   ===>   node   D
                / \        /    \
               C   D      A      C
        Args:
            node: an instance of `BSTNode` class or `BSTNode` subclass

        Returns:
            None
        """

        r = node.right
        if r is None:
            raise ValueError("no right subtree")
        rl = r.left

        p = node.parent

        if p is None:
            self.root = r
        else:
            if node.is_left_child():
                p.left = r
            else:
                p.right = r

        r.parent = p
        r.left = node

        node.parent = r
        node.right = rl

        if rl is not None:
            rl.parent = node

    def _rotate_right(self, node):
        """Right rotation of subtree with root at node.
            node                   A
           /    \                 / \
          A      B     ===>      C   node
         / \                        /    \
        C   D                      D      B
        Args:
            node: an instance of BSTNode class or BSTNode subclass

        Returns:
            None
        """

        left = node.left
        if left is None:
            raise ValueError("no left subtree")
        lr = left.right

        p = node.parent

        if p is None:
            self.root = left
        else:
            if node.is_left_child():
                p.left = left
            else:
                p.right = left

        left.parent = p
        left.right = node

        node.parent = left
        node.left = lr

        if lr is not None:
            lr.parent = node

    ###################################
    # Verification methods

    def _verify_links(self):
        if self.root.parent is not None:
            raise BrokenTreeError(
                "the root of the tree has parent"
                "\nself.root={}".format(self.root),
                self.root,
            )
        self._verify_links_recur(self.root)

    @staticmethod
    def _check_if_loop(node, direction):
        node_2 = getattr(node, direction)
        if node_2 is node:
            raise BrokenTreeError(
                "{} attribute of the node with key {} "
                "points at the same node {}".format(
                    repr(direction), repr(node.key), node),
                node,
            )

    @staticmethod
    def _check_connection(parent, direction):
        child = getattr(parent, direction)
        if child is not None:
            if parent is not child.parent:
                raise BrokenTreeError(
                    "child node {} does not point "
                    "at its parent {}".format(child, parent),
                    parent,
                )

    def _verify_links_recur(self, root):
        if root is None:
            return
        self._check_if_loop(root, 'left')
        self._check_if_loop(root, 'right')
        self._check_connection(root, 'left')
        self._check_connection(root, 'right')
        self._verify_links_recur(root.left)
        self._verify_links_recur(root.right)

    @staticmethod
    def _fits_in(limits, value):
        return ((limits[0] is None or value > limits[0]) and
                (limits[1] is None or value < limits[1]))

    def _verify_bin(self, root, limits):
        if root is None:
            return
        if not self._fits_in(limits, root.key):
            raise BrokenTreeError(
                "key of node {} does not fit "
                "in limits {}".format(root, repr(limits)),
                root,
            )
        self._verify_bin(root.left, [limits[0], root.key])
        self._verify_bin(root.right, [root.key, limits[1]])

    def verify(self):
        """Checks correctness of links between nodes, e.g.
        child parent attribute points at its parent. Verifies
        that tree is binary search tree.
        """

        if self.root is not None:
            self._verify_links()
            self._verify_bin(self.root, [None, None])