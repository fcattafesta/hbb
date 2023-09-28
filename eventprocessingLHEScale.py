from args_analysis import args

from nail.nail import *


def getFlowLHEScale1(flow):
    flow.Define("LHEScaleWeight1", "LHEScaleWeight[1]")
    flow.CentralWeight("LHEScaleWeight1")  # add a central weight

    return flow


def getFlowLHEScale7(flow):
    flow.Define("LHEScaleWeight7", "LHEScaleWeight[7]")
    flow.CentralWeight("LHEScaleWeight7")  # add a central weight

    return flow
