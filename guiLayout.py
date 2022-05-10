from datetime import date
from tkinter import *
from tkinter import ttk
import tkinter
import matplotlib as plt
from tkcalendar import Calendar, DateEntry
from covid import areaName, areaType, areaCode, df, rate
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
import matplotlib.dates as mdates
import calendar
from police import do, fplot, cplot
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

# areaName = ['MiddlesBrough', 'Leeds', 'London', 'Manchester', 'Oxford',
# 'Bradford', 'Sunderland']
# areaCode = ['TS1 1LY', 'TS1 1LH']
# rate = ['Daily Rate', 'Weekly rate', 'Total Cases']
# areaType = ['Nation', 'Region', 'Loc1', 'Loc2']

agegroup = [f'{i}-{i+4}' for i in range(0, 90, 5)]+['90+']

width = 1200
height = 700

root = Tk()
root.title('ICA')
root.geometry(str(width)+'x'+str(height))
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=4)
root.rowconfigure(0, weight=2)
root.rowconfigure(1, weight=40)
root.rowconfigure(2, weight=1)


style = ttk.Style()
style.configure('c.TFrame', background='white', foreground='red')
style.configure('v.TFrame', background='white', foreground='black')
style.configure('v.TLabel', background='blue', foreground='green')
style.configure('t1.TLabel', background='blue', foreground='green')
style.configure('t2.TLabel', background='green', foreground='blue')

# Basic Layout Starts -------------------------------------------

fHead = ttk.Frame(root)
fHead.columnconfigure(0, weight=1)
fHead.rowconfigure(0, weight=1)
fHead.grid(row=0, column=0, columnspan=2, sticky=NSEW)

fTab = ttk.Frame(root)
fTab.columnconfigure(0, weight=2)
fTab.columnconfigure(1, weight=3)
fTab.grid(row=1, column=0, sticky=NSEW)

fCView = ttk.Frame(root, style='v.TFrame')
fCView.columnconfigure(0, weight=1)
fCView.grid(row=1, column=1, sticky=NSEW)

fPView = ttk.Frame(root, style='v.TFrame')
fPView.columnconfigure(0, weight=1)
fPView.grid(row=1, column=1, sticky=NSEW)

fTail = ttk.Frame(root)
fTail.columnconfigure(0, weight=1)
fTail.rowconfigure(0, weight=1)
fTail.grid(row=2, column=0, columnspan=2, sticky=NSEW)
# Basic layout Ends ....................................


# Get selected tab and do something

# Header Starts --------------------------------------------------------
CHeader = ttk.Label(fHead, text='COVID-19', font=('Helvetica', 16))
CHeader.grid(row=0, column=0, pady=5)
PHeader = ttk.Label(fHead, text='United Kingdom Police Stop and Search',
                    font=('Helvetica', 16))
PHeader.grid(row=0, column=0, pady=5)
# Header Ends .............................................................

# Create tabs


def show(*args):
    global CHeader
    global PHeader
    tab = tabControl.index(tabControl.select())
    if tab == 0:
        PHeader.grid_remove()
        CHeader.grid()
        fPView.grid_remove()
        fCView.grid()
    else:
        CHeader.grid_remove()
        PHeader.grid()
        fCView.grid_remove()
        fPView.grid()


tabControl = ttk.Notebook(fTab)
tabControl.columnconfigure(0, weight=1)
tabControl.columnconfigure(1, weight=1)
tabControl.bind('<<NotebookTabChanged>>', show)

tab1 = ttk.Frame(tabControl)
tab1.columnconfigure(0, weight=1)
tab2 = ttk.Frame(tabControl)
tab2.columnconfigure(0, weight=1)
tab2.rowconfigure(0, weight=0)


tabControl.add(tab1, text='COVID-19')
tabControl.add(tab2, text='Stop and Search')
tabControl.pack(expand=1, fill="both")

# Populate tabs

# Tab1 Options
dateF = ttk.Frame(tab1)
dateF.grid(row=1, padx=10, pady=20, sticky=EW)
dateLab = ttk.Label(dateF, text='Date').grid()

dateMin = date(df.date.min().year, df.date.min().month, df.date.min().day)
dateMax = date(df.date.max().year, df.date.max().month, df.date.max().day)

dateFrom = StringVar()
dateTo = StringVar()

calFrom = DateEntry(dateF, selectmode='day', date_pattern='m/d/y',
                    textvariable=dateFrom, mindate=dateMin, maxdate=dateMax)
calFrom.set_date(dateMin)
calFrom.grid(row=1, column=0, padx=20)

calTo = DateEntry(dateF, selectmode='day', date_pattern='m/d/y',
                  textvariable=dateTo, mindate=dateMin, maxdate=dateMax)
calTo.grid(row=1, column=1, padx=20)


def my_upd(*args):  # triggered when value of string varaible changes
    pass  # read and display date


rateF = ttk.Frame(tab1)
for i in range(8):
    if i % 2 == 0:
        rateF.columnconfigure(i, weight=1)
    else:
        rateF.columnconfigure(i, weight=3)
rateF.grid(row=2, padx=10, pady=20, sticky=EW)


dailyLab = ttk.Label(rateF, text='Daily').grid(row=0, column=0)
weekLab = ttk.Label(rateF, text='Weekly').grid(row=0, column=2)
totalLab = ttk.Label(rateF, text='Cummulative').grid(row=0, column=4)

rateVar = StringVar()
rateVar.set(rate[1])
dailyRad = ttk.Radiobutton(rateF, variable=rateVar,
                           value=rate[1]).grid(row=0, column=1)
weekRad = ttk.Radiobutton(rateF, variable=rateVar,
                          value=rate[2]).grid(row=0, column=3)
totalRad = ttk.Radiobutton(rateF, variable=rateVar,
                           value=rate[0]).grid(row=0, column=5)


def wid():
    var = locVar.get()
    if var == 'UK':
        regF.grid_remove()
        regBox.set('United Kingdom')
    else:
        values = sorted(list(set(df.areaName[df.areaType == var])))
        regBox.set(values[0])
        regF.grid(row=4, pady=10)
        regLab.config(text=f'Select {var}')
        regBox.config(values=values)


locF = ttk.Frame(tab1)
for i in range(8):
    if i % 2 == 0:
        locF.columnconfigure(i, weight=1)
    else:
        locF.columnconfigure(i, weight=3)
locF.grid(row=3, padx=10, sticky=EW)

ukLab = ttk.Label(locF, text='UK').grid(row=0, column=0)
regionLab = ttk.Label(locF, text='Region').grid(row=0, column=2)
locLab = ttk.Label(locF, text='LTLA').grid(row=0, column=4)
locLab2 = ttk.Label(locF, text='UTLA').grid(row=0, column=6)

locVar = StringVar()
locVar.set('UK')
ubRad = ttk.Radiobutton(locF, variable=locVar,
                        value='UK', command=wid).grid(row=0, column=1)
regionRad = ttk.Radiobutton(locF, variable=locVar,
                            value='Region', command=wid).grid(row=0, column=3)
locRad = ttk.Radiobutton(locF, variable=locVar,
                         value='LTLA', command=wid).grid(row=0, column=5)
locRad2 = ttk.Radiobutton(locF, variable=locVar,
                          value='UTLA', command=wid).grid(row=0, column=7)

regF = ttk.Frame(tab1)
regLab = ttk.Label(regF, text='')
regLab.grid()
regBox = ttk.Combobox(regF, values=areaName)
regBox.set('United Kingdom')
regBox.grid()

# Plot Button


def plotChart():
    global plot1
    global canvas
    x = sorted(df.date[(df.areaName == regBox.get()) & (df.rate == rateVar.get(
    )) & ((df.date >= dateFrom.get()) & (df.date <= dateTo.get()))])
    y = df.total[(df.areaName == regBox.get()) & (df.rate == rateVar.get(
    )) & ((df.date >= dateFrom.get()) & (df.date <= dateTo.get()))]
    print(dateFrom.get())
    plot1.clear()

    # plot the new data
    plot1.plot(x, y)
    plot1.get_figure().autofmt_xdate()
    # Use a more precise date string for the x axis locations in the toolbar.
    plot1.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    plot1.set_title(f'{rateVar.get()} case of COVID-19 in {regBox.get()}')
    # call the draw method on your canvas
    canvas.draw()


plF = ttk.Button(tab1)
plF.grid(row=5, padx=10, pady=30, sticky=S)

plBtn = ttk.Button(plF, text='Plot', command=plotChart)
plBtn.grid(column=1, row=0)


# COMPARE SECTION Starts -----------------------------------------------------

def comp():
    global agegroup
    var = compVar.get()

    if var == 'Age':
        compList.delete(0, END)
        compBox.config(values=agegroup)
        compBox.set(agegroup[0])
        compRegF.grid_remove()
        [compList.insert]
    else:
        compRegF.grid(row=1, columnspan=5, pady=5)


def fillList(event):
    var = compBox.get()
    che = compList.get(0, tkinter.END)
    if var not in che:
        compList.insert((compList.size()+1), var)


def remOpt(event):
    compList.delete(ACTIVE)


def compChart(y):
    global plot1
    global canvas
    global compVar
    legend = list()
    plot1.clear()
    # plot the new data
    if compVar.get() == 'Age':
        for i in y:
            plot1.plot(sorted(df.date[(df.areaName == regBox.get(
            )) & (df.rate == rateVar.get(
            ))]), df[i][(df.areaName == regBox.get(
            )) & (df.rate == rateVar.get())], label='Lab')
            legend.append(i)
    else:
        for i in y:
            plot1.plot(sorted(df.date[(df.areaName ==
                                       i) & (df.rate == rateVar.get(
                                        ))]), df['total'][(df.areaName == i) &
                                                          (df.rate ==
                                                          rateVar.get(
                                                           ))], label='Lab')
            legend.append(i)

    plot1.get_figure().autofmt_xdate()
    plot1.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    if compVar.get() == 'Age':
        plot1.set_title(
            f'{rateVar.get()} case of COVID-19 in {regBox.get()} by {compVar.get()}')
    else:
        plot1.set_title(f'{rateVar.get()} case of COVID-19 by {compVar.get()}')
    plot1.legend(legend)
    canvas.draw()


def compL():
    var = compLocVar.get()
    compList.delete(0, END)
    values = sorted(list(set(df.areaName[df.areaType == var])))
    compBox.set(values[0])
    compBox.config(values=values)


def plotComp():
    che = compList.get(0, tkinter.END)
    compChart(che)


compF = ttk.Frame(tab1)
compF.grid(column=0)
compF.columnconfigure(0, weight=1)

compLab = ttk.Label(compF, text='Compare by:')
compLab.grid(row=0, column=0, pady=5, padx=5)

compBox = ttk.Combobox(compF, values=agegroup)
compBox.set(agegroup[0])
compBox.grid(row=2, column=0, columnspan=5, pady=5)
compBox.bind("<<ComboboxSelected>>", fillList)
compList = Listbox(compF)
compList.grid(row=3, column=0, columnspan=5)
compList.bind("<<ListboxSelect>>", remOpt)

compAgeLab = ttk.Label(compF, text='Age')
compAgeLab.grid(row=0, column=1)
compVar = StringVar()
compVar.set('Age')
compAge = ttk.Radiobutton(compF, variable=compVar, value='Age', command=comp)
compAge.grid(row=0, column=2)
compLocLab = ttk.Label(compF, text='Location')
compLocLab.grid(row=0, column=3)
compLoc = ttk.Radiobutton(compF, variable=compVar, value='Location',
                          command=comp)
compLoc.grid(row=0, column=4)

compRegF = ttk.Frame(compF)
compRegionLab = ttk.Label(compRegF, text='Region').grid(row=0, column=0)
compLocLab = ttk.Label(compRegF, text='LTLA').grid(row=0, column=2)
compLocLab2 = ttk.Label(compRegF, text='UTLA').grid(row=0, column=4)

compLocVar = StringVar()
compRegionRad = ttk.Radiobutton(compRegF, variable=compLocVar, value='Region',
                                command=compL).grid(row=0, column=1)
compLocRad = ttk.Radiobutton(compRegF, variable=compLocVar, value='LTLA',
                             command=compL).grid(row=0, column=3)
compLocRad2 = ttk.Radiobutton(compRegF, variable=compLocVar, value='UTLA',
                              command=compL).grid(row=0, column=5)

compBtn = ttk.Button(compF, text='Compare', command=plotComp)
compBtn.grid(column=0, row=4, columnspan=5, pady=15)

# Compare End ...............................................................


# Bottom Layout
lTail = ttk.Label(fTail, text='A0218247: Tolulope Jegede'
                  ).grid(row=0, column=0, sticky=E, padx=10)


# Plot Section Starts ------------------------------------------------------
def plot(view):
    global df
    global regBox
    global plot1
    global canvas
    fig = Figure(figsize=(7.5, 5.5),
                 dpi=100)
    x = sorted(df.date[(df.areaName == regBox.get()) & (df.rate == rateVar.get(
    )) & (df.date >= dateFrom.get()) & (df.date <= dateTo.get())])
    y = df.total[(df.areaName == regBox.get()) & (df.rate == rateVar.get(
    )) & (df.date >= dateFrom.get()) & (df.date <= dateTo.get())]
    plot1 = fig.add_subplot(111)
    plot1.plot(x, y)
    fig.autofmt_xdate()
    plot1.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    plot1.set_title(f'{rateVar.get()} case of COVID-19 in {regBox.get()}')
    canvas = FigureCanvasTkAgg(fig,
                               master=view)
    canvas.draw()
    canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(canvas,
                                   view)
    toolbar.update()
    canvas.get_tk_widget().pack()


def pplot(view):
    global plotP
    global canvasp
    age = fplot(monthComb.get(), yearComb.get(), policeBox.get(), viewBox.get(
    ))
    fig = Figure(figsize=(7.5, 5.5),
                 dpi=100)
    x = age.keys()
    y = age.values()

    plotP = fig.add_subplot(111)
    plotP.bar(x, y)

    plotP.set_title(
                    f'{view2.get()} distripution for {monthComb.get()}, {yearComb.get()}')
    canvasp = FigureCanvasTkAgg(fig,
                                master=view)
    canvasp.draw()
    canvasp.get_tk_widget().pack()
    toolbarp = NavigationToolbar2Tk(canvasp,
                                    view)
    toolbarp.update()
    canvasp.get_tk_widget().pack()


def pplotBtn():
    global plotP
    global canvasp
    dat = fplot(monthComb.get(), yearComb.get(), policeBox.get(), viewBox.get())
    x = dat.keys()
    y = dat.values()
    plotP.clear()
    plotP.bar(x, y)

    plotP.set_title(f'{viewBox.get()} distripution for {policeBox.get()} in {monthComb.get()}, {yearComb.get()}')
    canvasp.draw()


def explotBtn():
    global plotP
    global canvasp
    plotP.clear()
    legend = list()
    dat = cplot(frmonthComb.get(), int(fryearComb.get()), tomonthComb.get(),
                int(toyearComb.get()), ppoliceBox.get(), ppviewBox.get())

    for i in dat.Par.tolist():
        plotP.plot(sorted(dat.Date[dat.Par == i]), dat.Count[dat.Par == i])
        legend.append(i)
    plotP.legend(set(legend))
    plotP.set_title(f'{viewBox.get()} by {policeBox.get()} from {frmonthComb.get()}, {fryearComb.get()} to  {tomonthComb.get()}, {toyearComb.get()}')
    canvasp.draw()


# Tab 2 Starts ---------------------------------------------------------------
lTab2 = ttk.Label(tab2, text='Search by:').grid(row=0, column=0)

monthV = ttk.Frame(tab2)
monthV.grid(columnspan=5, row=2)
periodV = ttk.Frame(tab2)


def switch():
    var = view2.get()
    if var == 'Month':
        periodV.grid_remove()
        monthV.grid()
    else:
        monthV.grid_remove()
        periodV.grid(columnspan=5, row=2)


view2 = StringVar()
view2.set('Month')
monthOV = ttk.Label(tab2, text='Month overview').grid(row=0, column=1)
periodLab = ttk.Label(tab2, text='Period').grid(row=0, column=3)
monthRad = ttk.Radiobutton(tab2, variable=view2, value='Month', command=switch)
monthRad.grid(row=0, column=2)
periodRad = ttk.Radiobutton(tab2, variable=view2, value='Period',
                            command=switch)
periodRad.grid(row=0, column=4)

# infoM = ttk.Label(monthV, text='Choose month you want to view').grid()
infoP = ttk.Label(periodV, text='Choose period').grid()

monLab = ttk.Label(monthV, text='Month:').grid(row=1, column=0)
yearLab = ttk.Label(monthV, text='Year:').grid(row=2, column=0)
policeLab = ttk.Label(monthV, text='Police:').grid(row=3, column=0)
viewLab = ttk.Label(monthV, text='View by:').grid(row=4, column=0)

months = [i for i in list(calendar.month_name) if i != '']
years = list(range(2019, 2022))
policeVar = [i for i in do().keys()]
viewVar = ['Age', 'Gender', 'Ethnic', 'Stop Purpose', 'Outcome']

monthComb = ttk.Combobox(monthV, values=months)
monthComb.set(months[0])
monthComb.grid(row=1, column=1)
yearComb = ttk.Combobox(monthV, values=years)
yearComb.set(years[0])
yearComb.grid(row=2, column=1)


policeBox = ttk.Combobox(monthV, values=policeVar)
policeBox.set(policeVar[0])
policeBox.grid(row=3, column=1)

viewBox = ttk.Combobox(monthV, values=viewVar)
viewBox.set(viewVar[0])
viewBox.grid(row=4, column=1)


fromLab = ttk.Label(periodV, text='From:').grid(row=1, column=0)
toLab = ttk.Label(periodV, text='To:').grid(row=2, column=0)
pviewLab = ttk.Label(periodV, text='Explore by:').grid(row=3, column=0)
ppoliceLab = ttk.Label(periodV, text='Force:').grid(row=4, column=0)

frmonthComb = ttk.Combobox(periodV, values=months)
frmonthComb.set(months[0])
frmonthComb.grid(row=1, column=1)
fryearComb = ttk.Combobox(periodV, values=years)
fryearComb.set(years[0])
fryearComb.grid(row=1, column=2)

tomonthComb = ttk.Combobox(periodV, values=months)
tomonthComb.set(months[0])
tomonthComb.grid(row=2, column=1)
toyearComb = ttk.Combobox(periodV, values=years)
toyearComb.set(years[0])
toyearComb.grid(row=2, column=2)

ppoliceBox = ttk.Combobox(periodV, values=policeVar)
ppoliceBox.set(policeVar[0])
ppoliceBox.grid(row=4, column=1)

ppviewBox = ttk.Combobox(periodV, values=viewVar)
ppviewBox.set(viewVar[0])
ppviewBox.grid(row=3, column=1, columnspan=2)


def pplt():
    var = view2.get()
    if var == 'Month':
        pplotBtn()
    else:
        explotBtn()


mplotBtn = ttk.Button(tab2, text='Plot', command=pplt)
mplotBtn.grid(row=5)

pplot(fPView)
plot(fCView)


# Plot Section Ends ......................................................

root.mainloop()
