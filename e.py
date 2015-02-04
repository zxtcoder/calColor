#!/usr/bin/python

import math,os,sys
import Image, ImageDraw

h=6.626e-34
c=299792458
eV=1.602189e-19
nm=1e-9
pi=3.14159265358

RArray=[]

def colorZ(wl):
    return 1.8*math.exp(-1*(wl-450)*(wl-450)/873)

def colorY(wl):
    return 1.0*math.exp(-1*(wl-560)*(wl-560)/3517)

def colorX(wl):
    if wl<500:
        return 0.35*math.exp(-1*(wl-450)*(wl-450)/718)
    else:
        return 1.1*math.exp(-1*(wl-600)*(wl-600)/2043)


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
    RArray.append([wl,Ref,alpha])
f.close();


R=0;G=0;B=0
X=0;Y=0;Z=0
num=0;


wlBegin=300.0; wlEnd=700.0
wl=wlBegin; dwl=0.1

gS=1e-6

while wl<=wlEnd:
    for j in range(0,len(RArray)):
        if RArray[j][0]<wl*nm:
            break;
    lbig=RArray[j-1][0]; Rbig=RArray[j-1][1]; alphaB=RArray[j-1][2]
    lsmall=RArray[j][0]; Rsmall=RArray[j][1]; alphaSmall=RArray[j][2]
    Ref=(wl*nm-lsmall)/(lbig-lsmall)*(Rbig-Rsmall)+Rsmall
    alpha=(wl*nm-lsmall)/(lbig-lsmall)*(alphaB-alphaSmall)+alphaSmall

    sunC=1.0

    Z=Z + colorZ(wl)*Ref*dwl*sunC
    Y=Y + colorY(wl)*Ref*dwl*sunC
    X=X + colorX(wl)*Ref*dwl*sunC

    print wl,Ref,alpha
    wl=wl + dwl;
    
Y=Y/1.0
X=X/(wlEnd-wlBegin); Y=Y/(wlEnd-wlBegin); Z=Z/(wlEnd-wlBegin)

R=3.2406*X - 1.5372*Y - 0.4986*Z
G=-0.9689*X + 1.8758*Y +0.0415*Z
B=0.0557*X - 0.2040*Y + 1.0570*Z

if R<=0.00304:
    R=12.92*R
else:
    R=(1+0.055)*math.pow(R,1/2.4)-0.055

if G<=0.00304:
    G=12.92*G
else:
    G=(1+0.055)*math.pow(G,1/2.4)-0.055

if B<=0.00304:
    B=12.92*B
else:
    B=(1+0.055)*math.pow(B,1/2.4)-0.055




#print R,G,B
MAX=max(max(R,G),B)
print 255.0*R/MAX,255.0*G/MAX,255.0*B/MAX
