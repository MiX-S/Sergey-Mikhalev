from tkinter import *
import time


def draw_line(x0, y0, x1, y1):

    x1 += 1
    x0 += 1
    canvas.create_line(x0, y0, x1, y1, width=12, fill='red', tag = 'line')
    time.sleep(0.02)
    root.update()
    canvas.delete('line')

    if x1 < 400:
        # root.after(30, draw_line(x0, y0, x1, y1))
        draw_line(x0, y0, x1, y1)


def move_node():

    xspeed = 0.5
    yspeed = 0.5
    time.sleep(0.002)
    root.update()
    canvas.move(node, xspeed, yspeed)

    if canvas.coords(node)[0] < 200:
        move_node()


def change_nodes(node1, node2):

    coords1 = canvas.coords(node1)
    coords2 = canvas.coords(node2)
    # distance between nodes
    # dist = ((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2) ** 0.5
    # xspeed1 = (node2.x - node1.x) / 100
    # yspeed1 = (node2.y - node1.y) / 100
    dist = ((300) ** 2 + (200) ** 2) ** 0.5
    xspeed1 = (300) / 100
    yspeed1 = (200) / 100
    xspeed2 = -xspeed1
    yspeed2 = -yspeed1

    while canvas.coords(node1)[0] != coords2[0] and canvas.coords(node1)[1] != coords2[1]:
        canvas.move(node1, xspeed1, yspeed1)
        canvas.move(node2, xspeed2, yspeed2)
        time.sleep(0.005)
        root.update()




root = Tk()

canvas = Canvas(root, width=600, height=400)
canvas.pack()

x0, y0, x1, y1 = 10, 100, 200, 100
# draw_line(x0, y0, x1, y1)

node1 = canvas.create_oval(0, 0, 100, 100,
                           width=2, outline='black', fill='red')
node2 = canvas.create_oval(300, 200, 400, 300,
                           width=2, outline='black', fill='red')
change_nodes(node1, node2)


# move_node()
root.mainloop()