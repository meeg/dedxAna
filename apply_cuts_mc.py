#!/usr/bin/env python
import sys
import array, math
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, gPad, TF1, THStack, TLegend, TH2D, TH1D, TGraphErrors, TSpline3
import getopt
import utils

gROOT.SetBatch(True)
gStyle.SetOptStat(11)
gStyle.SetOptFit(1)

dimuoncuts = utils.dimuoncuts()

trackcuts = utils.trackcuts()

datacuts = " && ".join([dimuoncuts,trackcuts])
print datacuts


events = TChain("save")
events.Add("mc_drellyan_C_M026_S002_messy_v2.root")
outfilename="cut_data_messy"
outfile = TFile(outfilename+".root","RECREATE")

cutevents = events.CopyTree(" && ".join([datacuts]))

cutevents.Write()
outfile.Write()
outfile.Close()

events = TChain("save")
events.Add("mc_drellyan_C_M026_S002_clean_v2.root")
outfilename="cut_data_clean"
outfile = TFile(outfilename+".root","RECREATE")

cutevents = events.CopyTree(" && ".join([datacuts]))

cutevents.Write()
outfile.Write()
outfile.Close()

