#!/usr/bin/env python
import sys
import math
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, gPad, TF1, THStack, TLegend, TH2D, TH1D
import getopt

gROOT.SetBatch(True)
gStyle.SetOptStat(11)
#gStyle.SetOptFit(1)
infile = TFile("test_occupancy2.root")
#infile = TFile("roadCheck_test.root")

outfilename="normalization"

c = TCanvas("c","c",1200,900);
c.Print(outfilename+".pdf[")

outfile = TFile(outfilename+".root","RECREATE")

events = infile.Get("save")
events.Draw("RF00:D1>>hd1(50,0,1e3,400,0,4e4)","NIM3 && targetPos==6 && dataQuality==0","colz")
hist = gDirectory.Get("hd1")
hist.SetTitle("QIE vs. chamber intensity, NIM3 events;D1;QIE RF00")
c.Print(outfilename+".pdf");

nbinsX = hist.GetNbinsX()
nbinsY = hist.GetNbinsY()
hnorm = TH1D("hnormd1","hnormd1",nbinsX,hist.GetXaxis().GetBinLowEdge(1),hist.GetXaxis().GetBinUpEdge(nbinsX))
for ix in range(1,nbinsX+1):
    for iy in range(1,nbinsY+1):
        hnorm.Fill(hist.GetXaxis().GetBinCenter(ix), hist.GetBinContent(ix,iy)*hist.GetXaxis().GetBinCenter(ix))

hnorm.SetTitle("normalization;D1;QIE integral [arb. units]")
hnorm.Draw("hist")
c.Print(outfilename+".pdf");


events = infile.Get("save")
events.Draw("RF00:D1+D2+D3>>hdsum(40,0,4e3,400,0,4e4)","NIM3 && targetPos==6 && dataQuality==0","colz")
hist = gDirectory.Get("hdsum")
hist.SetTitle("QIE vs. chamber intensity, NIM3 events;D1+D2+D3;QIE RF00")
c.Print(outfilename+".pdf");

nbinsX = hist.GetNbinsX()
nbinsY = hist.GetNbinsY()
hnorm = TH1D("hnormdsum","hnormdsum",nbinsX,hist.GetXaxis().GetBinLowEdge(1),hist.GetXaxis().GetBinUpEdge(nbinsX))
for ix in range(1,nbinsX+1):
    for iy in range(1,nbinsY+1):
        hnorm.Fill(hist.GetXaxis().GetBinCenter(ix), hist.GetBinContent(ix,iy)*hist.GetXaxis().GetBinCenter(ix))

hnorm.SetTitle("normalization;D1+D2+D3;QIE integral [arb. units]")
hnorm.Draw("hist")
c.Print(outfilename+".pdf");


events = infile.Get("save")
events.Draw("RF00>>hqie(100,0,1e4)","NIM3 && targetPos==6 && dataQuality==0","")
hist = gDirectory.Get("hqie")
hist.SetTitle("QIE, NIM3 events;QIE RF00")
c.Print(outfilename+".pdf");

nbinsX = hist.GetNbinsX()
hnorm = TH1D("hnormqie","hnormqie",nbinsX,hist.GetXaxis().GetBinLowEdge(1),hist.GetXaxis().GetBinUpEdge(nbinsX))
for ix in range(1,nbinsX+1):
    hnorm.Fill(hist.GetXaxis().GetBinCenter(ix), hist.GetBinContent(ix)*hist.GetXaxis().GetBinCenter(ix))

hnorm.SetTitle("normalization;QIE;QIE integral [arb. units]")
hnorm.Draw("hist")
c.Print(outfilename+".pdf");


c.Print(outfilename+".pdf]");
outfile.Write()
outfile.Close()
