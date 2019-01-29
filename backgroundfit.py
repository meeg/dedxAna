#!/usr/bin/env python
import sys
import array, math
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, gPad, TF1, THStack, TLegend, TH2D, TH1D, TGraphErrors, TSpline3, TObjArray, TFractionFitter
import getopt
import utils

gROOT.SetBatch(True)
gStyle.SetOptStat(11)
gStyle.SetOptFit(1)

infile = TFile("backgroundfit_histos.root")

datafile = TFile("cut_data.root")
events = datafile.Get("save")

outfilename="backgroundfit"

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

qiecut = utils.qiecuts()
qualitycut = utils.qualitycuts()
runcut = utils.runcut()
intensityvar = utils.intensityvar()
binedgesqie = utils.binedgesqie()
binedgesmass = utils.binedgesmass()
xfcut = "xF>0.67 && xF<0.9"
xfcutname = "xF=[0.67,0.9]"



for targetnum in range(0,9):
    c.SetLogz(1)

    xfbinnum = 0
    targetcut = "targetPos=="+str(targetnum)
    if targetnum==0:
        targetcut = "targetPos>0"
    if targetnum==8:
        targetcut = "targetPos>=5"

    namestr = "tgt{0}xf{1}".format(targetnum,xfbinnum)
    titlestr = "{0}, {1}".format(targetnames[targetnum],xfcutname)

    histqiematrix = infile.Get("hqiematrix"+str(targetnum))
    histqiematrix.Sumw2()
    histqiematrix.Draw()
    c.Print(outfilename+".pdf");

    histqie = infile.Get("hqie"+str(targetnum))
    histqie.Sumw2()
    histqie.Draw()
    c.Print(outfilename+".pdf");


    #occupancyvar = "D1+D2+D3-44"
    occupancyvar = "D1-(pnumHitsSt1+nnumHitsSt1)"
    #occupancyvar = "D1-12"
    histdtot = TH2D("hdtot","hdtot",len(binedgesqie)-1,binedgesqie,300,0,600)
    events.Draw("{1}:{0}>>+hdtot".format(intensityvar,occupancyvar)," && ".join([targetcut,qualitycut,runcut,xfcut]),"colz")
    histdtot.SetTitle(occupancyvar+" vs. "+intensityvar)
    c.Print(outfilename+".pdf");
    #c.SetLogx(1)
    #c.Print(outfilename+".pdf");
    #c.SetLogx(0)

    nbinsX = histdtot.GetNbinsX()
    nbinsY = histdtot.GetNbinsY()

    #efffunc = TF1("efffunc","[1]/(1+exp([2]*([0]*x-[3])))",0,1000)
    #efffunc.SetParameters(1.0,1.0,0.0354,105)
    #efffunc.SetParameter(1,1.0)
    #efffunc = TF1("efffunc","TMath::Max(0.0,(1.0 - 0.0050*x*[0]))",0,1500)
    #efffunc = TF1("efffunc","(x*[0]<200) + (x*[0]>=200 && x*[0]<600)*(600-x*[0])/(600-200)",0,1500)
    #efffunc = TF1("efffunc","TMath::Max(0.0,(1.0 - 0.0018*x*[0]))",0,1500)
    efffunc = TF1("efffunc","TMath::Max(0.0,(1.0 - 0.001*x*[0]))",0,1500)
    efffunc.FixParameter(0,1.0)
    efffunc.Draw()
    c.Print(outfilename+".pdf");

    refprojnum=2
    refproj = histdtot.ProjectionY("refproj",refprojnum,refprojnum)
    refproj.SetTitle("{2} [{0}, {1}];{3}".format(histdtot.GetXaxis().GetBinLowEdge(refprojnum),histdtot.GetXaxis().GetBinUpEdge(refprojnum),intensityvar,occupancyvar))
    #refproj.GetXaxis().SetRangeUser(0,100)
    refproj.Draw()
    c.Print(outfilename+".pdf");
    refqie = histdtot.GetXaxis().GetBinCenter(refprojnum)

    efffunc.SetParameter(0,1.0)
    denomhist = refproj.Clone("denomhist")
    #for ix in range(1,denomhist.GetNbinsX()+1):
        #if denomhist.GetBinContent(ix)==1:
            #denomhist.SetBinContent(ix,0)
    denomhist.Divide(efffunc)
    denomhist.Draw()
    denominator = denomhist.Integral()
    c.Print(outfilename+".pdf");

    heff1d = histdtot.ProjectionX("heff1d_"+namestr)
    heff1d.Sumw2()
    qieArr = array.array('d')
    effArr = array.array('d')
    for ix in range(1,nbinsX+1):
        eff = denomhist.Clone("test"+str(ix))
        binqie = histdtot.GetXaxis().GetBinCenter(ix)
        efffunc.SetParameter(0,binqie/refqie)
        eff.Multiply(efffunc)
        #eff.Draw()
        #c.Print(outfilename+".pdf");
        numerator = eff.Integral()
        #eff.Draw()
        #efffunc.Draw("same")
        #c.Print(outfilename+".pdf");
        #print numerator/denominator
        print ix, binqie, refqie, denominator, numerator
        qieArr.append(binqie)
        effArr.append(numerator/denominator)
        heff1d.SetBinContent(ix,numerator/denominator)
        heff1d.SetBinError(ix,0.01)

    effgraph = TGraph(len(qieArr),qieArr,effArr)
    effgraph.Draw("A*")
    effgraph.SetName("effgraph_"+namestr)
    effgraph.SetTitle("Efficiency")
    effgraph.Write()
    c.Print(outfilename+".pdf");

    heff1d.Draw()
    c.Print(outfilename+".pdf");

    hist = TH2D("hdata_"+namestr,"hdata_"+namestr,len(binedgesqie)-1,binedgesqie,len(binedgesmass)-1,binedgesmass)
    events.Draw("mass:{0}>>+hdata_{1}".format(intensityvar,namestr)," && ".join([targetcut,qualitycut,runcut,xfcut]),"colz")
    hist.Sumw2()
    hist.SetTitle("mass vs. {0}, {1};{0};mass [GeV]".format(intensityvar,titlestr))
    c.Print(outfilename+".pdf");

    #hist = infile.Get("hdata")
    #hist.Sumw2()
    #hist.Draw("colz")
    #c.Print(outfilename+".pdf");

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


    hlumi = histqie.Clone("hlumiqie"+str(targetnum))
    intensityfunc = TF1("fx","x")
    intensityfunc.SetRange(0,1e5)
    hlumi.Multiply(intensityfunc)

    fitfunc = TF1("f","pol1")
    fitfunc.SetRange(0,1e5)

    hlumi.Scale(1.0/hlumi.GetMaximum())
    hlumi.SetTitle("luminosity normalization;{0};total {0} [arb. units]".format(intensityvar))
    hlumi.Draw("")
    c.Print(outfilename+".pdf");


    hlumi2d = hist.Clone("hlumi2d_"+namestr)

    for ix in range(1,nbinsX+1):
        for iy in range(1,nbinsY+1):
            hlumi2d.SetBinContent(ix,iy,hlumi.GetBinContent(ix))
            hlumi2d.SetBinError(ix,iy,hlumi.GetBinError(ix))

    histNormedNoEff = hist.Clone("histNormedNoEff_"+namestr)
    histNormedNoEff.SetTitle("Luminosity-normalized data;{0};mass [GeV]".format(intensityvar))
    histNormedNoEff.Divide(hlumi2d)
    histNormedNoEff.Draw("colz")
    #c.Print(outfilename+".pdf");



    firstbin = 1
    lastbin = hist.GetYaxis().FindBin(2.39)
    projlow = histNormedNoEff.ProjectionX("projlow_"+namestr,firstbin,lastbin)
    projlow.SetTitle("low mass, mass [{0},{1}]".format(histNormedNoEff.GetYaxis().GetBinLowEdge(firstbin),histNormedNoEff.GetYaxis().GetBinUpEdge(lastbin)))
    #projlow.GetYaxis().SetRangeUser(0,projlow.GetBinContent(projlow.GetMaximumBin()))
    projlow.SetMinimum(0)
    projlow.Draw()
    #c.Print(outfilename+".pdf");

    firstbin = hist.GetYaxis().FindBin(2.41)
    lastbin = hist.GetYaxis().FindBin(3.39)
    projhi1 = histNormedNoEff.ProjectionX("projhi1_"+namestr,firstbin,lastbin)
    projhi1.SetTitle("high mass, mass [{0},{1}]".format(histNormedNoEff.GetYaxis().GetBinLowEdge(firstbin),histNormedNoEff.GetYaxis().GetBinUpEdge(lastbin)))
    #projhi1.GetYaxis().SetRangeUser(0,projmed.GetBinContent(projmed.GetMaximumBin()))
    projhi1.SetMinimum(0)
    projhi1.Draw()
    #c.Print(outfilename+".pdf");

    firstbin = hist.GetYaxis().FindBin(3.41)
    lastbin = nbinsY
    projhi2 = histNormedNoEff.ProjectionX("projhi2_"+namestr,firstbin,lastbin)
    projhi2.SetTitle("high mass, mass [{0},{1}]".format(histNormedNoEff.GetYaxis().GetBinLowEdge(firstbin),histNormedNoEff.GetYaxis().GetBinUpEdge(lastbin)))
    #projhi2.GetYaxis().SetRangeUser(0,projhigh.GetBinContent(projhigh.GetMaximumBin()))
    projhi2.SetMinimum(0)
    projhi2.Draw()
    #c.Print(outfilename+".pdf");


    firstbin = hist.GetYaxis().FindBin(2.41)
    lastbin = nbinsY
    projhi = histNormedNoEff.ProjectionX("projhi_"+namestr,firstbin,lastbin)
    projhi.SetTitle("high mass, mass [{0},{1}]".format(histNormedNoEff.GetYaxis().GetBinLowEdge(firstbin),histNormedNoEff.GetYaxis().GetBinUpEdge(lastbin)))
    #projhigh.GetYaxis().SetRangeUser(0,projhigh.GetBinContent(projhigh.GetMaximumBin()))
    projhi.SetMinimum(0)
    projhi.Draw()
    #c.Print(outfilename+".pdf");


    hEff = projlow.Clone("hEff_"+namestr) #we assume projlow is pure background and divide by intensity to get the efficiency vs. intensity (only valid at low intensity where we expect the background to be linear)
    hEff.Divide(intensityfunc)
    hEff.Scale(0.6/hEff.GetBinContent(hEff.GetXaxis().FindBin(10e3))) #arbitrary normalization
    for ix in range(1,nbinsX+1):
        if hEff.GetBinContent(ix)<=0:
            hEff.SetBinContent(ix,1.0)
    hEff.Draw()
    c.Print(outfilename+".pdf");

    #minfitrange = 5e3
    minfitrange = 0
    maxfitrange = 30e3

    #fudge = 16.0
    fudge = 1

    fithi1 = projhi1.Clone("fithi1_"+namestr)
    fithi1.Divide(hEff)
    shi1 = fithi1.Fit(fitfunc,"S","",minfitrange,maxfitrange)
    shi1 = fithi1.Fit(fitfunc,"SWL","",minfitrange,maxfitrange)
    #c.Print(outfilename+".pdf");
    fitfunc.SetParameter(0,fudge*fitfunc.GetParameter(0))

    effhi1 = projhi1.Clone("effhi1_"+namestr)
    effhi1.Divide(fitfunc)
    effhi1.Draw()
    effhi1.SetMinimum(0)
    #c.Print(outfilename+".pdf");

    fithi2 = projhi2.Clone("fithi2_"+namestr)
    fithi2.Divide(hEff)
    shi2 = fithi2.Fit(fitfunc,"S","",minfitrange,maxfitrange)
    shi2 = fithi2.Fit(fitfunc,"SWL","",minfitrange,maxfitrange)
    #c.Print(outfilename+".pdf");
    fitfunc.SetParameter(0,fudge*fitfunc.GetParameter(0))

    effhi2 = projhi2.Clone("effhi2_"+namestr)
    effhi2.Divide(fitfunc)
    effhi2.Draw()
    effhi2.SetMinimum(0)
    #c.Print(outfilename+".pdf");

    fithi = projhi.Clone("fithi_"+namestr)
    fithi.Divide(hEff)
    shi = fithi.Fit(fitfunc,"S","",minfitrange,maxfitrange)
    shi = fithi.Fit(fitfunc,"SWL","",minfitrange,maxfitrange)
    #c.Print(outfilename+".pdf");
    fitfunc.SetParameter(0,fudge*fitfunc.GetParameter(0))

    effhi = projhi.Clone("effhi_"+namestr)
    effhi.Divide(fitfunc)
    effhi.Draw()
    effhi.SetMinimum(0)
    #c.Print(outfilename+".pdf");

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

    #heff1d = effhi
    if targetnum == 0:
        heff_alltargets = effhi
    heff1d = heff_alltargets

    minfitrange = 0
    maxfitrange = 80000

    fitlow = projlow.Clone("fitlow_"+namestr)
    fitlow.Divide(heff1d)
    s = fitlow.Fit(fitfunc,"S","",minfitrange,maxfitrange)
    s = fitlow.Fit(fitfunc,"SWL","",minfitrange,maxfitrange)
    fitlow.GetYaxis().SetRangeUser(-0.2*fitfunc.Eval(maxfitrange),3*fitfunc.Eval(maxfitrange))
    c.Print(outfilename+".pdf");

    fithi1 = projhi1.Clone("fithi1_"+namestr)
    fithi1.Divide(heff1d)
    s = fithi1.Fit(fitfunc,"S","",minfitrange,maxfitrange)
    s = fithi1.Fit(fitfunc,"SWL","",minfitrange,maxfitrange)
    fithi1.GetYaxis().SetRangeUser(-0.2*fitfunc.Eval(maxfitrange),3*fitfunc.Eval(maxfitrange))
    c.Print(outfilename+".pdf");

    fithi2 = projhi2.Clone("fithi2_"+namestr)
    fithi2.Divide(heff1d)
    s = fithi2.Fit(fitfunc,"S","",minfitrange,maxfitrange)
    s = fithi2.Fit(fitfunc,"SWL","",minfitrange,maxfitrange)
    fithi2.GetYaxis().SetRangeUser(-0.2*fitfunc.Eval(maxfitrange),3*fitfunc.Eval(maxfitrange))
    c.Print(outfilename+".pdf");

    heff2d = hist.Clone("heff2d_"+namestr)

    for ix in range(1,nbinsX+1):
        for iy in range(1,nbinsY+1):
            heff2d.SetBinContent(ix,iy,heff1d.GetBinContent(ix))
            heff2d.SetBinError(ix,iy,heff1d.GetBinError(ix))

    histNormed = histNormedNoEff.Clone("hEventsNormalized_"+namestr)
    histNormed.SetTitle("Efficiency-corrected, luminosity-normalized data;{0};mass [GeV]".format(intensityvar))
    histNormed.Divide(heff2d)
    histNormed.Draw("colz")
    #c.Print(outfilename+".pdf");

    massArr = array.array('d')
    zeroArr = array.array('d')
    sigArr = array.array('d')
    bkgArr = array.array('d')
    sigErrArr = array.array('d')
    bkgErrArr = array.array('d')
    hEffCorr = hist.Clone("hEffCorr_"+namestr)
    hEffCorr.SetTitle("deviation from linear fit;{0};mass [GeV]".format(intensityvar))
    massArr2 = array.array('d')
    zeroArr2 = array.array('d')
    sigArr2 = array.array('d')
    bkgArr2 = array.array('d')
    sigErrArr2 = array.array('d')
    bkgErrArr2 = array.array('d')

    minfitrange = 0
    maxfitrange = 80000

    firstbin = histNormed.GetXaxis().FindBin(minfitrange+1)
    lastbin = histNormed.GetXaxis().FindBin(maxfitrange-1)
    print firstbin,lastbin

    hist1d = hist.ProjectionY("hdata1d_"+namestr,firstbin,lastbin)
    hist1d.SetTitle("{0};mass [GeV]".format(titlestr))
    #hist1d.Draw()
    #c.Print(outfilename+".pdf");

    bkghist = hlumi.Clone("bkgcounts_"+namestr)
    sighist = hlumi.Clone("sigcounts_"+namestr)
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

    bkghist.Draw()
    c.Print(outfilename+".pdf");
    sighist.Draw()
    c.Print(outfilename+".pdf");

    bkghistnorm = bkghist.Clone("bkghistnorm_"+namestr)
    bkghistnorm.SetTitle("Background shape in raw data, normalized to bin width")
    #outfile.Add(bkghistnorm)
    sighistnorm = sighist.Clone("sighistnorm_"+namestr)
    sighistnorm.SetTitle("Signal shape in raw data, normalized to bin width")

    bkghistcounts = bkghist.Clone("bkghistcounts_"+namestr)
    bkghistcounts.SetTitle("Background counts for TFractionFitter")
    sighistcounts = sighist.Clone("sighistcounts_"+namestr)
    sighistcounts.SetTitle("Signal counts for TFractionFitter")
    bkghistweights = bkghist.Clone("bkghistweights_"+namestr)
    bkghistweights.SetTitle("Background weights for TFractionFitter")
    sighistweights = sighist.Clone("sighistweights_"+namestr)
    sighistweights.SetTitle("Signal weights for TFractionFitter")
    for ix in range(1,nbinsX+1):
        width = bkghistnorm.GetXaxis().GetBinUpEdge(ix) - bkghistnorm.GetXaxis().GetBinLowEdge(ix)
        bkghistnorm.SetBinContent(ix,bkghistnorm.GetBinContent(ix)*1.0/width)
        bkghistnorm.SetBinError(ix,bkghistnorm.GetBinError(ix)*1.0/width)
        sighistnorm.SetBinContent(ix,sighistnorm.GetBinContent(ix)*1.0/width)
        sighistnorm.SetBinError(ix,sighistnorm.GetBinError(ix)*1.0/width)
        bkghistcounts.SetBinContent(ix,bkghist.GetBinContent(ix)**2/bkghist.GetBinError(ix)**2)
        bkghistweights.SetBinContent(ix,bkghist.GetBinError(ix)**2/bkghist.GetBinContent(ix))
        sighistcounts.SetBinContent(ix,sighist.GetBinContent(ix)**2/sighist.GetBinError(ix)**2)
        sighistweights.SetBinContent(ix,sighist.GetBinError(ix)**2/sighist.GetBinContent(ix))

    #bkghistnorm.Draw()
    #c.Print(outfilename+".pdf");
    #sighistnorm.Draw()
    #c.Print(outfilename+".pdf");

    fitcomponents = TObjArray(2)
    fitcomponents.Add(sighistcounts)
    fitcomponents.Add(bkghistcounts)

    #c.Print(outfilename+".pdf]")
    #sys.exit(0)


    for iy in range(1,nbinsY+1):
        dataslice = hist.ProjectionX("rawdataslice"+str(iy),iy,iy)
        fracfitter = TFractionFitter(dataslice,fitcomponents,"Q")
        fracfitter.UnConstrain(0)
        fracfitter.UnConstrain(1)
        fracfitter.SetRangeX(firstbin,lastbin)
        fracfitter.SetWeight(0,sighistweights)
        fracfitter.SetWeight(1,bkghistweights)
        #fracfitter.SetData(dataslice)
        fitstatus = fracfitter.Fit()
        #print fitstatus.Get().Status()
        #print fitstatus.Parameter(0)
        if fitstatus.Get().Status()==0:
            #fitstatus.Print("V")
            dataslice.Draw("Ep")
            fracfitter.GetPlot().SetLineColor(2)
            fracfitter.GetPlot().Draw("same")
            #print fracfitter.GetChisquare(),fracfitter.GetNDF()
            #print fracfitter.GetPlot().Integral()
            #print sighist.Integral(firstbin,lastbin)*fitstatus.Parameter(0)+bkghist.Integral(firstbin,lastbin)*fitstatus.Parameter(1)
            #print fitstatus.Parameter(0), fitstatus.Parameter(1)
            total = sighist.Clone("temp_total")
            total.Scale(fitstatus.Parameter(0)/sighist.Integral(firstbin,lastbin))
            total.Add(bkghist,fitstatus.Parameter(1)/bkghist.Integral(firstbin,lastbin))
            #sigscale = fitstatus.Parameter(0)*(fracfitter.GetPlot().Integral()/sighist.Integral(firstbin,lastbin))
            #bkgscale = fitstatus.Parameter(1)*(fracfitter.GetPlot().Integral()/bkghist.Integral(firstbin,lastbin))
            #print sigscale,bkgscale,total.Integral(firstbin,lastbin)
            total.Scale(fracfitter.GetPlot().Integral())
            total.SetLineColor(4)
            total.Draw("same")
            #c.Print(outfilename+".pdf")
            massArr2.append(histNormed.GetYaxis().GetBinCenter(iy))
            zeroArr2.append(0)
            sigArr2.append(fitstatus.Parameter(0)*fracfitter.GetPlot().Integral())
            bkgArr2.append(fitstatus.Parameter(1)*fracfitter.GetPlot().Integral())
            sigErrArr2.append(fitstatus.ParError(0)*fracfitter.GetPlot().Integral())
            bkgErrArr2.append(fitstatus.ParError(1)*fracfitter.GetPlot().Integral())
        print fitstatus.Parameter(0), fitstatus.Parameter(1)
        fracfitter.Delete()

        proj = histNormed.ProjectionX("normslice"+str(iy),iy,iy)
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
            #print s.Get().Chi2(),s.Get().Ndf()
            #print s.Parameter(0),s.Parameter(1)
            #c.Print(outfilename+".pdf")
            #print histNormed.GetYaxis().GetBinCenter(iy),s.Parameter(0),s.Parameter(1)
            massArr.append(histNormed.GetYaxis().GetBinCenter(iy))
            zeroArr.append(0)
            sigArr.append(s.Parameter(0)*sighist.Integral(firstbin,lastbin))
            #print s.Parameter(0)*sighist.Integral(firstbin,lastbin)
            sigErrArr.append(s.ParError(0)*sighist.Integral(firstbin,lastbin))
            bkgArr.append(s.Parameter(1)*bkghist.Integral(firstbin,lastbin))
            bkgErrArr.append(s.ParError(1)*bkghist.Integral(firstbin,lastbin))

            #if (histNormed.GetYaxis().GetBinCenter(iy)==3.05):
                #s.Print("V")
            proj.Divide(fitfunc)
            for ix in range(1,nbinsX+1):
                hEffCorr.SetBinContent(ix,iy,proj.GetBinContent(ix))
                hEffCorr.SetBinError(ix,iy,proj.GetBinError(ix))
            #proj.Draw()
            #c.Print(outfilename+".pdf")

    siggraph=TGraphErrors(len(massArr),massArr,sigArr,zeroArr,sigErrArr)
    siggraph.SetTitle("Signal vs. mass, {0}=[{1},{2}];mass [GeV];counts".format(intensityvar,minfitrange,maxfitrange))
    siggraph.SetName("siggraph_"+namestr)
    siggraph.Write()
    #outfile.Add(graph)
    siggraph.Draw("A*")
    #c.Print(outfilename+".pdf");

    bkggraph=TGraphErrors(len(massArr),massArr,bkgArr,zeroArr,bkgErrArr)
    bkggraph.SetTitle("Background vs. mass, {0}=[{1},{2}];mass [GeV];counts".format(intensityvar,minfitrange,maxfitrange))
    bkggraph.SetName("bkggraph_"+namestr)
    bkggraph.SetMarkerColor(2)
    bkggraph.Write()
    #outfile.Add(graph2)
    bkggraph.Draw("*")
    c.Print(outfilename+".pdf");
    #bkggraph.Draw("A*")
    #c.Print(outfilename+".pdf");

    hist1d.Draw()
    siggraph.Draw("*")
    bkggraph.Draw("*")
    c.Print(outfilename+".pdf");

    siggraph2=TGraphErrors(len(massArr2),massArr2,sigArr2,zeroArr2,sigErrArr2)
    siggraph2.SetTitle("Signal vs. mass, {0}=[{1},{2}];mass [GeV];counts".format(intensityvar,minfitrange,maxfitrange))
    siggraph2.SetName("siggraph2_"+namestr)
    siggraph2.Write()
    #outfile.Add(graph)
    siggraph2.Draw("A*")
    #c.Print(outfilename+".pdf");

    bkggraph2=TGraphErrors(len(massArr2),massArr2,bkgArr2,zeroArr2,bkgErrArr2)
    bkggraph2.SetTitle("Background vs. mass, {0}=[{1},{2}];mass [GeV];counts".format(intensityvar,minfitrange,maxfitrange))
    bkggraph2.SetName("bkggraph2_"+namestr)
    bkggraph2.SetMarkerColor(2)
    bkggraph2.Write()
    #outfile.Add(graph2)
    bkggraph2.Draw("*")
    c.Print(outfilename+".pdf");
    #bkggraph2.Draw("A*")
    #c.Print(outfilename+".pdf");

    hist1d.Draw()
    siggraph2.Draw("*")
    bkggraph2.Draw("*")
    c.Print(outfilename+".pdf");

    c.SetLogz(0)
    hEffCorr.GetZaxis().SetRangeUser(0.5,2)
    hEffCorr.GetYaxis().SetRangeUser(1.0,5.5)
    hEffCorr.Draw("colz")
    c.Print(outfilename+".pdf");
    #hEffCorr.GetZaxis().SetRangeUser(0.8,1.2)
    #hEffCorr.GetXaxis().SetRangeUser(minfitrange,maxfitrange)
    #c.Print(outfilename+".pdf");
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
