# Variables
| Selection | Variable |
| -------- | -------- |
| M | invariant mass of the same signed oppite charge lepton pair |
| HT | LHE_HT or LHE_HTIncoming (are they equivalent?)|
| #J | LHE_NpNLO|
| LHEFilterPtZ | LHE_Vpt |
| genWeight | Generator_weight or (genWeight == LHEWeight_originalXWGTUP) |


xsec DY inclusiva 5765.40 pb


L equivalent = N_events*(1-2f)**2 / xsec

# inclusive file on gpfs
/gpfs/ddn/srm/cms/store/mc/RunIISummer20UL18NanoAODv9/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/250000/A87275E3-6D57-6A46-8EB2-17F616321665.root
| Selection | Number of events | f | xsec  [pb] | L equivalent [pb-1]|
| -------- | -------- | -------- | -------- | -------- |
// | 258335 | 42296/258335 = 0.164 | 5765.40 | 258335*(1-2*0.164)**2 / 5765.40 = |
LHE_HT>70 && LHE_HT<100 |15492 | 4857/15492 = 0.313 | 5765.40*15492/258335 = 345.74 | 15492*(1-2*0.313)**2 / 345.74  =


# Datasets
| Dataset | Number of events | f |xsec | L equivalent |
| -------- | -------- | -------- | -------- | -------- |
| /DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM| 94452816 |
| /DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM | 195510810 |
/DYJetsToLL_M-50_HT-70to100_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM | 17004433 |
/DYJetsToLL_M-50_HT-100to200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM | 26202328 |
/DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM | 18455718 |
/DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM | 8682257 |
/DYJetsToLL_M-50_HT-600to800_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM | 7035971 |
/DYJetsToLL_M-50_HT-800to1200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM | 6554679 |
/DYJetsToLL_M-50_HT-1200to2500_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM | 5966661 |
/DYJetsToLL_M-50_HT-2500toInf_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM | 1978203 |
/DYJetsToLL_LHEFilterPtZ-0To50_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM | 196207761 |
/DYJetsToLL_LHEFilterPtZ-50To100_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM | 122967660 |
/DYJetsToLL_LHEFilterPtZ-100To250_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM | 79527324 |
/DYJetsToLL_LHEFilterPtZ-250To400_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM | 24195330 |
/DYJetsToLL_LHEFilterPtZ-400To650_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM | 3936102 |
/DYJetsToLL_LHEFilterPtZ-650ToInf_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM | 3994997 |


/scratchnvme/malucchi/hbb_samples:
0       DYHT-100To200
0       DYHT-1200To2500
0       DYHT-200To400
0       DYHT-2500ToInf
0       DYHT-400To600
0       DYHT-600To800
0       DYHT-70To100
0       DYHT-800To1200
240G    DYM50
258G    DYZpt-0To50
139G    DYZpt-100To250
54G     DYZpt-250To400
9.3G    DYZpt-400To650
180G    DYZpt-50To100
9.8G    DYZpt-650ToInf
1.3T    EGamma_2018
10G     ggZH
805G    SingleMuon_2018
30G     ST_s-channel_4f_LD
151G    ST_t-channel_antitop_4f_ID
150G    ST_t-channel_antitop_5f_ID
281G    ST_t-channel_top_4f_ID
15G     ST_tW_antitop_5f_ID
21G     ST_tW_antitop_5f_NFHD
15G     ST_tW_top_5f_ID
22G     ST_tW_top_5f_NFHD
288G    TTTo2L2Nu
672G    TTToHadronic
961G    TTToSemiLeptonic
15G     WWTo2L2Nu
45G     WZTo2Q2L
14G     WZTo3LNu
9.1G    ZH
75G     ZZTo2L2Nu
46G     ZZTo2Q2L
131G    ZZTo4L
