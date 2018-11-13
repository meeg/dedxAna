#!/usr/bin/env python
import sys
import array, math
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, gPad, TF1, THStack, TLegend, TH2D, TH1D, TGraphErrors, TSpline3
import getopt
import utils

gROOT.SetBatch(True)
gStyle.SetOptStat(11)
gStyle.SetOptFit(1)
infile = TFile("cut_data.root")
events = infile.Get("save")

normevents = TChain("save")
normevents.Add("test_occupancy3.root")
normevents.Add("test_occupancy4.root")
#normfile = TFile("test_occupancy3.root")
#normevents = normfile.Get("save")

outfilename="backgroundfit_histos"

c = TCanvas("c","c",1200,900);
c.Print(outfilename+".pdf[")

c.SetLogz(1)
outfile = TFile(outfilename+".root","RECREATE")

qiecut = utils.qiecuts()
qualitycut = utils.qualitycuts()
#spillcut = "runID>13861 && runID<14388"
spillcut = "spillID>0"
#spillcut = "spillID>610e3"
targetcut = "targetPos==1" #H2
#targetcut = "targetPos==3" #D2
#targetcut = "targetPos==5" #Fe
#targetcut = "targetPos==6" #C
#targetcut = "targetPos==7" #W
#targetcut = "targetPos>=5" #solid targets
#targetcut = "targetPos>0"
xfcut = "xF>0.67 && xF<0.9"

intensityvar = utils.intensityvar()

binedgesqie = utils.binedgesqie()
binedgesmass = utils.binedgesmass()



histqiematrix = TH1D("hqiematrix","hqiematrix",len(binedgesqie)-1,binedgesqie)
normevents.Draw(intensityvar+">>+hqiematrix"," && ".join(["MATRIX1",targetcut,qualitycut,qiecut,spillcut]),"")
histqiematrix.SetTitle("triggers, MATRIX1 events;"+intensityvar)
c.Print(outfilename+".pdf");

histqie = TH1D("hqie","hqie",len(binedgesqie)-1,binedgesqie)
normevents.Draw(intensityvar+">>+hqie"," && ".join(["NIM3",targetcut,qualitycut,qiecut,spillcut]),"")
histqie.SetTitle("triggers, NIM3 events;"+intensityvar)
c.Print(outfilename+".pdf");

events = infile.Get("save")
#hist = TH2D("hdata","hdata",len(binedgesqie)-1,binedgesqie,35,0,7)
hist = TH2D("hdata","hdata",len(binedgesqie)-1,binedgesqie,len(binedgesmass)-1,binedgesmass)
events.Draw("mass:{0}>>+hdata".format(intensityvar)," && ".join([targetcut,qualitycut,spillcut,xfcut]),"colz")
hist.SetTitle("mass vs. "+intensityvar)
c.Print(outfilename+".pdf");


histd1 = TH2D("hd1","hd1",len(binedgesqie)-1,binedgesqie,200,0,1e3)
events.Draw("D1:{0}>>+hd1".format(intensityvar)," && ".join([targetcut,qualitycut,spillcut,xfcut]),"colz")
histd1.SetTitle("D1 vs. "+intensityvar)
c.Print(outfilename+".pdf");

histd3 = TH2D("hd3","hd3",len(binedgesqie)-1,binedgesqie,200,0,1e3)
events.Draw("D3:{0}>>+hd3".format(intensityvar)," && ".join([targetcut,qualitycut,spillcut,xfcut]),"colz")
histd3.SetTitle("D3 vs. "+intensityvar)
c.Print(outfilename+".pdf");

histdtot = TH2D("hdtot","hdtot",len(binedgesqie)-1,binedgesqie,300,0,1500)
events.Draw("D1+D2+D3:{0}>>+hdtot".format(intensityvar)," && ".join([targetcut,qualitycut,spillcut,xfcut]),"colz")
histdtot.SetTitle("D1+D2+D3 vs. "+intensityvar)
c.Print(outfilename+".pdf");


c.Print(outfilename+".pdf]");
outfile.Write()
outfile.Close()
