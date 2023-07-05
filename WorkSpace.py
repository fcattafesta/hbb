import ROOT
import os
import collections
import math
import copy
import re
import logging

from selections import selsMu, selsEle

logger = logging.getLogger(__name__)

##############################################################################################################
#########################  region[x] : keys are plot names, values are region names  #########################
##############################################################################################################
regionName = {x: x for x in selsMu + selsEle}


def writeSystematic(
    fname,
    region,
    varName,
    systematicDetail,
    all_histo_all_syst,
    availableSamples,
    datacard,
    year,
):
    f = ROOT.TFile(fname, "RECREATE")
    f.cd()

    for x in list(region.keys()):
        hname = ""
        for samp in availableSamples[x]:
            hname = varName[x] + "_" + region[x] + "_" + samp
            h = all_histo_all_syst[x][samp]["nom"].Clone(hname)
            h.Write()
        h_data_obs = all_histo_all_syst[x]["data" + year]["nom"].Clone(
            varName[x] + "_" + region[x] + "_data_obs"
        )
        h_data_obs.Write()

        systnameDict = {}
        for samp in availableSamples[x]:
            systnameDict[samp] = {}
            for sy in all_histo_all_syst[x][samp]:
                systnameDict[samp][sy] = sy

        hname = ""
        for samp in availableSamples[x]:
            for sy in all_histo_all_syst[x][samp]:
                hname = varName[x] + "_" + region[x] + "_" + samp
                hname = (
                    hname + "_" + systnameDict[samp][sy]
                )  # + ("Up" if sy.endswith("Up") else "Down")

                h = all_histo_all_syst[x][samp][sy].Clone(hname)
                h.Write()

    f.Close()

    for syst in systematicDetail:
        datacard.write(
            writeLine(syst, systematicDetail[syst], availableSamples, region)
        )


def writeLine(uncName, systematicDetailElement, allSamples, region):
    uncType = systematicDetailElement["type"]
    sampleWithSystematic = []
    if "decorrelate" in list(systematicDetailElement.keys()):
        for sl in list(systematicDetailElement["decorrelate"].values()):
            sampleWithSystematic += sl
    else:
        for sl in list(allSamples.values()):
            sampleWithSystematic += sl
        sampleWithSystematic = list(set(sampleWithSystematic))
    value = (
        1.0
        if "value" not in list(systematicDetailElement.keys())
        else systematicDetailElement["value"]
    )

    # print("uncName  ", uncName)
    # print("uncType  ", uncType)
    # print("value  ", value)
    # print("allSamples  ", allSamples)
    # print("sampleWithSystematic  ", sampleWithSystematic)

    line = ""
    position = []
    orderedUncertainties = []

    n = 0
    for x in list(allSamples.keys()):
        notThisRegion = [y for y in list(allSamples.keys()) if y != x]
        # print("notThisRegion  ", notThisRegion)
        for sl in allSamples[x]:
            # print("sl  ", sl)
            orderedUncertainties.append(0)
            for s in sampleWithSystematic:
                # print("s  ", s)
                # if re.search(s + "_", sl):
                # if re.search(s, sl):
                if re.search("^" + s + ".*", sl):
                    # print("ok1")

                    if all(
                        not re.search(regionName[region[y]] + "$", uncName)
                        for y in notThisRegion
                    ):
                        # print("ok2")
                        position.append(n)
                        if "valueFromPlots" in list(systematicDetailElement.keys()):
                            orderedUncertainties[-1] = str(
                                systematicDetailElement["valueFromPlots"][s]
                            )[:7]
                            # print("ok3")
                        else:
                            orderedUncertainties[-1] = value
            n += 1

    # print("position", position)
    if len(position) == 0:
        return ""

    line += uncName + "\t" * (4 - len(uncName) // 8)
    line += uncType + "\t" * (3 - len(uncType) // 8)
    line += writeUncertainities(
        orderedUncertainties, len(orderedUncertainties), position
    )

    return line + "\n"


def writeUncertainities(orderedUncertainties, lenght, position):
    uncLine = ""
    for n in range(lenght):
        if n in position:
            uncLine += str(orderedUncertainties[n])
        else:
            uncLine += "-"
        uncLine += "\t\t\t"

    return uncLine


def printSystematicGrouping(systematicDetail, outputFile="/groupingCheck.py"):
    outputName = open(outputFile, "w")
    print("{", file=outputName)

    for syst in systematicDetail:
        print('"' + syst + '" : {', file=outputName)
        for k in systematicDetail[syst]:
            print('\t"' + k + '" : ', systematicDetail[syst][k], ",", file=outputName)
        print("}", file=outputName)

    print("}", file=outputName)


def createNewSystematicForMergeWithOption(systematicDetail):
    systKeys = list(systematicDetail.keys())
    for syst in systKeys:
        if "additionalNormalizations" in list(systematicDetail[syst].keys()):
            systematicDetail[syst]["type"] = "lnN"
            systematicToAdd = systematicDetail[syst]["additionalNormalizations"]
            for n in range(len(systematicToAdd)):
                s = systematicToAdd[n]
                systematicDetail[syst + "__" + s] = copy.deepcopy(
                    systematicDetail[syst]
                )
                systematicDetail[syst + "__" + s].pop("additionalNormalizations", None)
                systematicDetail[syst + "__" + s].pop("groupValues", None)
                systematicDetail[syst + "__" + s]["type"] = "normalizationOnly"
                systematicDetail[syst]["additionalNormalizations"][n] = syst + "__" + s
        if "groupValues" in list(systematicDetail[syst].keys()):
            systematicDetail[syst]["type"] = "lnN"
            systematicToAdd = systematicDetail[syst]["groupValues"]
            for g in list(systematicToAdd.keys()):
                v = systematicToAdd[g]
                systematicDetail[syst + "__Norm" + g] = copy.deepcopy(
                    systematicDetail[syst]
                )
                systematicDetail[syst + "__Norm" + g]["value"] = systematicToAdd[g]
                systematicDetail[syst + "__Norm" + g].pop("decorrelate", None)
                systematicDetail[syst + "__Norm" + g]["decorrelate"] = {
                    g: systematicDetail[syst]["decorrelate"][g]
                }
                systematicDetail[syst + "__Norm" + g].pop(
                    "additionalNormalizations", None
                )
                systematicDetail[syst + "__Norm" + g].pop("groupValues", None)
                systematicDetail[syst + "__Norm" + g]["type"] = "lnN"
            systematicDetail[syst]["additionalNormalizations"] = systematicDetail[syst][
                "additionalNormalizations"
            ] + [syst + "__Norm"]


def divideShapeAndNormalization(systematicDetail):
    systKeys = list(systematicDetail.keys())
    for syst in systKeys:
        if "shapeAndNorm" == systematicDetail[syst]["type"]:
            systematicDetail[syst + "Shape"] = copy.deepcopy(systematicDetail[syst])
            systematicDetail[syst + "Shape"]["type"] = "shapeOnly"
            systematicDetail[syst]["type"] = "normalizationOnly"


def decorrelateNormOnly(systematicDetail, availableSamples):
    systKeys = list(systematicDetail.keys())
    for syst in systKeys:
        if "normalizationOnly" in list(
            systematicDetail[syst].keys()
        ) and "decorrelate" not in list(systematicDetail[syst].keys()):
            systematicDetail[syst]["decorrelate"] = {}
            for x in availableSamples:
                systematicDetail[syst]["decorrelate"][x] = x


def modifySystematicDetail(systematicDetail, listAllSample_noYear, all_histo_all_syst):
    systKeys = list(systematicDetail.keys())
    for syst in systKeys:
        if "decorrelate" not in list(systematicDetail[syst].keys()):
            systematicDetail[syst]["decorrelate"] = {"all": listAllSample_noYear}
        # print('systematicDetail[syst]["decorrelate"] 0', systematicDetail[syst]["decorrelate"])

        prima = [
            len(systematicDetail[syst]["decorrelate"][g])
            for g in systematicDetail[syst]["decorrelate"]
        ]
        # print("prima", prima)
        for g in list(systematicDetail[syst]["decorrelate"].keys()):
            systematicDetail[syst]["decorrelate"][g] = [
                s
                for s in systematicDetail[syst]["decorrelate"][g]
                if s in listAllSample_noYear
            ]
        # print("systematicDetail[syst][decorrelate] 1", systematicDetail[syst]["decorrelate"])

        keys = list(systematicDetail[syst]["decorrelate"].keys())
        for g in keys:
            if len(systematicDetail[syst]["decorrelate"][g]) == 0:
                systematicDetail[syst]["decorrelate"].pop(g, None)
                # print("g ", g, " systematicDetail[syst][decorrelate] 2", systematicDetail[syst]["decorrelate"])

        if len(systematicDetail[syst]["decorrelate"]) == 0:
            systematicDetail.pop(syst, None)
        elif len(list(systematicDetail[syst]["decorrelate"].keys())) > 1:
            for g in systematicDetail[syst]["decorrelate"]:
                systematicDetail[syst + g] = copy.deepcopy(systematicDetail[syst])
                # print("here0\n\n")
                if (
                    systematicDetail[syst]["type"] != "lnN"
                    and systematicDetail[syst]["type"] != "normalizationOnly"
                ):
                    for x in list(all_histo_all_syst.keys()):
                        for sampName in systematicDetail[syst]["decorrelate"][g]:
                            # print("here1\n\n")
                            for samp in list(all_histo_all_syst[x].keys()):
                                # print("sampName ", sampName, " samp ", samp)
                                if re.search(sampName, samp):
                                    # print("here2\n\n")
                                    if set([syst + "Up", syst + "Down"]).issubset(
                                        set(all_histo_all_syst[x][samp].keys())
                                    ):
                                        # print "--AA--AA--AA--AA ",g, " \t ",samp, " \t ",sampName, " \t ", all_histo_all_syst[x].keys()#, " \t ",
                                        all_histo_all_syst[x][samp][
                                            syst + g + "Up"
                                        ] = copy.deepcopy(
                                            all_histo_all_syst[x][samp][syst + "Up"]
                                        )
                                        all_histo_all_syst[x][samp][
                                            syst + g + "Down"
                                        ] = copy.deepcopy(
                                            all_histo_all_syst[x][samp][syst + "Down"]
                                        )
                                        # all_histo_all_syst[x][samp].pop(syst+"Up", None)
                                        # all_histo_all_syst[x][samp].pop(syst+"Down", None)

                            # all_histo_all_syst[x][""]
                # print("systematicDetail[syst + g] 0 ", systematicDetail[syst + g])
                systematicDetail[syst + g].pop("decorrelate", None)
                # print("systematicDetail[syst + g] 1 ", systematicDetail[syst + g])
                systematicDetail[syst + g]["decorrelate"] = {
                    g: systematicDetail[syst]["decorrelate"][g]
                }
                # print("systematicDetail[syst + g] 2 ", systematicDetail[syst + g])
            # print("systematicDetail[syst] 0 ", systematicDetail[syst])
            systematicDetail.pop(syst, None)


def removeUnusedSystematics(systematicDetail, all_histo_all_syst):
    systKeys = list(systematicDetail.keys())
    for syst in systKeys:
        if re.search("shape", systematicDetail[syst]["type"]) or re.search(
            "normalizationOnly", systematicDetail[syst]["type"]
        ):
            x = list(all_histo_all_syst.keys())[0]
            samp = list(all_histo_all_syst[x].keys())[0]
            # print "removeUnusedSystematics  ", syst, " \t ",all_histo_all_syst[x][samp].keys()

            sample = list(systematicDetail[syst]["decorrelate"].keys())[0]
            sysNoVarname = re.sub("Shape", "", re.sub(sample, "", syst))

            # if all( not re.search(sysNoVarname, s) for s in all_histo_all_syst[x][samp].keys() ) :
            if all(
                not re.search(re.sub("Up", "", re.sub("Down", "", s)), syst)
                for s in list(all_histo_all_syst[x][samp].keys())
            ):
                systematicDetail.pop(syst, None)
                print("removed ", syst)


def ScaleShapeOnlyPlot(systematicDetail, all_histo_all_syst):
    systKeys = list(systematicDetail.keys())
    for syst in systKeys:
        if systematicDetail[syst]["type"] == "shapeOnly":
            systematicDetail[syst]["type"] = "shape"
            for x in list(all_histo_all_syst.keys()):
                for samp in all_histo_all_syst[x]:
                    for s in list(all_histo_all_syst[x][samp].keys()):
                        if re.search(re.sub("Up", "", re.sub("Down", "", s)), syst):
                            if all_histo_all_syst[x][samp][s].Integral() > 0:
                                all_histo_all_syst[x][samp][s].Scale(
                                    all_histo_all_syst[x][samp]["nom"].Integral()
                                    / all_histo_all_syst[x][samp][s].Integral()
                                )


def valuesFromPlots(systematicDetail, all_histo_all_syst, region):
    for syst in list(systematicDetail.keys()):
        if systematicDetail[syst]["type"] == "normalizationOnly":
            systematicDetail[syst]["type"] = "lnN"
            systematicDetail[syst]["valueFromPlots"] = {}

            for x in list(all_histo_all_syst.keys()):
                systematicDetail[syst + "_" + regionName[region[x]]] = copy.deepcopy(
                    systematicDetail[syst]
                )

                for sKey in systematicDetail[syst]["decorrelate"]:
                    for s in systematicDetail[syst]["decorrelate"][sKey]:
                        value = 0.0
                        for samp in all_histo_all_syst[x]:
                            if re.search(s + "_", samp):
                                systName = syst[: -len(sKey)]
                                # print "CCCCC", samp, "  \t ",  systName, "  \t ",s
                                if re.search("__", syst):
                                    systName = re.match("^.*__(.*)$", syst).group(1)[
                                        : -len(sKey)
                                    ]
                                Nbins = (
                                    all_histo_all_syst[x][samp]["nom"].GetNbinsX() + 1
                                )
                                variationUp = (
                                    1.0
                                    if all_histo_all_syst[x][samp]["nom"].Integral(
                                        0, Nbins
                                    )
                                    <= 0
                                    else all_histo_all_syst[x][samp][
                                        systName + "Up"
                                    ].Integral(0, Nbins)
                                    / all_histo_all_syst[x][samp]["nom"].Integral(
                                        0, Nbins
                                    )
                                )
                                variationDown = (
                                    1.0
                                    if all_histo_all_syst[x][samp][
                                        systName + "Down"
                                    ].Integral(0, Nbins)
                                    <= 0
                                    else all_histo_all_syst[x][samp]["nom"].Integral(
                                        0, Nbins
                                    )
                                    / all_histo_all_syst[x][samp][
                                        systName + "Down"
                                    ].Integral(0, Nbins)
                                )
                                value = (variationUp + variationDown) / 2.0

                        systematicDetail[syst + "_" + regionName[region[x]]][
                            "valueFromPlots"
                        ][s] = value

            systematicDetail.pop(syst, None)


def SumErrors(v1, v2):
    print("valori", v1, v2)
    return math.exp(((math.log(v1)) ** 2.0 + (math.log(v2)) ** 2.0) ** 0.5)


def mergeTwoSystematics(systematicDetail, syst1, syst2, listAllSample_noYear):
    samples1 = list(systematicDetail[syst1]["decorrelate"].values())[
        0
    ]  # "decorrelate" has just one key
    samples2 = list(systematicDetail[syst2]["decorrelate"].values())[0]
    # newDecorrelate = list(set(samples1+samples2))

    if "valueFromPlots" not in list(systematicDetail[syst2].keys()):
        systematicDetail[syst2]["valueFromPlots"] = {}
        for s in samples2:
            systematicDetail[syst2]["valueFromPlots"][s] = (
                1.0
                if "value" not in list(systematicDetail[syst2].keys())
                else systematicDetail[syst2]["value"]
            )
    if "valueFromPlots" not in list(systematicDetail[syst1].keys()):
        systematicDetail[syst1]["valueFromPlots"] = {}
        for s in samples1:
            systematicDetail[syst1]["valueFromPlots"][s] = (
                1.0
                if "value" not in list(systematicDetail[syst1].keys())
                else systematicDetail[syst1]["value"]
            )

    print(syst1, "    \t ", systematicDetail[syst1]["decorrelate"])
    print("valueFromPlots \t ", systematicDetail[syst1]["valueFromPlots"])
    print(syst2, "    \t ", systematicDetail[syst2]["decorrelate"])
    print("valueFromPlots \t ", systematicDetail[syst2]["valueFromPlots"])

    newValues = {}
    for s in samples1:
        print(
            "check   ",
            s,
            1 if s not in samples1 else systematicDetail[syst1]["valueFromPlots"][s],
            1 if s not in samples2 else systematicDetail[syst2]["valueFromPlots"][s],
        )
        newValues[s] = SumErrors(
            1 if s not in samples1 else systematicDetail[syst1]["valueFromPlots"][s],
            1 if s not in samples2 else systematicDetail[syst2]["valueFromPlots"][s],
        )
    # systematicDetail[syst1]["decorrelate"]       = {"merged" : samples1}
    systematicDetail[syst1]["valueFromPlots"] = newValues

    print("merging ", syst1, " \t ", syst2)
    # systematicDetail.pop(syst2, None)


def mergeToSys(systematicDetail, listAllSample_noYear):
    systKeys = list(systematicDetail.keys())
    mergedSystematic = (
        []
    )  # the pop() cannot be done on the fly because several systematics can have identical "mergeToSys"
    for syst in systKeys:
        if "additionalNormalizations" in list(systematicDetail[syst].keys()):
            sysTomergeList = systematicDetail[syst]["additionalNormalizations"]
            for s in sysTomergeList:
                for sysTomerge in systKeys:
                    if re.search(
                        s + list(systematicDetail[syst]["decorrelate"].keys())[0],
                        sysTomerge,
                    ):
                        # if sysTomerge in systKeys :
                        if (
                            systematicDetail[syst]["type"] == "lnN"
                            and systematicDetail[sysTomerge]["type"] == "lnN"
                        ):
                            mergedSystematic.append(sysTomerge)
                            mergeTwoSystematics(
                                systematicDetail, syst, sysTomerge, listAllSample_noYear
                            )

    for s in set(mergedSystematic):
        systematicDetail.pop(s, None)


def modifyRegionName(region):
    k = list(regionName.keys())
    for r in k:
        fitOneRegion2Times = False
        count = 0
        for x in region:
            logger.info("AAAA %s %s %s" % (r, x, re.search(r + "$", x)))
            if re.search(r + "$", x):
                count += 1
        if count > 1:
            fitOneRegion2Times = True
        count = 0
        for x in region:
            if re.search(r + "$", x):
                count += 1
                if fitOneRegion2Times:
                    regionName[x] = regionName[r] + str(count)
                else:
                    regionName[x] = regionName[r]


def createWorkSpace(model, all_histo_all_syst, year, outdir="workspace/"):
    logger.info("WorkSpace creation")
    nBins = {}
    varName = {}
    plotName = (
        {}
    )  # it will be equal to varName because of how plot.py write all_histo_all_syst
    region = {}

    logger.info(list(all_histo_all_syst.keys()))
    for x in list(all_histo_all_syst.keys()):
        nBins[x] = all_histo_all_syst[x]["data" + year]["nom"].GetNbinsX() - 1
        varName[x] = (
            all_histo_all_syst[x]["data" + year]["nom"].GetName().split("___")[0]
        )
        plotName[x] = x
        region[x] = x.split("___")[1]  # keys are plot names, values are region names

    modifyRegionName(region)

    region = collections.OrderedDict(sorted(region.items()))

    os.system("mkdir -p " + outdir)
    datacard = open(outdir + "/datacard" + year + model.name + ".txt", "w")

    datacard.write(
        "imax " + str(len(list(all_histo_all_syst.keys()))) + "  number of channels\n"
    )
    datacard.write("jmax *  number of backgrounds\n")
    datacard.write(
        "kmax *  number of nuisance parameters (sources of systematical uncertainties)\n"
    )
    datacard.write("------------\n")
    for x in region:
        datacard.write(
            "shapes * "
            + region[x]
            + "  fileCombine"
            + year
            + model.name
            + ".root "
            + varName[x]
            + "_$CHANNEL_$PROCESS "
            + varName[x]
            + "_$CHANNEL_$PROCESS_$SYSTEMATIC\n"
        )
    datacard.write("------------\n")
    datacard.write("bin \t\t")
    for x in region:
        datacard.write(region[x] + " \t")
    datacard.write("\nobservation \t")
    for x in region:
        datacard.write(
            str(all_histo_all_syst[x]["data" + year]["nom"].Integral(1, nBins[x] + 1))
            + " \t\t"
        )
    datacard.write("\n------------\n")

    listSig = []
    listBkg = []
    for s in model.signal:
        listSig = listSig + model.signal[s]
    for s in model.background:
        listBkg = listBkg + model.background[s]

    listAllSample = listSig + listBkg
    availableSamples = {}
    processNumber = {}
    for n in range(len(listSig)):
        processNumber[listSig[n]] = -n
    for n in range(len(listBkg)):
        processNumber[listBkg[n]] = n + 1
    # if listBkg[n].startswith("EWK") : processNumber[listBkg[n]] = -n
    # else : processNumber[listBkg[n]] = n+1

    # remove samples with no predicted events
    emptySamples = {}
    for x in region:
        emptySamples[x] = []
        for s in listAllSample:
            if not all(
                all_histo_all_syst[x][s][sy].Integral(1, nBins[x] + 1) > 0.0
                for sy in list(all_histo_all_syst[x][s].keys())
            ):
                print(
                    "WARNING",
                    s,
                    " IS EMPTY",
                    [
                        (sy, all_histo_all_syst[x][s][sy].Integral(1, nBins[x] + 1))
                        for sy in list(all_histo_all_syst[x][s].keys())
                    ],
                )
                emptySamples[x].append(s)
        availableSamples[x] = [s for s in listAllSample if s not in emptySamples[x]]

    listAllSample_noYear = [s.split("_")[0] if "201" in s else s for s in listAllSample]
    # print("listAllSample_noYear", listAllSample_noYear)
    # print("listAllSample", listAllSample)
    availableSamples = collections.OrderedDict(sorted(availableSamples.items()))

    datacard.write("bin \t \t \t \t \t")
    for x in region:
        for s in availableSamples[x]:
            datacard.write(region[x] + " \t\t")

    datacard.write("\nprocess \t \t \t \t")
    for x in region:
        for s in availableSamples[x]:
            datacard.write(s + "\t" + ("" if len(s) > 15 else "\t"))

    datacard.write("\nprocess \t \t \t \t")
    for x in region:
        for s in availableSamples[x]:
            datacard.write(str(processNumber[s]) + "\t\t\t")

    datacard.write("\nrate \t \t \t \t \t")
    for x in region:
        for s in availableSamples[x]:
            datacard.write(
                str(all_histo_all_syst[x][s]["nom"].Integral(1, nBins[x] + 1)) + "\t\t"
            )
    datacard.write("\n------------\n")

    logger.info("region %s" % region)
    logger.info("varName %s" % varName)
    logger.info("availableSamples %s" % availableSamples)
    logger.info("\n ---------------------------- \n")

    # print("model.systematicDetail 0", model.systematicDetail)
    printSystematicGrouping(model.systematicDetail, outdir + "/grouping0.py")

    createNewSystematicForMergeWithOption(model.systematicDetail)
    printSystematicGrouping(model.systematicDetail, outdir + "/grouping1.py")
    # print("model.systematicDetail 1", model.systematicDetail)

    divideShapeAndNormalization(model.systematicDetail)
    printSystematicGrouping(model.systematicDetail, outdir + "/grouping2.py")
    # decorrelateNormOnly (model.systematicDetail, availableSamples)
    # print("model.systematicDetail 2", model.systematicDetail)

    modifySystematicDetail(
        model.systematicDetail, listAllSample_noYear, all_histo_all_syst
    )
    printSystematicGrouping(model.systematicDetail, outdir + "/grouping3.py")
    # print("model.systematicDetail 3", model.systematicDetail)

    removeUnusedSystematics(model.systematicDetail, all_histo_all_syst)
    printSystematicGrouping(model.systematicDetail, outdir + "/grouping4.py")
    # print("model.systematicDetail 4", model.systematicDetail)

    valuesFromPlots(model.systematicDetail, all_histo_all_syst, region)
    printSystematicGrouping(model.systematicDetail, outdir + "/grouping5.py")
    # print("model.systematicDetail 5", model.systematicDetail)

    ScaleShapeOnlyPlot(model.systematicDetail, all_histo_all_syst)
    printSystematicGrouping(model.systematicDetail, outdir + "/grouping6.py")
    # print("model.systematicDetail 6", model.systematicDetail)

    mergeToSys(model.systematicDetail, listAllSample_noYear)
    logger.info("model.systematicDetail 7 %s" % model.systematicDetail)
    printSystematicGrouping(model.systematicDetail, outdir + "/grouping7.py")

    writeSystematic(
        outdir + "/fileCombine" + year + model.name + ".root",
        region,
        varName,
        model.systematicDetail,
        all_histo_all_syst,
        availableSamples,
        datacard,
        year,
    )

    for x in list(region.keys()):
        datacard.write(region[x] + " autoMCStats 0 1\n\n")

    logger.info("WorkSpace end")
