# Written by Duncan Forgan 27/6/13
# Code takes binary system parameters as input, and determines

# for Stype systems: Maximum semimajor axis a planet orbiting primary may possess and maintain stable orbit
# for Ptype systems: minimum semimajor axis a planet orbiting binary may possess and maintain stable orbit

# References
# Rabl & Dvorak 1988, A&A, 191, 385
# Holman & Wiegert, 1999, AJ, 117, 621


fail = True

# Determine binary system type
while fail:
    systemtype = raw_input("What is the binary system type? (Enter P or S) ")

    if "P" in systemtype or "p" in systemtype:
        systemtype = "P"
        print "P type (circumbinary) system selected"
        fail = False
        
    if "S" in systemtype or "s" in systemtype:
        systemtype = "P"
        print "P type (circumbinary) system selected"
        fail = False

if "P" not in systemtype and "S" not in systemtype:
    print "Error: type incorrectly determined"

# Enter binary parameters

mprim = input("Enter mass of primary: ")
msec = input("Enter mass of secondary: ")
abin = input ("Enter binary semimajor axis: ")
ebin = input("Enter binary eccentricity: ")

# Calculate binary mass ratio
mratio = msec/(mprim+msec)

print "Binary mass ratio is ",mratio

if "S" in systemtype:
    amax = abin*(0.464 - 0.38*mratio -0.631*ebin + 0.586*mratio*ebin +0.15*ebin*ebin -0.198*mratio*ebin*ebin)
    print "Maximum planet semimajor axis around primary is ",amax
    
if "P" in systemtype:
    amin = abin*(1.6 +5.1*ebin +4.12*mratio -2.22*ebin*ebin - 4.27*mratio*ebin - 5.09*mratio*mratio + 4.61*mratio*mratio*ebin*ebin)
    print "Minimum planet semimajor axis around binary is ",amin

    
