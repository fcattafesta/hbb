main_dir='/gpfs/ddn/srm/cms/store/mc/RunIISummer20UL18NanoAODv9/'
suffix='_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v'
suffix2='_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v'
samples = {
    'DYM50' : {'folder': main_dir+'DYJetsToLL_M-50'+suffix+'2/', 'xsec':5765.4},
    'DYZpt-0To50': {'folder': main_dir+'DYJetsToLL_LHEFilterPtZ-0To50_MatchEWPDG20'+suffix+'1/', 'xsec': 1765.2},
    'DYZpt-50To100': {'folder': main_dir+'DYJetsToLL_LHEFilterPtZ-50To100_MatchEWPDG20'+suffix+'1/', 'xsec': 581.4},
    'DYZpt-100To250': {'folder': main_dir+'DYJetsToLL_LHEFilterPtZ-100To250_MatchEWPDG20'+suffix+'1/', 'xsec': 148.7},
    'DYZpt-250To400': {'folder': main_dir+'DYJetsToLL_LHEFilterPtZ-250To400_MatchEWPDG20'+suffix+'1/', 'xsec': 5.6},
    'DYZpt-400To650': {'folder': main_dir+'DYJetsToLL_LHEFilterPtZ-400To650_MatchEWPDG20'+suffix+'1/', 'xsec': 0.7},
    'DYZpt-650ToInf': {'folder': main_dir+'DYJetsToLL_LHEFilterPtZ-650ToInf_MatchEWPDG20'+suffix+'1/', 'xsec': 0.1},
    'DYHT-70To100': {'folder': main_dir+'DYJetsToLL_M-50_HT-70to100'+suffix+'1/', 'xsec': 345.7},
    'DYHT-100To200': {'folder': main_dir+'DYJetsToLL_M-50_HT-100to200'+suffix+'1/', 'xsec': 406.0},
    'DYHT-200To400': {'folder': main_dir+'DYJetsToLL_M-50_HT-200to400'+suffix+'1/', 'xsec': 84.7},
    'DYHT-400To600': {'folder': main_dir+'DYJetsToLL_M-50_HT-400to600'+suffix+'1/', 'xsec': 8.2},
    'DYHT-600To800': {'folder': main_dir+'DYJetsToLL_M-50_HT-600to800'+suffix+'1/', 'xsec': 1.7},
    'DYHT-800To1200': {'folder': main_dir+'DYJetsToLL_M-50_HT-800to1200'+suffix+'1/', 'xsec': 0.6},
    'DYHT-1200To2500': {'folder': main_dir+'DYJetsToLL_M-50_HT-1200to2500'+suffix+'1/', 'xsec': 0.1},
    'DYHT-2500ToInf': {'folder': main_dir+'DYJetsToLL_M-50_HT-2500toInf'+suffix+'1/', 'xsec': 0.0},
}

import os, glob
for sample in samples :
    if 'folder' in samples[sample].keys() :
        samples[sample]['files']= [x for x in glob.glob(samples[sample]['folder']+'/**/*.root', recursive=True)]
