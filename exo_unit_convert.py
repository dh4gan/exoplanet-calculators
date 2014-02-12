#!/usr/local/bin/python

from Tkinter import Frame, Button, Entry, Listbox,Text, END,SINGLE,W

class exo(Frame):
    """The base class for the exo_convert GUI"""
    
    # This is the constructor for the GUI
    def __init__(self,master=None):
        Frame.__init__(self,master)
        
        self.grid()
        
        for i in range(2):
            self.columnconfigure(i,minsize=10)
            self.rowconfigure(i,minsize=10)
         
        self.defineUnits()
        self.createWidgets()
        
        # Bind choice of variable (distance,mass,time)
        # Highlights variable selection and presents unit options
        self.inputlist.bind("<Button-1>",self.__varChoice)
    
        # Bind choice of unit (highlights unit selection)
        self.unitlist.bind("<Button-1>",self.__unitChoice)
    
        # Bind Entry of variable value to calculation
        self.inputfield.bind("<Return>",self.__calcConversion)
    
    # This function creates and defines the units
    
    def defineUnits(self):
        # Tuples which represent the various units allowed by each option
        
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
    
        # Keep the unit values in dictionaries, and use the above strings as keys
        
        self.distdict = {}        
        self.createUnitDict(self.distdict,self.distunits,self.distvalues)
        
        self.massdict = {}
        self.createUnitDict(self.massdict,self.massunits,self.massvalues)
        
        self.timedict = {}
        self.createUnitDict(self.timedict, self.timeunits, self.timevalues)  
    
        self.myunits = self.timeunits
        self.myvalues = self.timevalues
        self.mydict = self.timedict
        
        
    # This function creates a unit dictionary, with keys and unit values in cgs
    def createUnitDict(self,mydict,mykeys,myvalues):
        for i in range(len(myvalues)):
            mydict[mykeys[i]] = myvalues[i]
               
    # This function creates and adds all widgets to the GUI
    def createWidgets(self):
        
        # Create Widgets in order of appearance
        # This is not necessary, but makes code easier to read
        
        
        # Start with text telling user what to do
        self.varlabel = Text(self,height=1, width=20)
        self.varlabel.insert(END,"Which Variable?")
        
        # Place widget on the Frame according to a grid
        self.varlabel.grid(row=0,column=0,sticky=W)
        
        # Second text label asking user which units are being used
        
        self.unitlabel = Text(self,height=2,width=20)
        self.unitlabel.insert(END,"Which Units are you \nworking in?")
        self.unitlabel.grid(row=0,column=1,sticky=W)
        
        # Third text label asking user for numerical value
        
        self.numlabel = Text(self,height=1, width=20)
        self.numlabel.insert(END,"Enter Variable Value")
        self.numlabel.grid(row=0,column=2,sticky=W)
        
        # This creates a list of options for the user to select
        self.inputlist = Listbox(self, height=3, selectmode=SINGLE)
      
        # Tuple of choices we're going to put in this list
        paramlist = ('Distance', 'Time', 'Mass')
        
        # Add each item separately
        for item in paramlist:
            self.inputlist.insert(END,item)
            
        # Add it to the grid    
        self.inputlist.grid(row=1, sticky=W)
        
        # Add a unit list which produces a set of unit choices dependent on inputlist
        
        self.unitlist = Listbox(self, height=10,selectmode=SINGLE)
        self.unitlist.grid(row=1,column=1, sticky=W)
              
        # Number Entry Box
        self.inputfield = Entry(self)
        self.inputfield.insert(END, "0")
        self.inputfield.grid(row =1, column=2,sticky=W)
        
        
        # Text Output Box
        self.outputtext = Text(self, height=10)
        self.outputtext.grid(row=2,column=0,columnspan=3,sticky=W)
        self.outputtext.insert(END, "WAITING: ")
        # Create the Quit Button
        self.quitButton=Button(self,text='Quit',command=self.quit)
        self.quitButton.grid(row =3, column=0, sticky=W)
             

    # Event handler functions begin here    
    # This handler defines the choice of units available to the user, 
    # depending on selected variable
    
    def __varChoice(self, event):
        
        self.unitlist.delete(first=0,last=len(self.myvalues))
        num = 0
        try:
            num = self.inputlist.curselection()[0]       
            choice = int(num)
            
        except:
            choice = 0
            return
        
        # Highlight current choice in red
        self.inputlist.itemconfig(choice, selectbackground='red')
        
        if choice==0:
            #print 'Distance chosen'
            self.mydict=self.distdict
            self.myunits= self.distunits
            self.myvalues = self.distvalues
        elif choice==1:
            # print 'Time chosen'
            self.mydict=self.timedict
            self.myunits= self.timeunits
            self.myvalues = self.timevalues
        elif choice==2:
            # print 'Mass chosen'
            self.mydict=self.massdict
            self.myunits= self.massunits
            self.myvalues = self.massvalues
        
        # Add the units to the unitlist 
            
        for item in self.myunits:
            self.unitlist.insert(END,item)    
        del num
        
    def __unitChoice(self,event):
        num = 0
        try:
            num = self.unitlist.curselection()[0]       
            choice = int(num)
            
        except:
            choice = 0
            return
        
        # Highlight current choice in red
        self.unitlist.itemconfig(choice, selectbackground='red')
        
        
    # Handler takes current state of GUI, and calculates results
    def __calcConversion(self,event):
        
        num = 0
        # What units are being used?
        try:       
            num = self.unitlist.curselection()[0]       
            choice = int(num)
        except:
            choice = 0
            return
        
        self.outputtext.delete("1.0",index2=END)
        # Highlight current choice in red
        self.unitlist.itemconfig(choice, selectbackground='red')
          
        # What is the value in the entry field?
        value = self.inputfield.get()
        value = float(value)
 
        # Now perform calculation using dictionary 
 
        var = self.unitlist.get(choice)
       
        # Convert value to cgs
        
        value = value*self.mydict[var]
        
        # Create a new list of output answers
        
        output=[]
        self.outputtext.insert(END,"OUTPUT:    \n\n")
        
        # Calculate and output it to the GUI
        for i in range(len(self.myvalues)):
            output.append(value/self.myvalues[i])
            self.outputtext.insert(END,self.myunits[i] + ":  "+str(output[i])+"\n")    
       
 
# Main program begins here            
app = exo()
app.master.title("Exoplanet Calculator")
app.mainloop()
    