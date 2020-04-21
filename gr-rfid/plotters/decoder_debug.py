#!/usr/bin/env python3

import scipy
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
import numpy as np
from os import getcwd

relative_path_to_file = '/../misc/data/decoder'
decim = 5  # decimation of matched filter


def millergen(leng, seq):
    y_miller=np.zeros(4*leng);
    bits = seq;


    if(bits[0]==0):
        y_miller[0]=1;
        y_miller[1]=-1;
        y_miller[2]=1;
        y_miller[3]=-1;
    elif(bits[0]==1):  
        y_miller[0]=1;
        y_miller[1]=-1;
        y_miller[2]=-1;
        y_miller[3]=1;
    for i in range(1,leng):
        
        if(bits[i-1]==1):
            if(bits[i]==0 and y_miller[4*(i-1)]==1):
                y_miller[4*i]=-1;
                y_miller[4*i+1]=1;
                y_miller[4*i+2]=-1;
                y_miller[4*i+3]=1;
            elif(bits[i]==0 and y_miller[4*(i-1)]==-1):   
                y_miller[4*i]=1;
                y_miller[4*i+1]=-1;
                y_miller[4*i+2]=1;
                y_miller[4*i+3]=-1;
            elif(bits[i]==1 and y_miller[4*(i-1)]==1)  : 
                y_miller[4*i]=-1;
                y_miller[4*i+1]=1;
                y_miller[4*i+2]=1;
                y_miller[4*i+3]=-1;
            elif(bits[i]==1 and y_miller[4*(i-1)]==-1)  : 
                y_miller[4*i]=1;
                y_miller[4*i+1]=-1;
                y_miller[4*i+2]=-1;
                y_miller[4*i+3]=1; 
      
        elif(bits[i-1]==0):
            if(bits[i]==0 and y_miller[4*(i-1)]==1):
                y_miller[4*i]=-1;
                y_miller[4*i+1]=1;
                y_miller[4*i+2]=-1;
                y_miller[4*i+3]=1;
            elif(bits[i]==0 and y_miller[4*(i-1)]==-1):  
                y_miller[4*i]=1;
                y_miller[4*i+1]=-1;
                y_miller[4*i+2]=1;
                y_miller[4*i+3]=-1;
            elif(bits[i]==1 and y_miller[4*(i-1)]==1)  :   
                y_miller[4*i]=1;
                y_miller[4*i+1]=-1;
                y_miller[4*i+2]=-1;
                y_miller[4*i+3]=1;
            elif(bits[i]==1 and y_miller[4*(i-1)]==-1)  :  
                y_miller[4*i]=-1;
                y_miller[4*i+1]=1;
                y_miller[4*i+2]=1;
                y_miller[4*i+3]=-1; 
    return y_miller
f = scipy.fromfile(open(getcwd() + relative_path_to_file), dtype=scipy.float32)
#print (f[0] , len(f))

for i in range(len(f)//2):
    print(f[2*i], f[2*i+1])
#rn16 = f[-32:-1]
#rn16 = rn16[0::2]
#f = f[0:-32]
'''h_e = f[-2] + 1j * f[-1] *2
#print(h_e)
f = f[0:-2]
#h_en = 0.0527 - 0.0264j
f1 = f[0::2] + 1j * f[1::2]
f1 = f1[1::5]
f1 = f1[41:340]
#h_e = h_en
#f1 = [1.0847 - 0.5083j , 4.4262 -2.1219j, 1.0842 - 0.4808j, 4.4310 - 2.1231j]
res = []
for i in range(len(f1)//4):
    r1 = f1[4*i] - f1[4*i+1] + f1[4*i+2] -f1[4*i+3]
    r2 = f1[4*i] - f1[4*i+1] - f1[4*i+2] +f1[4*i+3]
    r1 = r1/(200 + 0j)
    r2 = r2/(200 + 0j)
    #print(abs(r1), abs(r2))
    a1=abs(r1-2*h_e)**2<=abs(r1+2*h_e)**2
    a2=abs(r1-2*h_e)**2+abs(r2)**2<=abs(r1)**2+abs(r2-2*h_e)**2
    a3=abs(r1-2*h_e)**2+abs(r2)**2<=abs(r1)**2+abs(r2+2*h_e)**2

    b1=abs(r1+2*h_e)**2<=abs(r1-2*h_e)**2
    b2=abs(r1+2*h_e)**2+abs(r2)**2<=abs(r1)**2+abs(r2-2*h_e)**2
    b3=abs(r1+2*h_e)**2+abs(r2)**2<=abs(r1)**2+abs(r2+2*h_e)**2

    c1=abs(r2-2*h_e)**2+abs(r1)**2<=abs(r2)**2+abs(r1-2*h_e)**2
    c2=abs(r2-2*h_e)**2+abs(r1)**2<=abs(r2)**2+abs(r1+2*h_e)**2
    c3=abs(r2-2*h_e)**2<=abs(r2+2*h_e)**2
    d1=abs(r2+2*h_e)**2+abs(r1)**2<=abs(r2)**2+abs(r1-2*h_e)**2
    d2=abs(r2+2*h_e)**2+abs(r1)**2<=abs(r2)**2+abs(r1+2*h_e)**2
    d3=abs(r2+2*h_e)**2<=abs(r2-2*h_e)**2

    #print(a1,a2,a3)
    #print(b1,b2,b3)
    #print(c1,c2,c3)
    #print(d1,d2,d3)
    if ((d1 and d2 and d3) or (c1 and c2 and c3)):
        res.append(1)
    elif ((b1 and b2 and b3) or (a1 and a2 and a3)):
        res.append(0)
    else:
        res.append(-1)

#print(res)
abs_f = abs(f1)
abs_f = abs_f / np.amax(abs_f)
# Matched filter to reduce hf noise
#abs_f = scipy.signal.correlate(abs_f, np.ones(decim), mode='same') / decim
#plt.scatter(f[0::2],f[1::2])
#print(f[0])
#plt.plot(abs_f)  
plotable = [f1[0], f1[1], f1[2],f1[3]]
#plotable = f1
#plotable = [i-h_e for i in plotable] 
#print(plotable)
pltable = [1.0847 - 0.5083j , 4.4262 -2.1219j, 1.0842 - 0.4808j, 4.4310 - 2.1231j]
# pltable = [i-h_en for i in pltable] 
#print(plotable)
#plt.plot(millergen(16, [1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1]))
#plt.plot(millergen(len(res),res))
#plt.plot(millergen(len(rn16),rn16))

X = [x.real for x in plotable]
Y = [y.imag for y in plotable]
#plt.scatter(X,Y)
#X = [x.real for x in pltable]
#Y = [y.imag for y in pltable]
#plt.scatter(X,Y)
plt.show();'''

