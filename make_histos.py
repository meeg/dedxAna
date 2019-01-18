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
runcut = utils.runcut()
intensityvar = utils.intensityvar()
binedgesqie = utils.binedgesqie()

targetnames = ["all targets","H2","flask","D2","empty","Fe","C","W","all solid targets"]

for targetnum in range(0,9):
    targetcut = "targetPos=="+str(targetnum)
    if targetnum==0:
        targetcut = "targetPos>0"
    if targetnum==8:
        targetcut = "targetPos>=5"
    histqiematrix = TH1D("hqiematrix"+str(targetnum),"hqiematrix"+str(targetnum),len(binedgesqie)-1,binedgesqie)
    normevents.Draw(intensityvar+">>+hqiematrix"+str(targetnum)," && ".join(["MATRIX1",targetcut,qualitycut,qiecut,runcut]),"")
    histqiematrix.SetTitle("triggers, MATRIX1 events, {0};{1}".format(targetnames[targetnum],intensityvar))
    c.Print(outfilename+".pdf");
    histqiematrix.Write()

    histqie = TH1D("hqie"+str(targetnum),"hqie"+str(targetnum),len(binedgesqie)-1,binedgesqie)
    normevents.Draw(intensityvar+">>+hqie"+str(targetnum)," && ".join(["NIM3",targetcut,qualitycut,qiecut,runcut]),"")
    histqie.SetTitle("triggers, NIM3 events, {0};{1}".format(targetnames[targetnum],intensityvar))
    c.Print(outfilename+".pdf");
    histqie.Write()



binedgesmass = utils.binedgesmass()
xfcut = "xF>0.67 && xF<0.9"

events = infile.Get("save")
hist = TH2D("hdata","hdata",len(binedgesqie)-1,binedgesqie,len(binedgesmass)-1,binedgesmass)
events.Draw("mass:{0}>>+hdata".format(intensityvar)," && ".join([targetcut,qualitycut,runcut,xfcut]),"colz")
hist.SetTitle("mass vs. "+intensityvar)
c.Print(outfilename+".pdf");

histd1 = TH2D("hd1","hd1",len(binedgesqie)-1,binedgesqie,200,0,1e3)
events.Draw("D1:{0}>>+hd1".format(intensityvar)," && ".join([targetcut,qualitycut,runcut,xfcut]),"colz")
histd1.SetTitle("D1 vs. "+intensityvar)
c.Print(outfilename+".pdf");

histd3 = TH2D("hd3","hd3",len(binedgesqie)-1,binedgesqie,200,0,1e3)
events.Draw("D3:{0}>>+hd3".format(intensityvar)," && ".join([targetcut,qualitycut,runcut,xfcut]),"colz")
histd3.SetTitle("D3 vs. "+intensityvar)
c.Print(outfilename+".pdf");

histdtot = TH2D("hdtot","hdtot",len(binedgesqie)-1,binedgesqie,300,0,1500)
events.Draw("D1+D2+D3:{0}>>+hdtot".format(intensityvar)," && ".join([targetcut,qualitycut,runcut,xfcut]),"colz")
histdtot.SetTitle("D1+D2+D3 vs. "+intensityvar)
c.Print(outfilename+".pdf");


c.Print(outfilename+".pdf]");
outfile.Write()
outfile.Close()
