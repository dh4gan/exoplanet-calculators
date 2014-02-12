#!/usr/local/bin/python
# Written by Duncan Forgan, 18th July 2012
# This code produces a Photon Wavelength/Frequency Calculator GUI
# We use the standard Tkinter toolkit which comes with pretty much all Python distributions

# We start by defining the GUI as a class (derived from the base class Frame), with methods
# to create the elements inside the window, and methods to handle events 

from Tkinter import Frame, Button, Entry, Listbox,Text, END,SINGLE,W

class photGUI(Frame):
    """The base class for the hill_calc GUI"""
    
    # This is the constructor for the GUI
    def __init__(self,master=None):
        # We begin by calling the base class's constructor first
        Frame.__init__(self,master)
    
        # We now have an empty window!
        
        # This command sets up a grid structure in the window
        self.grid()
        
        # This loop generates rows and columns in the grid
        for i in range(13):
            self.rowconfigure(i,minsize=10)
        for i in range(3):
            self.columnconfigure(i,minsize=30)
        
        # These are methods which appear below the constructor
        self.defineUnits() # this sets up the units I'll be using in the converter
        self.createWidgets() # this places the elements (or widgets) in the grid
        
        # This command "binds" the user's click to a method (varChoice)
        # This method will determine which variable the user wants (Distance, Mass, Time)
        self.inputlist.bind("<Button-1>",self.__varChoice)
    
        # This is a similar command for the selection of unit
        self.unitlist.bind("<Button-1>",self.__unitChoice)
    
        # Finally, this bind reads in whatever value is in the text box when the user hits return
        # and carries out the unit conversion
        
        self.inputfield.bind("<Return>",self.__calcConversion)
    
    # This function creates and defines the units
    
    def defineUnits(self):
        '''Method defines tuples that carry the various units stored by the converter'''
        
        self.speed = 2.997924580000019e10
        self.h = 6.6260755e-27     
        # Wavelengths
        
        self.wavunits = ('nm','um', 'cm','m')
        self.wavvalues = (1.0e-7, 1.0e-4,1.0,1.0e2)
        
        self.frequnits = ('Hz','MHz','GHz','THz')
        self.freqvalues = (1.0, 1.0e6, 1.0e9, 1.0e12)
        
        self.energunits = ('eV','keV','MeV','GeV','erg')
        self.energvalues = (1.0,1.0e3,1.0e6,1.0e9,1.6e-12)
        
        # Keep the unit values in dictionaries, and use the above strings as keys
        
        self.wavdict = {}        
        self.createUnitDict(self.wavdict,self.wavunits,self.wavvalues) # this method is shown below
        
        self.freqdict = {}
        self.createUnitDict(self.freqdict,self.frequnits,self.freqvalues)
        
        self.energdict = {}
        self.createUnitDict(self.energdict, self.energunits, self.energvalues)  
    
        self.myunits = self.wavunits
        self.myvalues = self.wavvalues
        self.mydict = self.wavdict
    
        
    def createUnitDict(self,mydict,mykeys,myvalues):
        '''This method takes a set of units and values, and creates a dictionary to store them in'''
        for i in range(len(myvalues)):
            mydict[mykeys[i]] = myvalues[i]
               
    def createWidgets(self):
        '''This method creates all widgets and adds them to the GUI'''
        
        # Create Widgets in order of appearance
        # This is not necessary, but makes code easier to read
        
        # Start with text telling user what to do
        self.varlabel = Text(self,height=1, width=20)
        self.varlabel.insert(END,"Which Variable?")
        
        # Place widget on the Frame according to a grid
        self.varlabel.grid(row=0,column=0,sticky=W)
        
        # Second text label asking user which units are being used
        self.unitlabel = Text(self,height=1,width=20)
        self.unitlabel.insert(END,"Which Units?")
        self.unitlabel.grid(row=0,column=1,sticky=W)
        
        # Third text label asking user for numerical value
        
        self.numlabel = Text(self,height=1, width=20)
        self.numlabel.insert(END,"Enter Variable Values")
        self.numlabel.grid(row=0,column=2,sticky=W)
        
        # This creates a list of options for the user to select
        self.inputlist = Listbox(self, height=4, selectmode=SINGLE)
      
        # Tuple of choices we're going to put in this list
        self.paramlist = ('Frequency', 'Wavelength', 'Energy')
        
        # Add each item separately
        for item in self.paramlist:
            self.inputlist.insert(END,item)
            
        # Add it to the grid    
        self.inputlist.grid(row=1, column=0,rowspan=4,sticky=W)
        
        # Add a unit list (several combinations of units allowed)
        
        self.unitlist = Listbox(self, height=4,selectmode=SINGLE)
        self.unitlist.grid(row=1,column=1,rowspan=4, sticky=W)
    
        # Number Entry Boxes (and Text Labels)
        
        self.inputlabel = Text(self,height=1,width=20)
        self.inputlabel.insert(END,"Waiting Selection")
        self.inputlabel.grid(row=1,column=2,sticky=W)
        
        self.inputfield = Entry(self)
        self.inputfield.grid(row=2,column=2,sticky=W)
        
        # Text Output Boxes
        self.wavoutput = Text(self, height=5, width=20)
        self.wavoutput.grid(row=7,column=0,rowspan=5,sticky=W)
        self.wavoutput.insert(END, "Wavelength: \n")
        
        self.freqoutput = Text(self, height=5, width=20)
        self.freqoutput.grid(row=7,column=1,rowspan=5,sticky=W)
        self.freqoutput.insert(END, "Frequency: \n")
        
        self.energoutput = Text(self, height=5, width=20)
        self.energoutput.grid(row=7,column=2,rowspan=5,sticky=W)
        self.energoutput.insert(END, "Energy: \n")
        
        # Create the Quit Button
        self.quitButton=Button(self,text='Quit',command=self.quit)
        self.quitButton.grid(row =13, column=0, sticky=W)
             

    # Event handler functions begin here    
    # This handler defines the choice of units available to the user, 
    # depending on selected variable
    
    def __varChoice(self, event):
        '''Handles the selection of variable: updates the list of units'''
        # Firstly, delete anything already in the units column
        self.unitlist.delete(first=0,last=len(self.myvalues))
        num = 0
        
        # Identify which option was clicked on
        try:
            num = self.inputlist.curselection()[0]       
            self.varchoice = int(num)
            
        except:
            self.varchoice = 0
            return
        
        # Get the string associated with this choice
        selection= self.inputlist.get(self.varchoice)
        
        print selection, " chosen"
        
        # Highlight current choice in red
        self.inputlist.itemconfig(self.varchoice, selectbackground='red')
        
        # If statement defines units being used
        if selection =='Wavelength':
            self.myunits = self.wavunits
            self.myvalues = self.wavvalues
            self.mydict = self.wavdict
        elif selection == 'Frequency':
            self.myunits = self.frequnits
            self.myvalues = self.freqvalues
            self.mydict = self.freqdict
        elif selection == 'Energy':
            self.myunits = self.energunits
            self.myvalues = self.energvalues
            self.mydict = self.energdict
            
        
        self.inputlabel.delete("1.0",index2=END)
        self.inputlabel.insert(END,selection)
        
        
        for i in range(len(self.myunits)):
            self.unitlist.insert(END,self.myunits[i])
        
    def __unitChoice(self,event):
        '''Handles the selection of units'''
        num = 0
        # Find which number is selected
        try:
            num = self.unitlist.curselection()[0]       
            self.unitchoice = int(num)
            
        except:
            self.unitchoice = 0
            return
        
        # Get the string (i.e. which unit is selected)
        selection= self.unitlist.get(self.unitchoice)
        
        print selection, " chosen"
        
        # Highlight current choice in red
        self.unitlist.itemconfig(self.unitchoice, selectbackground='red')
        
    # Handler takes current state of GUI, and calculates results
    def __calcConversion(self,event):
        '''This method takes the current state of all GUI variables, calculates one of four equations'''
        
        # Which variable has been selected for calculation?
        # This decides what equation to use
        
        a = self.inputfield.get()
        var = self.unitlist.get(self.unitchoice)
        a=float(a)
        
        freq = 0.0
        wav = 0.0
        energy = 0.0
        
        if self.varchoice==0:
            freq = a
            freq = freq*self.mydict[var]
            wav = self.speed/freq
            energy = self.h*freq/self.energdict['erg']
            
        elif self.varchoice==1:
            wav = a
            wav = wav*self.mydict[var]
            freq = self.speed/wav
            energy = self.speed*self.h/wav
            
        elif self.varchoice==2:
            energy = a
            energy=energy*self.energdict["erg"]
            freq = energy/self.h
            wav = self.speed*self.h/energy
            energy = energy*self.mydict[var]/self.energdict["erg"]
        
        # Remove all text in the output boxes
        self.wavoutput.delete("1.0",index2=END)
        self.freqoutput.delete("1.0",index2=END)
        self.energoutput.delete("1.0",index2=END)
        
        self.wavoutput.insert(END, "Wavelength: \n")
        self.freqoutput.insert(END, "Frequency: \n")
        self.energoutput.insert(END, "Energy: \n")
        
        # Calculate each conversion and output it to the GUI
        for i in range(len(self.wavvalues)):
            # As all units stored in cgs values, conversion is simple
            output = wav/self.wavvalues[i]
            
            # Express output in 
            
            # Add to the output list
            self.wavoutput.insert(END,self.wavunits[i] + ":  %.4e" % output+"\n")  
            
            
        for i in range(len(self.freqvalues)):
            # As all units stored in cgs values, conversion is simple
            output = freq/self.freqvalues[i]
            # Add to the output list
            self.freqoutput.insert(END,self.frequnits[i] + ":  %.4e" % output+"\n")        
            
        for i in range(len(self.energvalues)):
            # As all units stored in cgs values, conversion is simple
            output = energy/self.energvalues[i]
            # Add to the output list
            self.energoutput.insert(END,self.energunits[i] + ":  %.4e" % output+"\n")       
            
# End of methods and class definition
# Main program begins here            
app = photGUI() # Call the exo class
app.master.title("Photon Property Calculator") # Give it a title
app.mainloop() # This command allows the GUI to run until a terminate command is issued (e.g. the user clicks "Quit")
    