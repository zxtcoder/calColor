#!/usr/bin/python

import math,os,sys
import Image, ImageDraw

h=6.626e-34
c=299792458
eV=1.602189e-19
WL1=380e-9; WL2=780e-9

specArray=[]

im=Image.open("spectrum.png")
for x in range(0,im.size[0]):
    color=im.getpixel((x,20))
    specArray.append(color)

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
    RArray.append([wl,Ref])
f.close();


R=0;G=0;B=0
for i in range(0,len(specArray)):
    wl=1.0*i/len(specArray)*(WL2-WL1)+WL1
    for j in range(0,len(RArray)):
        if RArray[j][0]<wl:
            break;
    lbig=RArray[j-1][0]; Rbig=RArray[j-1][1]
    lsmall=RArray[j][0]; Rsmall=RArray[j][1]
    Ref=(wl-lsmall)/(lbig-lsmall)*(Rbig-Rsmall)+Rsmall
    print Ref
    R=R+specArray[i][0]*Ref;
    G=G+specArray[i][1]*Ref;
    B=B+specArray[i][2]*Ref;

MAX=max(max(R,G),B)
print R/MAX*255, G/MAX*255, B/MAX*255
    

