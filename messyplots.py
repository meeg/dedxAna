#!/usr/bin/env python
import sys
import array, math
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, gPad, TF1, THStack, TLegend, TH2D, TH1D, TGraphErrors, TSpline3
import getopt
import utils

gROOT.SetBatch(True)
gStyle.SetOptStat(11)
gStyle.SetOptFit(1)

cleanfile = TFile("clean.root")
clean = cleanfile.Get("save")

messyfile = TFile("messy.root")
messy = messyfile.Get("save")

messycleanfile = TFile("messyclean.root")
messyclean = messycleanfile.Get("save")

outfilename="messyplots"

c = TCanvas("c","c",1200,900);
c.Print(outfilename+".pdf[")

c.SetLogz(1)
outfile = TFile(outfilename+".root","RECREATE")

xfcut = "xF>0.67 && xF<0.9"

clean.Draw("mass:D1>>clean(10,0,500,10,0,10)",xfcut,"colz")
cleanhist = gDirectory.Get("clean")
c.Print(outfilename+".pdf");

messy.Draw("mass:D1>>messy(10,0,500,10,0,10)",xfcut,"colz")
messyhist = gDirectory.Get("messy")
c.Print(outfilename+".pdf");

messyclean.Draw("mass:D1>>messyclean(10,0,500,10,0,10)",xfcut,"colz")
messycleanhist = gDirectory.Get("messyclean")
c.Print(outfilename+".pdf");

c.SetLogz(0)

effhist = messyhist.Clone("eff")
effhist.Divide(cleanhist)

effhistnopickup = messycleanhist.Clone("effnopickup")
#effhist = messyhist.Clone("eff")
effhistnopickup.Divide(cleanhist)
#effhist.GetZaxis().SetRangeUser(0,1.5)

outfile.Write()

effhist.Draw("surf")
c.Print(outfilename+".pdf");

effhist.Draw("colz")
c.Print(outfilename+".pdf");

effhist.GetZaxis().SetRangeUser(0,1.0)

effhist.Draw("surf")
c.Print(outfilename+".pdf");

effhist.Draw("colz")
c.Print(outfilename+".pdf");


effhistnopickup.Draw("surf")
c.Print(outfilename+".pdf");

effhistnopickup.Draw("colz")
c.Print(outfilename+".pdf");


c.Print(outfilename+".pdf]");
outfile.Close()
