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
    RArray.append([wl,Ref,alpha])
f.close();


R=0;G=0;B=0

wlR=780; wlG=520; wlB=380

wl=wlB
dwl=0.1

gS=1e-6

while wl<=wlR:
    for j in range(0,len(RArray)):
        if RArray[j][0]<wl*nm:
            break;
    lbig=RArray[j-1][0]; Rbig=RArray[j-1][1]; alphaB=RArray[j-1][2]
    lsmall=RArray[j][0]; Rsmall=RArray[j][1]; alphaSmall=RArray[j][2]
    Ref=(wl*nm-lsmall)/(lbig-lsmall)*(Rbig-Rsmall)+Rsmall
    alpha=(wl*nm-lsmall)/(lbig-lsmall)*(alphaB-alphaSmall)+alphaSmall

    if wl>=wlB and wl<=wlG:
        dB=255+(wl-wlB)/(wlG-wlB)*(-255)
        dG=0+(wl-wlB)/(wlG-wlB)*(255)
        dR=0
    elif wl>wlG and wl<=wlR:
        dB=0
        dG=255+(wl-wlG)/(wlR-wlG)*(-255)
        dR=0+(wl-wlG)/(wlR-wlG)*(255)
    else:
        continue

    R=R + dR*Ref*dwl;
    G=G + dG*Ref*dwl;
    B=B + dB*Ref*dwl;
    wl=wl + dwl;
    print wl,Ref,alpha
    
G=G/2.2
MAX=max(max(R,G),B)
#print R/(wlR-wlB),G/(wlR-wlB)/2,B/(wlR-wlB)
print 255*R/MAX, 255*G/MAX, 255*B/MAX

