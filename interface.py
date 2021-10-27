from tkinter import Tk, Canvas, ttk, filedialog
from PIL import Image, ImageTk
from images import *
from dinic import *


def select_image():
    global file_path, fname, image, size, pn, intensities, obj_pixels,\
         bck_pixels, newObj, newBck, prObj, prBck, line, color, flag, G, lamb,\
         sigm, K

    file_path = filedialog.askopenfilename()

    if file_path:
        # clearing vars
        fname = get_fname(file_path)
        image = Image.open(file_path)
        size = image.size
        pn = pixel_node(size)
        intensities = node_intensities(size, image.load())
        obj_pixels = set()
        bck_pixels = set()
        newObj = set()
        newBck = set()
        prObj = {}
        prBck = {}
        for part in line:
            canvas.delete(part)
        line = []
        color = ''
        flag = ''
        G = {}
        lamb = 1
        sigm = 1
        K = None

        print(file_path)
        canvas.image_tk = ImageTk.PhotoImage(image)
        canvas.itemconfigure(image_id, image=canvas.image_tk)


def get_x_and_y(event):
    global lasx, lasy
    lasx, lasy = event.x, event.y


def draw_line(event):
    global lasx, lasy, obj_pixels, bck_pixels, newObj, newBck, flag, color,\
        line
    id = canvas.create_line((lasx, lasy, event.x, event.y),
                            fill=color,
                            width=2)
    line.append(id)
    lasx, lasy = event.x, event.y
    if flag == 'object':
        obj_pixels.add((lasx, lasy))
    elif flag == 'background':
        bck_pixels.add((lasx, lasy))
    elif flag == 'improving object':
        newObj.add((lasx, lasy))
    elif flag == 'improving background':
        newBck.add((lasx, lasy))
    else:
        print('Choose mode')


def flag_object():
    global flag, color
    flag = 'object'
    color = 'red'


def flag_background():
    global flag, color
    flag = 'background'
    color = 'blue'


def flag_improve_object():
    global flag, color
    flag = 'improving object'
    color = 'green'


def flag_improve_background():
    global flag, color
    flag = 'improving background'
    color = 'orange'


def segmentize():
    global fname, image, size, intensities, obj_pixels,\
         bck_pixels, prObj, prBck, G, lamb, sigm, K
    rel = pixel_node(size)
    obj = vertices(obj_pixels, rel)
    bck = vertices(bck_pixels, rel)
    prObj = histogram(intensities, obj)
    prBck = histogram(intensities, bck)
    data = gen_graph(image, obj, bck, prObj, prBck, intensities, neighbours=8,
                     lamb=lamb, sigma=sigm)
    G = data[0]
    K = data[1]
    G_f = dinic(G, 's', 't')
    segments = min_cut(G_f, 's', 't')
    res = build_segmented(segments, size)
    fname = get_fname(file_path)
    res.save(f'{save_path}' + fname + '.jpg')
    canvas.image_tk = ImageTk.PhotoImage(res)
    canvas.itemconfigure(image_id, image=canvas.image_tk)


def improve():
    global G, newObj, newBck, K, prObj, prBck, pn, intensities, lamb
    mod_graph(G, newObj, newBck, pn, K, lamb, prObj, prBck, intensities)
    G_f = dinic(G, 's', 't')
    segments = min_cut(G_f, 's', 't')
    res = build_segmented(segments, size)
    fname = get_fname(file_path)
    res.save(f'{save_path}' + fname + '.jpg')
    canvas.image_tk = ImageTk.PhotoImage(res)
    canvas.itemconfigure(image_id, image=canvas.image_tk)


# global variables.
save_path = '/home/mike/Desktop/graphproject/my_proj/segmented_images/'
file_path = ''
fname = ''

image = None
size = ()
pn = {}
intensities = {}
obj_pixels = set()
bck_pixels = set()
newObj = set()
newBck = set()
prObj = {}
prBck = {}

line = []
flag = ''
color = ''

G = {}
lamb = 1
sigm = 1
K = None

app = Tk()
app.geometry('1200x1000')

canvas = Canvas(app, bg='white', height=700, width=1000)
canvas.pack()
image_id = canvas.create_image(0, 0, anchor="nw")
canvas.bind('<Button-1>', get_x_and_y)
canvas.bind('<B1-Motion>', draw_line)

btn = ttk.Button(app, text='Select file', command=select_image)
btn1 = ttk.Button(app, text='Object pixels selection', command=flag_object)
btn2 = ttk.Button(app, text='Background pixels selection',
                  command=flag_background)
btn3 = ttk.Button(app, text='RUN', command=segmentize)
btn4 = ttk.Button(app, text="Add object pixels for improvement",
                  command=flag_improve_object)
btn5 = ttk.Button(app, text="Add background pixels for improvement",
                  command=flag_improve_background)
btn6 = ttk.Button(app, text='Improve segmentation', command=improve)

btn.pack()
btn1.pack()
btn2.pack()
btn3.pack()
btn4.pack()
btn5.pack()
btn6.pack()

app.mainloop()
