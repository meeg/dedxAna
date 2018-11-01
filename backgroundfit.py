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
s = histtriggerratio.Fit("pol2","S","",1000,50e3)
print s.Parameter(1)/(-2*s.Parameter(2)*30)
c.SetLogy(1)
histtriggerratio.Draw()
c.Print(outfilename+".pdf");
c.SetLogy(0)


nbinsX = hist.GetNbinsX()
nbinsY = hist.GetNbinsY()


hnorm = histqie.Clone("hnormqie")
#hnorm.Multiply(intensity)
intensityfunc = TF1("fx","x")
intensityfunc.SetRange(0,1e5)

fitfunc = TF1("f","pol1")
fitfunc.SetRange(0,1e5)

hnorm.Multiply(intensityfunc)
#for ix in range(1,nbinsX+1):
    #hnorm.SetBinContent(ix,0)
    #for i in range(0,int(histqie.GetBinContent(ix))):
        #hnorm.Fill(histqie.GetXaxis().GetBinCenter(ix), max(0.0,histqie.GetXaxis().GetBinCenter(ix)))

hnorm.Scale(1.0/hnorm.GetMaximum())
hnorm.SetTitle("luminosity normalization;{0};total {0} [arb. units]".format(intensityvar))
hnorm.Draw("")
c.Print(outfilename+".pdf");



#c.Print(outfilename+".pdf]");
#sys.exit(0)

#profiled1 = histd1.ProfileX()
#profiled1.Draw()
#c.Print(outfilename+".pdf");

#fitfunc = TF1("f","[0]*exp(([2]*abs(x-[1]))**[3])")
#fitfunc = TF1("f","(0.9876 - 0.002129*x)*[0]*exp([2]*(abs(x-[1]))**[3]+[4]*(x-[1]))")
#fitfunc = TF1("f","exp([0]*sqrt((x-[1])**2+[2]**2)+[3]*x+[4])")
#fitfunc = TF1("f","(0.9876 - 0.002129*x)*exp([0]*sqrt((x-[1])**2+[2]**2)+[3]*x+[4])")
#fitfunc = TF1("f","TMath::Max((0.9876 - 0.002129*x),0.0)*exp([0]*sqrt((x-[1])**2+[2]**2)+[3]*x+[4])")
#fitfuncD1 = TF1("f","TMath::Max((1.0 - 0.00174*x),0.0)*exp([0]*sqrt((x-[1])**2+[2]**2)+[3]*x+[4])")
#fitfuncD1.SetRange(0,400)
#fitfuncD1_fullEff = TF1("f2","exp([0]*sqrt((x-[1])**2+[2]**2)+[3]*x+[4])")
#fitfuncD1_fullEff.SetRange(0,1000)
#qieArr = array.array('d')
#zeroArr = array.array('d')
#pArrs = []
#pErrArrs = []
#for i in range(0,5):
    #pArrs.append(array.array('d'))
    #pErrArrs.append(array.array('d'))
#nbinsX = histd1.GetNbinsX()
#nbinsY = histd1.GetNbinsY()
#c.SetLogy(1)
#fitfunc.SetParameters(-0.15,30,200,0.1,30)
#for ix in range(1,nbinsX+1):
##for ix in range(nbinsX,0,-1):
    #fithist = histd1.ProjectionY("histproj"+str(ix),ix,ix)
    #if fithist.Integral()>100:
        #fitfunc.SetParameter(0,-0.23+4.0e-5*histd1.GetXaxis().GetBinCenter(ix))
        ##fitfunc.SetParameter(1,11-4.5e-3*histd1.GetXaxis().GetBinCenter(ix))
        #fitfunc.SetParameter(1,10)
        #fitfunc.SetParameter(2,0.85+1.0e-1*histd1.GetXaxis().GetBinCenter(ix))
        #fitfunc.SetParameter(3,0.24-6.7e-5*histd1.GetXaxis().GetBinCenter(ix))
        #fitfunc.SetParameter(4,7.1+1.1e-2*histd1.GetXaxis().GetBinCenter(ix))
        #s = fithist.Fit(fitfunc,"QSRL")
        ##for i in range(0,5):
            ##fitfunc_fullEff.SetParameter(i,s.Parameter(i))
        ##fitfunc_fullEff.Draw("same")
        ##c.Print(outfilename+".pdf")
        #if s.Get() and s.Get().IsValid():
            ##print histd1.GetXaxis().GetBinCenter(ix),fithist.GetMaximum(),fithist.GetMean(),fithist.GetRMS(),s.Parameter(0),s.Parameter(1),s.Parameter(2),s.Parameter(3),s.Parameter(4)
            #qieArr.append(histd1.GetXaxis().GetBinCenter(ix))
            #zeroArr.append(0)
            #for i in range(0,5):
                #pArrs[i].append(s.Parameter(i))
                #pErrArrs[i].append(s.ParError(i))
        #else:
            #print("fit failed")

#    temp = TH1D("temp"+str(ix),"temp"+str(ix),nbinsY,(histd1.GetYaxis().GetBinLowEdge(1)-44)/histd1.GetXaxis().GetBinCenter(ix),(histd1.GetYaxis().GetBinUpEdge(nbinsY+1)-44)/histd1.GetXaxis().GetBinCenter(ix))
#    for iy in range(1,nbinsY+1):
#        if histd1.GetYaxis().GetBinCenter(iy)>400:
#            break
#        temp.SetBinContent(iy,histd1.GetBinContent(ix,iy)/(0.9876 - 0.002129*histd1.GetYaxis().GetBinCenter(iy)))
#    temp.GetXaxis().SetRangeUser(0,0.5)
#    temp.Draw()
#    c.Print(outfilename+".pdf")
#c.SetLogy(0)

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



#histNormed = hist.Clone("hEventsNormalized")
#histNormed.SetTitle("Normalized data;{0};mass [GeV]".format(intensityvar))
hnorm2d = hist.Clone("hnorm2d")
#histNormed.Reset()
#histNormed = TH1()
#hist.Copy(histNormed)
#outfile.Add(histNormed)
#hist.SetTitle("")

#histd1FullEff = histd1.Clone("hd1FullEff")

##heff = TH1D("heff","heff",hist.GetNbinsX(),hist.GetXaxis().GetBinLowEdge(1),hist.GetXaxis().GetBinUpEdge(nbinsX))
#heff = histd1.ProjectionX()
##heff.Draw()
##c.Print(outfilename+".pdf");
#
#qieArr2 = array.array('d')
#effArr = array.array('d')
for ix in range(1,nbinsX+1):
    ##print histd1.GetXaxis().GetBinCenter(ix), heff.GetBinContent(ix)
    #integralFullEff = 1e-10
    #integralRealEff = 1e-10
    ##if histd1.GetXaxis().GetBinCenter(ix) <= qieArr[-1]:
        ##for i in range(0,5):
            ###fitfunc.SetParameter(i,parSplines[i].Eval(histd1.GetXaxis().GetBinCenter(ix)))
            ###fitfunc_fullEff.SetParameter(i,parSplines[i].Eval(histd1.GetXaxis().GetBinCenter(ix)))
            ##fitfunc.SetParameter(i,parFuncs[i].Eval(histd1.GetXaxis().GetBinCenter(ix)))
            ##fitfunc_fullEff.SetParameter(i,parFuncs[i].Eval(histd1.GetXaxis().GetBinCenter(ix)))
        ##for iy in range(1,histd1.GetNbinsY()):
            ##integralFullEff += fitfunc_fullEff.Eval(histd1.GetYaxis().GetBinCenter(iy))
            ##integralRealEff += fitfunc.Eval(histd1.GetYaxis().GetBinCenter(iy))
            ##histd1FullEff.SetBinContent(ix,iy,fitfunc_fullEff.Eval(histd1.GetYaxis().GetBinCenter(iy)))
        ###qieArr2.append(histd1.GetXaxis().GetBinCenter(ix))
        ###effArr.append(integralRealEff/integralFullEff)
#
    #eff = 0.9876 - 0.002129*profiled1.GetBinContent(ix)
    #weightedeff = 0
    #inveff = 0
    #numerator = 0
    #for iy in range(1,histd1.GetNbinsY()):
        #bineff = 0.9876 - 0.002129*histd1.GetYaxis().GetBinCenter(iy)
        #if bineff>0:
            #weightedeff += histd1.GetBinContent(ix,iy)*bineff
            #inveff += histd1.GetBinContent(ix,iy)/bineff
            #numerator += histd1.GetBinContent(ix,iy)
    #weightedeff /= (1+numerator)
    ##print inveff,heff.GetBinContent(ix)
    #if inveff==0:
        #inveff = 1
    #else:
        #inveff /= numerator
    #qieArr2.append(histd1.GetXaxis().GetBinCenter(ix))
    #effArr.append(1.0/inveff)
#
#
    ##print ix, eff, weightedeff, 1.0/(inveff+0.0001), integralRealEff/integralFullEff, profiled1.GetBinContent(ix)
    ##eff = 0.9876 - 0.002129*hist.GetXaxis().GetBinCenter(ix)
    ##if eff<0:
        ##eff = 0
    for iy in range(1,nbinsY+1):
        ##histNormed.SetBinContent(ix, iy, hist.GetBinContent(ix,iy)/(1.0+hnorm.GetBinContent(ix)*eff))
        ##histNormed.SetBinContent(ix, iy, hist.GetBinContent(ix,iy)*inveff/(1.0+hnorm.GetBinContent(ix)))
        ##histNormed.SetBinContent(ix, iy, hist.GetBinContent(ix,iy)*(integralFullEff/integralRealEff)/(1.0+hnorm.GetBinContent(ix)))
        #histNormed.SetBinContent(ix,iy,hist.GetBinContent(ix,iy)*inveff)
        #histNormed.SetBinError(ix,iy,hist.GetBinError(ix,iy)*inveff)
        ##for i in range(0,int(hist.GetBinContent(ix,iy))):
            ###histNormed.Fill(hist.GetXaxis().GetBinCenter(ix), hist.GetYaxis().GetBinCenter(iy), (integralFullEff/integralRealEff)/(1.0+hnorm.GetBinContent(ix)))
            ###histNormed.Fill(hist.GetXaxis().GetBinCenter(ix), hist.GetYaxis().GetBinCenter(iy), (integralFullEff/integralRealEff))
            ###histNormed.Fill(hist.GetXaxis().GetBinCenter(ix), hist.GetYaxis().GetBinCenter(iy), (integralFullEff/integralRealEff))
            ##histNormed.Fill(hist.GetXaxis().GetBinCenter(ix), hist.GetYaxis().GetBinCenter(iy), inveff)
            ###histNormed.Fill(hist.GetXaxis().GetBinCenter(ix), hist.GetYaxis().GetBinCenter(iy), max(0,1.0-0.35e-3*histd1.GetXaxis().GetBinCenter(ix)))
        ##print ix,iy,hist.GetBinContent(ix,iy)*(integralFullEff/integralRealEff)/(1.0+hnorm.GetBinContent(ix))
        ##histNormed.Fill(hist.GetXaxis().GetBinCenter(ix), hist.GetYaxis().GetBinCenter(iy), hist.GetBinContent(ix,iy)/(1.0+hnorm.GetBinContent(ix)*eff))
        hnorm2d.SetBinContent(ix,iy,hnorm.GetBinContent(ix))
        hnorm2d.SetBinError(ix,iy,hnorm.GetBinError(ix))
##
#histNormed.Divide(hnorm2d)
##hnorm.SetTitle("normalization;D1+D2+D3;QIE integral [arb. units]")
##outfile.Add(histNormed)
#effgraph=TGraph(len(qieArr2),qieArr2,effArr)
#effgraph.SetTitle("efficiency vs. intensity;{0};efficiency".format(intensityvar))
#effgraph.Draw("A*")
#effgraph.GetYaxis().SetRangeUser(0.0,1.1)
#c.Print(outfilename+".pdf");
#
##histd1FullEff.Draw("colz")
##c.Print(outfilename+".pdf");
#histNormed.Draw("colz")
#c.Print(outfilename+".pdf");

histNormedNoEff = hist.Clone("histNormedNoEff")
histNormedNoEff.SetTitle("Luminosity-normalized data;{0};mass [GeV]".format(intensityvar))
histNormedNoEff.Divide(hnorm2d)
histNormedNoEff.Draw("colz")
c.Print(outfilename+".pdf");



projlow = histNormedNoEff.ProjectionX("projlow",1,15)
projlow.SetTitle("low mass")
#projlow.GetYaxis().SetRangeUser(0,projlow.GetBinContent(projlow.GetMaximumBin()))
projlow.SetMinimum(0)
projlow.Draw()
c.Print(outfilename+".pdf");
projmed = histNormedNoEff.ProjectionX("projmed",16,30)
projmed.SetTitle("medium mass")
#projmed.GetYaxis().SetRangeUser(0,projmed.GetBinContent(projmed.GetMaximumBin()))
projmed.SetMinimum(0)
projmed.Draw()
c.Print(outfilename+".pdf");
projhigh = histNormedNoEff.ProjectionX("projhigh",31,60)
projhigh.SetTitle("high mass")
#projhigh.GetYaxis().SetRangeUser(0,projhigh.GetBinContent(projhigh.GetMaximumBin()))
projhigh.SetMinimum(0)
projhigh.Draw()
c.Print(outfilename+".pdf");

hEff = projlow.Clone("hEff") #we assume projlow is pure background and divide by intensity to get the efficiency vs. intensity (only valid at low intensity where we expect the background to be linear)
hEff.Divide(intensityfunc)
hEff.Scale(0.8/hEff.GetBinContent(5)) #arbitrary normalization
hEff.Draw()
c.Print(outfilename+".pdf");

minfitrange = 5e3
maxfitrange = 30e3


fitmed = projmed.Clone("fitmed")
fitmed.Divide(hEff)
smed = fitmed.Fit(fitfunc,"S","",minfitrange,maxfitrange)
smed = fitmed.Fit(fitfunc,"SWL","",minfitrange,maxfitrange)
c.Print(outfilename+".pdf");

effmed = projmed.Clone("effmed")
effmed.Divide(fitfunc)
effmed.Draw()
effmed.SetMinimum(0)
c.Print(outfilename+".pdf");

fithigh = projhigh.Clone("fithigh")
fithigh.Divide(hEff)
shigh = fithigh.Fit(fitfunc,"S","",minfitrange,maxfitrange)
shigh = fithigh.Fit(fitfunc,"SWL","",minfitrange,maxfitrange)
c.Print(outfilename+".pdf");

effhigh = projhigh.Clone("effhigh")
effhigh.Divide(fitfunc)
effhigh.Draw()
effhigh.SetMinimum(0)
c.Print(outfilename+".pdf");

"""
sigshape = projmed.Clone("sigshape")
sigshape.Scale(1.0/smed.Parameter(1))
sigshape.Add(projhigh,-1.0/shigh.Parameter(1))
sigshape.Scale(1.0/(smed.Parameter(0)/smed.Parameter(1)-shigh.Parameter(0)/shigh.Parameter(1)))

bkgshape = projmed.Clone("bkgshape")
bkgshape.Scale(1.0/smed.Parameter(0))
bkgshape.Add(projhigh,-1.0/shigh.Parameter(0))
bkgshape.Scale(1.0/(smed.Parameter(1)/smed.Parameter(0)-shigh.Parameter(1)/shigh.Parameter(0)))

sigshape.Draw()
c.Print(outfilename+".pdf");
bkgshape.Draw()
c.Print(outfilename+".pdf");

fitmed = projmed.Clone("fitmed")
fitmed.Divide(effmed)
smed = fitmed.Fit(fitfunc,"S","",minfitrange,maxfitrange)
smed = fitmed.Fit(fitfunc,"SWL","",minfitrange,maxfitrange)
c.Print(outfilename+".pdf");

effmed = projmed.Clone("effmed")
effmed.Divide(fitfunc)
effmed.Draw()
effmed.SetMinimum(0)
c.Print(outfilename+".pdf");

fithigh = projhigh.Clone("fithigh")
fithigh.Divide(effmed)
shigh = fithigh.Fit(fitfunc,"S","",minfitrange,maxfitrange)
shigh = fithigh.Fit(fitfunc,"SWL","",minfitrange,maxfitrange)
c.Print(outfilename+".pdf");

effhigh = projhigh.Clone("effhigh")
effhigh.Divide(fitfunc)
effhigh.Draw()
effhigh.SetMinimum(0)
c.Print(outfilename+".pdf");

sigshape = projmed.Clone("sigshape")
sigshape.Scale(1.0/smed.Parameter(1))
sigshape.Add(projhigh,-1.0/shigh.Parameter(1))
sigshape.Scale(1.0/(smed.Parameter(0)/smed.Parameter(1)-shigh.Parameter(0)/shigh.Parameter(1)))

bkgshape = projmed.Clone("bkgshape")
bkgshape.Scale(1.0/smed.Parameter(0))
bkgshape.Add(projhigh,-1.0/shigh.Parameter(0))
bkgshape.Scale(1.0/(smed.Parameter(1)/smed.Parameter(0)-shigh.Parameter(1)/shigh.Parameter(0)))

sigshape.Draw()
c.Print(outfilename+".pdf");
bkgshape.Draw()
c.Print(outfilename+".pdf");
"""

effmed.Draw()
effhigh.SetLineColor(2)
effhigh.Draw("same")
hEff.SetLineColor(3)
hEff.Draw("same")
c.Print(outfilename+".pdf");

heff2d = hist.Clone("heff2d")

for ix in range(1,nbinsX+1):
    for iy in range(1,nbinsY+1):
        heff2d.SetBinContent(ix,iy,effmed.GetBinContent(ix))
        heff2d.SetBinError(ix,iy,effmed.GetBinError(ix))



#minfitrange = 15000
#maxfitrange = 50000
#
#qieArr3 = array.array('d')
#dataEffArr = array.array('d')
#dataEffErrArr = array.array('d')
#zeroArr = array.array('d')
#hDataEff2d = hist.Clone("hDataEff2d")
#if True:
    #min_iy = 1
    #max_iy = 15
    ##proj = histNormed.ProjectionX("test_bkg",min_iy,max_iy)
    #proj = histNormedNoEff.ProjectionX("test_bkg",min_iy,max_iy)
    #proj.SetTitle("dimuons vs. intensity, mass [{0}, {1}];{2};arbitrary units".format(histNormed.GetYaxis().GetBinLowEdge(min_iy),histNormed.GetYaxis().GetBinUpEdge(max_iy),intensityvar))
    #maxval = proj.GetBinContent(proj.GetMaximumBin())
    #proj.GetYaxis().SetRangeUser(-0.1*maxval,1.1*maxval)
    #proj.GetXaxis().SetRangeUser(0,1e5)
    ##s = proj.Fit(fitfunc,"S","",minfitrange,maxfitrange)
    ##s = proj.Fit(fitfunc,"SWL","",minfitrange,maxfitrange)
    ##proj.GetYaxis().SetRangeUser(-0.2*fitfunc.Eval(maxfitrange),3*fitfunc.Eval(maxfitrange))
    #proj.Draw()
    #c.Print(outfilename+".pdf")
    #for ix in range(1,nbinsX+1):
        #qieArr3.append(proj.GetXaxis().GetBinCenter(ix))
        #zeroArr.append(0)
        #eff = proj.GetBinContent(ix)/proj.GetXaxis().GetBinCenter(ix)*75e3
        #effErr = proj.GetBinError(ix)/proj.GetXaxis().GetBinCenter(ix)*75e3
        #dataEffArr.append(eff)
        #dataEffErrArr.append(effErr)
        #for iy in range(1,nbinsY+1):
            ##histNormed.SetBinContent(ix, iy, hist.GetBinContent(ix,iy)/(1.0+hnorm.GetBinContent(ix)*eff))
            ##histNormed.SetBinContent(ix, iy, hist.GetBinContent(ix,iy)*inveff/(1.0+hnorm.GetBinContent(ix)))
            ##histNormed.SetBinContent(ix, iy, hist.GetBinContent(ix,iy)*(integralFullEff/integralRealEff)/(1.0+hnorm.GetBinContent(ix)))
            #hDataEff2d.SetBinContent(ix,iy,eff)
            #hDataEff2d.SetBinError(ix,iy,effErr)
#
#if True:
    #min_iy = 21
    #max_iy = 30
    ##proj = histNormed.ProjectionX("test_bkg",min_iy,max_iy)
    #proj = histNormedNoEff.ProjectionX("test_bkg",min_iy,max_iy)
    #proj.SetTitle("dimuons vs. intensity, mass [{0}, {1}];{2};arbitrary units".format(histNormed.GetYaxis().GetBinLowEdge(min_iy),histNormed.GetYaxis().GetBinUpEdge(max_iy),intensityvar))
    #maxval = proj.GetBinContent(proj.GetMaximumBin())
    #proj.GetYaxis().SetRangeUser(-0.1*maxval,1.1*maxval)
    #proj.GetXaxis().SetRangeUser(0,1e5)
    ##s = proj.Fit(fitfunc,"S","",minfitrange,maxfitrange)
    ##s = proj.Fit(fitfunc,"SWL","",minfitrange,maxfitrange)
    ##proj.GetYaxis().SetRangeUser(-0.2*fitfunc.Eval(maxfitrange),3*fitfunc.Eval(maxfitrange))
    #proj.Draw()
    #c.Print(outfilename+".pdf")
#if True:
    #min_iy = 31
    #max_iy = 60
    ##proj = histNormed.ProjectionX("test_bkg",min_iy,max_iy)
    #proj = histNormedNoEff.ProjectionX("test_bkg",min_iy,max_iy)
    #proj.SetTitle("dimuons vs. intensity, mass [{0}, {1}];{2};arbitrary units".format(histNormed.GetYaxis().GetBinLowEdge(min_iy),histNormed.GetYaxis().GetBinUpEdge(max_iy),intensityvar))
    #maxval = proj.GetBinContent(proj.GetMaximumBin())
    #proj.GetYaxis().SetRangeUser(-0.1*maxval,1.1*maxval)
    #proj.GetXaxis().SetRangeUser(0,1e5)
    ##s = proj.Fit(fitfunc,"S","",minfitrange,maxfitrange)
    ##s = proj.Fit(fitfunc,"SWL","",minfitrange,maxfitrange)
    ##proj.GetYaxis().SetRangeUser(-0.2*fitfunc.Eval(maxfitrange),3*fitfunc.Eval(maxfitrange))
    #proj.Draw()
    #c.Print(outfilename+".pdf")

#dataeffgraph=TGraphErrors(len(qieArr3),qieArr3,dataEffArr,zeroArr,dataEffErrArr)
##dataeffgraph.SetTitle("efficiency vs. intensity;{0};efficiency".format(intensityvar))
#effgraph.Draw("A*")
#dataeffgraph.SetMarkerColor(2)
#dataeffgraph.Draw("*")
##dataeffgraph.GetYaxis().SetRangeUser(0.0,1.1)
##dataeffgraph.GetXaxis().SetRangeUser(5e3,80e3)
#c.Print(outfilename+".pdf");

histNormed = histNormedNoEff.Clone("hEventsNormalized")
histNormed.SetTitle("Efficiency-corrected, luminosity-normalized data;{0};mass [GeV]".format(intensityvar))
histNormed.Divide(heff2d)
histNormed.Draw("colz")
c.Print(outfilename+".pdf");

#if True:
    #min_iy = 1
    #max_iy = 15
    ##proj = histNormed.ProjectionX("test_bkg",min_iy,max_iy)
    #proj = histNormed.ProjectionX("test_bkg",min_iy,max_iy)
    #proj.SetTitle("normalized dimuons vs. intensity, mass [{0}, {1}];{2};arbitrary units".format(histNormed.GetYaxis().GetBinLowEdge(min_iy),histNormed.GetYaxis().GetBinUpEdge(max_iy),intensityvar))
    #maxval = proj.GetBinContent(proj.GetMaximumBin())
    #proj.GetYaxis().SetRangeUser(-0.1*maxval,1.1*maxval)
    #proj.GetXaxis().SetRangeUser(0,1e5)
    #s = proj.Fit(fitfunc,"S","",minfitrange,maxfitrange)
    #s = proj.Fit(fitfunc,"SWL","",minfitrange,maxfitrange)
    #proj.GetYaxis().SetRangeUser(-0.2*fitfunc.Eval(maxfitrange),3*fitfunc.Eval(maxfitrange))
    #c.Print(outfilename+".pdf")
#
#if True:
    #min_iy = 26
    #max_iy = 40
    ##proj = histNormed.ProjectionX("test_bkg",min_iy,max_iy)
    #proj = histNormed.ProjectionX("test_bkg",min_iy,max_iy)
    #proj.SetTitle("normalized dimuons vs. intensity, mass [{0}, {1}];{2};arbitrary units".format(histNormed.GetYaxis().GetBinLowEdge(min_iy),histNormed.GetYaxis().GetBinUpEdge(max_iy),intensityvar))
    #maxval = proj.GetBinContent(proj.GetMaximumBin())
    #proj.GetYaxis().SetRangeUser(-0.1*maxval,1.1*maxval)
    #proj.GetXaxis().SetRangeUser(0,1e5)
    #s = proj.Fit(fitfunc,"S","",minfitrange,maxfitrange)
    #s = proj.Fit(fitfunc,"SWL","",minfitrange,maxfitrange)
    #proj.GetYaxis().SetRangeUser(-0.2*fitfunc.Eval(maxfitrange),3*fitfunc.Eval(maxfitrange))
    #c.Print(outfilename+".pdf")

massArr = array.array('d')
zeroArr = array.array('d')
p0Arr = array.array('d')
p1Arr = array.array('d')
p0ErrArr = array.array('d')
p1ErrArr = array.array('d')
hEffCorr = hist.Clone("hEffCorr")
hEffCorr.SetTitle("deviation from linear fit;{0};mass [GeV]".format(intensityvar))
#c.Print(outfilename+".pdf]");
#sys.exit(0)

minfitrange = 3000
maxfitrange = 60000


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
        p0Arr.append(s.Parameter(0))
        p0ErrArr.append(s.ParError(0))
        p1Arr.append(s.Parameter(1)*0.5*maxfitrange)
        p1ErrArr.append(s.ParError(1)*0.5*maxfitrange)
        #if (histNormed.GetYaxis().GetBinCenter(iy)==3.05):
            #s.Print("V")
        proj.Divide(fitfunc)
        for ix in range(1,nbinsX+1):
            hEffCorr.SetBinContent(ix,iy,proj.GetBinContent(ix))
            hEffCorr.SetBinError(ix,iy,proj.GetBinError(ix))
        #proj.Draw()
        #c.Print(outfilename+".pdf")

graph=TGraphErrors(len(massArr),massArr,p0Arr,zeroArr,p0ErrArr)
graph.SetTitle("Signal vs. mass, {0}=[0,1000];mass [GeV];arbitrary units".format(intensityvar))
graph.SetName("siggraph")
graph.Write()
#outfile.Add(graph)
graph.Draw("A*")
c.Print(outfilename+".pdf");

graph2=TGraphErrors(len(massArr),massArr,p1Arr,zeroArr,p1ErrArr)
graph2.SetTitle("Background vs. mass, {0}=[0,1000];mass [GeV];arbitrary units".format(intensityvar))
graph2.SetName("bkggraph")
graph2.Write()
#outfile.Add(graph2)
graph2.SetMarkerColor(2)
graph2.Draw("*")
c.Print(outfilename+".pdf");
graph2.Draw("A*")
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
