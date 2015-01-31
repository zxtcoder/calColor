#!/usr/bin/python

import math,os,sys
import Image, ImageDraw

h=6.626e-34
c=299792458
eV=1.602189e-19
nm=1e-9
pi=3.14159265358

RArray=[]

fName=sys.argv[1]
f=open(fName, 'r')
content=f.readlines()
for line in content:
    lstr=line[:-1].split(' ');
    real=float(lstr[2]); img=float(lstr[3])
    wl=float(lstr[1]); eng=float(lstr[0])

    a2=(math.sqrt(real*real + img*img) + real)/2
    b2=(math.sqrt(real*real + img*img) - real)/2
    a=math.sqrt(a2); b=math.sqrt(b2)
    Ref=((a-1)*(a-1)+b2)/((a+1)*(a+1)+b2)

    alpha=2*pi/wl*math.sqrt(2)*math.sqrt(math.sqrt(real*real + img*img) - real)
    
#    print wl,Ref,alpha
    RArray.append([wl,Ref])
f.close();


R=0;G=0;B=0
X=0;Y=0;Z=0
num=0;

wl=350.0; dwl=0.1

while wl<=700.0:
    for j in range(0,len(RArray)):
        if RArray[j][0]<wl*nm:
            break;
    lbig=RArray[j-1][0]; Rbig=RArray[j-1][1]
    lsmall=RArray[j][0]; Rsmall=RArray[j][1]
    Ref=(wl*nm-lsmall)/(lbig-lsmall)*(Rbig-Rsmall)+Rsmall

    sunC=1.0/2555.0*12*math.exp(-1*(wl-530)*(wl-530)/14426)

    Z=Z + 1.8*math.exp(-1*(wl-450)*(wl-450)/873)*Ref*dwl*sunC
    Y=Y + 1.0*math.exp(-1*(wl-560)*(wl-560)/3517)*Ref*dwl*sunC
    if wl<500:
        X=X + 0.35*math.exp(-1*(wl-450)*(wl-450)/718)*Ref*dwl*sunC
    else:
        X=X + 1.1*math.exp(-1*(wl-600)*(wl-600)/2043)*Ref*dwl*sunC

  

    wl=wl + dwl;
    
    
X=X/105; Y=Y/105; Z=Z/105

R=2.3646*X - 0.8965*Y - 0.4681*Z
G=-0.5152*X + 1.4264*Y + 0.0888*Z
B=0.0052*X - 0.0144*Y + 1.0092*Z

MAX=max(max(R,G),B)
print R/MAX*255, G/MAX*255, B/MAX*255
