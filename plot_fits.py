#!/usr/bin/env python
import sys
import array, math
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, gPad, TF1, THStack, TLegend, TH2D, TH1D, TGraphErrors, TSpline3, TObjArray, TFractionFitter
import getopt
import utils

gROOT.SetBatch(True)
gStyle.SetOptStat(0)
#gStyle.SetOptFit(1)

infile = TFile("backgroundfit.root")
mixfile = TFile("mixplots.root")


outfilename="backgroundfit_summary"

c = TCanvas("c","c",1200,900);
c.Print(outfilename+".pdf[")

outfile = TFile(outfilename+".root","RECREATE")

#targetcut = "targetPos==1" #H2
#targetcut = "targetPos==3" #D2
#targetcut = "targetPos==5" #Fe
#targetcut = "targetPos==6" #C
#targetcut = "targetPos==7" #W
#targetcut = "targetPos>=5" #solid targets
#targetcut = "targetPos>0"
#targetnames = ["","H2","flask","D2","empty","Fe","C","W"]

#xfcut = "xF>0.67 && xF<0.9"
#xfcutname = "xF=[0.67,0.9]"

c.Clear()
c.Divide(2,4)
for targetnum in range(1,9):
    c.cd(targetnum)
    xfbinnum = 0
    namestr = "tgt{0}xf{1}".format(targetnum,xfbinnum)
    effhi = infile.Get("effhi_"+namestr)
    effhi.Draw()
c.cd()
c.Print(outfilename+".pdf");

c.Clear()
c.Divide(2,4)
for targetnum in range(1,9):
    c.cd(targetnum)
    hlumi = infile.Get("hlumiqie"+str(targetnum))
    hlumi.Draw()
c.cd()
c.Print(outfilename+".pdf");


c.Clear()
c.Divide(2,4)
for targetnum in range(1,9):
    c.cd(targetnum)
    xfbinnum = 0
    namestr = "tgt{0}xf{1}".format(targetnum,xfbinnum)

    bkghist = infile.Get("bkgcounts_"+namestr)
    sighist = infile.Get("sigcounts_"+namestr)
    bkghist.Draw()
c.cd()
c.Print(outfilename+".pdf");

c.Clear()
c.Divide(2,4)
for targetnum in range(1,9):
    c.cd(targetnum)
    xfbinnum = 0
    namestr = "tgt{0}xf{1}".format(targetnum,xfbinnum)

    hist1d = infile.Get("hdata1d_"+namestr)
    siggraph = infile.Get("siggraph_"+namestr)
    bkggraph = infile.Get("bkggraph_"+namestr)

    hist1d.Draw()
    hist1d.GetXaxis().SetRangeUser(1.5,7.0)
    siggraph.Draw("*")
    bkggraph.Draw("*")
c.cd()
c.Print(outfilename+".pdf");

c.Clear()
c.Divide(2,4)
leg = []
for targetnum in range(1,9):
    c.cd(targetnum)
    #leg.append(TLegend(0.0,0.75,0.2,0.9))
    leg.append(TLegend(0.55,0.65,0.9,0.9))
    xfbinnum = 0
    namestr = "tgt{0}xf{1}".format(targetnum,xfbinnum)

    hist1d = infile.Get("hdata1d_"+namestr)
    siggraph2 = infile.Get("siggraph2_"+namestr)
    bkggraph2 = infile.Get("bkggraph2_"+namestr)
    leg[targetnum-1].AddEntry(hist1d,"data")
    leg[targetnum-1].AddEntry(siggraph2,"true dimuons")
    leg[targetnum-1].AddEntry(bkggraph2,"coincidence background")

    hist1d.Draw()
    siggraph2.Draw("*")
    bkggraph2.Draw("*")
    leg[targetnum-1].Draw()
c.cd()
c.Print(outfilename+".pdf");

c.Clear()
c.Divide(2,4)
leg = []
for targetnum in range(1,9):
    c.cd(targetnum)
    #leg.append(TLegend(0.0,0.75,0.2,0.9))
    leg.append(TLegend(0.55,0.65,0.9,0.9))
    xfbinnum = 0
    namestr = "tgt{0}xf{1}".format(targetnum,xfbinnum)

    mixhist = mixfile.Get("rawdataslice_{0}".format(namestr))
    bkggraph2 = infile.Get("bkggraph2_"+namestr)
    mixhist.Scale(max(bkggraph2.GetY())/mixhist.GetMaximum())
    leg[targetnum-1].AddEntry(mixhist,"mixed data")
    leg[targetnum-1].AddEntry(bkggraph2,"coincidence background")

    mixhist.Draw()
    bkggraph2.Draw("*")
    leg[targetnum-1].Draw()
c.cd()
c.Print(outfilename+".pdf");

c.Print(outfilename+".pdf]");
outfile.Write()
outfile.Close()
#sys.exit(0)
