#!/usr/bin/env python
import sys
import array, math
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, gPad, TF1, THStack, TLegend, TH2D, TH1D, TGraphErrors, TSpline3, TObjArray, TFractionFitter
import getopt
import utils

gROOT.SetBatch(True)
gStyle.SetOptStat(11)
gStyle.SetOptFit(1)

datafile = TFile("cut_data_mix.root")
events = datafile.Get("save")

outfilename="mixplots"

c = TCanvas("c","c",1200,900);
c.Print(outfilename+".pdf[")

outfile = TFile(outfilename+".root","RECREATE")
outfile.cd()

#targetcut = "targetPos==1" #H2
#targetcut = "targetPos==3" #D2
#targetcut = "targetPos==5" #Fe
#targetcut = "targetPos==6" #C
#targetcut = "targetPos==7" #W
#targetcut = "targetPos>=5" #solid targets
#targetcut = "targetPos>0"
targetnames = ["all targets","H2","flask","D2","empty","Fe","C","W","all solid targets"]

#qiecut = utils.qiecuts()
qualitycut = utils.qualitycuts(True)
runcut = utils.runcut()
intensityvar = utils.intensityvar(True)
#binedgesqie = utils.binedgesqie()
binedgesqie = array.array('d',[0,30e3,50e3,80e3,100e3])
binedgesmass = utils.binedgesmass()
xfcut = "xF>0.67 && xF<0.9"
xfcutname = "xF=[0.67,0.9]"

for targetnum in range(1,9):
    c.SetLogz(1)

    xfbinnum = 0
    targetcut = "targetPos=="+str(targetnum)
    if targetnum==0:
        targetcut = "targetPos>0"
    if targetnum==8:
        targetcut = "targetPos>=5"

    namestr = "tgt{0}xf{1}".format(targetnum,xfbinnum)
    titlestr = "{0}, {1}".format(targetnames[targetnum],xfcutname)

    hist = TH2D("hdata_"+namestr,"hdata_"+namestr,len(binedgesqie)-1,binedgesqie,len(binedgesmass)-1,binedgesmass)
    events.Draw("mass:{0}>>+hdata_{1}".format(intensityvar,namestr)," && ".join([targetcut,qualitycut,runcut,xfcut]),"colz")
    hist.Sumw2()
    hist.SetTitle("mass vs. {0}, {1}".format(intensityvar,titlestr))
    #c.Print(outfilename+".pdf");

    #hist = infile.Get("hdata")
    #hist.Sumw2()
    #hist.Draw("colz")
    #c.Print(outfilename+".pdf");

    #histd1 = infile.Get("hd1")
    #histd1.Sumw2()
    #histd1.Draw("colz")
    #c.Print(outfilename+".pdf");


    nbinsX = hist.GetNbinsX()
    nbinsY = hist.GetNbinsY()

    hstack = THStack("hs",hist.GetTitle())
    dataslice = hist.ProjectionY("rawdataslice_{0}".format(namestr))
    dataslice.Scale(1.0/dataslice.Integral())
    dataslice.SetLineColor(4)
    hstack.Add(dataslice)
    for ix in range(1,nbinsX+1):
        dataslice = hist.ProjectionY("rawdataslice_{0}_{1}".format(namestr,ix),ix,ix)
        #dataslice.Draw()
        #c.Print(outfilename+".pdf");
        if ix<4:
            dataslice.Scale(1.0/dataslice.Integral())
            dataslice.SetLineColor(ix)
            hstack.Add(dataslice)
    hstack.Draw("nostack")
    c.Print(outfilename+".pdf");

    outfile.Write()

#    qieArr = array.array('d')
#    zeroArr = array.array('d')
#    p0Arr = array.array('d')
#    p0ErrArr = array.array('d')
#    for ix in range(1,nbinsX+1):
#        proj = hEffCorr.ProjectionY("effCorr"+str(ix),ix,ix)
#        proj.SetTitle("efficiency correction, {2} [{0}, {1}];mass;arbitrary units".format(hEffCorr.GetXaxis().GetBinLowEdge(ix),hEffCorr.GetXaxis().GetBinUpEdge(ix),intensityvar))
#        proj.GetYaxis().SetRangeUser(-0.1,1.5)
#        s = proj.Fit("pol0","QS","",1.0,5.5)
#        if s.Get() and s.Get().IsValid() and s.Get().Ndf()>0:
#            #c.Print(outfilename+".pdf")
#            qieArr.append(hEffCorr.GetXaxis().GetBinCenter(ix))
#            zeroArr.append(0)
#            p0Arr.append(s.Parameter(0))
#            p0ErrArr.append(s.ParError(0))
#
#    graph4=TGraphErrors(len(qieArr),qieArr,p0Arr,zeroArr,p0ErrArr)
#    graph4.SetTitle("deviation from linear fit;{0};data/fit".format(intensityvar))
#    #graph4.Fit("pol1","QS","",5e3,50e3)
#    graph4.SetMarkerColor(2)
#    graph4.Draw("A*X")
#    #graph4.GetXaxis().SetRangeUser(50,2000)
#    graph4.GetYaxis().SetRangeUser(0.8,1.2)
#    #c.Print(outfilename+".pdf");
#    #effgraph.Draw("*")
#    #c.Print(outfilename+".pdf");

c.Print(outfilename+".pdf]");
outfile.Write()
outfile.Close()
#sys.exit(0)
