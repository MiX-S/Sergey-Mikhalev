import tkinter as tk
import time


class MainFrame(tk.Frame):
    def __init__(self, root):
        super().__init__()
        self._canvas = None
        self.grid(row=0, column=0, sticky=(tk.S, tk.E, tk.N, tk.W))
        self._add_menu()
        self._add_canvas()
        self._root = root
        self.d = 25

    def _add_menu(self):
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)
        file_menu = tk.Menu(menu_bar)
        game_menu = tk.Menu(menu_bar)


        menu_bar.add_cascade(label="file", menu=file_menu)
        menu_bar.add_cascade(label='game', menu=game_menu)

    @staticmethod
    def _draw_grid(canvas):
        canvas.create_line((101, 10, 101, 290))
        canvas.create_line((195, 10, 195, 290))
        canvas.create_line((10, 101, 290, 101))
        canvas.create_line((10, 195, 290, 195))

    @staticmethod
    def _get_cell_pos(x, y):
        x_idx = (x - 9) // 94
        y_idx = (y - 9) // 94
        if x_idx < 0 or x_idx > 2:
            x_idx = None
        if y_idx < 0 or y_idx > 2:
            y_idx = None
        return x_idx, y_idx

    @staticmethod
    def _get_mark_bounding_box(cell_pos):
        x0 = 19 + cell_pos[0] * 94
        y0 = 19 + cell_pos[1] * 94
        x1 = 9 + (cell_pos[0] + 1) * 94 - 10
        y1 = 9 + (cell_pos[1] + 1) * 94 - 10
        return x0, y0, x1, y1

    def draw_circle(self, cell_pos):
        x0, y0, x1, y1 = self._get_mark_bounding_box(cell_pos)
        self._canvas.create_arc(x0, y0, x1, y1, start=0, extent=359.999, width=12, outline='blue', style='arc')

    def draw_cross(self, cell_pos):
        x0, y0, x1, y1 = self._get_mark_bounding_box(cell_pos)
        self._canvas.create_line(x0, y0, x1, y1, width=12, fill='red')
        self._canvas.create_line(x0, y1, x1, y0, width=12, fill='red')


    def draw_connection(self, node, parent):
        # distance between nodes
        dist = ((node.x - parent.x)**2 + (node.y - parent.y)**2) ** 0.5
        # paranetres of angle
        sin_alpha = (node.y - parent.y) / dist
        cos_alpha = (node.x - parent.x) / dist

        x0, y0 = parent.x + self.d * cos_alpha, parent.y + self.d * sin_alpha
        x1, y1 = node.x - self.d * cos_alpha, node.y - self.d * sin_alpha

        return self._canvas.create_line(x0, y0, x1, y1, width=2, fill='black')# , arrow=tk.LAST)

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

        node.fig = self._canvas.create_oval(node.x - self.d, node.y - self.d, node.x + self.d, node.y + self.d,
                           width=2, outline='black', fill='red')
        node.text = self._canvas.create_text(node.x, node.y, text=str(node.value), fill='white',
                           font=('Helvetica', '20'))
        if parent is not None:
            node.connect = self.draw_connection(node, parent)

    def recolor_node(self, node, color='black'):
        self._canvas.create_oval(node.x - self.d, node.y - self.d, node.x + self.d, node.y + self.d,
                                 width=2, outline='black', fill=color)
        self._canvas.create_text(node.x, node.y, text=str(node.value), fill='white',
                                 font=('Helvetica', '20'))

    def _move_connection(self, node1, node2):

        # distance between nodes
        dist = ((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2) ** 0.5

        if dist > 2 * self.d and node2.y > node1.y:
            self._canvas.delete(node2.connect)
            node2.connect = self.draw_connection(node=node2, parent=node1)
        elif dist > 2 * self.d and node2.y < node1.y:
            self._canvas.delete(node2.connect)
            node2.connect = self.draw_connection(node=node1, parent=node2)
        else:
            pass


    def flip_nodes(self, node1, node2):

        coords1 = self._canvas.coords(node1.fig)
        coords2 = self._canvas.coords(node2.fig)

        xspeed1, yspeed1 = (node2.x - node1.x) / 100, (node2.y - node1.y) / 100
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

            time.sleep(0.003)
            self._root.update()

    def _draw_victory_line(self, descr):
        if isinstance(descr, tuple):
            if descr[0] == 0:
                x = 9 + 94 * descr[1] + 47
                self._canvas.create_line(x, 9, x, 291, width=8)
            else:
                y = 9 + 94 * descr[1] + 47
                self._canvas.create_line(9, y, 291, y, width=8)
        else:
            if descr == 2:
                self._canvas.create_line(9, 291, 291, 9, width=8)
            else:
                self._canvas.create_line(9, 9, 291, 291, width=8)

    def draw_victory(self, victory_line):
        line_descr = self._classify_line(victory_line)
        self._draw_victory_line(line_descr)

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
        self._canvas.delete('all')