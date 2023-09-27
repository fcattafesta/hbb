from args_analysis import args

if args.oversampling:
    from nail.nail import *
else:
    from nail.nailOriginal import *


def getFlowLHEScale1(flow):
    flow.CentralWeight("LHEScaleWeight[1]")  # add a central weight

    return flow


def getFlowLHEScale7(flow):
    flow.CentralWeight("LHEScaleWeight[7]")  # add a central weight

    return flow
