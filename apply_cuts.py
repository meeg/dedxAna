#!/usr/bin/env python
import sys
import array, math
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, gPad, TF1, THStack, TLegend, TH2D, TH1D, TGraphErrors, TSpline3
import getopt
import utils

gROOT.SetBatch(True)
gStyle.SetOptStat(11)
gStyle.SetOptFit(1)

events = TChain("save")
events.Add("test.root")
events.Add("test2.root")
#infile = TFile("test.root")
#events = infile.Get("save")

outfilename="cut_data"

outfile = TFile(outfilename+".root","RECREATE")

#MATRIX1 && abs(dx)<.25 && abs(dy-1.6)<.22 && dx*dx+(dy-1.6)*(dy-1.6)<.06 && dz>-280 && dz<-5 && abs(dpx)<1.8 && abs(dpy)<2 && dpx*dpx+dpy*dpy<5 && dpz>38 && dpz<116 && abs(trackSeparation)<270 && chisq_dimuon<18 && pchisq_target<15 && ppz1>9 && ppz1<75 && pnumHits>13 && pxT*pxT+(pyT-1.6)*(pyT-1.6)<320 && pxD*pxD+(pyD-1.6)*(pyD-1.6)<1100 && pxD*pxD+(pyD-1.6)*(pyD-1.6)>16 && pchisq_target<1.5*pchisq_upstream && pchisq_target<1.5*pchisq_dump && pz0<-5 && pz0>-320 && pchisq/(pnumHits-5)<12 && py1/py3<1 && nchisq_target<15 && npz1>9 && npz1<75 && nnumHits>13 && nxT*nxT+(nyT-1.6)*(nyT-1.6)<320 && nxD*nxD+(nyD-1.6)*(nyD-1.6)<1100 && nxD*nxD+(nyD-1.6)*(nyD-1.6)>16 && nchisq_target<1.5*nchisq_upstream && nchisq_target<1.5*nchisq_dump && nz0<-5 && nz0>-320 && nchisq/(nnumHits-5)<12 && ny1/ny3<1


#qiecut = " && ".join([i+"<5000" for i in ["RFm{0:02d}".format(j) for j in range(8,0,-1)]+["RF00"]+["RFp{0:02d}".format(j) for j in range(1,9)]])
qualitycut = utils.qualitycuts()

dimuoncuts = utils.dimuoncuts()

trackcuts = utils.trackcuts()

datacuts = " && ".join(["MATRIX1",dimuoncuts,trackcuts])
print datacuts


cutevents = events.CopyTree(" && ".join([qualitycut,datacuts]))

cutevents.Write()
outfile.Write()
outfile.Close()
