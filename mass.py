import ROOT

ROOT.gInterpreter.ProcessLine('#include "utils.h"')


def mass(path, outpath):
    df = ROOT.RDataFrame("Events", path)

    df = (
        df.Define(
            "LHELepton_Mask", "abs(LHEPart_pdgId) < 19 && abs(LHEPart_pdgId) > 10"
        )
        .Define("LHELepton_pt", "LHEPart_pt[LHELepton_Mask]")
        .Define("LHELepton_eta", "LHEPart_eta[LHELepton_Mask]")
        .Define("LHELepton_phi", "LHEPart_phi[LHELepton_Mask]")
        .Define("LHELepton_mass", "LHEPart_mass[LHELepton_Mask]")
        .Define(
            "LHELepton_InvMass",
            "InvMass(LHELepton_pt, LHELepton_eta, LHELepton_phi, LHELepton_mass)",
        )
    )

    h_m = df.Histo1D(("m", "m", 100, 0, 200), "LHELepton_InvMass")

    # plot
    ROOT.gStyle.SetOptFit(0)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetTextFont(42)
    c = ROOT.TCanvas("c", "c", 800, 700)
    c.SetLeftMargin(0.15)

    h_m.SetTitle("")
    h_m.GetXaxis().SetTitle("m_{ll} [GeV]")
    h_m.GetXaxis().SetTitleSize(0.04)
    h_m.GetYaxis().SetTitle("Events / 2 GeV")
    h_m.GetYaxis().SetTitleSize(0.04)
    # h_m.GetYaxis().SetRangeUser(0.1, 1e7)
    h_m.SetFillColorAlpha(ROOT.kBlue - 3, 0.5)
    h_m.SetLineColor(ROOT.kBlue - 3)
    h_m.SetLineWidth(2)

    h_m.DrawClone("hist")

    cms_label = ROOT.TLatex()
    cms_label.SetTextSize(0.04)
    cms_label.DrawLatexNDC(0.2, 0.92, "#bf{CMS} #it{Private Work}")
    c.Update()
    c.SaveAs(f"mass_{outpath}")
