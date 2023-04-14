import ROOT

ROOT.gInterpreter.ProcessLine('#include "utils.h"')


def lhe_zpt(df, zpt):
    df = df.Filter(f"LHE_Vpt > {zpt}")
    return df


def mass(df, outpath):
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


def zpt(path, zpt, outpath):
    df = ROOT.RDataFrame("Events", path)

    df = mass(df, outpath)

    h_pre = df.Histo1D(("pre", "pre", 100, 0, 1000), "LHE_Vpt")

    df = lhe_zpt(df, zpt)

    h_post = df.Histo1D(("post", "post", 100, 0, 1000), "LHE_Vpt")

    # plot
    ROOT.gStyle.SetOptFit(0)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetTextFont(42)
    c = ROOT.TCanvas("c", "c", 800, 700)
    c.SetLeftMargin(0.15)
    # c.SetLogy()

    h_pre.SetTitle("")
    h_pre.GetXaxis().SetTitle("LHE_Vpt [GeV]")
    h_pre.GetXaxis().SetTitleSize(0.04)
    h_pre.GetYaxis().SetTitle("Events / 10 GeV")
    h_pre.GetYaxis().SetTitleSize(0.04)
    # h_pre.GetYaxis().SetRangeUser(0.1, 1e7)
    h_pre.SetFillColorAlpha(ROOT.kBlue - 3, 0.5)
    h_pre.SetLineColor(ROOT.kBlue - 3)
    h_pre.SetLineWidth(2)

    h_post.SetFillColorAlpha(ROOT.kOrange + 7, 0.2)
    h_post.SetLineColor(ROOT.kOrange + 7)
    h_post.SetLineWidth(2)

    h_pre.DrawClone("hist")
    h_post.DrawClone("hist same")

    legend = ROOT.TLegend(0.72, 0.75, 0.89, 0.88)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.02)
    legend.AddEntry("pre", "precut", "f")
    legend.AddEntry("post", "postcut", "f")
    legend.DrawClone("NDC NB")

    cms_label = ROOT.TLatex()
    cms_label.SetTextSize(0.04)
    cms_label.DrawLatexNDC(0.2, 0.92, "#bf{CMS} #it{Private Work}")
    c.Update()
    c.SaveAs(outpath)
