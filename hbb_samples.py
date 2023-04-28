main_dir='/gpfs/ddn/srm/cms/store/mc/RunIISummer20UL18NanoAODv9/'
suffix='/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/'
samples = {
    'DYM50' : {'folder': main_dir+'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8'+suffix, 'xsec':5765.4},
    'DYZpt-0To50': {'folder': main_dir+'DYJetsToLL_LHEFilterPtZ-0To50_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8'+suffix, 'xsec': 5028.9},
    'DYZpt-50To100': {'folder': main_dir+'DYJetsToLL_LHEFilterPtZ-50To100_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8'+suffix, 'xsec': 581.4},
    'DYZpt-100To250': {'folder': main_dir+'DYJetsToLL_LHEFilterPtZ-100To250_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8'+suffix, 'xsec': 148.7},
    'DYZpt-250To400': {'folder': main_dir+'DYJetsToLL_LHEFilterPtZ-250To400_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8'+suffix, 'xsec': 5.6},
    'DYZpt-400To650': {'folder': main_dir+'DYJetsToLL_LHEFilterPtZ-400To650_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8'+suffix, 'xsec': 0.7},
    'DYZpt-650ToInf': {'folder': main_dir+'DYJetsToLL_LHEFilterPtZ-650ToInf_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8'+suffix, 'xsec': 0.1},
}