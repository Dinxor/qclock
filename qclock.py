from tkinter import *
import time
import pickle

class WindowDraggable():
    def __init__(self, label):
        self.label = label
        label.bind('<ButtonPress-1>', self.StartMove)
        label.bind('<ButtonRelease-1>', self.StopMove)
        label.bind('<B1-Motion>', self.OnMotion)

    def StartMove(self, event):
        self.x = event.x
        self.y = event.y

    def StopMove(self, event):
        self.x = None
        self.y = None

    def OnMotion(self,event):
        x = (event.x_root - self.x)
        y = (event.y_root - self.y)
        master.geometry("+%s+%s" % (x, y))

class TextClock():
    def __init__(self, label):
        self.label = label
        self.lang = lang[0]
        self.qid = []
        self.words = []
        self.symbols = []
        self.stars = [1,1,1,1,1]
        self.qfont = 24
        self.qact = "F0F0F0"
        self.qshade = "292929"
        self.qbackgr = "030303"
        self.qcols = 1
        self.qrows = 1
        self.qekv = 13
        self.qwidth = 1
        self.qheight = 1
        self.oldtime = 61
        self.oldmin = 0
        self.oldhr = 0
        self.readlang()
        self.make_clock()
        self.update_clock()

    def readlang(self):
        f = open(lang[0], 'rb')
        self.symbols = pickle.load(f)
        self.words = pickle.load(f)
        set = pickle.load(f)
        f.close()
        self.qcols,self.qrows,self.qekv = set
        self.qheight=2*self.qfont*(self.qrows+1)
        self.qwidth=2*self.qfont*(self.qcols+1)

    def placetext(self, x, y, txt):
        id_ = w.create_text(x, y, text=txt, font=("arial", self.qfont), fill='#'+str(self.qshade))
        return id_

    def update_stars(self, num):
        if num != 0:
            for i in range(1, num +1):
                w.itemconfig(self.stars[i], fill='#'+str(self.qact))
        else:
            for i in range(1, 5):
                w.itemconfig(self.stars[i], fill='#'+str(self.qshade))

    def update_word(self, currmin, currhr):
        for s in self.words[self.oldmin+12]+self.words[self.oldhr]:
            w.itemconfig(self.qid[s[0]][s[1]], fill='#'+str(self.qshade))
        for s in self.words[currmin+12]+self.words[currhr]:
            w.itemconfig(self.qid[s[0]][s[1]], fill='#'+str(self.qact))

    def make_clock(self):
        w.delete(ALL)
        self.oldtime = 61
        w.config(height=self.qheight, width=self.qwidth, bg='#'+str(self.qbackgr))
        s = [0.6*self.qfont,self.qfont,self.qwidth-0.8*self.qfont,self.qheight-0.8*self.qfont]
        k = [0,1],[2,1],[2,3],[1,3]
        for i in range(4):
            self.stars[i+1] = self.placetext(s[k[i][0]], s[k[i][1]], '*')
        for i in range(self.qcols):
            self.qid.append([])
            for j in range(self.qrows):
                self.qid[i].append(self.placetext(2*self.qfont*(i+1), 2*self.qfont*(j+1), self.symbols[i][j]))

    def update_clock(self):
        if self.lang != lang[0]:
            self.qid = []
            self.words = []
            self.symbols = []
            self.stars = [1,1,1,1,1]
            self.lang = lang[0]
            self.readlang()
            self.make_clock()
        now = time.localtime(time.time())
        if now.tm_min != self.oldtime:
            currmin = now.tm_min // 5
            currhr = (now.tm_hour + (1 if currmin > self.qekv else 0)) % 12
            self.update_stars(now.tm_min % 5)
            self.update_word(currmin, currhr)
            master.update()
            self.oldtime = now.tm_min
            self.oldmin = currmin
            self.oldhr = currhr
        w.after(1000, self.update_clock)

def quit():
    master.quit()
    master.destroy()

def hide():
    master.overrideredirect(0)
    master.iconify()

def onVisibility(event):
    if (master.state() == 'normal') & (master.overrideredirect() != True):
        master.overrideredirect(1)

def switchlang():
    lang[0],lang[1] = lang[1],lang[0]

def activate_menu(event):
    posx =  event.x_root
    posy =  event.y_root
    menu = Menu(master, tearoff = 0)
    menu.add_command(label = 'Minimize', command = hide)
    menu.add_command(label = 'Language', command = switchlang)
    menu.add_command(label = 'Quit', command = quit)
    menu.tk_popup(posx, posy)

master = Tk()
master.overrideredirect(1)
master.bind("<Visibility>", onVisibility)
master.geometry('+200+200')
#master.wm_iconbitmap('q2.ico')
master.title("qclock")
lang = ['rus1.lng','eng1.lng']
w = Canvas(master, height=100, width=100, highlightthickness=0, relief='ridge')
TextClock(w)
WindowDraggable(w)
w.bind("<Button-3>", activate_menu)
w.pack()

master.mainloop()
