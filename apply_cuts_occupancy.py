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
events.Add("occupancy_rs67_db01.root")
events.Add("occupancy_rs67_db03.root")
#infile = TFile("test.root")
#events = infile.Get("save")

outfilename="cut_data_occupancy"

outfile = TFile(outfilename+".root","RECREATE")

cutevents = events.CopyTree("NIM3")

cutevents.Write()
outfile.Write()
outfile.Close()
