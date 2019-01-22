#!/bin/bash
#../bin/make_occupancy ../../notes/merged.tsv seaquestdb01.fnal.gov 3310 67 qqbar2mu+mu- test_occupancy3.root
#../bin/make_tuple ../../notes/merged.tsv seaquestdb01.fnal.gov 3310 67 qqbar2mu+mu- test.root
~/git/dedxAna/tuplemaker/bin/make_occupancy ~/git/dedxAna/notes/merged.tsv seaquestdb01.fnal.gov 3310 67 qqbar2mu+mu- occupancy_rs67_db01.root > occupancy_rs67_db01.txt
~/git/dedxAna/tuplemaker/bin/make_occupancy ~/git/dedxAna/notes/merged.tsv e906-db3.fnal.gov 3306 67 qqbar2mu+mu- occupancy_rs67_db03.root > occupancy_rs67_db03.txt
~/git/dedxAna/tuplemaker/bin/make_tuple ~/git/dedxAna/notes/merged.tsv seaquestdb01.fnal.gov 3310 67 qqbar2mu+mu- dimuon_rs67_db01.root > dimuon_rs67_db01.txt
~/git/dedxAna/tuplemaker/bin/make_tuple ~/git/dedxAna/notes/merged.tsv e906-db3.fnal.gov 3306 67 qqbar2mu+mu- dimuon_rs67_db03.root > dimuon_rs67_db03.txt
~/git/dedxAna/tuplemaker/bin/make_tuplemix ~/git/dedxAna/notes/merged.tsv seaquestdb01.fnal.gov 3310 67 qqbar2mu+mu- dimuonmix_rs67_db01.root > dimuonmix_rs67_db01.txt
~/git/dedxAna/tuplemaker/bin/make_tuplemix ~/git/dedxAna/notes/merged.tsv e906-db3.fnal.gov 3306 67 qqbar2mu+mu- dimuonmix_rs67_db03.root > dimuonmix_rs67_db03.txt
~/git/dedxAna/tuplemaker/bin/make_mc mc_drellyan_C_M026_S002_messy_v2 seaquel.physics.illinois.edu 3283 qqbar2mu+mu- mc_drellyan_C_M026_S002_messy_v2.root > mc_drellyan_C_M026_S002_messy_v2.txt
~/git/dedxAna/tuplemaker/bin/make_mc mc_drellyan_C_M026_S002_clean_v2 seaquel.physics.illinois.edu 3283 qqbar2mu+mu- mc_drellyan_C_M026_S002_clean_v2.root > mc_drellyan_C_M026_S002_clean_v2.txt
