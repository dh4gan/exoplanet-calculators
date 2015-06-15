# Written 15/6/15 by D Forgan
# This code produces a simple Paczynski curve for a single microlensing event
# assuming rectilinear motion of source and lens

import numpy as np
import matplotlib.pyplot as plt

# Define parameters of interest

# Stellar curve
t0s = 10.0
tEs = 3.0
u0s = 0.5

# Planetary curve
t0p = 13.0
tEp = 0.1
u0p = 1.0


tmin = 0.0
tmax = 20.0
npoints = 1000

time = np.linspace(tmin,tmax, npoints)

ustar = np.zeros(npoints)
curvestar = np.zeros(npoints)

uplanet = np.zeros(npoints)
curveplanet = np.zeros(npoints)

totalcurve = np.zeros(npoints)

for i in range(npoints):
    ustar[i] = u0s*u0s + np.power((time[i] - t0s)/tEs, 2)
    curvestar[i] = (ustar[i]+2)/(np.sqrt(ustar[i])*np.sqrt(ustar[i] + 4)) -1.0
    
    uplanet[i] = u0p*u0p + np.power((time[i] - t0p)/tEp, 2)
    curveplanet[i] = (uplanet[i]+2)/(np.sqrt(uplanet[i])*np.sqrt(uplanet[i] + 4)) -1.0
    
totalcurve = curvestar+curveplanet
    
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.set_ylim(0,2.0)
ax1.set_xlim(tmin,tmax)
ax1.set_xlabel('Time (hours)')
ax1.set_ylabel('Magnification (Arbitrary Units)')
ax1.plot(time,curvestar, label = 'stellar signal')
ax1.plot(time,curveplanet, label = 'planet signal')
ax1.plot(time,totalcurve, label = 'total signal')

ax1.legend(loc='upper right')

plt.savefig('microlensingcurve.png', format='png')