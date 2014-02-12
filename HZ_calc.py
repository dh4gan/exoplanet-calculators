# Written by Duncan Forgan, 12th January 2014
# This code produces a GUI to calculate Habitable Zone limits
# We use the standard Tkinter toolkit which comes with pretty much all Python distributions

# We start by defining the GUI as a class (derived from the base class Frame), with methods
# to create the elements inside the window, and methods to handle events 

from Tkinter import Frame, Button, Entry, Text, END,W

class HZGUI(Frame):
    """The base class for the HZ GUI"""
    
    # This is the constructor for the GUI
    def __init__(self,master=None):
        # We begin by calling the base class's constructor first
        Frame.__init__(self,master)
    
        # We now have an empty window!
        
        # This command sets up a grid structure in the window
        self.grid()
        
        # This loop generates rows and columns in the grid
        for i in range(11):
            self.rowconfigure(i,minsize=10)
        for i in range(2):
            self.columnconfigure(i,minsize=10)
        
        # These are methods which appear below the constructor
        self.createWidgets() # this places the elements (or widgets) in the grid
    
        # Finally, this bind reads in whatever value is in the text box when the user hits return
        # and carries out the unit conversion
        
        for i in range(len(self.inputfield)):
            self.inputfield[i].bind("<Return>",self.__calcConversion)
               
    def createUnitDict(self,mydict,mykeys,myvalues):
        '''This method takes a set of units and values, and creates a dictionary to store them in'''
        for i in range(len(myvalues)):
            mydict[mykeys[i]] = myvalues[i]
            
    def createWidgets(self):
        '''This method creates all widgets and adds them to the GUI'''
        
        # Create Widgets in order of appearance
        # This is not necessary, but makes code easier to read
        
        
        width_default= 30
        
        # Start with text asking for Luminosity
        self.varlabel = Text(self,height=2, width=width_default)
        self.varlabel.insert(END,"Luminosity\n(Solar Luminosities)")
        
        # Place widget on the Frame according to a grid
        self.varlabel.grid(row=0,column=0,sticky=W)
        
        # Second text label asking for Teff
        self.unitlabel = Text(self,height=2,width=width_default)
        self.unitlabel.insert(END,"Effective Temperature \n(K)")
        self.unitlabel.grid(row=0,column=1,sticky=W)
        
        # Number Entry Boxes for L and Teff (and Text Labels)
        
        self.inputfield = []
        self.inputlabels = []
        
        # L
        self.inputfield.append(Entry(self))
        self.inputfield[-1].insert(END,"1.0")
        self.inputfield[-1].grid(row=1,column=0)
        
        # Teff
        self.inputfield.append(Entry(self))
        self.inputfield[-1].insert(END,"5780.0")
        self.inputfield[-1].grid(row=1,column=1)
        
    
        self.nHZ = 7 # Different types of HZ boundary
        
        # Text Output Box
        self.outputtext = Text(self, height=self.nHZ+1, width=width_default)
        self.outputtext.grid(row=4,column=0,rowspan=self.nHZ,sticky=W)
        self.outputtext.insert(END, "WAITING: ")
        
        self.outputval = Text(self,height=self.nHZ+1,width=width_default)
        self.outputval.grid(row=4,column=1,rowspan =self.nHZ,sticky=W)
        
        # Create the Quit Button
        self.quitButton=Button(self,text='Quit',command=self.quit)
        self.quitButton.grid(row =15, column=1, sticky='E')
             

    # Event handler functions begin here    
    # This handler defines the choice of units available to the user, 
    # depending on selected variable
    
   
        
    # Handler takes current state of GUI, and calculates results
    def __calcConversion(self,event):
        '''This method takes the current state of all GUI variables, calculates one of four equations'''
        
        
        self.outputtext.delete("1.0",index2=END)
        self.outputval.delete("1.0",index2=END)
        
        nboundaries = self.nHZ
        
        # Seff
        seff = [0.0]*nboundaries
        
        # Seffsun - solar constant at this boundary
        seffsun = [0.0]*nboundaries
        
        seffsun[0]= 1.7763
        seffsun[1] = 1.0385
        seffsun[2] = 1.0146
        seffsun[3] = 0.3507
        seffsun[4] = 0.3207
        seffsun[5] = 0.2484
        seffsun[6] = 0.5408

        # a,b,c,d - fitting parameters
        a=[0.0]*nboundaries
        b=[0.0]*nboundaries
        c=[0.0]*nboundaries
        d=[0.0]*nboundaries
        
        a[0] = 1.4335e-4
        a[1] = 1.2456e-4
        a[2] = 8.1884e-5 
        a[3] = 5.9578e-5
        a[4] = 5.4471e-5
        a[5] = 4.2588e-5
        a[6] = 4.4499e-5

        b[0] = 3.3954e-9 
        b[1] = 1.4612e-8
        b[2] = 1.9394e-9
        b[3] = 1.6707e-9
        b[4] = 1.5275e-9
        b[5] = 1.1963e-9
        b[6] = 1.4065e-10

        c[0] = -7.6364e-12
        c[1] = -7.6345e-12
        c[2] = -4.3618e-12
        c[3] = -3.0058e-12
        c[4] = -2.7481e-12
        c[5] = -2.1709e-12
        c[6] = -2.2750e-12

        d[0] = -1.1950e-15
        d[1] = -1.7511E-15
        d[2] = -6.8260e-16
        d[3] = -5.1925e-16
        d[4] = -4.7474e-16
        d[5] = -3.8282e-16
        d[6] = -3.3509e-16
        
        
        # List describing each boundary

        boundarynames = ['Recent Venus','Runaway Greenhouse', 'Moist Greenhouse','Maximum Greenhouse', 'Early Mars', '2AU Cloud Limit ', 'CO2 condensation']
        
        innerouterchange = 2 # This denotes the last value for inner boundaries
        
        rhz = [0.0]*nboundaries
        
        lum = float(self.inputfield[0].get())
        T = float(self.inputfield[1].get())
        
        tstar = T-5780.0
        
        # Calculate Seff for each boundary
        
        for i in range(nboundaries):
            seff[i] =  seffsun[i] + a[i]*tstar + b[i]*tstar**2 + c[i]*tstar**3 + d[i]*tstar**4
            
            if(lum!=0.0):
                rhz[i] = (lum/seff[i])**0.5
        
        
        # Remove all text in the output box
        self.outputtext.delete("1.0",index2=END)
        
        # If Luminosity is 0, then print Seff
        # Otherwise, print rhz            
         
        if(lum!=0.0):
            for i in range(nboundaries):
                self.outputtext.insert(END, str(boundarynames[i]) + " (distance) \n")
                self.outputval.insert(END, str(rhz[i]) +"\n")
                if(i==innerouterchange):
                    self.outputtext.insert(END, str("-------\n"))
                    self.outputval.insert(END, str("-------\n"))
                
            
       
        if(lum==0.0):            
            for i in range(nboundaries):
                self.outputtext.insert(END, str(boundarynames[i]) + " (flux) \n")
                self.outputval.insert(END, str(seff[i]) +"\n")
                if(i==innerouterchange):
                    self.outputtext.insert(END, str("-------\n"))
                    self.outputval.insert(END, str("-------\n"))
                
            
            self.outputtext.insert(END,"ERROR")
        
        

# End of methods and class definition
# Main program begins here            
app = HZGUI() # Call the exo class
app.master.title("Habitable Zone Calculator") # Give it a title
app.mainloop() # This command allows the GUI to run until a terminate command is issued (e.g. the user clicks "Quit")
    