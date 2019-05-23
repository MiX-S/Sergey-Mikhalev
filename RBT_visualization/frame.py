import tkinter as tk
import time


class MainFrame(tk.Frame):
    def __init__(self, root, game, d=25, speed=1, size=(600, 400), depth=5):
        super().__init__()
        self._canvas = None
        self.grid(row=0, column=0, sticky=(tk.S, tk.E, tk.N, tk.W))
        # self._add_menu()
        self._add_canvas()
        self._root = root
        self._game = game
        self.d = d
        self.speed = speed
        self.size = size
        self.depth = depth
        self._game.add_frame(self)

    def _add_menu(self):
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)
        file_menu = tk.Menu(menu_bar)
        field_menu = tk.Menu(menu_bar)

        file_menu.add_command(label="save", command=self._game.save)
        file_menu.add_command(label="load", command=self._game.load)

        field_menu.add_command(label='clean', command=self._game.reset_canvas())

        menu_bar.add_cascade(label="file", menu=file_menu)
        menu_bar.add_cascade(label='field', menu=field_menu)

    def draw_connection(self, node, parent):
        # distance between nodes
        dist = ((node.x - parent.x) ** 2 + (node.y - parent.y) ** 2) ** 0.5
        # parametres of angle
        sin_alpha = (node.y - parent.y) / dist
        cos_alpha = (node.x - parent.x) / dist

        x0, y0 = parent.x + self.d * cos_alpha, parent.y + self.d * sin_alpha
        x1, y1 = node.x - self.d * cos_alpha, node.y - self.d * sin_alpha
        x, y = x0, y0
        xspeed, yspeed = (x1 - x0) / int(100 / self.speed), (y1 - y0) / int(100 / self.speed)
        # if node.connect is not None:
        #     self._canvas.delete(node.connect)
        node.connect = self._canvas.create_line(x0, y0, x, y, width=2, fill='black')  # , arrow=tk.LAST)

        for _ in range(int(100 / self.speed)):
            self._canvas.delete(node.connect)
            x, y = x + xspeed, y + yspeed
            node.connect = self._canvas.create_line(x0, y0, x, y, width=2, fill='black')  # , arrow=tk.LAST)
            self._root.update()
            time.sleep(0.003 / self.speed)

        time.sleep(0.2 / self.speed)

    def _get_node_coords(self, node):
        width, height = self.size[0], self.size[1]
        max_depth = self.depth
        if node.parent is None:
            x, y = width / 2, 50
        else:
            parent_x = node.parent.new_x or node.parent.x
            parent_y = node.parent.new_y or node.parent.y
            if node.is_left_child():
                if node.parent.parent is None:
                    x = parent_x - min(parent_x, width - parent_x) / 2
                else:
                    grandparent_x = node.parent.parent.new_x or node.parent.parent.x
                    x = parent_x - abs(grandparent_x - parent_x) / 2

            elif node.is_right_child():
                if node.parent.parent is None:
                    x = parent_x + min(parent_x, width - parent_x) / 2
                else:
                    grandparent_x = node.parent.parent.new_x or node.parent.parent.x
                    x = parent_x + abs(grandparent_x - parent_x) / 2
            y = parent_y + (height - 100) / max_depth
        return x, y

    def draw_node(self, node, parent=None, side=None):
        width, height = 600, 400
        max_depth = 5
        if parent is None:
            node.x, node.y = 300, 50
        else:
            if side == 'left':
                node.x = parent.x - min(parent.x, width - parent.x) / 2
            elif side == 'right':
                node.x = parent.x + min(parent.x, width - parent.x) / 2
            else:
                raise Exception('unknown parameter side = {}'.format(side))
            node.y = parent.y + (height - 100) / max_depth

        node.x, node.y = self._get_node_coords(node)
        if parent is not None:
            self.draw_connection(node, parent)

        node.fig = self._canvas.create_oval(node.x - self.d, node.y - self.d, node.x + self.d, node.y + self.d,
                                            width=2, outline='black', fill='red')
        node.text = self._canvas.create_text(node.x, node.y, text=str(node.value), fill='white',
                                             font=('Helvetica', '20'))
        node.color = 'red'
        self._root.update()
        time.sleep(1 / self.speed)

    def _get_all_nodes(self, node):

        nodes = []
        nodes.append(node)
        if node.left is not None:
            nodes += self._get_all_nodes(node.left)
        if node.right is not None:
            nodes += self._get_all_nodes(node.right)
        return nodes

    def _get_all_coords(self, nodes, left=True, down=True):

        new_coords = []
        right, up = not left, not down
        if left and down:
            for node in nodes:
                if node.left is not None:
                    new_coords.append((node.left.x, node.left.y))
                else:
                    new_x = (node.parent.x + node.x) / 2
                    new_y = 2 * node.y - node.parent.y
                    new_coords.append((new_x, new_y))
        elif left and up:
            for node in nodes:
                if node.is_right_child:
                    new_coords.append((node.parent.x, node.parent.y))
                else:
                    new_x = 2 * node.x - node.parent.x
                    new_y = node.parent.y
                    new_coords.append((new_x, new_y))
        elif right and down:
            pass
        else:
            pass

        return new_coords

    def _move_all_nodes(self, all_nodes):

        coords = [self._canvas.coords(node.fig) for node in all_nodes]

        xspeeds = [(node.new_x - node.x) / int(100 / self.speed) for node in all_nodes]
        yspeeds = [(node.new_y - node.y) / int(100 / self.speed) for node in all_nodes]

        for _ in range(int(100 / self.speed)):
            for i in range(len(all_nodes)):
                # move nodes
                self._canvas.move(all_nodes[i].fig, xspeeds[i], yspeeds[i])
                # self._canvas.delete(node.fig)
                # self._canvas.create_oval(node.x - self.d, node.y - self.d, node.x + self.d, node.y + self.d,
                #                         width=2, outline='black', fill=color)
                # move nodes' values
                self._canvas.move(all_nodes[i].text, xspeeds[i], yspeeds[i])
                # self._canvas.delete(node.text)
                # self._canvas.create_text(node.x, node.y, text=str(node.value), fill='white',
                #                         font=('Helvetica', '20'))

                all_nodes[i].x, all_nodes[i].y = all_nodes[i].x + xspeeds[i], all_nodes[i].y + yspeeds[i]
                # redraw connection
                if all_nodes[i].parent is not None:
                    self._move_connection_moment(all_nodes[i], all_nodes[i].parent)
            self._root.update()
            time.sleep(0.003 / self.speed)

    def _update_coords(self, node):
        """
        Get new coordinates for all nodes after rotation
        :param node: root of Tree
        :return:
        """
        nodes_to_move = []

        def upd_coords(node, nodes_to_move):
            if node.x != self._get_node_coords(node)[0] or node.y != self._get_node_coords(node)[1]:
                node.new_x, node.new_y = self._get_node_coords(node)
                nodes_to_move.append(node)
            if node.left is not None:
                upd_coords(node.left, nodes_to_move)
            if node.right is not None:
                upd_coords(node.right, nodes_to_move)

        if node is not None:
            upd_coords(node, nodes_to_move)
        return nodes_to_move

    def rotate_left_redraw_connect(self, node):
        r = node.right
        rl = r.left
        p = node.parent

        # Redraw all connections
        self._canvas.delete(r.connect)
        if node.parent is not None:
            self._canvas.delete(node.connect)
            self.draw_connection(r, node.parent)
        self.draw_connection(node, r)

        if rl is not None:
            self._canvas.delete(rl.connect)
            self.draw_connection(rl, node)

    def rotate_right_redraw_connect(self, node):
        l = node.left
        lr = l.right
        p = node.parent

        # Redraw all connections
        self._canvas.delete(l.connect)
        if node.parent is not None:
            self._canvas.delete(node.connect)
            self.draw_connection(l, node.parent)
        self.draw_connection(node, l)

        if lr is not None:
            self._canvas.delete(lr.connect)
            self.draw_connection(lr, node)

    def rotate(self, node):

        # Update coords and move nodes
        nodes_to_move = self._update_coords(node)
        for node in nodes_to_move:
            print('value: ', node.value)
            print('old coords: ', node.x, node.y)
            print('new coords: ', node.new_x, node.new_y)
        self._move_all_nodes(nodes_to_move)

    def rotate_left_old(self, node):

        r = node.right
        rl = r.left
        p = node.parent

        # Redraw all connections
        if node.connect is not None:
            self._canvas.delete(node.connect)
            self.draw_connection(r, node.parent)
        self._canvas.delete(r.connect)
        # self.draw_connection(node, r)
        self._canvas.delete(rl.connect)
        # self.draw_connection(rl, node)

        # 1: get all nodes for each subtree
        node_nodes = self._get_all_nodes(node)
        rl_nodes = self._get_all_nodes(rl)
        r_nodes = self._get_all_nodes(r)
        all_nodes = node_nodes + rl_nodes + r_nodes
        # 2: get all new coords for each subtree
        node_coords = self._get_all_coords(node_nodes, left=True, down=True)
        rl_coords = [(2 * node_coords[0][0] - node_coords[1][0], rl.y)]
        # rl_coords = []
        r_coords = self._get_all_coords(r_nodes, left=True, down=False)
        all_coords = node_coords + rl_coords + r_coords
        # 3: move all nodes to their new positions
        self._move_all_nodes(all_nodes, all_coords)

    def recolor_node(self, node, color='black'):
        self._canvas.delete(node.fig)
        self._canvas.delete(node.text)
        node.fig = self._canvas.create_oval(node.x - self.d, node.y - self.d, node.x + self.d, node.y + self.d,
                                            width=2, outline='black', fill=color)
        node.text = self._canvas.create_text(node.x, node.y, text=str(node.value), fill='white',
                                             font=('Helvetica', '20'))
        node.color = color
        self._root.update()
        time.sleep(0.5 / self.speed)

    def draw_connection_moment(self, node, parent):
        # distance between nodes
        dist = ((node.x - parent.x) ** 2 + (node.y - parent.y) ** 2) ** 0.5
        # parametres of angle
        sin_alpha = (node.y - parent.y) / dist
        cos_alpha = (node.x - parent.x) / dist

        x0, y0 = parent.x + self.d * cos_alpha, parent.y + self.d * sin_alpha
        x1, y1 = node.x - self.d * cos_alpha, node.y - self.d * sin_alpha
        node.connect = self._canvas.create_line(x0, y0, x1, y1, width=2, fill='black')

    def _move_connection_moment(self, node, parent):

        # distance between nodes
        dist = ((node.x - parent.x) ** 2 + (node.y - parent.y) ** 2) ** 0.5

        if dist > 2 * self.d:
            self._canvas.delete(node.connect)
            self.draw_connection_moment(node=node, parent=parent)
        else:
            pass

    def _move_connection(self, node1, node2):

        # distance between nodes
        dist = ((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2) ** 0.5

        if dist > 2 * self.d and node2.y > node1.y:
            self._canvas.delete(node2.connect)
            self.draw_connection_moment(node=node2, parent=node1)
        elif dist > 2 * self.d and node2.y < node1.y:
            self._canvas.delete(node2.connect)
            self.draw_connection_moment(node=node1, parent=node2)
        else:
            pass

    def _remove(self, node, successor):
        self._canvas.delete(node.fig)
        self._canvas.delete(node.text)
        node.fig = self._canvas.create_oval(node.x - self.d, node.y - self.d, node.x + self.d, node.y + self.d,
                                            width=2, outline='black', fill=node.color)
        node.text = self._canvas.create_text(node.x, node.y, text=str(successor.value), fill='white',
                                             font=('Helvetica', '20'))
        self._root.update()
        time.sleep(0.5 / self.speed)

    def flip_nodes(self, node1, node2):

        coords1 = self._canvas.coords(node1.fig)
        coords2 = self._canvas.coords(node2.fig)

        xspeed1, yspeed1 = (node2.x - node1.x) * self.speed / 100, (node2.y - node1.y) * self.speed / 100
        xspeed2, yspeed2 = -xspeed1, -yspeed1

        while self._canvas.coords(node1.fig)[0] != coords2[0] and self._canvas.coords(node1.fig)[1] != coords2[1]:
            # move nodes
            self._canvas.move(node1.fig, xspeed1, yspeed1)
            self._canvas.move(node2.fig, xspeed2, yspeed2)
            # move nodes' values
            self._canvas.move(node1.text, xspeed1, yspeed1)
            self._canvas.move(node2.text, xspeed2, yspeed2)

            node1.x, node1.y = node1.x + xspeed1, node1.y + yspeed1
            node2.x, node2.y = node2.x + xspeed2, node2.y + yspeed2
            # redraw connection
            self._move_connection(node1, node2)

            self._root.update()
            time.sleep(0.003 / self.speed)

    def _process_mouse_click(self, canvas, event):
        cell_pos = self._get_cell_pos(event.x, event.y)
        if cell_pos[0] is not None and cell_pos[1] is not None:
            self._game.receive_move(cell_pos)

    def _add_event_processing(self, canvas):
        canvas.bind("<Button-1>", lambda e: self._process_mouse_click(canvas, e))

    def _add_canvas(self):
        canvas = tk.Canvas(self, width=600, height=400, background='white')
        canvas.grid(column=0, row=0, padx=5, pady=5)
        self._add_event_processing(canvas)
        self._canvas = canvas
        pass

    def reset_canvas(self):
        if self._canvas is not None:
            self._canvas.delete('all')
        #if self.rbt is not None:
        #    self.rbt.root = None

