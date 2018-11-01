#!/usr/bin/env python
import sys
import array, math
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, gPad, TF1, THStack, TLegend, TH2D, TH1D, TGraphErrors, TSpline3
import getopt

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

#def makepotbins(maxpot):
    #edges = array.array('d')
    #pot = 0
    #while pot <= maxpot:
        #edges.append(pot)
        #pot += 2000
    #return edges

gROOT.SetBatch(True)
gStyle.SetOptStat(11)
gStyle.SetOptFit(1)
infile = TFile("test.root")
events = infile.Get("save")

normfile = TFile("test_occupancy3.root")
normevents = normfile.Get("save")

outfilename="backgroundfit_histos"

c = TCanvas("c","c",1200,900);
c.Print(outfilename+".pdf[")

c.SetLogz(1)
outfile = TFile(outfilename+".root","RECREATE")


#qiecut = " && ".join([i+"<5000" for i in ["RFm{0:02d}".format(j) for j in range(8,0,-1)]+["RF00"]+["RFp{0:02d}".format(j) for j in range(1,9)]])
qiecut = "RFmax<Inh_thres"
#spillcut = "runID>13861 && runID<14388"
spillcut = "spillID>0"
#spillcut = "spillID>610e3"
qualitycut = "dataQuality==0"
#targetcut = "targetPos==6"
#targetcut = "targetPos==1"
targetcut = "targetPos>0"
xfcut = "xF>0.67 && xF<0.9"
potcut = "PotPerQie<1e4&&PotPerQie>0.1"
datacuts = "MATRIX1 && chisq_dimuon<17 && pchisq_target<14 && nchisq_target<14 && pchisq/(pnumHits-5)<12 && nchisq/(nnumHits-5)<12 && pnumHits>13 && nnumHits>13"
#datacuts = "chisq_dimuon<17 && pchisq_target<14 && nchisq_target<14 && pchisq/(pnumHits-5)<12 && nchisq/(nnumHits-5)<12 && pnumHits>13 && nnumHits>13"
#datacuts = "chisq_dimuon<25 && abs(dx)<2 && abs(dy)<2"

#qiepedestal = 36
#qiepedestal = 0
qiepedestal = 50
intensityvar = "(RF00-{0})*PotPerQie".format(qiepedestal)

#binedges = makeqiebins(6000)
#binedges = makepotbins(1e5)
maxqie = 100e3
#nbins = 50
#nbins = 100
nbins = 100
binedges = array.array('d',[1.0*maxqie*x/nbins for x in range(0,nbins+1)])



histqiematrix = TH1D("hqiematrix","hqiematrix",len(binedges)-1,binedges)
normevents.Draw(intensityvar+">>+hqiematrix"," && ".join(["MATRIX1",targetcut,qualitycut,qiecut,potcut,spillcut]),"")
histqiematrix.SetTitle("triggers, MATRIX1 events;"+intensityvar)
c.Print(outfilename+".pdf");

histqie = TH1D("hqie","hqie",len(binedges)-1,binedges)
normevents.Draw(intensityvar+">>+hqie"," && ".join(["NIM3",targetcut,qualitycut,qiecut,potcut,spillcut]),"")
histqie.SetTitle("triggers, NIM3 events;"+intensityvar)
c.Print(outfilename+".pdf");

events = infile.Get("save")
hist = TH2D("hdata","hdata",len(binedges)-1,binedges,70,0,7)
events.Draw("mass:{0}>>+hdata".format(intensityvar)," && ".join([targetcut,qualitycut,potcut,spillcut,xfcut,datacuts]),"colz")
hist.SetTitle("mass vs. "+intensityvar)
c.Print(outfilename+".pdf");


#histd1 = TH2D("hd1","hd1",len(binedges)-1,binedges,100,0,1e3)
#events.Draw("D1:{0}>>+hd1".format(intensityvar)," && ".join([targetcut,qualitycut,potcut,spillcut,xfcut,datacuts]),"colz")
#histd1.SetTitle("D1 vs. "+intensityvar)
#c.Print(outfilename+".pdf");


#c.Print(outfilename+".pdf]");
outfile.Write()
outfile.Close()
