from tkinter import *
import copy
import pickle

def inputtext(event):
    x = event.x
    y = event.y
    mx = int(nx.get())
    my = int(ny.get())
    ki = (x-10)//32
    kj = (y-10)//32
#    print(x, ' ', y)
    if (ki<mx) & (kj<my):
        if mode.get() == 0:
            md[ki][kj] = sm.get()
            w.itemconfig(mid[ki][kj], text = md[ki][kj])
            if clearafter.get() == 1:
                sm.delete(0, END)
        else:
            cword.append([])
            cword[-1].append(ki)
            cword[-1].append(kj)
            w.itemconfig(currword, text = getcword())

def getword(val):
    tword = ''
    for s in words[val]:
        tword += md[s[0]][s[1]]
    return tword

def getcword():
    tword = ''
    for s in cword:
        tword += md[s[0]][s[1]]
    return tword

def save_button():
    words[cn] = copy.deepcopy(cword)
    w.itemconfig(tw[cn], text = getcword())

def bks_button():
    id = len(cword)
    if id >0:
        cword.pop()
        w.itemconfig(currword, text = getcword())

def inc_button():
    global cword
    global cn
    if cn < 23:
        cn +=1
        w.itemconfig(numword, text = str(cn))
        cword = copy.deepcopy(words[cn])
        w.itemconfig(currword, text = getcword())

def dec_button():
    global cword
    global cn
    if cn > 0:
        cn -=1
        w.itemconfig(numword, text = str(cn))
        cword = copy.deepcopy(words[cn])
        w.itemconfig(currword, text = getcword())

def read_button():
    global md
    global words
    global cn
    global cword
    set = []
    f = open(fe.get(), 'rb')
    md = pickle.load(f)
    words = pickle.load(f)
    set = pickle.load(f)
    f.close()
    x = set[0]
    nx.delete(0, END)
    nx.insert(0, x)
    y = set[1]
    ny.delete(0, END)
    ny.insert(0, y)
    ek = set[2]
    ne.delete(0, END)
    ne.insert(0, ek)
    for i in range(x):
        for j in range(y):
            w.itemconfig(mid[i][j], text = md[i][j])
    for i in range(24):
        w.itemconfig(tw[i], text = getword(i))
    cn = 0
    cword = copy.deepcopy(words[cn])
    w.itemconfig(currword, text = getcword())
    w.itemconfig(numword, text = str(cn))

def write_button():
    x = int(nx.get())
    y = int(ny.get())
    set = []
    set.append(x)
    set.append(y)
    set.append(int(ne.get()))
    f = open(fe.get(), 'wb')
    md1 = []
    for s in md[:x]:
        md1.append(s[:y])
    pickle.dump(md1, f)
    pickle.dump(words, f)
    pickle.dump(set, f)
    f.close()

master = Tk()
master.geometry('+200+200')
w = Canvas(master, height=700, width=1000)
md = []
mid = []
words = []
tw = []
cword = []
for i in range(24): words.append([]) 
cn = 0
w.bind("<Button-1>", inputtext)
w.pack()
for i in range(16):
    md.append([])
    mid.append([])
    for j in range(16):
        mid[i].append(w.create_text(24 + 32*i, 24 + 32*j, text=str(max(i, j)+1), font=("tahoma", 12)))
        md[i].append(str(max(i, j)+1))
ls = Label(text = 'Input symbol:')
ls.place(x=20, y=560)
sm = Entry(width=5,bd=3)
sm.insert(0, '*')
sm.place(x=100, y=560)
clearafter = IntVar()
ca = Checkbutton(text="Clear after insert", variable = clearafter)
ca.place(x=20, y=600)
mode = IntVar()
rm1 = Radiobutton(text='Symbols', value=0, variable=mode, state = 'active')
rm1.place(x=20, y=520)
rm2 = Radiobutton(text='Words', value=1, variable=mode)
rm2.place(x=180, y=520)
btndec = Button(text="<", command=dec_button)
btndec.place(x=180, y=560)
numword = w.create_text(215, 570, text='0')
currword = w.create_text(180, 600, text='')
btninc = Button(text=">", command=inc_button)
btninc.place(x=230, y=560)
btnsave = Button(text="Save", command=save_button)
btnsave.place(x=260, y=560)
btnbks = Button(text="Backspc", command=bks_button)
btnbks.place(x=260, y=600)
le = Label(text = 'Input ekv:')
le.place(x=370, y=520)
ne = Entry(master,width=5,bd=3)
ne.place(x=440, y=520)
ne.insert(0, 13)
lx = Label(text = 'Input cols:')
lx.place(x=370, y=560)
nx = Entry(master,width=5,bd=3)
nx.place(x=440, y=560)
nx.insert(0, 16)
ly = Label(text = 'Input rows:')
ly.place(x=370, y=600)
ny = Entry(master,width=5,bd=3)
ny.place(x=440, y=600)
ny.insert(0, 16)
btnread = Button(text="Read", command=read_button)
btnread.place(x=540, y=520)
btnwrite = Button(text="Write", command=write_button)
btnwrite.place(x=540, y=560)
fe = Entry(master,width=15, bd=3)
fe.place(x=540, y=600)
fe.insert(0, 'language.lng')

for i in range(12):
    w.create_text(560, 24 + 32*i, text=str(i)+' h:', font=("tahoma", 10))
    tw.append(w.create_text(640, 24 + 32*i, text='', font=("tahoma", 10)))
for i in range(12, 24):
    w.create_text(760, 24 + 32*(i-12), text=str(5*(i-12))+' m:', font=("tahoma", 10))
    tw.append(w.create_text(840, 24 + 32*(i-12), text='', font=("tahoma", 10)))

master.mainloop()
