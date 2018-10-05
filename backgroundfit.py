#!/usr/bin/env python
import sys
import array, math
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, gPad, TF1, THStack, TLegend, TH2D, TH1D, TGraphErrors, TSpline3
import getopt

def makeqiebins(maxqie=0):
    stepcounts = [17,20,21,20,20,21,20,20,21,20,20,21,6]
    edges = array.array('d')
    i=-1
    stepsize = 1
    for bigstep in range(0,13):
        for littlestep in range(0,stepcounts[bigstep]):
            i += stepsize
            #print i,i-0.5*stepsize
            edges.append(i-0.5*stepsize)
            if (i==540):
                binedges.append(i+0.5*stepsize)
                #print i+0.5*stepsize
                i+=15
            if (maxqie!=0 and i>maxqie):
                return edges
        edges.append(i+0.5*stepsize)
        #print i+0.5*stepsize
        stepsize *= 2
        #print "new stepsize"
    return edges

def makepotbins(maxpot):
    edges = array.array('d')
    pot = 0
    while pot <= maxpot:
        edges.append(pot)
        pot += 2000
    return edges

gROOT.SetBatch(True)
gStyle.SetOptStat(11)
gStyle.SetOptFit(1)
infile = TFile("test.root")
events = infile.Get("save")

normfile = TFile("test_occupancy3.root")
normevents = normfile.Get("save")

outfilename="backgroundfit"

c = TCanvas("c","c",1200,900);
c.Print(outfilename+".pdf[")

c.SetLogz(1)
outfile = TFile(outfilename+".root","RECREATE")


#qiecut = " && ".join([i+"<5000" for i in ["RFm{0:02d}".format(j) for j in range(8,0,-1)]+["RF00"]+["RFp{0:02d}".format(j) for j in range(1,9)]])
qiecut = "RFmax<3800"
spillcut = "runID>13861 && runID<14388"
qualitycut = "dataQuality==0"
targetcut = "targetPos==6"
xfcut = "xF>0.67 && xF<0.9"
potcut = "PotPerQie<1e4&&PotPerQie>0.1"

#binedges = makeqiebins(6000)
binedges = makepotbins(1e5)


histqiematrix = TH1D("hqiematrix","hqiematrix",len(binedges)-1,binedges)
normevents.Draw("RF00*PotPerQie>>+hqiematrix"," && ".join(["MATRIX1",targetcut,qualitycut,qiecut,potcut,spillcut]),"")
histqiematrix.SetTitle("triggers, MATRIX1 events;RF00*PotPerQie")
c.Print(outfilename+".pdf");

histqie = TH1D("hqie","hqie",len(binedges)-1,binedges)
normevents.Draw("RF00*PotPerQie>>+hqie"," && ".join(["NIM3",targetcut,qualitycut,qiecut,potcut,spillcut]),"")
histqie.SetTitle("triggers, NIM3 events;RF00*PotPerQie")
c.Print(outfilename+".pdf");

histtriggerratio = histqiematrix.Clone("hqiematrix")
histtriggerratio.Divide(histqie)
histtriggerratio.SetTitle("trigger ratio, MATRIX1/NIM3;RF00*PotPerQie")
histtriggerratio.Fit("pol2")
histtriggerratio.Draw()
c.Print(outfilename+".pdf");

nbinsX = histqie.GetNbinsX()
hnorm = histqie.Clone("hnormqie")
for ix in range(1,nbinsX+1):
    hnorm.SetBinContent(ix,0)
    for i in range(0,int(histqie.GetBinContent(ix))):
        hnorm.Fill(histqie.GetXaxis().GetBinCenter(ix), max(0.0,histqie.GetXaxis().GetBinCenter(ix)))

hnorm.Scale(1e-6)
hnorm.SetTitle("luminosity normalization;RF00*PotPerQie;total RF00*PotPerQie [arb. units]")
hnorm.Draw("")
c.Print(outfilename+".pdf");



#nbinsIntensity = hnorm.GetNbinsX()
#minIntensity = hnorm.GetXaxis().GetBinLowEdge(1)
#maxIntensity = hnorm.GetXaxis().GetBinUpEdge(nbinsIntensity)
events = infile.Get("save")
hist = TH2D("h1","h1",len(binedges)-1,binedges,70,0,7)
#events.Draw("mass:D1+D2+D3>>h1({0},{1},{2},100,0,10)".format(nbinsIntensity,minIntensity,maxIntensity),"targetPos==6 && abs(xF-0.7)<0.02","colz")
#events.Draw("mass:RF00>>h1({0},{1},{2},100,0,10)".format(nbinsIntensity,minIntensity,maxIntensity),"targetPos==6 && abs(xF-0.7)<0.02","colz")
#events.Draw("mass:RF00>>h1({0},{1},{2},80,0,8)".format(nbinsIntensity,minIntensity,maxIntensity),"targetPos==6 && dataQuality==0 && xF>0.67 && xF<0.9","colz")
events.Draw("mass:RF00*PotPerQie>>+h1"," && ".join([targetcut,qualitycut,potcut,spillcut,xfcut]),"colz")
#hist = gDirectory.Get("h1")
hist.SetTitle("mass vs. RF00*PotPerQie")
c.Print(outfilename+".pdf");


histd1 = TH2D("hd1","hd1",len(binedges)-1,binedges,100,0,1e3)
#events.Draw("D1:RF00>>hd1({0},{1},{2},100,0,1e3)".format(nbinsIntensity,minIntensity,maxIntensity),"targetPos==6 && abs(xF-0.7)<0.02","colz")
#events.Draw("D1:RF00>>hd1({0},{1},{2},100,0,1e3)".format(nbinsIntensity,minIntensity,maxIntensity),"targetPos==6 && dataQuality==0 && xF>0.67 && xF<0.9","colz")
events.Draw("D1:RF00*PotPerQie>>+hd1"," && ".join([targetcut,qualitycut,potcut,spillcut,xfcut]),"colz")
#histd1 = gDirectory.Get("hd1")
histd1.SetTitle("D1 vs. RF00*PotPerQie")
c.Print(outfilename+".pdf");

#c.Print(outfilename+".pdf]");
#sys.exit(0)

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

#c.Print(outfilename+".pdf]");
#outfile.Write()
#outfile.Close()
#sys.exit(0)

#parSplines = []
#parFuncs = []
#for i in range(0,5):
    ##graph=TGraph(len(qieArr),qieArr,pArrs[i])
    #parFuncs.append(TF1("parFunc"+str(i),"pol3"))
    #graph=TGraphErrors(len(qieArr),qieArr,pArrs[i],zeroArr,pErrArrs[i])
    #graph.Fit(parFuncs[i])
    ##graph.Draw("A*")
    ##c.Print(outfilename+".pdf");
    #parSplines.append(TSpline3("fitSpline"+str(i),graph))
    ##parSplines[i].Draw()
    ##c.Print(outfilename+".pdf");



histNormed = hist.Clone("hEventsNormalized")
histNormed.SetTitle("Normalized data;RF00;mass [GeV]")
hnorm2d = hist.Clone("hnorm2d")
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
    #if histd1.GetXaxis().GetBinCenter(ix) <= qieArr[-1]:
        #for i in range(0,5):
            ##fitfunc.SetParameter(i,parSplines[i].Eval(histd1.GetXaxis().GetBinCenter(ix)))
            ##fitfunc_fullEff.SetParameter(i,parSplines[i].Eval(histd1.GetXaxis().GetBinCenter(ix)))
            #fitfunc.SetParameter(i,parFuncs[i].Eval(histd1.GetXaxis().GetBinCenter(ix)))
            #fitfunc_fullEff.SetParameter(i,parFuncs[i].Eval(histd1.GetXaxis().GetBinCenter(ix)))
        #for iy in range(1,histd1.GetNbinsY()):
            #integralFullEff += fitfunc_fullEff.Eval(histd1.GetYaxis().GetBinCenter(iy))
            #integralRealEff += fitfunc.Eval(histd1.GetYaxis().GetBinCenter(iy))
            #histd1FullEff.SetBinContent(ix,iy,fitfunc_fullEff.Eval(histd1.GetYaxis().GetBinCenter(iy)))
        ##qieArr2.append(histd1.GetXaxis().GetBinCenter(ix))
        ##effArr.append(integralRealEff/integralFullEff)

    eff = 0.9876 - 0.002129*profiled1.GetBinContent(ix)
    weightedeff = 0
    for iy in range(1,histd1.GetNbinsY()):
        weightedeff += histd1.GetBinContent(ix,iy)*(0.9876 - 0.002129*histd1.GetYaxis().GetBinCenter(iy))
    weightedeff /= (1+heff.GetBinContent(ix))
    inveff = 0
    for iy in range(1,histd1.GetNbinsY()):
        inveff += histd1.GetBinContent(ix,iy)/(0.9876 - 0.002129*histd1.GetYaxis().GetBinCenter(iy))
    #print inveff,heff.GetBinContent(ix)
    if inveff==0:
        inveff = 1
    else:
        inveff /= (heff.GetBinContent(ix))
    qieArr2.append(histd1.GetXaxis().GetBinCenter(ix))
    effArr.append(1.0/inveff)


    #print ix, eff, weightedeff, 1.0/(inveff+0.0001), integralRealEff/integralFullEff, profiled1.GetBinContent(ix)
    #eff = 0.9876 - 0.002129*hist.GetXaxis().GetBinCenter(ix)
    #if eff<0:
        #eff = 0
    for iy in range(1,nbinsY+1):
        #histNormed.SetBinContent(ix, iy, hist.GetBinContent(ix,iy)/(1.0+hnorm.GetBinContent(ix)*eff))
        #histNormed.SetBinContent(ix, iy, hist.GetBinContent(ix,iy)*inveff/(1.0+hnorm.GetBinContent(ix)))
        #histNormed.SetBinContent(ix, iy, hist.GetBinContent(ix,iy)*(integralFullEff/integralRealEff)/(1.0+hnorm.GetBinContent(ix)))
        histNormed.SetBinContent(ix,iy,0.0)
        for i in range(0,int(hist.GetBinContent(ix,iy))):
            #histNormed.Fill(hist.GetXaxis().GetBinCenter(ix), hist.GetYaxis().GetBinCenter(iy), (integralFullEff/integralRealEff)/(1.0+hnorm.GetBinContent(ix)))
            #histNormed.Fill(hist.GetXaxis().GetBinCenter(ix), hist.GetYaxis().GetBinCenter(iy), (integralFullEff/integralRealEff))
            #histNormed.Fill(hist.GetXaxis().GetBinCenter(ix), hist.GetYaxis().GetBinCenter(iy), (integralFullEff/integralRealEff))
            histNormed.Fill(hist.GetXaxis().GetBinCenter(ix), hist.GetYaxis().GetBinCenter(iy), inveff)
            #histNormed.Fill(hist.GetXaxis().GetBinCenter(ix), hist.GetYaxis().GetBinCenter(iy), max(0,1.0-0.35e-3*histd1.GetXaxis().GetBinCenter(ix)))
        #print ix,iy,hist.GetBinContent(ix,iy)*(integralFullEff/integralRealEff)/(1.0+hnorm.GetBinContent(ix))
        #histNormed.Fill(hist.GetXaxis().GetBinCenter(ix), hist.GetYaxis().GetBinCenter(iy), hist.GetBinContent(ix,iy)/(1.0+hnorm.GetBinContent(ix)*eff))
        hnorm2d.SetBinContent(ix,iy,hnorm.GetBinContent(ix))
        hnorm2d.SetBinError(ix,iy,hnorm.GetBinError(ix))
#
histNormed.Divide(hnorm2d)
#hnorm.SetTitle("normalization;D1+D2+D3;QIE integral [arb. units]")
#outfile.Add(histNormed)
effgraph=TGraph(len(qieArr2),qieArr2,effArr)
effgraph.SetTitle("efficiency vs. intensity;RF00;efficiency")
effgraph.Draw("A*")
c.Print(outfilename+".pdf");

#histd1FullEff.Draw("colz")
#c.Print(outfilename+".pdf");
histNormed.Draw("colz")
c.Print(outfilename+".pdf");

minfitrange = 2000
maxfitrange = 40000

fitfunc = TF1("f","pol1")
fitfunc.SetRange(0,1e5)
massArr = array.array('d')
zeroArr = array.array('d')
p0Arr = array.array('d')
p1Arr = array.array('d')
p0ErrArr = array.array('d')
p1ErrArr = array.array('d')
hEffCorr = hist.Clone("hEffCorr")
for iy in range(1,nbinsY+1):
    proj = histNormed.ProjectionX("test"+str(iy),iy,iy)
    proj.SetTitle("normalized dimuons vs. intensity, mass [{0}, {1}];RF00;arbitrary units".format(histNormed.GetYaxis().GetBinLowEdge(iy),histNormed.GetYaxis().GetBinUpEdge(iy)))
    maxval = proj.GetMaximum()
    proj.GetYaxis().SetRangeUser(-0.1*maxval,1.1*maxval)
    proj.GetXaxis().SetRangeUser(minfitrange,1e5)
    #print proj.Integral()
    #if proj.Integral()>0:
    for ix in range(1,nbinsX+1):
        hEffCorr.SetBinContent(ix,iy,0.0)
    s = proj.Fit(fitfunc,"QSWL","",minfitrange,maxfitrange)
    if s.Get() and s.Get().IsValid() and s.Get().Ndf()>0:
        c.Print(outfilename+".pdf")
        #print histNormed.GetYaxis().GetBinCenter(iy),s.Parameter(0),s.Parameter(1)
        massArr.append(histNormed.GetYaxis().GetBinCenter(iy))
        zeroArr.append(0)
        p0Arr.append(s.Parameter(0))
        p0ErrArr.append(s.ParError(0))
        p1Arr.append(s.Parameter(1)*0.5*maxfitrange)
        p1ErrArr.append(s.ParError(1)*0.5*maxfitrange)
        if (histNormed.GetYaxis().GetBinCenter(iy)==3.05):
            s.Print("V")
        proj.Divide(fitfunc)
        for ix in range(1,nbinsX+1):
            hEffCorr.SetBinContent(ix,iy,proj.GetBinContent(ix))
            hEffCorr.SetBinError(ix,iy,proj.GetBinError(ix))
        #proj.Draw()
        #c.Print(outfilename+".pdf")

graph=TGraphErrors(len(massArr),massArr,p0Arr,zeroArr,p0ErrArr)
graph.SetTitle("Signal vs. mass, RF00=[0,1000];mass [GeV];arbitrary units")
graph.Draw("A*")
c.Print(outfilename+".pdf");

graph2=TGraphErrors(len(massArr),massArr,p1Arr,zeroArr,p1ErrArr)
graph2.SetTitle("Background vs. mass, RF00=[0,1000];mass [GeV];arbitrary units")
graph2.SetMarkerColor(2)
graph2.Draw("*")
c.Print(outfilename+".pdf");
graph2.Draw("A*")
c.Print(outfilename+".pdf");


c.SetLogz(0)
hEffCorr.GetZaxis().SetRangeUser(0,10)
hEffCorr.GetYaxis().SetRangeUser(1.0,5.5)
hEffCorr.SetTitle("deviation from linear fit;RF00;mass [GeV]")
hEffCorr.Draw("colz")
c.Print(outfilename+".pdf");
qieArr = array.array('d')
zeroArr = array.array('d')
p0Arr = array.array('d')
p0ErrArr = array.array('d')
for ix in range(1,nbinsX+1):
    proj = hEffCorr.ProjectionY("effCorr"+str(ix),ix,ix)
    proj.SetTitle("efficiency correction, RF00 [{0}, {1}];mass;arbitrary units".format(hEffCorr.GetXaxis().GetBinLowEdge(ix),hEffCorr.GetXaxis().GetBinUpEdge(ix)))
    proj.GetYaxis().SetRangeUser(-0.1,1.5)
    s = proj.Fit("pol0","QS","",1.0,5.5)
    if s.Get() and s.Get().IsValid() and s.Get().Ndf()>0:
        #c.Print(outfilename+".pdf")
        qieArr.append(hEffCorr.GetXaxis().GetBinCenter(ix))
        zeroArr.append(0)
        p0Arr.append(s.Parameter(0))
        p0ErrArr.append(s.ParError(0))

graph4=TGraphErrors(len(qieArr),qieArr,p0Arr,zeroArr,p0ErrArr)
graph4.SetTitle("deviation from linear fit;RF00;data/fit")
graph4.Fit("pol1","QS","",100,1000)
#graph4.Fit("pol2","QS","",100,1000)
#graph4.Fit("pol2","QS","",100,1500)
graph4.SetMarkerColor(2)
graph4.Draw("A*X")
#graph4.GetXaxis().SetRangeUser(50,2000)
graph4.GetYaxis().SetRangeUser(-0.1,1.5)
c.Print(outfilename+".pdf");
effgraph.Draw("*")
c.Print(outfilename+".pdf");

c.Print(outfilename+".pdf]");
outfile.Write()
outfile.Close()
