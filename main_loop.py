# This is the Orbital Gravity Simulation v0.1
# X and Y axes are defined by the international celestial reference frame
# Each body is specified by seven parameters: x, y, z, vx, vy, vz, and GM
# The origin is considered to be the barycenter of the solar system, not the center of the star.
# If you don't know the barycenter, adjust_calc.py will convert from sun-centered coordinates.
# The program will take coordinates in km or AU. 1 AU=149597870.700 km.
# Velocities should be given in km/day or AU/day.
# Gravitational parameters are given in au^3/day^2
# Output coordinates are in AU and output velocity in AU/day
# Output time is given in days since epoch by default. Alternately the user can enter a start date.
from input_loop import manual, from_file, data_divide
from adjust_calc import km_to_au, au_to_km
from math import sqrt,pow
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
def gravity_step(obj_a,obj_b, time_step=1):
    #Newtonian approximation, accurate to within 1.112*10^-17 of the final value
    diffx=obj_a[0][0]-obj_b[0][0]
    diffy=obj_a[0][1]-obj_b[0][1]
    diffz=obj_a[0][2]-obj_b[0][2]
    dist2=pow(diffx,2)+pow(diffy,2)+pow(diffz,2)
    dv=time_step*obj_b[2]/dist2
    dist=sqrt(dist2)
    obj_a[1][0]-=dv*diffx/dist
    obj_a[1][1]-=dv*diffy/dist
    obj_a[1][2]-=dv*diffz/dist
    return obj_a

#simulate_until=int(input("How long should the program simulate?"))
#timestep=int(input("How many days is each step?"))
#data_form=input("[M]anual entry or Import from [F]ile?")
#outfile=open(input("Where should output be stored?")+".csv","W")
date=0
data=[]
root=Tk()
root.title("Orbital Gravity Simulation v0.1")
root.resizable(FALSE,FALSE)
mainframe= ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
units=StringVar()
units.set("AU")
step=StringVar()
inmethod=StringVar()
#fancyinmethod=StringVar()
indata=StringVar()
outfilename=StringVar()
outfilename.set("output.csv")
endtime=StringVar()
def start(*args):
    global timestep,simulate_until,data,outfile,units
    timestep=int(step.get())
    simulate_until=int(endtime.get())
    if inmethod.get()=='Filename':
        with open(indata.get()) as f:
            rawdat=f.read()
    else:
        rawdat=indata.get()
    km=False
    if units.get()=="KM":
        km=True
    outfile=open(outfilename.get(),"w")
    data=data_divide(rawdat,km)
    root.destroy()
def file_input():
    global indata
    filename=filedialog.askopenfilename()
    with open(filename) as f:
        indata.set(f.read())
def window_input():
    global indata
    entry_window=TopLevel(root)
    entryframe = ttk.Frame(entry_window, padding="3 3 12 12")
    entryframe.grid(column=0, row=0, sticky=(N, W, E, S))
    entryframe.columnconfigure(0, weight=1)
    entryframe.rowconfigure(0, weight=1)
    ttk.Label(entryframe,text="Data should be formatted as x,y,z,vx,vy,vz,GM").grid(column=1,row=1)
    data_entry=ttk.Entry(entryframe,textvariable=indata)
    data_entry.grid(column=1,row=2,columnspan=4,rowspan=8)
    ttk.Button(entryframe,command=lambda n:entry_window.destroy()).grid(column=4,row=10)



#ttk.Label(mainframe,text="Select input format").grid(column=1,row=1,sticky=W)
#ttk.Radiobutton(mainframe,text='From file',variable=inmethod,value='Filename').grid(column=2,row=1)
#ttk.Radiobutton(mainframe,text='Manual in window',variable=inmethod,value='Data').grid(column=3,row=1)
#ttk.Label(mainframe,text="Data should be formatted as x,y,z,vx,vy,vz,GM").grid(column=2,row=2,columnspan=2)
#ttk.Label(mainframe,textvariable=inmethod).grid(column=1,row=3)
#data_entry=ttk.Entry(mainframe,textvariable=indata)
#data_entry.grid(column=2,row=3)
ttk.Label(mainframe,text="Choose input").grid(column=1,row=1,sticky=W)
ttk.Button(mainframe,text="Load from File",command=file_input).grid(column=2,row=1)
ttk.Button(mainframe,text="Enter Manually",command=window_input).grid(column=3,row=1)
ttk.Label(mainframe,text="Preview").grid(column=1,row=2)
ttk.Entry(mainframe,textvariable=indata,state="readonly").grid(column=1,row=3)
ttk.Label(mainframe,text="Preferred units").grid(column=1,row=4)
ttk.Radiobutton(mainframe,text='Kilometers',variable=units,value='KM').grid(column=2,row=4)
ttk.Radiobutton(mainframe,text='Astronomical Units',variable=units,value='AU').grid(column=3,row=4)
ttk.Label(mainframe,text="Time Step").grid(column=1,row=5)
ttk.Entry(mainframe,width=5,textvariable=step).grid(column=2,row=5,sticky=E)
ttk.Label(mainframe,text="days").grid(column=3,row=5,sticky=W)
ttk.Label(mainframe,text="Simulation duration").grid(column=1,row=6)
ttk.Entry(mainframe,width=5,textvariable=endtime).grid(column=2,row=6,sticky=E)
ttk.Label(mainframe,text="days").grid(column=3,row=6,sticky=W)
ttk.Label(mainframe,text="Output file").grid(column=1,row=7)
ttk.Entry(mainframe,textvariable=outfilename).grid(column=2,row=7)
ttk.Button(mainframe,text="Start",command=start).grid(column=3,row=8)
root.mainloop()
#if data_form=="M":
#    data=manual()

while date<simulate_until:
    for a in data:
        for b in data:
            if a!=b:
                a=gravity_step(a,b,timestep)
    for a in data:
        a[0][0]+=a[1][0]*timestep
        a[0][1]+=a[1][1]*timestep
        a[0][2]+=a[1][2]*timestep
    date+=timestep
    out=str(data).replace("[","").replace("]","")
    outfile.write(str(date)+","+out+"\n")
outfile.close()