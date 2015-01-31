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
    
    print wl,Ref,alpha
    RArray.append([wl,Ref])
f.close();


R=0;G=0;B=0

for wl in range(400,720):
    for j in range(0,len(RArray)):
        if RArray[j][0]<wl*nm:
            break;
    lbig=RArray[j-1][0]; Rbig=RArray[j-1][1]
    lsmall=RArray[j][0]; Rsmall=RArray[j][1]
    Ref=(wl*nm-lsmall)/(lbig-lsmall)*(Rbig-Rsmall)+Rsmall


    if wl>=380 and wl<420:
        r=0; g=0; b=255    
    elif wl>=420 and wl<=440:
        r=-255.0*(wl-440.0)/(440.0-420.0); g=0.0; b=255.0
    elif wl>440 and wl<=490:
        r=0.0; g=255.0*(wl-440.0)/(490.0-440.0); b=255.0
    elif wl>490 and wl<=510:
        r=0.0; g=255.0; b=-255.0*(wl-510.0)/(510.0-490.0)
    elif wl>510 and wl<=580:
        r=255*(wl-510.0)/(580.0-510.0); g=255.0; b=0.0
    elif wl>580 and wl<=645:
        r=255.0; g=-255.0*(wl-645.0)/(645.0-580.0); b=0.0
    elif wl>645 and wl<720:
        r=255.0; g=0.0; b=0.0
    else:
        continue
    R=R+r*Ref;
    G=G+g*Ref;
    B=B+b*Ref;

MAX=max(max(R,G),B)
print R/MAX*255, G/MAX*255, B/MAX*255
    

