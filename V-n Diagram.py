from math import *
import numpy as np
import matplotlib.pyplot as plt

## -------- MANEOUVRE LOAD DIAGRAM V-n -------- ##

#Defining velocities and load factors
Vstall = 14                     # [m/s] SAVED-P&P-PERF-07
Vmvr   = sqrt(3.8 * Vstall**2)  # [m/s] from n = V**2 / Vstall**2
Vc     = 22.3                   # [m/s] SAVED-P&P-PERF-01
Vd     = Vc * 1.4               # [m/s] REF TO Luis Parada Thesis Tecnico for factor of 1.2, OR CS-VLA 335 b) 2) for 1.4
Vneg   = sqrt(1.52*Vstall**2)   # [m/s] 
nmax   = 3.8                    # max from SMM dept, from certification CS-LUAS.337
nmin   = -1*0.4*nmax            # nmax * 0.4 REF TO Luis Parada Thesis Tecnico for factor of 0.4

#Setting up lists for plots
Vlist   = []
nlist   = []
V2list  = []
n2list  = []
V3list  = []
n3list  = []
V4list  = []
n4list  = []
V5list  = []
n5list  = []
V6list  = []
n6list  = []
V7list  = []
n7list  = []
V8list  = []
n8list  = []
V9list  = []
n9list  = []
V10list = []
n10list = []
V11list = []
n11list = []
V12list = []
n12list = []
V13list = []
n13list = []
V14list = []
n14list = []
V15list = []
n15list = []


## Positive Stall Limit
Vlist = np.arange(0,Vmvr,0.01)

for V in Vlist:
    n = (1/(Vstall**2)) * V**2
    nlist.append(n)

## Positive Structural Limit
V2list = np.arange(Vmvr,Vd+0.01,0.01)

for V in V2list:
    n = 3.8
    n2list.append(n)

## Negative Stall Limit
V3list = np.arange(0,Vneg,0.01)

for V in V3list:
    n = - (1/(Vstall**2)) * V**2
    n3list.append(n)

## Negative Structural Limit
V4list = np.arange(Vneg, Vc+0.01, 0.01)

for V in V4list:
    n = -1.52
    n4list.append(n)

## Dive Speed Limit
n5list = np.arange(0,nmax,0.001)

for n in n5list:
    V = Vd
    V5list.append(V)

## Stall Speed
n6list = np.arange(-1,1,0.001)

for n in n6list:
    V = Vstall
    V6list.append(V)

## Pre-dive speed limit
V8list = [Vc,Vd]
n8list = [nmin,0]



## -------- GUST LOAD DIAGRAM V-n -------- ##

# NOTE: CS-VLA REQS ARE NOT USED DIRECTLY AS THESE YIELD LOAD FACTORS 92% HIGHER
# (ref paper -Flight Loads of Mini UAV by Andrzej Majka)
# Thus, delta n (change in load factor) is always divided by 1.92



rho = 1.16727                       # [kg/m3] density at cruise altitude of 500m
rhoSL = 1.225                       # [kg/m3] density at sea level
uc  = 15.2                          # derived gust velocity for cruise speed (CS-VLA 333 (c) (1) (i) )
ud  = 7.62                          # derived gust velocity for dive speed (CS-VLA 333 (c) (1) (ii) )
clalpha = 4.3299                    # C_L_alpha of the wing from Aero department                                        <-----------  ##  UPDATE!  ##
WS = 121.26                         # [N/m2] wing loading (W/S) from SAVED-WING-AERO-A01
g = 9.80665                         # [m/s2] acceleration due to gravity
MS = WS / g                         # [kg/m2] wing loading (M/S) used in CS-VLA 341
chord = 0.47                        # [m] mean geometric chrod = surface area / wingspan = 1.41/3
mug = (2*MS) / (rho*chord*clalpha)  # "aeroplane mass ratio" from CS-VLA 341
Kg = (0.88*mug)/(5.3+mug)           # gust alleviation factor

#Gust loads for Vc
V9list = np.arange(0,Vc+0.01,0.01)

for V in V9list:
    G1 = 1 + ((rho*uc*clalpha*Kg)/(2*WS*1.92)) * V
    n9list.append(G1)

V10list = np.arange(0,Vc+0.01,0.01)

for V in V10list:
    G2 = 1 - ((rho*uc*clalpha*Kg)/(2*WS*1.92)) * V
    n10list.append(G2)

#Gust loads for Vd
V11list = np.arange(0,Vd+0.01,0.01)

for V in V11list:
    G3 = 1 + ((rho*ud*clalpha*Kg)/(2*WS*1.92)) * V
    n11list.append(G3)

V12list = np.arange(0,Vd+0.01,0.01)

for V in V12list:
    G4 = 1 - ((rho*ud*clalpha*Kg)/(2*WS*1.92)) * V
    n12list.append(G4)

#Connecting gust loads into diamond shape
V13list = [Vc,Vd]                       #Bottom Connection Line
n13list = [n10list[-1],n12list[-1]]

V14list = [Vc,Vd]                       #Top Connection Line
n14list = [n9list[-1],n11list[-1]]

V15list = [Vd,Vd]                       #Vertical Middle Connection Line
n15list = [n11list[-1],n12list[-1]]


## Cruise Speed
n7list = np.arange(nmin,n9list[-1]+0.001,0.001)

for n in n7list:
    V = Vc
    V7list.append(V)


## -------- Plotting and formatting the V-n Diagram -------- ##

plt.plot(Vlist,nlist, label="Stall Limit")
plt.plot(V3list,n3list, label="(Negative) Stall Limit")
plt.plot(V2list,n2list, label="Structural Limit, $n_{max}$=3.8")
plt.plot(V4list,n4list, label="(Negative) Structural Limit, $n_{min}$=-1.52")
plt.plot(V6list,n6list, color="grey", linestyle="dashed", label="Stall speed, $V_{stall}$=14$m/s$")
plt.plot(V7list,n7list, color="grey", linestyle="dashdot", label="Cruise speed, $V_c$=22.3$m/s$")
plt.plot(V5list,n5list, label="Dive speed, $V_d$=31.2$m/s$")
plt.plot(V8list,n8list)
plt.plot(V9list,n9list, color="black", linestyle="dotted", label="Gust Load Envelope")
plt.plot(V10list,n10list, color="black", linestyle="dotted")
plt.plot(V11list,n11list, color="black", linestyle="dotted")
plt.plot(V12list,n12list, color="black", linestyle="dotted")
plt.plot(V13list,n13list, color="black", linestyle="dotted")
plt.plot(V14list,n14list, color="black", linestyle="dotted")
plt.plot(V15list,n15list, color="black", linestyle="dotted")
plt.legend()
plt.title("Maneouvre and Gust Load Diagram")
plt.xlabel("V [m/s]")
plt.ylabel("n [-]")
plt.grid()
plt.show()


### -----  TO DO: UPDATE SCRPT  -------  ###
### Update clalpha and chord --> DONE

