#!/usr/bin/env python
# Dominic Smith <dosmith@cern.ch>

import ROOT
import sys
import math
from optparse import OptionParser

ROOT.gROOT.SetBatch(1)

parser = OptionParser()
parser.add_option('-i', '--inputPath', default='root://cms-xrd-global.cern.ch//store/mc/RunIIFall15MiniAODv2/SMS-T1tttt_mGluino-1500_mLSP-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v2/20000/A6A3AF86-9FC1-E511-918B-901B0E542962.root',action = 'store', type = 'string')
(options, args) = parser.parse_args(sys.argv)
inputPath = options.inputPath

##____________________________________________________________________________||
def main():

    printHeader()
    if getNEvents(inputPath):
        count(inputPath)

##____________________________________________________________________________||
def printHeader():
    print '%6s'  % 'run',
    print '%10s' % 'lumi',
    print '%9s'  % 'event',
    print '%10s' % 'jet.pt',
    print '%10s' % 'nSubJets',
    print '%10s' % 'subjetPts',
    print
    
##____________________________________________________________________________||
def count(inputPath):

    files = [inputPath]

    events = Events(files)

    handleJets = Handle("std::vector<pat::Jet>")

    for event in events:

        run = event.eventAuxiliary().run()
        lumi = event.eventAuxiliary().luminosityBlock()
        eventId = event.eventAuxiliary().event()

        event.getByLabel('slimmedJetsAK8', handleJets)
        jets = map(Jet, handleJets.product())

        for jet in jets:

            subjets = jet.subjets('SoftDrop')
            nSubjets = int(subjets.size())
            subjetPts = [sj.pt() for sj in subjets]
            print '%6d'    % run,
            print '%10d'   % lumi,
            print '%9d'    % eventId,            
            print '%10.3f' % jet.pt(),
            print '%10.3f' % nSubjets,
            print '{0}'.format(subjetPts)
            

##____________________________________________________________________________||
def getNEvents(inputPath):
    file = ROOT.TFile.Open(inputPath)
    events = file.Get('Events')
    return events.GetEntries()

##____________________________________________________________________________||
def loadLibraries():
    argv_org = list(sys.argv)
    sys.argv = [e for e in sys.argv if e != '-h']
    ROOT.gSystem.Load("libFWCoreFWLite")
    ROOT.AutoLibraryLoader.enable()
    ROOT.gSystem.Load("libDataFormatsFWLite")
    ROOT.gSystem.Load("libDataFormatsPatCandidates")
    sys.argv = argv_org

##____________________________________________________________________________||
loadLibraries()
from DataFormats.FWLite import Events, Handle
from PhysicsTools.Heppy.physicsobjects.PhysicsObjects import Jet

##____________________________________________________________________________||
if __name__ == '__main__':
    main()