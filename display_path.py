from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import matplotlib.colors as colors
#from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2TkAgg)

#from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np
from random import sample
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
def color_generate(num,totalnum,date,maxdate):
    val=3*num/totalnum
    if val<1:
        r=val
        g=0
        b=0
    elif val<2:
        r=1
        g=val-1
        b=0
    else:
        r=1
        g=1
        b=val-2
    rgba=(r,g,b,date/maxdate)
    return rgba
def color_generate_2(num,totalnum,date,maxdate):
    val = 2 * num / totalnum
    if val < 1:
        r = 1-val
        g = 1
    else:
        r = 0
        g = 2-val
    rgba = (r, g, 1-(date/maxdate), date / maxdate)
    return rgba
def flatcolorgenerate(num,totalnum):
    '''val = 3 * num / totalnum
    if val < 1:
        r = val
        g = 0
        b = 0
    elif val < 2:
        r = 1
        g = val - 1
        b = 0
    else:
        r = 1
        g = 1
        b = val - 2
    rgb = (r, g, b)
    return rgb'''
    hsv=np.array([num/totalnum,0.5,1.0])
    return colors.hsv_to_rgb(hsv)
def input_read(filename):
    with open(filename) as f:
        mynums=[[float(n) for n in line.split(",")] for line in f.read().splitlines()]
    #Make sure this works for an arbitrary number of objects
    xs=[]
    ys=[]
    zs=[]
    c=[]
    for timestep in mynums:
        v=int(len(timestep)/7)
        for n in range(v):
            #date, xn,yn,zn,vxn,vyn,vzn,GMn
            xs.append(timestep[7*n+1])
            ys.append(timestep[7*n+2])
            zs.append(timestep[7*n+3])
            c.append(color_generate_2(n,v-1,timestep[0],mynums[-1][0]))
    return xs,ys,zs,c

def input_read_fast(filename,fract=1):
    with open(filename) as f:
        in_nums=[[float(n) for n in line.split(",")] for line in f.read().splitlines()]
    #Make sure this works for an arbitrary number of objects
    mynums=sample(in_nums,int(fract*len(in_nums)))
    mynums.sort()
    xs=[]
    ys=[]
    zs=[]
    c=[]
    for timestep in mynums:
        v=int(len(timestep)/7)
        for n in range(v):
            #date, xn,yn,zn,vxn,vyn,vzn,GMn
            xs.append(timestep[7*n+1])
            ys.append(timestep[7*n+2])
            zs.append(timestep[7*n+3])
            c.append(color_generate_2(n,v-1,timestep[0],mynums[-1][0]))
    return xs,ys,zs,c
def input_read_subplots(filename):
    with open(filename) as f:
        mynums=[[float(n) for n in line.split(",")] for line in f.read().splitlines()]
    #Make sure this works for an arbitrary number of objects
    #xs=[]
    #ys=[]
    #zs=[]
    #colors=[]
    plots=[]
    for n in range(int(len(mynums[0])/7)):
        plots.append([[],[],[],flatcolorgenerate(n,int(len(mynums[0])/7))])
    for timestep in mynums:
        v=int(len(timestep)/7)
        for n in range(v):
            #date, xn,yn,zn,vxn,vyn,vzn,GMn
            plots[n][0].append(timestep[7*n+1])
            plots[n][1].append(timestep[7*n+2])
            plots[n][2].append(timestep[7*n+3])

    return plots
def last_points(plots):
    xs=[]
    ys=[]
    zs=[]
    colors=[]
    for plot in plots:
        xs.append(plot[0][-1])
        ys.append(plot[1][-1])
        zs.append(plot[2][-1])
        colors.append(plot[3])
    return xs,ys,zs,colors
class NavigationAssistant():
    def __init__(self,axes):
        self.ax=axes
        self.window=Toplevel(root)
        self.frame=ttk.Frame(self.window, padding="3 3 12 12")
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        ttk.Label(self.frame,text="Lower bound").grid(column=1,row=2)
        ttk.Label(self.frame,text="X").grid(column=2,row=1)
        ttk.Label(self.frame,text="Y").grid(column=3,row=1)
        ttk.Label(self.frame,text="Z").grid(column=4,row=1)
        self.xvar=StringVar()
        self.yvar=StringVar()
        self.zvar=StringVar()
        self.xwidth=StringVar()
        self.ywidth=StringVar()
        self.zwidth=StringVar()
        ttk.Entry(self.frame,textvariable=self.xvar).grid(column=2,row=2)
        ttk.Entry(self.frame, textvariable=self.yvar).grid(column=3, row=2)
        ttk.Entry(self.frame, textvariable=self.zvar).grid(column=4, row=2)
        ttk.Label(self.frame,text="Upper Bound").grid(column=1,row=3)
        ttk.Entry(self.frame,  textvariable=self.xwidth).grid(column=2, row=3)
        ttk.Entry(self.frame, textvariable=self.ywidth).grid(column=3, row=3)
        ttk.Entry(self.frame, textvariable=self.zwidth).grid(column=4, row=3)
        ttk.Button(self.frame,text="Resize",command=self.resize).grid(column=4,row=4)
    def resize(self):
        self.ax.set_xbound(int(self.xvar.get()),int(self.xwidth.get()))
        self.ax.set_ybound(int(self.yvar.get()), int(self.ywidth.get()))
        self.ax.set_zbound(int(self.zvar.get()), int(self.zwidth.get()))

def draw_plot(plots,labels=None):
    fig=plt.figure()
    #fig = Figure(figsize=(5,4),dpi=100)
    ax = fig.add_subplot(111, projection='3d')
    for plot in plots:
        xs,ys,zs,c=plot[0],plot[1],plot[2],plot[3]
        ax.plot(xs,ys,zs,str(colors.to_hex(c)))
    xs,ys,zs,c=last_points(plots)
    ax.scatter(xs=xs,ys=ys,zs=zs,color=c)
    if labels !=None:
        for n in range(len(labels)):
            ax.text(x=xs[n],y=ys[n],z=zs[n],s=labels[n])
    print(str(ax.can_pan()))
    print(str(ax.can_zoom()))
    NavigationAssistant(ax)
    #canvas=FigureCanvasTkAgg(fig,master=rootframe)
    #canvas.draw()
    #canvas.get_tk_widget().grid(column=1,row=1,columnspan=5,rowspan=4)
    #toolbar= NavigationToolbar2TkAgg(canvas,root)
    #toolbar.update()

    plt.show()
'''def plot_relative(plots,center):
    #Given a list of planets to track and the index of the object to be held as a fixed point, graphs the movements relative to the fixed body
    fig=plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for plot in plots:
        xs,ys,zs,c=[plot[0][n]-plots[center][0][n] for n in range(len(plot[0]))],[plot[1][n]-plots[center][1][n] for n in range(len(plot[1]))],[plot[2][n]-plots[center][2][n] for n in range(len(plot[2]))],plot[3]
        ax.plot(xs,ys,zs,str(colors.to_hex(c)))
    xs,ys,zs,c=last_points()'''
def make_relative(plots,center):
    #Given a list of objects to graph and the index of one to be held fixed, adjusts the list to be relative to the specified object
    newplots=[]
    for plot in plots:
        newplots.append([[plot[0][n]-plots[center][0][n] for n in range(len(plot[0]))],[plot[1][n]-plots[center][1][n] for n in range(len(plot[1]))],[plot[2][n]-plots[center][2][n] for n in range(len(plot[2]))],plot[3]])
    return newplots
#fig= plt.figure()
#ax=fig.add_subplot(111,projection='3d')
root=Tk()
r2=Toplevel(root)
#r2=root
root.title("3D Graphing Application for Solar System Viewing")
r2.title("Data selector")
r2.resizable(FALSE,FALSE)
#root.resizable(FALSE,FALSE)
mainframe= ttk.Frame(r2, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
rootframe=ttk.Frame(root,padding="3 3 12 12")
rootframe.grid(column=0, row=0, sticky=(N, W, E, S))
rootframe.columnconfigure(0, weight=1)
rootframe.rowconfigure(0, weight=1)
filename=StringVar()
lab=StringVar()
cent=StringVar()


def file_input():
    global filename
    filename.set(filedialog.askopenfilename())
def labels_input():
    global lab
    with open(filedialog.askopenfilename()) as labels:
        lab.set(labels.read())

#fn=input("What file to open? ")
#labelsin=input('What are these bodies called? Enter "None" to omit labels')
def start(*args):
    global filename,lab,cent,yncent
    fn=filename.get()
    labelsin=lab.get()
    center=cent.get()
    #if labelsin=="None":
    #    labels=None
    #else:
    labels=labelsin.split(",")
    r2.destroy()
#center=input('Choose the index of the body used as a center, or enter "B" for barycenter')
    if len(center)==0:
        draw_plot(input_read_subplots(fn), labels)
    else:
        draw_plot(make_relative(input_read_subplots(fn),int(center)),labels)

ttk.Button(mainframe, text="Load Data From File", command=file_input).grid(column=1, row=1)
ttk.Label(mainframe, text="Enter labels. Leave blank for no labels").grid(column=1, row=2)
ttk.Entry(mainframe, textvariable=lab).grid(column=2, row=2)
ttk.Label(mainframe,text="Alternately, load labels from a file. You will be able to edit them afterwards").grid(column=1,row=3)
ttk.Button(mainframe,text="Select Labels",command=labels_input).grid(column=2,row=3)
ttk.Label(mainframe, text="Select a custom center. Leave blank to use the barycenter.").grid(column=1, row=4)
centername = ttk.Entry(mainframe, textvariable=cent).grid(column=2, row=4)
ttk.Button(mainframe, text="Start", command=start).grid(column=2, row=5)
root.mainloop()
#fm=input("Fast mode? (Y/N) ")
#if fm=="Y":
#    xs,ys,zs,colors=input_read_fast(fn,0.02)
#else:
#    xs,ys,zs,colors=input_read(fn)
#ax.scatter(xs,ys,zs,c=colors)

#plt.show()