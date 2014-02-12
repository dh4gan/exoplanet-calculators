#!/usr/local/bin/python
# Written by Duncan Forgan, 18th July 2012
# This code produces a Hill Radius Calculator GUI
# We use the standard Tkinter toolkit which comes with pretty much all Python distributions

# We start by defining the GUI as a class (derived from the base class Frame), with methods
# to create the elements inside the window, and methods to handle events 

from Tkinter import Frame, Button, Entry, Listbox,Text, END,SINGLE,W

class hillGUI(Frame):
    """The base class for the hill_calc GUI"""
    
    # This is the constructor for the GUI
    def __init__(self,master=None):
        # We begin by calling the base class's constructor first
        Frame.__init__(self,master)
    
        # We now have an empty window!
        
        # This command sets up a grid structure in the window
        self.grid()
        
        # This loop generates rows and columns in the grid
        for i in range(10):
            self.rowconfigure(i,minsize=10)
        for i in range(3):
            self.columnconfigure(i,minsize=10)
        
        # These are methods which appear below the constructor
        #self.defineUnits() # this sets up the units I'll be using in the converter
        self.createWidgets() # this places the elements (or widgets) in the grid
        
        # This command "binds" the user's click to a method (varChoice)
        # This method will determine which variable the user wants (Distance, Mass, Time)
        self.inputlist.bind("<Button-1>",self.__varChoice)
    
        # This is a similar command for the selection of unit
        #self.unitlist.bind("<Button-1>",self.__unitChoice)
    
        # Finally, this bind reads in whatever value is in the text box when the user hits return
        # and carries out the unit conversion
        
        for i in range(len(self.inputfield)):
            self.inputfield[i].bind("<Return>",self.__calcConversion)
               
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
        #self.unitlabel = Text(self,height=1,width=20)
        #self.unitlabel.insert(END,"Which Units?")
        #self.unitlabel.grid(row=0,column=1,sticky=W)
        
        # Third text label asking user for numerical value
        
        self.numlabel = Text(self,height=1, width=20)
        self.numlabel.insert(END,"Enter Variable Values")
        self.numlabel.grid(row=0,column=2,sticky=W)
        
        # This creates a list of options for the user to select
        self.inputlist = Listbox(self, height=4, selectmode=SINGLE)
      
        # Tuple of choices we're going to put in this list
        self.paramlist = ('Semi Major Axis', 'Planet Mass', 'Star Mass','Hill Radius')
        
        # Add each item separately
        for item in self.paramlist:
            self.inputlist.insert(END,item)
            
        # Add it to the grid    
        self.inputlist.grid(row=1, column=0,rowspan=4,sticky=W)
        
        # Add a unit list (several combinations of units allowed)
        
        #self.unitlist = Listbox(self, height=4,selectmode=SINGLE)
        #self.unitlist.grid(row=1,column=1,rowspan=4, sticky=W)
        
        #unitcombos = ('cgs','Solar units', 'Galactic Units') 
    
        #for item in unitcombos:
        #    self.unitlist.insert(END,item)
    
        # Number Entry Boxes (and Text Labels)
        
        self.inputfield = []
        self.inputlabels = []
    
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
        
        # Text Output Box
        self.outputtext = Text(self, height=1, width=40)
        self.outputtext.grid(row=7,column=0,columnspan=2,sticky=W)
        self.outputtext.insert(END, "WAITING: ")
        # Create the Quit Button
        self.quitButton=Button(self,text='Quit',command=self.quit)
        self.quitButton.grid(row =8, column=0, sticky=W)
             

    # Event handler functions begin here    
    # This handler defines the choice of units available to the user, 
    # depending on selected variable
    
    def __varChoice(self, event):
        '''Handles the selection of variable: updates the list of units'''
        # Firstly, delete anything already in the units column
#        self.unitlist.delete(first=0,last=len(self.myvalues))
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

        
    # Handler takes current state of GUI, and calculates results
    def __calcConversion(self,event):
        '''This method takes the current state of all GUI variables, calculates one of four equations'''
        print 'Calculating'
        # Which variable has been selected for calculation?
        # This decides what equation to use
        
        a = self.inputfield[0].get()
        a=float(a)
        
        mp = self.inputfield[1].get()
        mp=float(mp)
        
        ms = self.inputfield[2].get()
        ms = float(ms)
        
        rh = self.inputfield[3].get()
        rh = float(rh)
        
        if self.varchoice==0:
            a = rh*(3*ms/mp)*0.3333
            value = a
        elif self.varchoice==1:
            mp = 3*ms*rh**3/a**3
            value = mp
        elif self.varchoice==2:
            ms = mp*a**3/(3*rh**3)
            value = ms
        elif self.varchoice==3:
            rh = a *(mp/(3*ms))**0.3333
            value = rh
            
        
        # Remove all text in the output box
        self.outputtext.delete("1.0",index2=END)
        self.outputtext.insert(END,str(self.paramlist[self.varchoice])+":    "+str(value))
        

# End of methods and class definition
# Main program begins here            
app = hillGUI() # Call the exo class
app.master.title("Hill Radius Calculator") # Give it a title
app.mainloop() # This command allows the GUI to run until a terminate command is issued (e.g. the user clicks "Quit")
    