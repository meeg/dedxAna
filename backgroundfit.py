#!/usr/bin/env python
import sys
import array, math
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, gPad, TF1, THStack, TLegend, TH2D, TH1D, TGraphErrors, TSpline3
import getopt

gROOT.SetBatch(True)
gStyle.SetOptStat(11)
gStyle.SetOptFit(1)

infile = TFile("backgroundfit_histos.root")
#events = infile.Get("save")


outfilename="backgroundfit"

c = TCanvas("c","c",1200,900);
c.Print(outfilename+".pdf[")

c.SetLogz(1)
outfile = TFile(outfilename+".root","RECREATE")


histqiematrix = infile.Get("hqiematrix")
histqiematrix.Sumw2()
histqiematrix.Draw()
c.Print(outfilename+".pdf");

histqie = infile.Get("hqie")
histqie.Sumw2()
histqie.Draw()
c.Print(outfilename+".pdf");

hist = infile.Get("hdata")
hist.Sumw2()
hist.Draw("colz")
c.Print(outfilename+".pdf");

#histd1 = infile.Get("hd1")
#histd1.Sumw2()
#histd1.Draw("colz")
#c.Print(outfilename+".pdf");

intensityvar = histqie.GetXaxis().GetTitle()

histtriggerratio = histqiematrix.Clone("hqieratio")
histtriggerratio.Sumw2()
histtriggerratio.Divide(histqie)
histtriggerratio.SetTitle("trigger ratio, MATRIX1/NIM3;"+intensityvar)
s = histtriggerratio.Fit("pol2","S","",1000,60e3)
histtriggerratio.GetXaxis().SetRangeUser(0,60e3)
print s.Parameter(1)/(-2*s.Parameter(2)*30)
#c.SetLogy(1)
histtriggerratio.Draw()
c.Print(outfilename+".pdf");
c.SetLogy(0)


nbinsX = hist.GetNbinsX()
nbinsY = hist.GetNbinsY()


hlumi = histqie.Clone("hlumiqie")
#hlumi.Multiply(intensity)
intensityfunc = TF1("fx","x")
intensityfunc.SetRange(0,1e5)

fitfunc = TF1("f","pol1")
fitfunc.SetRange(0,1e5)

hlumi.Multiply(intensityfunc)

hlumi.Scale(1.0/hlumi.GetMaximum())
hlumi.SetTitle("luminosity normalization;{0};total {0} [arb. units]".format(intensityvar))
hlumi.Draw("")
c.Print(outfilename+".pdf");


hlumi2d = hist.Clone("hlumi2d")

for ix in range(1,nbinsX+1):
    for iy in range(1,nbinsY+1):
        hlumi2d.SetBinContent(ix,iy,hlumi.GetBinContent(ix))
        hlumi2d.SetBinError(ix,iy,hlumi.GetBinError(ix))

histNormedNoEff = hist.Clone("histNormedNoEff")
histNormedNoEff.SetTitle("Luminosity-normalized data;{0};mass [GeV]".format(intensityvar))
histNormedNoEff.Divide(hlumi2d)
histNormedNoEff.Draw("colz")
c.Print(outfilename+".pdf");



firstbin = 1
lastbin = hist.GetYaxis().FindBin(2.39)
projlow = histNormedNoEff.ProjectionX("projlow",firstbin,lastbin)
projlow.SetTitle("low mass, mass [{0},{1}]".format(histNormedNoEff.GetYaxis().GetBinLowEdge(firstbin),histNormedNoEff.GetYaxis().GetBinUpEdge(lastbin)))
#projlow.GetYaxis().SetRangeUser(0,projlow.GetBinContent(projlow.GetMaximumBin()))
projlow.SetMinimum(0)
projlow.Draw()
c.Print(outfilename+".pdf");

firstbin = hist.GetYaxis().FindBin(2.41)
lastbin = hist.GetYaxis().FindBin(3.39)
projhi1 = histNormedNoEff.ProjectionX("projhi1",firstbin,lastbin)
projhi1.SetTitle("high mass, mass [{0},{1}]".format(histNormedNoEff.GetYaxis().GetBinLowEdge(firstbin),histNormedNoEff.GetYaxis().GetBinUpEdge(lastbin)))
#projhi1.GetYaxis().SetRangeUser(0,projmed.GetBinContent(projmed.GetMaximumBin()))
projhi1.SetMinimum(0)
projhi1.Draw()
c.Print(outfilename+".pdf");

firstbin = hist.GetYaxis().FindBin(3.41)
lastbin = nbinsY
projhi2 = histNormedNoEff.ProjectionX("projhi2",firstbin,lastbin)
projhi2.SetTitle("high mass, mass [{0},{1}]".format(histNormedNoEff.GetYaxis().GetBinLowEdge(firstbin),histNormedNoEff.GetYaxis().GetBinUpEdge(lastbin)))
#projhi2.GetYaxis().SetRangeUser(0,projhigh.GetBinContent(projhigh.GetMaximumBin()))
projhi2.SetMinimum(0)
projhi2.Draw()
c.Print(outfilename+".pdf");


firstbin = hist.GetYaxis().FindBin(2.41)
lastbin = nbinsY
projhi = histNormedNoEff.ProjectionX("projhi",firstbin,lastbin)
projhi.SetTitle("high mass, mass [{0},{1}]".format(histNormedNoEff.GetYaxis().GetBinLowEdge(firstbin),histNormedNoEff.GetYaxis().GetBinUpEdge(lastbin)))
#projhigh.GetYaxis().SetRangeUser(0,projhigh.GetBinContent(projhigh.GetMaximumBin()))
projhi.SetMinimum(0)
projhi.Draw()
c.Print(outfilename+".pdf");


hEff = projlow.Clone("hEff") #we assume projlow is pure background and divide by intensity to get the efficiency vs. intensity (only valid at low intensity where we expect the background to be linear)
hEff.Divide(intensityfunc)
hEff.Scale(0.6/hEff.GetBinContent(hEff.GetXaxis().FindBin(10e3))) #arbitrary normalization
hEff.Draw()
c.Print(outfilename+".pdf");

minfitrange = 5e3
maxfitrange = 25e3


fithi1 = projhi1.Clone("fithi1")
fithi1.Divide(hEff)
shi1 = fithi1.Fit(fitfunc,"S","",minfitrange,maxfitrange)
shi1 = fithi1.Fit(fitfunc,"SWL","",minfitrange,maxfitrange)
c.Print(outfilename+".pdf");

effhi1 = projhi1.Clone("effhi1")
effhi1.Divide(fitfunc)
effhi1.Draw()
effhi1.SetMinimum(0)
c.Print(outfilename+".pdf");

fithi2 = projhi2.Clone("fithi2")
fithi2.Divide(hEff)
shi2 = fithi2.Fit(fitfunc,"S","",minfitrange,maxfitrange)
shi2 = fithi2.Fit(fitfunc,"SWL","",minfitrange,maxfitrange)
c.Print(outfilename+".pdf");

effhi2 = projhi2.Clone("effhi2")
effhi2.Divide(fitfunc)
effhi2.Draw()
effhi2.SetMinimum(0)
c.Print(outfilename+".pdf");

fithi = projhi.Clone("fithi")
fithi.Divide(hEff)
shi = fithi.Fit(fitfunc,"S","",minfitrange,maxfitrange)
shi = fithi.Fit(fitfunc,"SWL","",minfitrange,maxfitrange)
c.Print(outfilename+".pdf");

effhi = projhi.Clone("effhi")
effhi.Divide(fitfunc)
effhi.Draw()
effhi.SetMinimum(0)
c.Print(outfilename+".pdf");

#sigshape = projmed.Clone("sigshape")
#sigshape.Scale(1.0/smed.Parameter(1))
#sigshape.Add(projhigh,-1.0/shigh.Parameter(1))
#sigshape.Scale(1.0/(smed.Parameter(0)/smed.Parameter(1)-shigh.Parameter(0)/shigh.Parameter(1)))
#
#bkgshape = projmed.Clone("bkgshape")
#bkgshape.Scale(1.0/smed.Parameter(0))
#bkgshape.Add(projhigh,-1.0/shigh.Parameter(0))
#bkgshape.Scale(1.0/(smed.Parameter(1)/smed.Parameter(0)-shigh.Parameter(1)/shigh.Parameter(0)))
#
#sigshape.Draw()
#c.Print(outfilename+".pdf");
#bkgshape.Draw()
#c.Print(outfilename+".pdf");

effhi.Draw()
effhi.GetYaxis().SetRangeUser(0.0,1.5)
effhi1.SetLineColor(2)
effhi1.Draw("same")
effhi2.SetLineColor(4)
effhi2.Draw("same")
#hEff.SetLineColor(3)
#hEff.Draw("same")
#efffitfunc = TF1("f","[0]/x")
#efffitfunc.SetRange(0,1e5)
#effmed.Fit(efffitfunc)
c.Print(outfilename+".pdf");

heff1d = effhi

minfitrange = 0
maxfitrange = 80000

fitlow = projlow.Clone("fitlow")
fitlow.Divide(heff1d)
s = fitlow.Fit(fitfunc,"S","",minfitrange,maxfitrange)
s = fitlow.Fit(fitfunc,"SWL","",minfitrange,maxfitrange)
c.Print(outfilename+".pdf");



heff2d = hist.Clone("heff2d")

for ix in range(1,nbinsX+1):
    for iy in range(1,nbinsY+1):
        heff2d.SetBinContent(ix,iy,heff1d.GetBinContent(ix))
        heff2d.SetBinError(ix,iy,heff1d.GetBinError(ix))

histNormed = histNormedNoEff.Clone("hEventsNormalized")
histNormed.SetTitle("Efficiency-corrected, luminosity-normalized data;{0};mass [GeV]".format(intensityvar))
histNormed.Divide(heff2d)
histNormed.Draw("colz")
c.Print(outfilename+".pdf");

massArr = array.array('d')
zeroArr = array.array('d')
p0Arr = array.array('d')
p1Arr = array.array('d')
p0ErrArr = array.array('d')
p1ErrArr = array.array('d')
sigArr = array.array('d')
bkgArr = array.array('d')
sigErrArr = array.array('d')
bkgErrArr = array.array('d')
hEffCorr = hist.Clone("hEffCorr")
hEffCorr.SetTitle("deviation from linear fit;{0};mass [GeV]".format(intensityvar))
#c.Print(outfilename+".pdf]");
#sys.exit(0)

minfitrange = 0
maxfitrange = 80000

firstbin = histNormed.GetXaxis().FindBin(minfitrange)
lastbin = histNormed.GetXaxis().FindBin(maxfitrange)

hist1d = hist.ProjectionY("hdata1d",firstbin,lastbin)
hist1d.Draw()
c.Print(outfilename+".pdf");

bkghist = hlumi.Clone("bkgcounts")
sighist = hlumi.Clone("sigcounts")
bkghist.SetTitle("Background shape in raw data")
sighist.SetTitle("Signal shape in raw data")
bkghist.Multiply(heff1d)
sighist.Multiply(heff1d)

fitfunc.SetParameter(0,0)
fitfunc.SetParameter(1,1)
bkghist.Multiply(fitfunc)

fitfunc.SetParameter(0,1)
fitfunc.SetParameter(1,0)
sighist.Multiply(fitfunc)

#bkghist.Draw()
#c.Print(outfilename+".pdf");
#sighist.Draw()
#c.Print(outfilename+".pdf");

bkghistnorm = bkghist.Clone("bkghistnorm")
bkghistnorm.SetTitle("Background shape in raw data, normalized to bin width")
sighistnorm = sighist.Clone("sighistnorm")
sighistnorm.SetTitle("Signal shape in raw data, normalized to bin width")
for ix in range(1,nbinsX+1):
    width = bkghistnorm.GetXaxis().GetBinUpEdge(ix) - bkghistnorm.GetXaxis().GetBinLowEdge(ix)
    bkghistnorm.SetBinContent(ix,bkghistnorm.GetBinContent(ix)*1.0/width)
    bkghistnorm.SetBinError(ix,bkghistnorm.GetBinError(ix)*1.0/width)
    sighistnorm.SetBinContent(ix,sighistnorm.GetBinContent(ix)*1.0/width)
    sighistnorm.SetBinError(ix,sighistnorm.GetBinError(ix)*1.0/width)

bkghistnorm.Draw()
c.Print(outfilename+".pdf");
sighistnorm.Draw()
c.Print(outfilename+".pdf");


for iy in range(1,nbinsY+1):
    proj = histNormed.ProjectionX("test"+str(iy),iy,iy)
    proj.SetTitle("normalized dimuons vs. intensity, mass [{0}, {1}];{2};arbitrary units".format(histNormed.GetYaxis().GetBinLowEdge(iy),histNormed.GetYaxis().GetBinUpEdge(iy),intensityvar))
    maxval = proj.GetMaximum()
    proj.GetYaxis().SetRangeUser(-0.1*maxval,1.1*maxval)
    #proj.GetXaxis().SetRangeUser(minfitrange,1e5)
    proj.GetXaxis().SetRangeUser(0,1e5)
    #print proj.Integral()
    #if proj.Integral()>0:
    for ix in range(1,nbinsX+1):
        hEffCorr.SetBinContent(ix,iy,0.0)
    proj.Fit(fitfunc,"Q","",minfitrange,maxfitrange)
    s = proj.Fit(fitfunc,"QSWL","",minfitrange,maxfitrange)
    if s.Get() and s.Get().IsValid() and s.Get().Ndf()>0 and s.Get().Status()==0 and s.Get().CovMatrixStatus()==3:
        proj.GetYaxis().SetRangeUser(-0.2*fitfunc.Eval(maxfitrange),3*fitfunc.Eval(maxfitrange))
        c.Print(outfilename+".pdf")
        #print histNormed.GetYaxis().GetBinCenter(iy),s.Parameter(0),s.Parameter(1)
        massArr.append(histNormed.GetYaxis().GetBinCenter(iy))
        zeroArr.append(0)
        p0Arr.append(s.Parameter(0)*sighist.Integral(firstbin,lastbin))
        #print s.Parameter(0)*sighist.Integral(firstbin,lastbin)
        p0ErrArr.append(s.ParError(0)*sighist.Integral(firstbin,lastbin))
        p1Arr.append(s.Parameter(1)*bkghist.Integral(firstbin,lastbin))
        p1ErrArr.append(s.ParError(1)*bkghist.Integral(firstbin,lastbin))

        #if (histNormed.GetYaxis().GetBinCenter(iy)==3.05):
            #s.Print("V")
        proj.Divide(fitfunc)
        for ix in range(1,nbinsX+1):
            hEffCorr.SetBinContent(ix,iy,proj.GetBinContent(ix))
            hEffCorr.SetBinError(ix,iy,proj.GetBinError(ix))
        #proj.Draw()
        #c.Print(outfilename+".pdf")

graph=TGraphErrors(len(massArr),massArr,p0Arr,zeroArr,p0ErrArr)
graph.SetTitle("Signal vs. mass, {0}=[{1},{2}];mass [GeV];arbitrary units".format(intensityvar,minfitrange,maxfitrange))
graph.SetName("siggraph")
graph.Write()
#outfile.Add(graph)
graph.Draw("A*")
c.Print(outfilename+".pdf");

graph2=TGraphErrors(len(massArr),massArr,p1Arr,zeroArr,p1ErrArr)
graph2.SetTitle("Background vs. mass, {0}=[{1},{2}];mass [GeV];arbitrary units".format(intensityvar,minfitrange,maxfitrange))
graph2.SetName("bkggraph")
graph2.Write()
#outfile.Add(graph2)
graph2.SetMarkerColor(2)
graph2.Draw("*")
c.Print(outfilename+".pdf");
graph2.Draw("A*")
c.Print(outfilename+".pdf");

hist1d.Draw()
graph.Draw("*")
graph2.Draw("*")
c.Print(outfilename+".pdf");

c.SetLogz(0)
hEffCorr.GetZaxis().SetRangeUser(0.5,2)
hEffCorr.GetYaxis().SetRangeUser(1.0,5.5)
hEffCorr.Draw("colz")
c.Print(outfilename+".pdf");
hEffCorr.GetZaxis().SetRangeUser(0.8,1.2)
hEffCorr.GetXaxis().SetRangeUser(minfitrange,maxfitrange)
c.Print(outfilename+".pdf");

qieArr = array.array('d')
zeroArr = array.array('d')
p0Arr = array.array('d')
p0ErrArr = array.array('d')
for ix in range(1,nbinsX+1):
    proj = hEffCorr.ProjectionY("effCorr"+str(ix),ix,ix)
    proj.SetTitle("efficiency correction, {2} [{0}, {1}];mass;arbitrary units".format(hEffCorr.GetXaxis().GetBinLowEdge(ix),hEffCorr.GetXaxis().GetBinUpEdge(ix),intensityvar))
    proj.GetYaxis().SetRangeUser(-0.1,1.5)
    s = proj.Fit("pol0","QS","",1.0,5.5)
    if s.Get() and s.Get().IsValid() and s.Get().Ndf()>0:
        #c.Print(outfilename+".pdf")
        qieArr.append(hEffCorr.GetXaxis().GetBinCenter(ix))
        zeroArr.append(0)
        p0Arr.append(s.Parameter(0))
        p0ErrArr.append(s.ParError(0))

graph4=TGraphErrors(len(qieArr),qieArr,p0Arr,zeroArr,p0ErrArr)
graph4.SetTitle("deviation from linear fit;{0};data/fit".format(intensityvar))
#graph4.Fit("pol1","QS","",5e3,50e3)
graph4.SetMarkerColor(2)
graph4.Draw("A*X")
#graph4.GetXaxis().SetRangeUser(50,2000)
graph4.GetYaxis().SetRangeUser(0.8,1.2)
c.Print(outfilename+".pdf");
#effgraph.Draw("*")
#c.Print(outfilename+".pdf");

c.Print(outfilename+".pdf]");
outfile.Write()
outfile.Close()
