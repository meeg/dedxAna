#!/usr/bin/env python
import sys
tmpargv = sys.argv
sys.argv = []
import math
import getopt
from ROOT import TFile
import utils
import root_numpy, numpy
import numpy.lib.recfunctions
import numpy.ma
import esutil.sqlite_util


sys.argv = tmpargv

def print_usage():
    print("\nUsage: {0} <input ROOT file name> <output ROOT file name>".format(sys.argv[0]))
    print

#if len(sys.argv)!=3:
    #print_usage()
    #sys.exit(0)

#branchlist=["x1_st1",
    #"tx1_st1",
    #"y1",
    #"ty1",
    #"x2_st1",
    #"tx2_st1",
    #"y2",
    #"ty2"]

dimuoncuts = utils.dimuoncuts()
trackcuts = utils.trackcuts()
datacuts = " && ".join([dimuoncuts,trackcuts])
print datacuts

mcbranchlist = ["targetPos",
        "mcrunID",
        "mcspillID",
        "mceventID",
        "mass",
        "xF"]

occbranchlist = [
        "targetPos",
        "spillID",
        "eventID",
        "runID",
        "D1",
        "RF00",
        "PotPerQie",
        "NIM3"]

#events = root_numpy.root2array("dimuons.root",branches=branchlist)
#messy = root_numpy.root2array("cut_data_messy.root")
#messyfile = TFile("cut_data_messy.root")
#messyfile = TFile("mc_drellyan_C_M026_S002_messy_v2.root")
#messytree = messyfile.Get("save")
#print(messytree.GetEntries())
#messytree = TFile("mc_drellyan_C_M026_S002_messy_v2.root").Get("save")
#messytreecut = messytree.CopyTree(" && ".join([datacuts]))
#cutmessy = events.CopyTree(" && ".join([datacuts]))
#messy = root_numpy.root2array("mc_drellyan_C_M026_S002_messy_v2.root",treename="save",selection=" && ".join([datacuts]))
messy = root_numpy.root2array("mc_drellyan_C_M026_S002_messy_v2.root",treename="save",selection=" && ".join([datacuts]),branches=mcbranchlist)
print(messy.size)
print(messy.dtype.names)
#clean = root_numpy.root2array("cut_data_clean.root")
#clean = root_numpy.root2array("mc_drellyan_C_M026_S002_clean_v2.root",treename="save",selection=" && ".join([datacuts]))
clean = root_numpy.root2array("mc_drellyan_C_M026_S002_clean_v2.root",treename="save",selection=" && ".join([datacuts]),branches=mcbranchlist)
print(clean.size)
print(clean.dtype.names)
#occupancy = root_numpy.root2array("cut_data_occupancy.root",treename="save",selection="targetPos==6")
occupancy = root_numpy.root2array("cut_data_occupancy.root",treename="save",selection="targetPos==6",branches=occbranchlist)
#print(occupancy.dtype.names)

print(occupancy.size)
print(occupancy.dtype.names)

embed = root_numpy.root2array("mc_drellyan_C_M026_S002_messy_v2_embed.root",treename="save")

sc = esutil.sqlite_util.SqliteConnection("temp.sqlite")
try:
    sc.execute("DROP TABLE messy")
    sc.execute("DROP TABLE clean")
    sc.execute("DROP TABLE occupancy")
    sc.execute("DROP TABLE embed")
except:
    pass
sc.array2table(messy,"messy")
sc.array2table(clean,"clean")
sc.array2table(occupancy,"occupancy")
sc.array2table(embed,"embed")

joinedclean = sc.execute("SELECT clean.mcrunID,clean.mceventID,clean.mass,clean.xF,embed.runID,embed.spillID,embed.eventID,occupancy.D1,occupancy.RF00,occupancy.PotPerQie FROM clean JOIN embed ON clean.mceventID = embed.mceventID JOIN occupancy ON embed.runID = occupancy.runID AND embed.eventID = occupancy.eventID",asarray=True)
print(joinedclean.dtype)
root_numpy.array2root(joinedclean,"clean.root",mode="recreate",treename="save")

joinedmessy = sc.execute("SELECT messy.mcrunID,messy.mceventID,messy.mass,messy.xF,embed.runID,embed.spillID,embed.eventID,occupancy.D1,occupancy.RF00,occupancy.PotPerQie FROM messy JOIN embed ON messy.mceventID = embed.mceventID JOIN occupancy ON embed.runID = occupancy.runID AND embed.eventID = occupancy.eventID",asarray=True)
print(joinedmessy.dtype)
root_numpy.array2root(joinedmessy,"messy.root",mode="recreate",treename="save")

joinedmessyclean = sc.execute("SELECT messy.mcrunID,messy.mceventID,clean.mass,clean.xF,messy.mass AS massmessy,messy.xF AS xFmessy,embed.runID,embed.spillID,embed.eventID,occupancy.D1,occupancy.RF00,occupancy.PotPerQie FROM messy JOIN embed ON messy.mceventID = embed.mceventID JOIN occupancy ON embed.runID = occupancy.runID AND embed.eventID = occupancy.eventID JOIN clean ON messy.mceventID = clean.mceventID",asarray=True)
print(joinedmessyclean.dtype)
root_numpy.array2root(joinedmessyclean,"messyclean.root",mode="recreate",treename="save")

