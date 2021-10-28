from tkinter import Tk, Canvas, ttk, filedialog, Frame, Entry
from PIL import Image, ImageTk
from images import *
from dinic import *


def select_image():
    global file_path, fname, image, size, pn, intensities, obj_pixels,\
         bck_pixels, newObj, newBck, prObj, prBck, line, color, flag, G, lamb,\
         sigm, K, neigh, minimorumObj, minimorumBck

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
        minimorumObj = None
        minimorumBck = None
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
        neigh = 4
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


def change_lamb():
    global lamb
    res = lambda_entry.get()
    if res != '':
        lamb = float(res)


def change_sigm():
    global sigm
    res = sigma_entry.get()
    if res != '':
        sigm = float(res)


def switch_neighbours4():
    global neigh
    neigh = 4


def switch_neighbours8():
    global neigh
    neigh = 8


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
         bck_pixels, prObj, prBck, G, lamb, sigm, neigh, K,\
         minimorumBck, minimorumObj
    print(lamb)
    print(sigm)
    print(neigh)
    rel = pixel_node(size)
    obj = vertices(obj_pixels, rel)
    bck = vertices(bck_pixels, rel)
    prObj = histogram(intensities, obj)
    minimorumObj = worse_than_worst(prObj)
    prBck = histogram(intensities, bck)
    minimorumBck = worse_than_worst(prBck)
    data = gen_graph(image, obj, bck, prObj, prBck,
                     (minimorumObj, minimorumBck), intensities,
                     neighbours=neigh, lamb=lamb, sigma=sigm)
    G = data[0]
    K = data[1]
    G_f = dinic(G, 's', 't')
    segments = min_cut(G_f, 's', 't')
    res = build_segmented(segments, size)
    fname = get_fname(file_path)
    res.save(f'{save_path}' + fname + '_' + str(int(lamb)) + 'l' +
             str(int(sigm)) + 's' + str(neigh) + 'n' + '.jpg')
    canvas.image_tk = ImageTk.PhotoImage(res)
    canvas.itemconfigure(image_id, image=canvas.image_tk)


def improve():
    global G, newObj, newBck, K, prObj, prBck, pn, intensities, lamb,\
        minimorumBck, minimorumObj
    mod_graph(G, newObj, newBck, pn, K, lamb, prObj, prBck,
              (minimorumObj, minimorumBck), intensities)
    G_f = dinic(G, 's', 't')
    segments = min_cut(G_f, 's', 't')
    res = build_segmented(segments, size)
    fname = get_fname(file_path)
    res.save(f'{save_path}' + fname + '_' + str(int(lamb)) + 'l' +
             str(int(sigm)) + 's' + str(neigh) + 'n' + '.jpg')
    canvas.image_tk = ImageTk.PhotoImage(res)
    canvas.itemconfigure(image_id, image=canvas.image_tk)


# global variables.
save_path = '/home/mike/Desktop/graphproject/my_proj/parametric_research/'
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
minimorumObj = None
prBck = {}
minimorumBck = None

line = []
flag = ''
color = ''

G = {}
lamb = 1
sigm = 1
neigh = 4
K = None

app = Tk()
app.geometry('1200x1000')

canvas = Canvas(app, bg='white', height=700, width=1000)
canvas.pack()
image_id = canvas.create_image(0, 0, anchor="nw")
canvas.bind('<Button-1>', get_x_and_y)
canvas.bind('<B1-Motion>', draw_line)

btnframe = Frame(app)
btnframe.pack()
ttk.Button(btnframe, text='Select file', command=select_image).\
    grid(row=0, column=1)

ttk.Button(btnframe, text='Object pixels selection',
           command=flag_object).grid(row=1, column=0)
ttk.Button(btnframe, text='Background pixels selection',
           command=flag_background).grid(row=1, column=2)
ttk.Button(btnframe, text='RUN', command=segmentize).\
    grid(row=2, column=1)

ttk.Button(btnframe, text="Add object pixels for improvement",
           command=flag_improve_object).grid(row=3, column=0)
ttk.Button(btnframe, text="Add background pixels for improvement",
           command=flag_improve_background).grid(row=3, column=2)
ttk.Button(btnframe, text='Improve segmentation', command=improve)\
    .grid(row=4, column=1)

lambda_entry = Entry(btnframe)
lambda_entry.grid(row=5, column=0)
ttk.Button(btnframe, text='Change \u03BB', command=change_lamb).\
    grid(row=6, column=0)

sigma_entry = Entry(btnframe)
sigma_entry.grid(row=5, column=2)
ttk.Button(btnframe, text='Change \u03C3', command=change_sigm).\
    grid(row=6, column=2)

ttk.Button(btnframe, text='4 neighbours for pixels',
           command=switch_neighbours4).grid(row=7, column=0)

ttk.Button(btnframe, text='8 neighbours for pixels',
           command=switch_neighbours8).grid(row=7, column=2)

app.mainloop()
# print(lamb)
