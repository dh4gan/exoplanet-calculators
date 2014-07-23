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

print msol, rsol
print mjup, rjup
print mearth, rearth

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

print 'Inner boundary given by Roche limit: ', aroche/AU

amin = 0.002*AU
amax = 0.007*AU

emin = 0.0001
emax = 0.1

semimaj = np.linspace(amin, amax, num=npoints)
eccentricity = np.linspace(emin, emax, num=npoints)

tidal = np.zeros((npoints,npoints))

for i in range(npoints):
    a = semimaj[i]
    for j in range(npoints):        
        ecc = eccentricity[j]                                
        
        tidal[j,i] = 21.0*rhosec*rhosec*ecc*ecc*rsec**5*(G*mprim)**2.5
        
        tidal[j,i] = tidal[j,i]/(38.0*gamma*Q*a**7.5)
        
        
        
# Plot figure


fig1 = plt.figure()
ax = fig1.add_subplot(111)
ax.set_xlabel('Semimajor Axis (AU)', fontsize = 16)
ax.set_ylabel('Eccentricity', fontsize = 16)
plt.pcolor(semimaj/AU, eccentricity, tidal, cmap = 'Spectral', vmax = 5000.0)
colourbar=plt.colorbar()
colourbar.set_label(r'Tidal Heating per Unit Area ($erg \,s^{-1} cm^{-2}$)', fontsize=16)

# plot contours corresponding to Io, Europa tidal heating levels

contours = plt.contour(semimaj/AU, eccentricity,tidal, levels = (fIo, fEuropa_upper, fEuropa_lower), colors='white')

fmt = {}
strs = [ 'Io', 'Europa Upper Limit', 'Europa Lower Limit']
for l,s in zip( contours.levels, strs ):
    fmt[l] = s

plt.clabel(contours, contours.levels,fmt=fmt,fontsize=14)


# Add vertical lines showing Io and Europa positions
plt.vlines(amoons,ymin = emin, ymax = emax, colors='white', linestyles='dashed')

#plt.vlines(aroche/AU,ymin = emin, ymax = emax, colors='red')

plt.show()

