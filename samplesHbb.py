main_dir='/gpfs/ddn/srm/cms/store/mc/RunIISummer20UL18NanoAODv9/'
suffix='_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v'
suffix2='_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v'
suffix3='_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v'

flavourSplitting= {
          'bb' : "isBB",
        }



samples = {
    'DYM50' : {'folder': main_dir+'DYJetsToLL_M-50'+suffix+'2/', 'xsec':5765.40, 'subsamples': flavourSplitting },
    'DYZpt-0To50': {'folder': main_dir+'DYJetsToLL_LHEFilterPtZ-0To50_MatchEWPDG20'+suffix+'1/', 'xsec': 1341.42},
    'DYZpt-50To100': {'folder': main_dir+'DYJetsToLL_LHEFilterPtZ-50To100_MatchEWPDG20'+suffix+'1/', 'xsec': 359.52},
    'DYZpt-100To250': {'folder': main_dir+'DYJetsToLL_LHEFilterPtZ-100To250_MatchEWPDG20'+suffix+'1/', 'xsec': 88.36},
    'DYZpt-250To400': {'folder': main_dir+'DYJetsToLL_LHEFilterPtZ-250To400_MatchEWPDG20'+suffix+'1/', 'xsec': 3.52},
    'DYZpt-400To650': {'folder': main_dir+'DYJetsToLL_LHEFilterPtZ-400To650_MatchEWPDG20'+suffix+'1/', 'xsec': 0.49},
    'DYZpt-650ToInf': {'folder': main_dir+'DYJetsToLL_LHEFilterPtZ-650ToInf_MatchEWPDG20'+suffix+'1/', 'xsec': 0.05},
    # 'DYHT-70To100': {'folder': main_dir+'DYJetsToLL_M-50_HT-70to100'+suffix2+'1/', 'xsec': 345.7},
    # 'DYHT-100To200': {'folder': main_dir+'DYJetsToLL_M-50_HT-100to200'+suffix2+'1/', 'xsec': 406.0},
    # 'DYHT-200To400': {'folder': main_dir+'DYJetsToLL_M-50_HT-200to400'+suffix2+'1/', 'xsec': 84.7},
    # 'DYHT-400To600': {'folder': main_dir+'DYJetsToLL_M-50_HT-400to600'+suffix2+'1/', 'xsec': 8.2},
    # 'DYHT-600To800': {'folder': main_dir+'DYJetsToLL_M-50_HT-600to800'+suffix2+'1/', 'xsec': 1.7},
    # 'DYHT-800To1200': {'folder': main_dir+'DYJetsToLL_M-50_HT-800to1200'+suffix2+'1/', 'xsec': 0.6},
    # 'DYHT-1200To2500': {'folder': main_dir+'DYJetsToLL_M-50_HT-1200to2500'+suffix2+'1/', 'xsec': 0.1},
    # 'DYHT-2500ToInf': {'folder': main_dir+'DYJetsToLL_M-50_HT-2500toInf'+suffix2+'1/', 'xsec': 0.0},
    'ST_tW_antitop_5f_NoFullyHadronicDecays': {'folder': main_dir+'ST_tW_antitop_5f_NoFullyHadronicDecays'+suffix3+'1/', 'xsec': 0},
    #'S'
}

import os, glob
addSubSamples={}
for sample in samples :
    if 'subsamples' in samples[sample].keys() :
        for ss in samples[sample]['subsamples'] :
            addSubSamples["%s_%s"%(sample,ss)]={'xsec':samples[sample]['xsec']}
    if 'folder' in samples[sample].keys() :
        samples[sample]['files']= [x for x in glob.glob(samples[sample]['folder']+'/*.root')]
samples.update(addSubSamples)






'''
/gpfs/ddn/srm/cms/store/mc/RunIISummer20UL18NanoAODv9/DYJetsToLL_LHEFilterPtZ-0To50_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1
/gpfs/ddn/srm/cms/store/mc/RunIISummer20UL18NanoAODv9/DYJetsToLL_LHEFilterPtZ-50To100_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1
/gpfs/ddn/srm/cms/store/mc/RunIISummer20UL18NanoAODv9/DYJetsToLL_LHEFilterPtZ-100To250_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1
/gpfs/ddn/srm/cms/store/mc/RunIISummer20UL18NanoAODv9/DYJetsToLL_LHEFilterPtZ-250To400_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1
/gpfs/ddn/srm/cms/store/mc/RunIISummer20UL18NanoAODv9/DYJetsToLL_LHEFilterPtZ-400To650_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1
/gpfs/ddn/srm/cms/store/mc/RunIISummer20UL18NanoAODv9/DYJetsToLL_LHEFilterPtZ-650ToInf_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1

/gpfs/ddn/srm/cms/store/mc/RunIISummer20UL18NanoAODv9/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2
'''
