#!/usr/bin/env python
import array

def qualitycuts():
    return "dataQuality==0 && RF00*PotPerQie>100"

def qiecuts():
    return "RFmax<Inh_thres"

def dimuoncuts():
    dimuoncutlist = []
    dimuoncutlist.append("abs(dx)<.25") #target cut X
    dimuoncutlist.append("abs(dy-1.6)<.22") #target cut Y
    dimuoncutlist.append("dx*dx+(dy-1.6)*(dy-1.6)<.06") #target cut XY
    dimuoncutlist.append("dz>-280 && dz<-5") #target cut Z
    dimuoncutlist.append("abs(dpx)<1.8")
    dimuoncutlist.append("abs(dpy)<2")
    dimuoncutlist.append("dpx*dpx+dpy*dpy<5")
    dimuoncutlist.append("dpz>38 && dpz<116")
    dimuoncutlist.append("abs(trackSeparation)<270")
    dimuoncutlist.append("chisq_dimuon<18") #quality cut
    dimuoncutlist.append("abs(pchisq_target+nchisq_target-chisq_dimuon)<2")
    dimuoncutlist.append("py3*ny3<0")
    dimuoncutlist.append("pnumHits+nnumHits>29")
    #dimuoncutlist.append("")
    return " && ".join(dimuoncutlist)

def trackcuts():
    trackcutlist = []
    trackcutlist.append("Qchisq_target<15") #target cut chisq
    trackcutlist.append("Qpz1>9 && Qpz1<75")
    trackcutlist.append("QnumHits>13") #quality cut
    trackcutlist.append("QxT*QxT+(QyT-1.6)*(QyT-1.6)<320") #target cut XY
    trackcutlist.append("QxD*QxD+(QyD-1.6)*(QyD-1.6)<1100") #dump cut XY
    trackcutlist.append("QxD*QxD+(QyD-1.6)*(QyD-1.6)>16") #dump miss cut XY
    trackcutlist.append("Qchisq_target<1.5*Qchisq_upstream") #target-upstream cut
    trackcutlist.append("Qchisq_target<1.5*Qchisq_dump") #target-dump cut
    trackcutlist.append("Qz0<-5 && Qz0>-320") #target cut Z
    trackcutlist.append("Qchisq/(QnumHits-5)<12") #quality cut
    trackcutlist.append("Qy1/Qy3<1")
    #trackcutlist.append("abs(abs(Qpx1-Qpx3)-.416)<.008")
    #trackcutlist.append("abs(Qpy1-Qpy3)<.008")
    #trackcutlist.append("abs(Qpz1-Qpz3)<.008")
    trackcutlist.append("Qy1*Qy3>0")
    #trackcutlist.append("")
    trackcuts = " && ".join(trackcutlist)
    return " && ".join([trackcuts.replace('Q','p'),trackcuts.replace('Q','n')])

def intensityvar():
    qiepedestal = 36
    return "(RF00-{0})*PotPerQie".format(qiepedestal)

def binedgesqie():
    maxqie = 100e3
    nbinsqie = 20
    breakpoint = 30e3
    nbinslo = 6
    nbinshi = 7
    return array.array('d',[1.0*breakpoint*x/nbinslo for x in range(0,nbinslo+1)] + [breakpoint + 1.0*(maxqie-breakpoint)*x/nbinshi for x in range(1,nbinshi+1)])
    #return array.array('d',[1.0*maxqie*x/nbinsqie for x in range(0,nbinsqie+1)])

def binedgesmass():
    maxmass = 7.0
    minmass = 0.0
    nbins = 35
    edges = array.array('d')
    mass = 0
    delta = 0.4
    while (mass<=7.0):
        edges.append(mass)
        if mass>=4.0:
            delta = 0.4
        elif mass >= 2.4:
            delta = 0.2
        mass += delta
    return array.array('d',[minmass + 1.0*maxmass*x/nbins for x in range(0,nbins+1)])
    #return edges

"""
def makeqiebins(maxqie=0):
    stepcounts = [17,20,21,20,20,21,20,20,21,20,20,21,6]
    edges = array.array('d')
    i=-1
    stepsize = 1
    for bigstep in range(0,13):
        for littlestep in range(0,stepcounts[bigstep]):
            i += stepsize
            #print i,i-0.5*stepsize
            edges.append(i-0.5*stepsize)
            if (i==540):
                binedges.append(i+0.5*stepsize)
                #print i+0.5*stepsize
                i+=15
            if (maxqie!=0 and i>maxqie):
                return edges
        edges.append(i+0.5*stepsize)
        #print i+0.5*stepsize
        stepsize *= 2
        #print "new stepsize"
    return edges
"""
