#!/usr/bin/env python
import sys
import array, math
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, gPad, TF1, THStack, TLegend, TH2D, TH1D, TGraphErrors, TSpline3
import getopt

gROOT.SetBatch(True)
gStyle.SetOptStat(11)
#gStyle.SetOptFit(1)
infile = TFile("test.root")
normfile = TFile("normalization.root")

outfilename="backgroundfit"

c = TCanvas("c","c",1200,900);
c.Print(outfilename+".pdf[")

c.SetLogz(1)
outfile = TFile(outfilename+".root","RECREATE")

hnorm = normfile.Get("hnormqie")

nbinsIntensity = hnorm.GetNbinsX()
minIntensity = hnorm.GetXaxis().GetBinLowEdge(1)
maxIntensity = hnorm.GetXaxis().GetBinUpEdge(nbinsIntensity)
events = infile.Get("save")
#events.Draw("mass:D1+D2+D3>>h1({0},{1},{2},100,0,10)".format(nbinsIntensity,minIntensity,maxIntensity),"targetPos==6 && abs(xF-0.7)<0.02","colz")
#events.Draw("mass:RF00>>h1({0},{1},{2},100,0,10)".format(nbinsIntensity,minIntensity,maxIntensity),"targetPos==6 && abs(xF-0.7)<0.02","colz")
events.Draw("mass:RF00>>h1({0},{1},{2},200,0,10)".format(nbinsIntensity,minIntensity,maxIntensity),"targetPos==6 && dataQuality==0 && xF>0.67 && xF<0.9","colz")
hist = gDirectory.Get("h1")
c.Print(outfilename+".pdf");



#events.Draw("D1:RF00>>hd1({0},{1},{2},100,0,1e3)".format(nbinsIntensity,minIntensity,maxIntensity),"targetPos==6 && abs(xF-0.7)<0.02","colz")
events.Draw("D1:RF00>>hd1({0},{1},{2},100,0,1e3)".format(nbinsIntensity,minIntensity,maxIntensity),"targetPos==6 && dataQuality==0 && xF>0.67 && xF<0.9","colz")
histd1 = gDirectory.Get("hd1")
c.Print(outfilename+".pdf");

profiled1 = histd1.ProfileX()
#profiled1.Draw()
#c.Print(outfilename+".pdf");

#fitfunc = TF1("f","[0]*exp(([2]*abs(x-[1]))**[3])")
#fitfunc = TF1("f","(0.9876 - 0.002129*x)*[0]*exp([2]*(abs(x-[1]))**[3]+[4]*(x-[1]))")
#fitfunc = TF1("f","exp([0]*sqrt((x-[1])**2+[2]**2)+[3]*x+[4])")
#fitfunc = TF1("f","(0.9876 - 0.002129*x)*exp([0]*sqrt((x-[1])**2+[2]**2)+[3]*x+[4])")
#fitfunc = TF1("f","TMath::Max((0.9876 - 0.002129*x),0.0)*exp([0]*sqrt((x-[1])**2+[2]**2)+[3]*x+[4])")
fitfunc = TF1("f","TMath::Max((1.0 - 0.00174*x),0.0)*exp([0]*sqrt((x-[1])**2+[2]**2)+[3]*x+[4])")
fitfunc.SetRange(0,400)
fitfunc_fullEff = TF1("f2","exp([0]*sqrt((x-[1])**2+[2]**2)+[3]*x+[4])")
fitfunc_fullEff.SetRange(0,1000)
qieArr = array.array('d')
zeroArr = array.array('d')
pArrs = []
pErrArrs = []
for i in range(0,5):
    pArrs.append(array.array('d'))
    pErrArrs.append(array.array('d'))
histd1FullEff = histd1.Clone("hd1FullEff")
nbinsX = histd1.GetNbinsX()
nbinsY = histd1.GetNbinsY()
c.SetLogy(1)
fitfunc.SetParameters(-0.15,30,200,0.1,30)
for ix in range(1,nbinsX+1):
#for ix in range(nbinsX,0,-1):
    fithist = histd1.ProjectionY("histproj"+str(ix),ix,ix)
    if fithist.Integral()>100:
        fitfunc.SetParameter(0,-0.23+4.0e-5*histd1.GetXaxis().GetBinCenter(ix))
        #fitfunc.SetParameter(1,11-4.5e-3*histd1.GetXaxis().GetBinCenter(ix))
        fitfunc.SetParameter(1,10)
        fitfunc.SetParameter(2,0.85+1.0e-1*histd1.GetXaxis().GetBinCenter(ix))
        fitfunc.SetParameter(3,0.24-6.7e-5*histd1.GetXaxis().GetBinCenter(ix))
        fitfunc.SetParameter(4,7.1+1.1e-2*histd1.GetXaxis().GetBinCenter(ix))
        s = fithist.Fit(fitfunc,"QSRL")
        #for i in range(0,5):
            #fitfunc_fullEff.SetParameter(i,s.Parameter(i))
        #fitfunc_fullEff.Draw("same")
        #c.Print(outfilename+".pdf")
        if s.Get() and s.Get().IsValid():
            #print histd1.GetXaxis().GetBinCenter(ix),fithist.GetMaximum(),fithist.GetMean(),fithist.GetRMS(),s.Parameter(0),s.Parameter(1),s.Parameter(2),s.Parameter(3),s.Parameter(4)
            qieArr.append(histd1.GetXaxis().GetBinCenter(ix))
            zeroArr.append(0)
            for i in range(0,5):
                pArrs[i].append(s.Parameter(i))
                pErrArrs[i].append(s.ParError(i))
        else:
            print("fit failed")

#    temp = TH1D("temp"+str(ix),"temp"+str(ix),nbinsY,(histd1.GetYaxis().GetBinLowEdge(1)-44)/histd1.GetXaxis().GetBinCenter(ix),(histd1.GetYaxis().GetBinUpEdge(nbinsY+1)-44)/histd1.GetXaxis().GetBinCenter(ix))
#    for iy in range(1,nbinsY+1):
#        if histd1.GetYaxis().GetBinCenter(iy)>400:
#            break
#        temp.SetBinContent(iy,histd1.GetBinContent(ix,iy)/(0.9876 - 0.002129*histd1.GetYaxis().GetBinCenter(iy)))
#    temp.GetXaxis().SetRangeUser(0,0.5)
#    temp.Draw()
#    c.Print(outfilename+".pdf")
c.SetLogy(0)

parSplines = []
parFuncs = []
for i in range(0,5):
    #graph=TGraph(len(qieArr),qieArr,pArrs[i])
    parFuncs.append(TF1("parFunc"+str(i),"pol3"))
    graph=TGraphErrors(len(qieArr),qieArr,pArrs[i],zeroArr,pErrArrs[i])
    graph.Draw("A*")
    graph.Fit(parFuncs[i])
    c.Print(outfilename+".pdf");
    parSplines.append(TSpline3("fitSpline"+str(i),graph))
    #parSplines[i].Draw()
    #c.Print(outfilename+".pdf");



histNormed = hist.Clone("hEventsNormalized")
#histNormed.Reset()
#histNormed = TH1()
#hist.Copy(histNormed)
#outfile.Add(histNormed)
#hist.SetTitle("")

nbinsX = histNormed.GetNbinsX()
nbinsY = histNormed.GetNbinsY()
#heff = TH1D("heff","heff",hist.GetNbinsX(),hist.GetXaxis().GetBinLowEdge(1),hist.GetXaxis().GetBinUpEdge(nbinsX))
heff = histd1.ProjectionX()
#heff.Draw()
#c.Print(outfilename+".pdf");

qieArr2 = array.array('d')
effArr = array.array('d')
for ix in range(1,nbinsX+1):
    #print histd1.GetXaxis().GetBinCenter(ix), heff.GetBinContent(ix)
    integralFullEff = 1e-10
    integralRealEff = 1e-10
    if histd1.GetXaxis().GetBinCenter(ix) <= qieArr[-1]:
        for i in range(0,5):
            #fitfunc.SetParameter(i,parSplines[i].Eval(histd1.GetXaxis().GetBinCenter(ix)))
            #fitfunc_fullEff.SetParameter(i,parSplines[i].Eval(histd1.GetXaxis().GetBinCenter(ix)))
            fitfunc.SetParameter(i,parFuncs[i].Eval(histd1.GetXaxis().GetBinCenter(ix)))
            fitfunc_fullEff.SetParameter(i,parFuncs[i].Eval(histd1.GetXaxis().GetBinCenter(ix)))
        for iy in range(1,histd1.GetNbinsY()):
            integralFullEff += fitfunc_fullEff.Eval(histd1.GetYaxis().GetBinCenter(iy))
            integralRealEff += fitfunc.Eval(histd1.GetYaxis().GetBinCenter(iy))
            histd1FullEff.SetBinContent(ix,iy,fitfunc_fullEff.Eval(histd1.GetYaxis().GetBinCenter(iy)))
        qieArr2.append(histd1.GetXaxis().GetBinCenter(ix))
        effArr.append(integralRealEff/integralFullEff)

    eff = 0.9876 - 0.002129*profiled1.GetBinContent(ix)
    weightedeff = 0
    for iy in range(1,histd1.GetNbinsY()):
        weightedeff += histd1.GetBinContent(ix,iy)*(0.9876 - 0.002129*histd1.GetYaxis().GetBinCenter(iy))
    weightedeff /= (1+heff.GetBinContent(ix))
    inveff = 0
    for iy in range(1,histd1.GetNbinsY()):
        inveff += histd1.GetBinContent(ix,iy)/(0.9876 - 0.002129*histd1.GetYaxis().GetBinCenter(iy))
    inveff /= (1+heff.GetBinContent(ix))


    print ix, eff, weightedeff, 1.0/(inveff+0.0001), integralRealEff/integralFullEff, profiled1.GetBinContent(ix)
    #eff = 0.9876 - 0.002129*hist.GetXaxis().GetBinCenter(ix)
    if eff<0:
        eff = 0
    for iy in range(1,nbinsY+1):
        #histNormed.SetBinContent(ix, iy, hist.GetBinContent(ix,iy)/(1.0+hnorm.GetBinContent(ix)*eff))
        #histNormed.SetBinContent(ix, iy, hist.GetBinContent(ix,iy)*inveff/(1.0+hnorm.GetBinContent(ix)))
        histNormed.SetBinContent(ix, iy, hist.GetBinContent(ix,iy)*(integralFullEff/integralRealEff)/(1.0+hnorm.GetBinContent(ix)))
        #print ix,iy,hist.GetBinContent(ix,iy)*(integralFullEff/integralRealEff)/(1.0+hnorm.GetBinContent(ix))
        #histNormed.Fill(hist.GetXaxis().GetBinCenter(ix), hist.GetYaxis().GetBinCenter(iy), hist.GetBinContent(ix,iy)/(1.0+hnorm.GetBinContent(ix)*eff))
#
#hnorm.SetTitle("normalization;D1+D2+D3;QIE integral [arb. units]")
#outfile.Add(histNormed)
graph=TGraph(len(qieArr2),qieArr2,effArr)
graph.Draw("A*")
c.Print(outfilename+".pdf");

histd1FullEff.Draw("colz")
c.Print(outfilename+".pdf");
histNormed.Draw("colz")
c.Print(outfilename+".pdf");

#c.Print(outfilename+".pdf]");
#outfile.Write()
#outfile.Close()
#sys.exit(0)

massArr = array.array('d')
p0Arr = array.array('d')
p1Arr = array.array('d')
for iy in range(1,nbinsY+1):
    proj = histNormed.ProjectionX("test",iy,iy)
    print proj.Integral()
    #if proj.Integral()>0:
    s = proj.Fit("pol1","QS","",0,1000)
    if s.Get() and s.Get().IsValid():
        #c.Print(outfilename+".pdf")
        #print histNormed.GetYaxis().GetBinCenter(iy),s.Parameter(0),s.Parameter(1)
        massArr.append(histNormed.GetYaxis().GetBinCenter(iy))
        p0Arr.append(s.Parameter(0))
        p1Arr.append(s.Parameter(1)*500)

graph=TGraph(len(massArr),massArr,p0Arr)
graph.Draw("A*")
c.Print(outfilename+".pdf");

graph2=TGraph(len(massArr),massArr,p1Arr)
graph2.SetMarkerColor(2)
graph2.Draw("*")
c.Print(outfilename+".pdf");
graph2.Draw("A*")
c.Print(outfilename+".pdf");

c.Print(outfilename+".pdf]");
outfile.Write()
outfile.Close()
