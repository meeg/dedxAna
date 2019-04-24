#!/usr/bin/env python
import sys
import array, math
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, gPad, TF1, THStack, TLegend, TH2D, TH1D, TGraphErrors, TSpline3, TEfficiency
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

xfcut = "xF>0.67 && xF<0.9 && RFmax<Inh_thres"
#xfcut = "xF>0.67 && xF<0.9"
dimensions = "(50,0,500,40,0,10)"
cuts = xfcut

clean.Draw("mass:D1>>clean"+dimensions,cuts,"colz")
cleanhist = gDirectory.Get("clean")
c.Print(outfilename+".pdf");

messy.Draw("mass:D1>>messy"+dimensions,cuts,"colz")
messyhist = gDirectory.Get("messy")
c.Print(outfilename+".pdf");

messyclean.Draw("mass:D1>>messyclean"+dimensions,cuts,"colz")
messycleanhist = gDirectory.Get("messyclean")
c.Print(outfilename+".pdf");

c.SetLogz(0)

effhist = messyhist.Clone("eff")
effhist.Divide(cleanhist)

effhistnopickup = messycleanhist.Clone("effnopickup")
effhistnopickup.Sumw2()
#effhist = messyhist.Clone("eff")
effhistnopickup.Divide(cleanhist)
effhist.GetZaxis().SetRangeUser(0,1.0)

eff = TEfficiency(messycleanhist,cleanhist)
eff.SetName("teff")
eff.Write()

outfile.Write()

effhist.Draw("surf")
c.Print(outfilename+".pdf");

effhist.Draw("colz")
c.Print(outfilename+".pdf");


effhistnopickup.Draw("surf")
c.Print(outfilename+".pdf");

effhistnopickup.Draw("colz")
c.Print(outfilename+".pdf");

effhistnopickup.Draw("e")
c.Print(outfilename+".pdf");

eff.Draw("colz")
c.Print(outfilename+".pdf");

efffunc = TF1("efffunc","TMath::Max(0.0,([0] - x/[1]))",0,1500)
#efffunc.SetParameter(0,1.0)
#efffunc.SetParameter(1,500)

massArr = array.array('d')
zeroArr = array.array('d')
xintArr = array.array('d')
yintArr = array.array('d')
xintErrArr = array.array('d')
yintErrArr = array.array('d')
for iy in range(1,cleanhist.GetNbinsY()+1):
    cleanslice = cleanhist.ProjectionX("cleanslice",iy,iy)
    messyslice = messycleanhist.ProjectionX("messyslice",iy,iy)
    sliceeff = TEfficiency(messyslice,cleanslice)
    efffunc.SetParameters(1.0,500)
    efffunc.FixParameter(0,1.0)
    s = sliceeff.Fit(efffunc,"S")
    sliceeff.Draw("AP")
    #c.Print(outfilename+".pdf");

    if s.Get() and s.Get().IsValid() and s.Get().CovMatrixStatus()==3:
        massArr.append(cleanhist.GetYaxis().GetBinCenter(iy))
        zeroArr.append(0)
        xintArr.append(s.Parameter(1))
        yintArr.append(s.Parameter(0))
        xintErrArr.append(s.ParError(1))
        yintErrArr.append(s.ParError(0))

xintgraph = TGraphErrors(len(massArr),massArr,xintArr,zeroArr,xintErrArr)
xintgraph.SetTitle("X-intercept;mass [GeV];D1")
xintgraph.SetName("xintgraph")
xintgraph.Write()
xintgraph.Draw("A*")
xintgraph.GetYaxis().SetRangeUser(0,1000)
xintgraph.Fit("pol3")
c.Print(outfilename+".pdf");

yintgraph = TGraphErrors(len(massArr),massArr,yintArr,zeroArr,yintErrArr)
yintgraph.Draw("A*")
yintgraph.GetYaxis().SetRangeUser(0.5,1.5)
c.Print(outfilename+".pdf");

#clean.Draw("D1>>cleanslice(10,0,500)",xfcut+" && mass>{0} && mass<{1}".format(5.0,5.2))
#cleanslice = gDirectory.Get("cleanslice")
#messyclean.Draw("D1>>messyslice(10,0,500)",xfcut+" && mass>{0} && mass<{1}".format(5.0,5.2))
#messyslice = gDirectory.Get("messyslice")



c.Print(outfilename+".pdf]");
outfile.Close()
