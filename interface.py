from tkinter import Tk, Canvas, ttk, filedialog
from PIL import Image, ImageTk
from images import *
from dinic import *


def select_image():
    # ask the user for the filename
    global file_path, size, obj_pixels, bck_pixels, G, line
    file_path = filedialog.askopenfilename()

    # only show the image if they chose something
    if file_path:
        print(file_path)
        # open the file
        G = {}
        obj_pixels = set()
        bck_pixels = set()
        for part in line:
            canvas.delete(part)
        image = Image.open(file_path)
        size = image.size
        # create the image object, and save it so that it
        # won't get deleted by the garbage collector
        canvas.image_tk = ImageTk.PhotoImage(image)

        # configure the canvas item to use this image
        canvas.itemconfigure(image_id, image=canvas.image_tk)


def get_x_and_y(event):
    global lasx, lasy
    lasx, lasy = event.x, event.y


def draw_line(event):
    global lasx, lasy, obj_pixels, bck_pixels, flag, color, line
    id = canvas.create_line((lasx, lasy, event.x, event.y),
                            fill=color,
                            width=2)
    line.append(id)
    lasx, lasy = event.x, event.y
    if flag == 'object':
        obj_pixels.add((lasx, lasy))
    elif flag == 'background':
        bck_pixels.add((lasx, lasy))


def flag_object():
    global flag, color
    flag = 'object'
    color = 'red'


def flag_background():
    global flag, color
    flag = 'background'
    color = 'blue'


def segmentize():
    global file_path, obj_pixels, bck_pixels, size, G
    G = gen_graph(file_path, obj_pixels, bck_pixels, neighbours=8)
    G_f = dinic(G, 's', 't')
    segments = min_cut(G_f, 's', 't')
    res = build_segmented(segments, size)
    fname = get_fname(file_path)
    res.save(fname + '.jpg')


app = Tk()
app.geometry('650x650')
obj_pixels = set()
bck_pixels = set()
file_path = ''
size = ()
line = []
flag = 'object'
color = 'red'
G = {}
canvas = Canvas(app, bg='white', height=500, width=500)
canvas.pack()
image_id = canvas.create_image(0, 0, anchor="nw")
btn = ttk.Button(app, text='Select file', command=select_image)
btn.pack()
btn1 = ttk.Button(app, text='Object pixels selection', command=flag_object)
btn2 = ttk.Button(app, text='Background pixels selection',
                  command=flag_background)
btn1.pack()
btn2.pack()
btn3 = ttk.Button(app, text='RUN', command=segmentize)
btn3.pack()
canvas.bind('<Button-1>', get_x_and_y)
canvas.bind('<B1-Motion>', draw_line)
app.mainloop()
