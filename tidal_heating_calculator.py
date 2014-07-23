# Written 24/4/14 by dh4gan
# This code uses the standard Peale et al (1980) equation for 
# tidal heating per unit area (see also Scharf 2006)
# Fixing the primary and secondary body structural parameters,
# It creates 2D maps of flux in secondary semimajor axis and eccentricity

import numpy as np
import matplotlib.pyplot as plt

# All calculations are in cgs

# Define unit conversions

msol = 1.99e33
rsol = 6.955e10

mjup = 1.8986e30
rjup = 7.1492e8

mearth = 5.9736e27
rearth = 6.371e7

AU = 1.496e13

# Known tidal heating rates

fEuropa_lower = 50.0 # erg s^-1 cm^-2 
fEuropa_upper = 300.0
fSolar = 1.361e6 # Solar constant for reference

fIo = 1500.0

aIo = 2.819e-3
aEuropa = 4.485e-3

amoons = [aIo,aEuropa]

# Only physical constant required is G

G = 6.67e-8

# Now define fixed parameters

gamma = 1.0e11 # dyne cm^{-2}
Q = 100.0 # Tidal dissipation parameter

mprim = 10.0*mjup
msec = 1.0*mearth 
rsec = 1.0*rearth
rhosec = 5.0 # g cm^{-3}

# Now define grid of a and e to map onto

npoints = 200

aroche = (3.0*mprim/(2.0*np.pi*rhosec))**0.333

print "The Primary has mass", mprim/mjup, " Jupiter masses"
print "The Secondary has mass", msec/mearth, " Earth masses"
print "The Secondary has radius", rsec/rearth, " Earth radii"
print "The Secondary density is ", rhosec, " g cm-3"

print 'Roche limit: ', aroche/AU


a = input("Enter the Secondary semimajor axis: ")
ecc = input("Enter the Secondary eccentricity: ")

a = a*AU

tidal = 21.0*rhosec*rhosec*ecc*ecc*rsec**5*(G*mprim)**2.5
tidal = tidal/(38.0*gamma*Q*a**7.5)
        
        
print "The tidal heating in this configuration is", tidal, "erg s-1 cm-2"
