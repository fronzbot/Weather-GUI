#!/bin/python

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from decimal import *

import pywapi
import math
import time
import urllib
import shutil
import io
import pickle
import os

###################################################
###        THESE NEED TO BE IMPLEMENTED         ###
###################################################

    
def chooseStyle():
    # Allow user to select from a list
    # of preconfigured window stlyles
    print("CHOOSE STYLE")

def sendNewConfig():
    # Send current color configuration
    # information over serial to device.
    # Display pop-up indicating success/fail
    print("SEND CONFIG")

def viewMonitor():
    # Display pop-up window that shows
    # information being sent and info
    # being recieved over serial
    print("MONITOR")

def logSerialData():
    # Log all serial send and receive
    # events in a log file.
    # Used for debugging
    print("LOGGING DATA")

def openLog():
    # Open a saved .log file for viewing
    print("OPEN LOG")

def setLocation():
    # Popup window to choose location
    setlocwindow = Toplevel(root)
    setlocwindow.title('Set Location')
    setlocwindow.lift(root)
    setlocwindow.protocol('WM_DELETE_WINDOW', setlocwindow.withdraw)
    setlocwindow.resizable(0,0)



def tutorial():
    # Popup window with detailed tutorial on
    # how to use the program with the hardware
    print("TUTORIAL")
        
########################################################
########################################################
def basicStyle():
    locframe.grid_remove()
    mainframe.pack(fill=BOTH,expand=True)
    
def defaultStyle():
    locframe.grid()
    mainframe.pack(fill=BOTH,expand=True)
    
def chooseUnits():
    city = ''.join(cityEntry.get().split())
    currentLoc = ['', country.get(),
                  state.get(), cityEntry.get()]
    stateChoice = findCountry()
    
    if stateChoice[0]:
        currentLoc[0] = city+','+stateChoice[1]
    else:
        currentLoc[0] = city+','+country.get()
        
    weatherParse(currentLoc, False)
    
def updateRecentLoc():
    x=0
    for i in range(-1,-6,-1):
        try:
            recentlocmenu.entryconfig(x, label=pastFiveLoc[i][0], state=NORMAL)
        except:
            pass
        x = x+1

# Takes in location list and parses weather data,
# reprints screen and logs data
def weatherParse(loc, logLocation):
    "loc = ['weather location','country','state','city']"
    if loc[0] is not '':
        try:
            weather = pywapi.get_weather_from_google(loc[0])
            noError = True
            cityWeather.set(loc[0])
            country.set(loc[1])
            state.set(loc[2])
            cityEntry.config(state=NORMAL)
            cityEntry.delete(0, END)
            cityEntry.insert(0,loc[3])
            if loc[2] != '----------':
                state['values']=listDict[country.get()]
        except urllib.error.HTTPError:
            noError = False
            errorMessage('URL')
        except NameError as n:
            noError = False
            errorMessage('NAME')
            
        if noError:
            temp = int(weather['current_conditions']['temp_f'])
            tMaj = ttk.Label(majortempframe, textvariable=majortemp,
                          foreground=getTempColor(temp), font='Tahoma 42 bold')
            tMajUnit = ttk.Label(majortempframe, textvariable=majTempUnit,
                                 foreground=getTempColor(temp), font='Tahoma 16 bold')
            tMin = ttk.Label(minortempframe, textvariable=minortemp,
                          foreground=getTempColor(temp), font='Tahoma 12 bold')
            tMaj.grid(column=0,row=0,sticky=W)
            tMajUnit.grid(column=1,row=0,sticky=(S,W))
            tMin.grid(column=0,row=1,sticky=E)
            
            
            if tempUnits.get() == 'F':
                majortemp.set(weather['current_conditions']['temp_f'])
                majTempUnit.set('F')
                minortemp.set('('+weather['current_conditions']['temp_c']+' C)')
                
            elif tempUnits.get() == 'C':
                majortemp.set(weather['current_conditions']['temp_c'])
                majTempUnit.set('C')
                minortemp.set('('+weather['current_conditions']['temp_f']+' F)')
                
            condition.set(weather['current_conditions']['condition'])
            setConditionImage(weather['current_conditions']['icon'])
            humidity.set(weather['current_conditions']['humidity'].split(':')[1])
            windSpeed.set(weather['current_conditions']['wind_condition'].split(':')[1])
            
    if logLocation:
        if pastFiveLoc[0][0] == '':
            pastFiveLoc[0] = loc
                
        elif (len(pastFiveLoc) >= 5):
            for i in range(0,4):
                pastFiveLoc[i] = pastFiveLoc[i+1]
            pastFiveLoc[4] = loc
        else:
            pastFiveLoc.append(loc)
        
        locationLog = io.open('data/loc.dat',mode='wb')
        pickle.dump(pastFiveLoc[0:],locationLog,3)
        locationLog.close()
        updateRecentLoc()        

def setConditionImage(condImage):
    global imageObj
    
    hour = int(time.ctime().split()[3].split(':')[0])
    if (hour >= 7) and (hour <= 19):
        timeOfDay = 'day/'
    else:
        timeOfDay = 'night/'
        
    condImage = condImage.split('/')[-1]
    if condImage == '':
        imageObj = PhotoImage(file='images/unknown.gif')
    else:
        condImage = 'images/'+timeOfDay+condImage
        if os.path.exists(condImage):
            imageObj = PhotoImage(file=condImage)
        else:
            imageObj = PhotoImage(file='images/unknown.gif')
    conditioncanvas.create_image(25,25,image=imageObj)
        
    

def locOne():
    weatherParse(pastFiveLoc[-1], True)

def locTwo():
    weatherParse(pastFiveLoc[-2], True)

def locThree():
    weatherParse(pastFiveLoc[-3], True)

def locFour():
    weatherParse(pastFiveLoc[-4], True)

def locFive():
    weatherParse(pastFiveLoc[-5], True)


    
###################
### Color class ###
###################
class Color:
    def __init__(self, color):
        
        self.color = color

    def set_color(self, color):
        self.color = color

# Open new window for color selection
def editColors(*args):
    colorWindow.deiconify()

# Load a saved color configuration file
def loadColorFile():
    # Allow user to load color config
    # information.  Can only load .cfg
    types = [('Configuration File', '.cfg'),('All Files', '.*')]
    loadFile = filedialog.askopenfilename(initialdir='config', filetypes=types)

    if loadFile == '':
        pass
    elif loadFile[-4:] != '.cfg':
        errorMessage('LOAD')
    else:
        f = open(loadFile,'rb')
        userColors = pickle.load(f)
        f.close()

        if userColors[0] != '':
            veryCold.color = userColors[0]
        if userColors[1] != '':
            cold.color = userColors[1]
        if userColors[2] != '':
            cool.color = userColors[2]
        if userColors[3] != '':
            neutral.color = userColors[3]
        if userColors[4] != '':
            warm.color = userColors[4]
        if userColors[5] != '':
            hot.color = userColors[5]
        if userColors[6] != '':
            scorching.color = userColors[6]
        f = open('config/user.dat','wb')
        pickle.dump(userColors, f)
        f.close()
        setBarPos()
        getWeather()  

#Set state options after choosing country
def setStates(*args):
    cityEntry.delete(0, END)
    cityEntry.config(state=DISABLED)
    countryChoice = country.get()
    if countryChoice == 'United States of America':
        state.set('CHOOSE STATE')
    elif countryChoice == 'Canada':
        state.set('CHOOSE PROVINCE')
    elif countryChoice == 'Australia':
        state.set('CHOOSE TERRITORY')
    else:
        state.set('----------')
        cityEntry.config(state=NORMAL)
    state['values']=listDict[countryChoice]

#Should grey out city entry until country selected- does not work currently
def allowCity(*args):
    cityEntry.config(state=NORMAL)

def findCountry():
    stateChoice = state.get()
    if stateChoice in USStates[0:]:
        stateChoice = StateAbbr[stateChoice]
        return [True, stateChoice]
    elif stateChoice in AUProvince[0:]:
        stateChoice = AUAbbr[stateChoice]
        return [True, stateChoice]
    elif stateChoice in CANProvince[0:]:
        return [True, stateChoice]
    else:
        return [False, stateChoice]
    
#Gets weather for city choice    
def getWeather(*args):
    global pastFiveLoc

    countryChoice = country.get()
    stateChoice = state.get()
    city = cityEntry.get()


    #Allows for spaces in city entry field
    cityChoice = ''.join(city.split())
    
    stateChoice = findCountry()
    location = ['',
                countryChoice,
                state.get(),
                cityChoice]        
    if stateChoice[0]:
        location[0] = cityChoice+','+stateChoice[1]           
    else:
        location[0] = cityChoice+','+countryChoice

    weatherParse(location, True)

##########################      
### Get Color For Temp ###
########################## 
def getTempColor(temp):
    global currentColorsList

    if temp in range(-60,20):
        colorCode = veryCold.color 
        userColors[0]=colorCode
        tempToSet = 'Very Cold'

    if temp in range(20,40):
        colorCode = cold.color 
        userColors[1]=colorCode
        tempToSet = 'Cold'

    if temp in range(40,55):
        colorCode = cool.color
        userColors[2]=colorCode
        tempToSet = 'Cool'

    if temp in range(55,68):
        colorCode = neutral.color 
        userColors[3]=colorCode
        tempToSet = 'Neutral'

    if temp in range(68,77):
        colorCode = warm.color 
        userColors[4]=colorCode
        tempToSet = 'Warm'

    if temp in range(77,89):
        colorCode = hot.color
        userColors[5]=colorCode
        tempToSet = 'Hot'

    if temp in range(89,120):
        colorCode = scorching.color
        userColors[6]=colorCode
        tempToSet = 'Scorching'

    if temp not in range(-60,120):
        colorCode = '#000000'

    if colorTemp.get() == 'CHOOSE TEMP COLOR':
        colorTemp.set(tempToSet)
        setBarPos()
    
    return colorCode



###################################################
###  Formats Slider Position into Color String  ###
###################################################
def sliderPosition(*args):
    global currentColorsList
    global veryCold,cold,cool,neutral,warm,hot,scorching
    
    redPos = redbar.get()
    greenPos = greenbar.get()
    bluePos = bluebar.get()
    
    redbar.set(redPos)
    greenbar.set(greenPos)
    bluebar.set(bluePos)

    redPos = int(redPos)
    greenPos = int(greenPos)
    bluePos = int(bluePos)
    
    getcontext().prec=4
    slideColorCode = str.format('#{0:02x}{1:02x}{2:02x}',
                          int(redPos),int(greenPos),int(bluePos))

    chosenTemp = colorTemp.get()
    
    tempDict = {'Very Cold':[veryCold, 0],'Cold':[cold, 1],'Cool':[cool, 2],
                'Neutral':[neutral, 3],'Warm':[warm, 4],'Hot':[hot, 5],
                'Scorching':[scorching, 6]}
    tempDict[chosenTemp][0].set_color(slideColorCode)
    userColors[tempDict[chosenTemp][1]] = slideColorCode
    colorbox.create_rectangle('1 1 1 1', outline=slideColorCode,width=100)
    getWeather()

###########################################
###  Loads color information from file  ###
###########################################
def setColor(*args):
    types = [('Configuration File', '.cfg'),('All Files', '.*')]
    saveFile = filedialog.asksaveasfilename(defaultextension='.cfg',initialdir='config',
                                            initialfile='mycolors.cfg', filetypes=types)

    if saveFile != '':
        save = open(saveFile,'wb')
        pickle.dump(userColors, save, 3)
        save.close()
        colorLocFile = open('config/user.dat', 'wb')
        pickle.dump(userColors, colorLocFile, 3)
        colorLocFile.close()
        setBarPos()
        colorWindow.withdraw()


##############################
###  Loads default colors  ###
##############################
def defaultColor(*args):
    veryCold.color = '#003399'
    cold.color = '#0000FF'
    cool.color = '#00CCCC'
    neutral.color = '#228B22'
    warm.color = '#FFCC00'
    hot.color = '#FF7518'
    scorching.color = '#FF0000'
    colors = [veryCold.color, cold.color, cool.color,
              neutral.color, warm.color, hot.color,
              scorching.color]
    f = open('config/user.dat', 'wb')
    pickle.dump(colors, f, 3)
    f.close()

    setBarPos()
    getWeather()


###############################################
###  Sets bar position based on color info  ###
###############################################
def setBarPos(*args):
    chosenTemp = colorTemp.get()
    tempDict = {'Very Cold':veryCold.color,'Cold':cold.color,'Cool':cool.color,
                'Neutral':neutral.color,'Warm':warm.color,'Hot':hot.color,
                'Scorching':scorching.color}
    
    red_pos = int(tempDict[chosenTemp][1:3],16)
    green_pos = int(tempDict[chosenTemp][3:5],16)
    blue_pos = int(tempDict[chosenTemp][5:],16)

    redbar.set(red_pos)
    greenbar.set(green_pos)
    bluebar.set(blue_pos)
    
    colorbox.create_rectangle('1 1 1 1', outline=tempDict[chosenTemp],width=100)


#########################
###  Displays README  ###
#########################
def helpMenu():
    readme = open('README.txt','r')
    readmeText = readme.readlines()
    displayText = ''
    for i in range(len(readmeText)):
        displayText = displayText + readmeText[i]
        
    messagebox.showinfo(message='--About',detail=displayText,
                        icon='info',title='About',default='ok',parent=root)

################################
###  Error Message Handling  ###
################################
def errorMessage(error):
    errList = ['Invalid Location',
               'Could not retrieve weather data',
               'File type mismatch! Must load .cfg file',
               'Unknown error!']    

    errorDict = {'NAME':errList[0],
                 'URL':errList[1],
                 'LOAD':errList[2]}

    if error not in errorDict:
        errorMsg = errList[3]
    else:
        errorMsg = errorDict[error]

    messagebox.showinfo(message='ERROR',detail=errorMsg,
                        icon='error',default='ok',parent=root)


##############################################
##############################################
####            Program Setup             ####
##############################################
##############################################

    
root = Tk()
root.title("Weather Getter")
root.wm_iconbitmap('images/weather.ico')
root.resizable(0,0)

#######################
### Lists and Dicts ###
#######################

dataFile = open('data/data.dat','rb')
allLocaleData = pickle.load(dataFile)

USStates = allLocaleData[0]
CANProvince = allLocaleData[1]
AUProvince = allLocaleData[2]
AUAbbr = allLocaleData[3]
StateAbbr = allLocaleData[4]

listDict = {'Australia':AUProvince[0:],'Austria':'',
            'Canada':CANProvince[0:],'England':'',
            'Germany':'','Greece':'','Ireland':'',
            'Italy':'','Netherlands':'','Poland':'',
            'Russia':'','United States of America':USStates[0:],
            'CHOOSE COUNTRY':'','':''}

# Get Previous locations
pastFiveLoc = [['']]
try:
    f = open('data/loc.dat','rb')
    pastFiveLoc = pickle.load(f)
    f.close()
except IOError:
    pastFiveLoc = [['']]
except EOFError:
    f.close()
    os.remove('data/loc.dat')


####################
### Set up Frame ###
####################
mainframe = ttk.Frame(root, padding="3 3 3 3")
mainframe.pack()

locframe = ttk.Frame(mainframe, padding = "5 5 5 5", relief="groove")
locframe.grid(column=0, row=0, sticky=(N,W))
locframe.columnconfigure(0, weight=1)
locframe.rowconfigure(0, weight=1)

mainweatherframe = ttk.Frame(mainframe, padding="5 5 5 5", relief="groove")
mainweatherframe.grid(column=1, row=0, sticky=N)
mainweatherframe.columnconfigure(1, weight=1)
mainweatherframe.rowconfigure(0, weight=1)

majortempframe = ttk.Frame(mainweatherframe, padding="5 5 5 5", relief="sunken")
majortempframe.grid(column=1, row=1, sticky=N)
majortempframe.columnconfigure(1, weight=1)
majortempframe.rowconfigure(1, weight=1)
minortempframe = ttk.Frame(majortempframe, padding="5 5 5 5")
minortempframe.grid(column=2, row=0,sticky=E)
majortempframe.columnconfigure(2, weight=1)
majortempframe.rowconfigure(0, weight=1)

weatherframe = ttk.Frame(mainweatherframe, padding="5 5 5 5")
weatherframe.grid(column=1, row=2, sticky=(N,E))
weatherframe.columnconfigure(1, weight=1)
weatherframe.rowconfigure(2, weight=1)




###################
### Set up Menu ###
###################
root.option_add('*tearOff', FALSE)
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Set Location", command=setLocation)

#Recent Locations
recentlocmenu = Menu(filemenu, tearoff=0, postcommand=updateRecentLoc)
recentlocmenu.add_command(label=pastFiveLoc[-1][0], command=locOne)
try:
    recentlocmenu.add_command(label=pastFiveLoc[-2][0], command=locTwo)
except IndexError:
    recentlocmenu.add_command(label='', command=locTwo, state=DISABLED)

try:
    recentlocmenu.add_command(label=pastFiveLoc[-3][0], command=locThree)
except IndexError:
    recentlocmenu.add_command(label='', command=locThree, state=DISABLED)

try:
    recentlocmenu.add_command(label=pastFiveLoc[-4][0], command=locFour)
except IndexError:
    recentlocmenu.add_command(label='', command=locFour, state=DISABLED)

try:
    recentlocmenu.add_command(label=pastFiveLoc[-5][0], command=locFive)
except IndexError:
    recentlocmenu.add_command(label='', command=locFive, state=DISABLED)
    
filemenu.add_cascade(label="Recent Locations", menu=recentlocmenu)
###
filemenu.add_separator()
filemenu.add_command(label="Save Color Configuration", command=setColor)
filemenu.add_command(label="Load Color Configuration", command=loadColorFile)
filemenu.add_command(label="Load Default Colors", command=defaultColor)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=quit)
menubar.add_cascade(label="File", menu=filemenu)

optionsmenu = Menu(menubar, tearoff=0)
style = StringVar()
stylemenu = Menu(optionsmenu, tearoff=0)
stylemenu.add_radiobutton(label="Default", variable=style,
                          value="default", command=defaultStyle)
stylemenu.add_radiobutton(label="Basic", variable=style,
                          value="basic", command=basicStyle)
style.set("default")
optionsmenu.add_cascade(label="Select Window Style", menu=stylemenu)
menubar.add_cascade(label="Options", menu=optionsmenu)
optionsmenu.add_separator()
tempUnits = StringVar()
optionsmenu.add_radiobutton(label='Celcius', variable=tempUnits,
                            value='C', command=chooseUnits)
optionsmenu.add_radiobutton(label='Farenheit', variable=tempUnits,
                            value='F', command=chooseUnits)
tempUnits.set('F') 
optionsmenu.add_separator()

optionsmenu.add_command(label="Choose Colors", command=editColors)


serialmenu = Menu(menubar, tearoff=0)
serialmenu.add_command(label="Send Color Config", command=sendNewConfig)
serialmenu.add_separator()
serialmenu.add_command(label="Open Log...", command=openLog)
serialmenu.add_command(label="Log Serial Data", command=logSerialData)
serialmenu.add_separator()
serialmenu.add_command(label="View Monitor", command=viewMonitor)
menubar.add_cascade(label="Serial", menu=serialmenu)            

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Tutorial", command=tutorial)
helpmenu.add_command(label="About", command=helpMenu)
menubar.add_cascade(label="Help", menu=helpmenu)
root.config(menu=menubar)



#################
### Variables ###
#################
okToGetColor = False
veryCold = Color('#003399')
cold = Color('#0000FF')
cool = Color('#00CCCC')
neutral = Color('#228B22')
warm = Color('#FFCC00')
hot = Color('#FF7518')
scorching = Color('#FF0000')
userColors = [veryCold.color, cold.color, cool.color,
              neutral.color,warm.color,hot.color,
              scorching.color]

slideColorCode = Color('#FFFFFF')


cityWeather = StringVar()
majortemp = StringVar()
minortemp = StringVar()
majTempUnit = StringVar()
condition = StringVar()
humidity = StringVar()
windSpeed = StringVar()

countryVar = StringVar()
stateVar = StringVar()
cityVar = StringVar()
countrySelection = StringVar()
stateSelection = StringVar()
citySelection = StringVar()



#####################
### Set up Labels ###
#####################
ttk.Label(locframe, text="Country").grid(column=0,row=1,sticky=W)
ttk.Label(locframe, text="State/Province").grid(column=0, row=3, sticky=W)
ttk.Label(locframe, text="City").grid(column=0,row=5,sticky=W)
ttk.Label(weatherframe, text="Humidity:", font=("Tahoma 8 bold")).grid(column=0,row=3,sticky=E)
ttk.Label(weatherframe, text="Wind:", font=("Tahoma 8 bold")).grid(column=0,row=4,sticky=E)

# For weather conditions
cityweatherlabel = ttk.Label(mainweatherframe, textvariable=cityWeather, font=("Tahoma 10 bold")).grid(column=1,row=0,sticky=N)
weatherconditionlabel = ttk.Label(weatherframe, textvariable=condition, font=("Tahoma 9 bold")).grid(column=0,row=1,sticky=E)
weatherhumiditylabel = ttk.Label(weatherframe, textvariable=humidity, font=("Tahoma 9")).grid(column=1,row=3,sticky=W)
weatherwindlabel = ttk.Label(weatherframe, textvariable=windSpeed, font=("Tahoma 9")).grid(column=1,row=4,sticky=W)
conditioncanvas = Canvas(weatherframe, width=50, height=50)
conditioncanvas.grid(column=1, row=1,sticky=N)


#########################
### Set up Comboboxes ###
#########################
country = ttk.Combobox(locframe, textvariable=countryVar, state="readonly")
country.grid(column=0,row=2)
country['values']=('Australia','Austria','Canada','England','Germany','Greece','Ireland',
                   'Italy','Netherlands','Poland','Russia','United States of America')
country.set('CHOOSE COUNTRY')
country.bind('<<ComboboxSelected>>',setStates)


state = ttk.Combobox(locframe, textvariable=stateVar, state="readonly")
state.grid(column=0,row=4)
state['values']=listDict[country.get()]
state.bind('<<ComboboxSelected>>',allowCity)

#############################
### Set up Select buttons ###
#############################
ttk.Label(locframe, textvariable=citySelection).grid(column=0,row=7,sticky=(W,E),pady=8)
getweatherbutton = ttk.Button(locframe, text="Get Weather", command=getWeather).grid(column=0,row=7,sticky=S)


#########################
### Set up City Entry ###
#########################
cityEntry = ttk.Entry(locframe, width=23, textvariable=cityVar, state=DISABLED)
cityEntry.grid(column=0, row=6, sticky=W)



#########################################
###  For Color Selction Popup Window  ###
#########################################

redVar = StringVar()
greenVar = StringVar()
blueVar = StringVar()
colorTempVar = StringVar()
setColorTempOK = StringVar()
saveColorVar = StringVar()

# Set uo new window and frames
colorWindow = Toplevel(root)
colorWindow.title('Choose Colors')
colorWindow.lift(root)
colorWindow.protocol('WM_DELETE_WINDOW', colorWindow.withdraw)
colorWindow.resizable(0,0)
sliderframe = ttk.Frame(colorWindow, padding = "5 5 5 5")
sliderframe.grid(column=0, row=0, sticky=W)
sliderframe.columnconfigure(0, weight=1)
sliderframe.rowconfigure(0, weight=1)
    
canvasframe = ttk.Frame(colorWindow)
canvasframe.grid(column=1,row=0)
canvasframe.columnconfigure(1, weight=1)
canvasframe.rowconfigure(0, weight=1)

#For colors
ttk.Label(sliderframe, text="R:", font=("Tahoma 8 bold")).grid(column=0,row=2,sticky=W)
ttk.Label(sliderframe, text="G:", font=("Tahoma 8 bold")).grid(column=0,row=3,sticky=W)
ttk.Label(sliderframe, text="B:", font=("Tahoma 8 bold")).grid(column=0,row=4,sticky=W)

colorTemp = ttk.Combobox(sliderframe, textvariable=colorTempVar, state="readonly")
colorTemp.grid(column=1, row=0, sticky=(N,W), pady=8)
colorTemp['values']=('Very Cold','Cold','Cool','Neutral','Warm','Hot','Scorching')
colorTemp.set('CHOOSE TEMP COLOR')
colorTemp.bind('<<ComboboxSelected>>', setBarPos)

ttk.Label(canvasframe, textvariable=saveColorVar).grid(column=0,row=2,sticky=S)
ttk.Button(canvasframe, text="Save Colors", command=setColor).grid(column=0,row=1,sticky=S,padx=5)


# Set up Color Selection 
redbar = ttk.Scale(sliderframe,from_=0,to=255,length=140,orient='horizontal',variable=redVar)
redbar.grid(column=1,row=2,sticky=W)
redbar.bind('<ButtonRelease-1>',sliderPosition)

greenbar = ttk.Scale(sliderframe,from_=0,to=255,length=140,orient='horizontal',variable=greenVar)
greenbar.grid(column=1,row=3,sticky=W)
greenbar.bind('<ButtonRelease-1>',sliderPosition)

bluebar = ttk.Scale(sliderframe,from_=0,to=255,length=140,orient='horizontal',variable=blueVar)
bluebar.grid(column=1,row=4,sticky=W)
bluebar.bind('<ButtonRelease-1>',sliderPosition)

# Set up Canvas    
colorbox = Canvas(canvasframe, width=50, height=50)
colorbox.grid(column=0, row=0)

colorWindow.withdraw()
    
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)


#Grabs saved Color data
try:
    f = open('config/user.dat','rb')
    userColors = pickle.load(f)
    f.close()
    if userColors[0] != '':
        veryCold.color = userColors[0]
    if userColors[1] != '':
        cold.color = userColors[1]
    if userColors[2] != '':
        cool.color = userColors[2]
    if userColors[3] != '':
        neutral.color = userColors[3]
    if userColors[4] != '':
        warm.color = userColors[4]
    if userColors[5] != '':
        hot.color = userColors[5]
    if userColors[6] != '':
        scorching.color = userColors[6]
except IOError:
    pass
except EOFError:
    f.close()
    if os.path.exists('config/user.dat'):
        os.remove('config/user.dat')


#Grabs previous location data
#Sets fields to display previous location data
try:
    f = open('data/loc.dat','rb')
    pastFiveLoc = pickle.load(f)
    f.close()
    if pastFiveLoc[-1][1] != 'United States of America':
        tempUnits.set('C')
        
    weatherParse(pastFiveLoc[-1], False)                   
except IOError:
    pass
except EOFError:
    f.close()
    if os.path.exists('data/loc.dat'):
        os.remove('data/loc.dat')

root.bind('<Return>',getWeather)
root.mainloop()

if __name__ is "__main__":
    setStates(*args)
    allowCity(*args)
    getWeather(*args)
    sliderPosition(*args)
    setColor(*args)
    setBarPos(*args)
    editColors(*args)

  

        
