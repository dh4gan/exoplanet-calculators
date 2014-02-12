#!/usr/local/bin/python
# Written by Duncan Forgan, 18th July 2012
# This code calculates Keplerian Velocities and Periods
# We use the standard Tkinter toolkit which comes with pretty much all Python distributions

# We start by defining the GUI as a class (derived from the base class Frame), with methods
# to create the elements inside the window, and methods to handle events 

from Tkinter import Frame, Button, Entry, Listbox,Text, END,SINGLE,W

class kepGUI(Frame):
    """The base class for the hill_calc GUI"""
    
    # This is the constructor for the GUI
    def __init__(self,master=None):
        # We begin by calling the base class's constructor first
        Frame.__init__(self,master)
    
        # We now have an empty window!
        
        # This command sets up a grid structure in the window
        self.grid()
        
        # This loop generates rows and columns in the grid
        for i in range(7):
            self.rowconfigure(i,minsize=10)
        for i in range(3):
            self.columnconfigure(i,minsize=10)
        
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
        
        for i in range(len(self.inputfield)):
            self.inputfield[i].bind("<Return>",self.__calcConversion)
    
    # This function creates and defines the units
    
    def defineUnits(self):
        '''Method defines tuples that carry the various units stored by the converter'''
        
        # Distances
        
        self.distunits = ('pc','AU','Solar Radii','Jupiter Radii', 'Saturn Radii','Neptune Radii ','Earth Radii','Mars Radii', 'Moon Radii','cm')
        # All values in cm 
        self.distvalues = (3.08568025e18, 1.496e13, 6.995e10,7.1492e8,6.0268e8,2.4764e8,6.371e7,3.396e7,1.73814e7,1.0)
        
        # Masses
        
        self.massunits = ('Solar Masses', 'Jupiter Masses','Saturn Masses', 'Neptune Masses', 'Earth Masses', 'Mars Masses', 'Moon Masses',  'kg','g')
        # All values in g
        self.massvalues = (1.988920e33,1.8986e30,5.6846e29, 1.0243e29, 5.9736e27,6.4185e26, 7.3477e25, 1000.0,1.0)
        
        # Time
        
        self.timeunits = ('seconds','minutes' ,'hours', 'days','Martian sols','weeks', 'years', 'Mars years', 'Jupiter years')
        # All values in seconds
        self.timevalues = (1.0,60.0,3600.0, 86400.0,88775.244, 604800.0,31556926.0,59354294.4 , 374335776.0)
        self.pi = 3.141592654
        
        # Keep the unit values in dictionaries, and use the above strings as keys
        
        self.distdict = {}        
        self.createUnitDict(self.distdict,self.distunits,self.distvalues) # this method is shown below
        
        self.massdict = {}
        self.createUnitDict(self.massdict,self.massunits,self.massvalues)
        
        self.timedict = {}
        self.createUnitDict(self.timedict, self.timeunits, self.timevalues)  
    
        self.myunits = self.timeunits
        self.myvalues = self.timevalues
        self.mydict = self.timedict
        
        # Define the combination of units that composes each choice (cgs, solar, Galactic)
    
        
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
        self.paramlist = ('Semi Major Axis', 'Central Mass','Angular Velocity', 'Orbital Period')
        
        # Add each item separately
        for item in self.paramlist:
            self.inputlist.insert(END,item)
            
        # Add it to the grid    
        self.inputlist.grid(row=1, column=0,rowspan=4,sticky=W)
        
        # Add a unit list (several combinations of units allowed)
        
        self.unitlist = Listbox(self, height=4,selectmode=SINGLE)
        self.unitlist.grid(row=1,column=1,rowspan=4, sticky=W)
        
        unitcombos = ('cgs','Solar', 'Galactic')
        self.unitG = (6.67e-8, 4.0*self.pi*self.pi, 1.0 )
    
        for item in unitcombos:
            self.unitlist.insert(END,item)
    
        # Number Entry Boxes (and Text Labels)
        
        self.inputfield = []
        self.inputlabels = []
 
        # Text Output Box
        self.outputtext = Text(self, height=1, width=40)
        self.outputtext.grid(row=5,column=0,columnspan=2,sticky=W)
        self.outputtext.insert(END, "Select Variable ")
    
        irow = 0
        for i in range(len(self.paramlist)):
            
            irow = irow+1
            self.inputlabels.append(Text(self,height=1,width=20))
            self.inputlabels[i].insert(END,self.paramlist[i])
            self.inputlabels[i].grid(row=irow,column=2,sticky='N')
            irow = irow+1
            self.inputfield.append(Entry(self))
            self.inputfield[i].insert(END, "1.0")
            self.inputfield[i].grid(row =irow, column=2,sticky='N')
            print irow
        

        # Create the Quit Button
        self.quitButton=Button(self,text='Quit',command=self.quit)
        self.quitButton.grid(row =8, column=0, sticky=W)
             

    # Event handler functions begin here    
    # This handler defines the choice of units available to the user, 
    # depending on selected variable
    
    def __varChoice(self, event):
        '''Handles the selection of variable: updates the list of units'''
        # Firstly, delete anything already in the units column
        #self.unitlist.delete(first=0,last=len(self.myvalues))
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
        
        # Remove all text in the output box, and tell user to define units
        self.outputtext.delete("1.0",index2=END)
        self.outputtext.insert(END, "Now Define Units")
        
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
        
        # If statement defines units being used
        self.G=1.0
        if selection =='cgs':
            self.G = self.unitG[0]
        if selection =='Solar':
            self.G = self.unitG[1]
        if selection == 'Galactic':
            self.G = self.unitG[2] # TODO - calculate this properly!
        
        print self.G, self.unitG[1]
        # Remove all text in the output box, and tell user to define units
        self.outputtext.delete("1.0",index2=END)
        self.outputtext.insert(END, "Now Enter Values")
        
    # Handler takes current state of GUI, and calculates results
    def __calcConversion(self,event):
        '''This method takes the current state of all GUI variables, calculates one of four equations'''
        
        # Which variable has been selected for calculation?
        # This decides what equation to use
        
        a = self.inputfield[0].get()
        a=float(a)
        
        ms = self.inputfield[1].get()
        ms = float(ms)
        
        omega = self.inputfield[2].get()
        omega = float(omega)
        
        tau = self.inputfield[3].get()
        tau = float(tau)
        
        if self.varchoice==0:
            a = (self.G*ms/omega**2)**0.333
            value = a
        elif self.varchoice==1:
            ms = omega**2*a**3/self.G
            value = ms
        elif self.varchoice==2:
            omega = (self.G*ms/a**3)**0.5
            value = omega
        elif self.varchoice==3:
            omega = (self.G*ms/a**3)**0.5
            tau = 2.0*self.pi/omega
            value =tau
        
        # Remove all text in the output box
        self.outputtext.delete("1.0",index2=END)
        self.outputtext.insert(END,str(self.paramlist[self.varchoice])+":    "+str(value)+"\n")
        

# End of methods and class definition
# Main program begins here            
app = kepGUI() # Call the exo class
app.master.title("Keplerian Velocity Calculator") # Give it a title
app.mainloop() # This command allows the GUI to run until a terminate command is issued (e.g. the user clicks "Quit")
    