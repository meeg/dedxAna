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

outfilename="fiteff"

c = TCanvas("c","c",1200,900);
c.Print(outfilename+".pdf[")

c.SetLogz(1)
outfile = TFile(outfilename+".root","RECREATE")

#MATRIX1 && abs(dx)<.25 && abs(dy-1.6)<.22 && dx*dx+(dy-1.6)*(dy-1.6)<.06 && dz>-280 && dz<-5 && abs(dpx)<1.8 && abs(dpy)<2 && dpx*dpx+dpy*dpy<5 && dpz>38 && dpz<116 && abs(trackSeparation)<270 && chisq_dimuon<18 && pchisq_target<15 && ppz1>9 && ppz1<75 && pnumHits>13 && pxT*pxT+(pyT-1.6)*(pyT-1.6)<320 && pxD*pxD+(pyD-1.6)*(pyD-1.6)<1100 && pxD*pxD+(pyD-1.6)*(pyD-1.6)>16 && pchisq_target<1.5*pchisq_upstream && pchisq_target<1.5*pchisq_dump && pz0<-5 && pz0>-320 && pchisq/(pnumHits-5)<12 && py1/py3<1 && nchisq_target<15 && npz1>9 && npz1<75 && nnumHits>13 && nxT*nxT+(nyT-1.6)*(nyT-1.6)<320 && nxD*nxD+(nyD-1.6)*(nyD-1.6)<1100 && nxD*nxD+(nyD-1.6)*(nyD-1.6)>16 && nchisq_target<1.5*nchisq_upstream && nchisq_target<1.5*nchisq_dump && nz0<-5 && nz0>-320 && nchisq/(nnumHits-5)<12 && ny1/ny3<1


#qiecut = " && ".join([i+"<5000" for i in ["RFm{0:02d}".format(j) for j in range(8,0,-1)]+["RF00"]+["RFp{0:02d}".format(j) for j in range(1,9)]])
qiecut = "RFmax<Inh_thres"
#spillcut = "runID>13861 && runID<14388"
spillcut = "spillID>0"
#spillcut = "spillID>610e3"
#targetcut = "targetPos==6"
#targetcut = "targetPos==1"
targetcut = "targetPos>0"
xfcut = "xF>0.67 && xF<0.9"

intensityvar = utils.intensityvar()

#binedges = makeqiebins(6000)
#binedges = makepotbins(1e5)
maxqie = 100e3
nbinsqie = 50
#nbinsqie = 100
#nbinsqie = 200
binedgesqie = array.array('d',[1.0*maxqie*x/nbinsqie for x in range(0,nbinsqie+1)])
#binedgesqie = array.array('d',[1.0*maxqie*10**(0.2*(x-nbinsqie)) for x in range(0,nbinsqie+1)])

#histd1 = TH2D("hd1","hd1",len(binedgesqie)-1,binedgesqie,200,0,1e3)
#events.Draw("D1:{0}>>+hd1".format(intensityvar)," && ".join([targetcut,qualitycut,potcut,spillcut,xfcut,datacuts]),"colz")
#histd1.SetTitle("D1 vs. "+intensityvar)
#c.Print(outfilename+".pdf");
#
#histd3 = TH2D("hd3","hd3",len(binedgesqie)-1,binedgesqie,200,0,1e3)
#events.Draw("D3:{0}>>+hd3".format(intensityvar)," && ".join([targetcut,qualitycut,potcut,spillcut,xfcut,datacuts]),"colz")
#histd3.SetTitle("D3 vs. "+intensityvar)
#c.Print(outfilename+".pdf");

#occupancyvar = "D1+D2+D3-44"
occupancyvar = "D1-12"
histdtot = TH2D("hdtot","hdtot",len(binedgesqie)-1,binedgesqie,300,0,600)
events.Draw("{1}:{0}>>+hdtot".format(intensityvar,occupancyvar)," && ".join([targetcut,spillcut,xfcut]),"colz")
histdtot.SetTitle(occupancyvar+" vs. "+intensityvar)
c.Print(outfilename+".pdf");
c.SetLogx(1)
c.Print(outfilename+".pdf");
c.SetLogx(0)

nbinsX = histdtot.GetNbinsX()
nbinsY = histdtot.GetNbinsY()

qieArr = array.array('d')
scaledInterceptArr = array.array('d')
#scaledInterceptErrArr = array.array('d')
for ix in range(1,nbinsX+1):
    proj = histdtot.ProjectionY("slice"+str(ix),ix,ix)
    proj.SetTitle("{2} [{0}, {1}];{3}".format(histdtot.GetXaxis().GetBinLowEdge(ix),histdtot.GetXaxis().GetBinUpEdge(ix),intensityvar,occupancyvar))
    binqie = histdtot.GetXaxis().GetBinCenter(ix)
    proj.GetXaxis().SetRangeUser(0,0.04*binqie)
    #s = proj.Fit("pol1","QSL","",0.008*binqie,max(0.016*binqie,100))
    #print -s.Parameter(0)/s.Parameter(1), -s.Parameter(0)/s.Parameter(1)/binqie
    #qieArr.append(binqie)
    #scaledInterceptArr.append(-s.Parameter(0)/s.Parameter(1)/binqie)
    #proj.Draw()
    #c.Print(outfilename+".pdf");

#graph = TGraph(len(qieArr),qieArr,scaledInterceptArr)
#graph.Draw("A*")
#graph.GetXaxis().SetRangeUser(0,20e3)
#graph.GetYaxis().SetRangeUser(0,0.01)
#c.Print(outfilename+".pdf");

refprojnum=2
refproj = gDirectory.Get("slice"+str(refprojnum))
refproj.GetXaxis().SetRangeUser(0,100)
refproj.Draw()
c.Print(outfilename+".pdf");
refqie = histdtot.GetXaxis().GetBinCenter(refprojnum)

lowproj = gDirectory.Get("slice"+str(3))
lowproj.Draw()
lowproj.GetXaxis().SetRangeUser(0,200)
c.Print(outfilename+".pdf");

highproj = gDirectory.Get("slice"+str(8))
highproj.Draw()
highproj.GetXaxis().SetRangeUser(0,600)
c.Print(outfilename+".pdf");

#efffunc = TF1("efffunc","(x*[0]<200) + (x*[0]>=200 && x*[0]<600)*(600-x*[0])/(600-200)",0,1500)
efffunc = TF1("efffunc","TMath::Max(0.0,(1.0 - 0.0018*x*[0]))",0,1500)
efffunc.SetParameter(0,1)
efffunc.Draw()
c.Print(outfilename+".pdf");


"""
for ix in range(1,nbinsX/3+1):
    proj = gDirectory.Get("slice"+str(ix))
    eff = proj.Clone("eff"+str(ix))
    binqie = histdtot.GetXaxis().GetBinCenter(ix)
    eff.Rebin(int(binqie/refqie))
    for iy in range(1,eff.GetNbinsX()+1):
        if (refproj.GetBinContent(iy)>0):
            eff.SetBinContent(iy,eff.GetBinContent(iy)/(refproj.GetBinContent(iy)))
    eff.GetXaxis().SetRangeUser(0,800)
    eff.Scale(1.0/eff.GetBinContent(eff.GetXaxis().FindBin(200)))
    eff.RecursiveRemove(eff.GetFunction("pol1"))
    eff.Draw()
    efffunc.Draw("same")
    c.Print(outfilename+".pdf");
"""

qieArr = array.array('d')
effArr = array.array('d')
for ix in range(1,nbinsX+1):
    proj = gDirectory.Get("slice"+str(ix))
    eff = refproj.Clone("test"+str(ix))
    binqie = histdtot.GetXaxis().GetBinCenter(ix)
    efffunc.SetParameter(0,1.0)
    eff.Divide(efffunc)
    denominator = eff.Integral()
    efffunc.SetParameter(0,binqie/refqie)
    eff.Multiply(efffunc)
    numerator = eff.Integral()
    #eff.Draw()
    #efffunc.Draw("same")
    #c.Print(outfilename+".pdf");
    #print numerator/denominator
    qieArr.append(binqie)
    effArr.append(numerator/denominator)

graph = TGraph(len(qieArr),qieArr,effArr)
graph.Draw("A*")
#graph.GetXaxis().SetRangeUser(0,20e3)
#graph.GetYaxis().SetRangeUser(0,0.01)
c.Print(outfilename+".pdf");

    #eff.Rebin(int(binqie/refqie))
    #for iy in range(1,eff.GetNbinsX()+1):
        #if (refproj.GetBinContent(iy)>0):
            #eff.SetBinContent(iy,eff.GetBinContent(iy)/(refproj.GetBinContent(iy)))
    #eff.GetXaxis().SetRangeUser(0,800)
    #eff.Scale(1.0/eff.GetBinContent(eff.GetXaxis().FindBin(200)))
    #eff.RecursiveRemove(eff.GetFunction("pol1"))
    #eff.Draw()
    #c.Print(outfilename+".pdf");

#events.Draw("{0}>>hdtotlow(1500,0,1500)".format(occupancyvar),"{0}>2000 && {0}<3000".format(intensityvar),"colz")
#histlow = gDirectory.Get("hdtotlow")
##histlow.Scale(1.0/histlow.Integral())
#histlow.GetXaxis().SetRangeUser(0,100)
#s = histlow.Fit("pol1","QSL","",20,40)
#print s.Parameter(0)/s.Parameter(1)
#c.Print(outfilename+".pdf");
#
#events.Draw("{0}>>hdtotmed(1500,0,1500)".format(occupancyvar),"{0}>4000 && {0}<6000".format(intensityvar),"colz")
#histmed = gDirectory.Get("hdtotmed")
##histmed.Scale(1.0/histmed.Integral())
#histmed.GetXaxis().SetRangeUser(0,200)
#s = histmed.Fit("pol1","QSL","",40,80)
#print s.Parameter(0)/s.Parameter(1)
#c.Print(outfilename+".pdf");
#
#events.Draw("{0}>>hdtothigh(1500,0,1500)".format(occupancyvar),"{0}>6000 && {0}<9000".format(intensityvar),"colz")
#histhigh = gDirectory.Get("hdtothigh")
##histhigh.Scale(1.0/histhigh.Integral())
#histhigh.GetXaxis().SetRangeUser(0,300)
#s = histhigh.Fit("pol1","QSL","",60,120)
#print s.Parameter(0)/s.Parameter(1)
#c.Print(outfilename+".pdf");

c.Print(outfilename+".pdf]");
outfile.Write()
outfile.Close()
