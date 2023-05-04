
#include <Math/VectorUtil.h>
#include <ROOT/RVec.hxx>
#include "Math/Vector4D.h"
#include <ROOT/RDataFrame.hxx>
#include "helpers.h"
#define MemberMap(vector,member) Map(vector,[](auto x){return x.member;})
#define P4DELTAR ROOT::Math::VectorUtil::DeltaR<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float>>,ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float>>> 
//ROOT::Math::PtEtaPhiMVector,ROOT::Math::PtEtaPhiMVector> 
#include <vector>
#include <map>
#include <utility>
using namespace std;
#ifndef NAILSTUFF
#define NAILSTUFF
using RNode = ROOT::RDF::RNode;
struct Result {
 Result() {}
// Result(RNode  rdf_) {rdf[""]=rdf_;}
 std::map<std::string,RNode> rdf;
 ROOT::RDF::RResultPtr<TH1D> histo;
 std::vector<ROOT::RDF::RResultPtr<TH1D>> histos;
 std::map<std::string,std::vector<ROOT::RDF::RResultPtr<TH1D> > > histosOutSplit;
};
template <typename T>
class NodeCaster {
   public:
    static ROOT::RDF::RNode Cast(T rdf)
    {
              return ROOT::RDF::RNode(rdf);
    }
};
#endif
bool func__isBB(unsigned int __slot ) {  return true; }
float func__LHE_Zpt(unsigned int __slot , const Float_t & LHE_Vpt) {  return LHE_Vpt; }
ROOT::VecOps::RVec<float> func__Muon_iso(unsigned int __slot , const ROOT::VecOps::RVec<Float_t> & Muon_pfRelIso04_all) {  return (Muon_pfRelIso04_all); }
ROOT::VecOps::RVec<int> func__SelectedMuon(unsigned int __slot , const ROOT::VecOps::RVec<Float_t> & Muon_pt, const ROOT::VecOps::RVec<Bool_t> & Muon_mediumId, const ROOT::VecOps::RVec<Float_t> & Muon_eta, const ROOT::VecOps::RVec<float> & Muon_iso) {  return Muon_iso < 0.25 && Muon_mediumId && Muon_pt > 20. && abs(Muon_eta) < 2.4; }
ROOT::VecOps::RVec<float> func__SelectedMuon_eta(unsigned int __slot , const ROOT::VecOps::RVec<int> & SelectedMuon, const ROOT::VecOps::RVec<Float_t> & Muon_eta) {  return At(Muon_eta,SelectedMuon); }
ROOT::VecOps::RVec<float> func__SelectedMuon_mass(unsigned int __slot , const ROOT::VecOps::RVec<int> & SelectedMuon, const ROOT::VecOps::RVec<Float_t> & Muon_mass) {  return At(Muon_mass,SelectedMuon); }
ROOT::VecOps::RVec<float> func__SelectedMuon_phi(unsigned int __slot , const ROOT::VecOps::RVec<int> & SelectedMuon, const ROOT::VecOps::RVec<Float_t> & Muon_phi) {  return At(Muon_phi,SelectedMuon); }
ROOT::VecOps::RVec<float> func__SelectedMuon_pt(unsigned int __slot , const ROOT::VecOps::RVec<int> & SelectedMuon, const ROOT::VecOps::RVec<Float_t> & Muon_pt) {  return At(Muon_pt,SelectedMuon); }
ROOT::VecOps::RVec<int> func__SelectedMuon_charge(unsigned int __slot , const ROOT::VecOps::RVec<Int_t> & Muon_charge, const ROOT::VecOps::RVec<int> & SelectedMuon) {  return At(Muon_charge,SelectedMuon); }
int func__nSelectedMuon(unsigned int __slot , const ROOT::VecOps::RVec<int> & SelectedMuon) {  return Sum(SelectedMuon); }
bool func__twoMuons(unsigned int __slot , const int & nSelectedMuon) {  return nSelectedMuon==2; }
ROOT::VecOps::RVec<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > > func__SelectedMuon_p4(unsigned int __slot , const ROOT::VecOps::RVec<float> & SelectedMuon_mass, const ROOT::VecOps::RVec<float> & SelectedMuon_pt, const ROOT::VecOps::RVec<float> & SelectedMuon_phi, const ROOT::VecOps::RVec<float> & SelectedMuon_eta) {  return vector_map_t<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> >	>(SelectedMuon_pt , SelectedMuon_eta, SelectedMuon_phi, SelectedMuon_mass); }
ROOT::VecOps::RVec<ROOT::VecOps::RVec<unsigned long> > func__MuMu_allpairs(unsigned int __slot , const ROOT::VecOps::RVec<int> & SelectedMuon) {  return Combinations(Nonzero(SelectedMuon),Nonzero(SelectedMuon)); }
ROOT::VecOps::RVec<int> func__MuMu(unsigned int __slot , const ROOT::VecOps::RVec<ROOT::VecOps::RVec<unsigned long> > & MuMu_allpairs) {  return At(MuMu_allpairs,0) < At(MuMu_allpairs,1); }
ROOT::VecOps::RVec<unsigned long> func__MuMu0(unsigned int __slot , const ROOT::VecOps::RVec<ROOT::VecOps::RVec<unsigned long> > & MuMu_allpairs, const ROOT::VecOps::RVec<int> & MuMu) {  return At(At(MuMu_allpairs,0),MuMu); }
ROOT::VecOps::RVec<unsigned long> func__MuMu1(unsigned int __slot , const ROOT::VecOps::RVec<ROOT::VecOps::RVec<unsigned long> > & MuMu_allpairs, const ROOT::VecOps::RVec<int> & MuMu) {  return At(At(MuMu_allpairs,1),MuMu); }
ROOT::VecOps::RVec<int> func__MuMu0_charge(unsigned int __slot , const ROOT::VecOps::RVec<int> & SelectedMuon_charge, const ROOT::VecOps::RVec<unsigned long> & MuMu0) {  return Take(SelectedMuon_charge,MuMu0); }
ROOT::VecOps::RVec<int> func__MuMu1_charge(unsigned int __slot , const ROOT::VecOps::RVec<int> & SelectedMuon_charge, const ROOT::VecOps::RVec<unsigned long> & MuMu1) {  return Take(SelectedMuon_charge,MuMu1); }
ROOT::VecOps::RVec<unsigned long> func__OppositeSignMuMu(unsigned int __slot , const ROOT::VecOps::RVec<int> & MuMu1_charge, const ROOT::VecOps::RVec<int> & MuMu0_charge) {  return Nonzero(MuMu0_charge != MuMu1_charge); }
bool func__twoOppositeSignMuons(unsigned int __slot , const ROOT::VecOps::RVec<unsigned long> & OppositeSignMuMu) {  return OppositeSignMuMu.size() > 0; }
unsigned long func__Mu_index(unsigned int __slot , const ROOT::VecOps::RVec<unsigned long> & OppositeSignMuMu) {  return At(OppositeSignMuMu,0,-200); }
int func__Mu0(unsigned int __slot , const unsigned long & Mu_index, const ROOT::VecOps::RVec<unsigned long> & MuMu0) {  return int(At(MuMu0,Mu_index)); }
ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > func__Mu0_p4(unsigned int __slot , const int & Mu0, const ROOT::VecOps::RVec<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > > & SelectedMuon_p4) {  return At(SelectedMuon_p4,Mu0); }
int func__Mu1(unsigned int __slot , const ROOT::VecOps::RVec<unsigned long> & MuMu1, const unsigned long & Mu_index) {  return int(At(MuMu1,Mu_index)); }
ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > func__Mu1_p4(unsigned int __slot , const int & Mu1, const ROOT::VecOps::RVec<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > > & SelectedMuon_p4) {  return At(SelectedMuon_p4,Mu1); }
ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > func__Z(unsigned int __slot , const ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > & Mu0_p4, const ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > & Mu1_p4) {  return Mu0_p4+Mu1_p4; }
float func__Reco_Zpt(unsigned int __slot , const ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > & Z) {  return Z.Pt(); }
float func__Reco_ZMass(unsigned int __slot , const ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > & Z) {  return Z.M(); }
ROOT::VecOps::RVec<int> func__GenMuon(unsigned int __slot , const ROOT::VecOps::RVec<Float_t> & GenPart_pt, const ROOT::VecOps::RVec<Int_t> & GenPart_pdgId, const ROOT::VecOps::RVec<Int_t> & GenPart_status, const ROOT::VecOps::RVec<Float_t> & GenPart_eta) {  return abs(GenPart_pdgId) == 13 && GenPart_status == 1 && GenPart_pt > 20. && abs(GenPart_eta) < 2.4; }
ROOT::VecOps::RVec<float> func__GenMuon_eta(unsigned int __slot , const ROOT::VecOps::RVec<Float_t> & GenPart_eta, const ROOT::VecOps::RVec<int> & GenMuon) {  return At(GenPart_eta,GenMuon); }
ROOT::VecOps::RVec<float> func__GenMuon_mass(unsigned int __slot , const ROOT::VecOps::RVec<int> & GenMuon, const ROOT::VecOps::RVec<Float_t> & GenPart_mass) {  return At(GenPart_mass,GenMuon); }
ROOT::VecOps::RVec<float> func__GenMuon_phi(unsigned int __slot , const ROOT::VecOps::RVec<int> & GenMuon, const ROOT::VecOps::RVec<Float_t> & GenPart_phi) {  return At(GenPart_phi,GenMuon); }
ROOT::VecOps::RVec<float> func__GenMuon_pt(unsigned int __slot , const ROOT::VecOps::RVec<Float_t> & GenPart_pt, const ROOT::VecOps::RVec<int> & GenMuon) {  return At(GenPart_pt,GenMuon); }
ROOT::VecOps::RVec<int> func__GenMuon_pdgId(unsigned int __slot , const ROOT::VecOps::RVec<Int_t> & GenPart_pdgId, const ROOT::VecOps::RVec<int> & GenMuon) {  return At(GenPart_pdgId,GenMuon); }
int func__nGenMuon(unsigned int __slot , const ROOT::VecOps::RVec<int> & GenMuon) {  return Sum(GenMuon); }
bool func__twoGenMuons(unsigned int __slot , const int & nGenMuon) {  return nGenMuon==2; }
ROOT::VecOps::RVec<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > > func__GenMuon_p4(unsigned int __slot , const ROOT::VecOps::RVec<float> & GenMuon_pt, const ROOT::VecOps::RVec<float> & GenMuon_phi, const ROOT::VecOps::RVec<float> & GenMuon_mass, const ROOT::VecOps::RVec<float> & GenMuon_eta) {  return vector_map_t<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> >	>(GenMuon_pt , GenMuon_eta, GenMuon_phi, GenMuon_mass); }
ROOT::VecOps::RVec<double> func__GenMuon_charge(unsigned int __slot , const ROOT::VecOps::RVec<int> & GenMuon_pdgId) {  return -GenMuon_pdgId/abs(GenMuon_pdgId); }
ROOT::VecOps::RVec<ROOT::VecOps::RVec<unsigned long> > func__GenMuMu_allpairs(unsigned int __slot , const ROOT::VecOps::RVec<int> & GenMuon) {  return Combinations(Nonzero(GenMuon),Nonzero(GenMuon)); }
ROOT::VecOps::RVec<int> func__GenMuMu(unsigned int __slot , const ROOT::VecOps::RVec<ROOT::VecOps::RVec<unsigned long> > & GenMuMu_allpairs) {  return At(GenMuMu_allpairs,0) < At(GenMuMu_allpairs,1); }
ROOT::VecOps::RVec<unsigned long> func__GenMuMu0(unsigned int __slot , const ROOT::VecOps::RVec<int> & GenMuMu, const ROOT::VecOps::RVec<ROOT::VecOps::RVec<unsigned long> > & GenMuMu_allpairs) {  return At(At(GenMuMu_allpairs,0),GenMuMu); }
ROOT::VecOps::RVec<unsigned long> func__GenMuMu1(unsigned int __slot , const ROOT::VecOps::RVec<int> & GenMuMu, const ROOT::VecOps::RVec<ROOT::VecOps::RVec<unsigned long> > & GenMuMu_allpairs) {  return At(At(GenMuMu_allpairs,1),GenMuMu); }
ROOT::VecOps::RVec<double> func__GenMuMu0_charge(unsigned int __slot , const ROOT::VecOps::RVec<double> & GenMuon_charge, const ROOT::VecOps::RVec<unsigned long> & GenMuMu0) {  return Take(GenMuon_charge,GenMuMu0); }
ROOT::VecOps::RVec<double> func__GenMuMu1_charge(unsigned int __slot , const ROOT::VecOps::RVec<double> & GenMuon_charge, const ROOT::VecOps::RVec<unsigned long> & GenMuMu1) {  return Take(GenMuon_charge,GenMuMu1); }
ROOT::VecOps::RVec<unsigned long> func__OppositeSignGenMuMu(unsigned int __slot , const ROOT::VecOps::RVec<double> & GenMuMu0_charge, const ROOT::VecOps::RVec<double> & GenMuMu1_charge) {  return Nonzero(GenMuMu0_charge != GenMuMu1_charge); }
bool func__twoOppositeSignGenMuons(unsigned int __slot , const ROOT::VecOps::RVec<unsigned long> & OppositeSignGenMuMu) {  return OppositeSignGenMuMu.size() > 0; }
unsigned long func__GenMu_index(unsigned int __slot , const ROOT::VecOps::RVec<unsigned long> & OppositeSignGenMuMu) {  return At(OppositeSignGenMuMu,0,-200); }
int func__GenMu0(unsigned int __slot , const unsigned long & GenMu_index, const ROOT::VecOps::RVec<unsigned long> & GenMuMu0) {  return int(At(GenMuMu0,GenMu_index)); }
ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > func__GenMu0_p4(unsigned int __slot , const int & GenMu0, const ROOT::VecOps::RVec<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > > & GenMuon_p4) {  return At(GenMuon_p4,GenMu0); }
int func__GenMu1(unsigned int __slot , const unsigned long & GenMu_index, const ROOT::VecOps::RVec<unsigned long> & GenMuMu1) {  return int(At(GenMuMu1,GenMu_index)); }
ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > func__GenMu1_p4(unsigned int __slot , const int & GenMu1, const ROOT::VecOps::RVec<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > > & GenMuon_p4) {  return At(GenMuon_p4,GenMu1); }
ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > func__GenZ(unsigned int __slot , const ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > & GenMu0_p4, const ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > & GenMu1_p4) {  return GenMu0_p4+GenMu1_p4; }
float func__Gen_Zpt(unsigned int __slot , const ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > & GenZ) {  return GenZ.Pt(); }
float func__Gen_ZMass(unsigned int __slot , const ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > & GenZ) {  return GenZ.M(); }
float func__twoGenMuons_twoOppositeSignGenMuonsWeight__Central(unsigned int __slot , const Float_t & genWeight) {  return genWeight; }
float func__Weight__Central(unsigned int __slot , const Float_t & genWeight) {  return genWeight; }
float func__twoMuonsWeight__Central(unsigned int __slot , const Float_t & genWeight) {  return genWeight; }
float func__twoMuons_twoOppositeSignMuonsWeight__Central(unsigned int __slot , const Float_t & genWeight) {  return genWeight; }
float func__twoGenMuonsWeight__Central(unsigned int __slot , const Float_t & genWeight) {  return genWeight; }
float func__twoOppositeSignMuonsWeight__Central(unsigned int __slot , const Float_t & genWeight) {  return genWeight; }
float func__twoOppositeSignGenMuonsWeight__Central(unsigned int __slot , const Float_t & genWeight) {  return genWeight; }


std::vector<ROOT::RDF::RResultPtr<TH1D>> histosWithSelection_eventProcessor(std::map<std::string,RNode> &rdf, std::string sel="1");
Result eventProcessor_nail(RNode rdf,int nThreads,std::map<std::string,std::string> outSplit=std::map<std::string,std::string>()) {
     Result r;
     if(nThreads > 0)
     ROOT::EnableImplicitMT(nThreads);
	
	   auto rdf0 =rdf.DefineSlot("isBB",func__isBB,{})
.DefineSlot("LHE_Zpt",func__LHE_Zpt,{"LHE_Vpt"})
.DefineSlot("Muon_iso",func__Muon_iso,{"Muon_pfRelIso04_all"})
.DefineSlot("SelectedMuon",func__SelectedMuon,{"Muon_pt","Muon_mediumId","Muon_eta","Muon_iso"})
.DefineSlot("SelectedMuon_eta",func__SelectedMuon_eta,{"SelectedMuon","Muon_eta"})
.DefineSlot("SelectedMuon_mass",func__SelectedMuon_mass,{"SelectedMuon","Muon_mass"})
.DefineSlot("SelectedMuon_phi",func__SelectedMuon_phi,{"SelectedMuon","Muon_phi"})
.DefineSlot("SelectedMuon_pt",func__SelectedMuon_pt,{"SelectedMuon","Muon_pt"})
.DefineSlot("SelectedMuon_charge",func__SelectedMuon_charge,{"Muon_charge","SelectedMuon"})
.DefineSlot("nSelectedMuon",func__nSelectedMuon,{"SelectedMuon"})
.DefineSlot("twoMuons",func__twoMuons,{"nSelectedMuon"})
.DefineSlot("SelectedMuon_p4",func__SelectedMuon_p4,{"SelectedMuon_mass","SelectedMuon_pt","SelectedMuon_phi","SelectedMuon_eta"})
.DefineSlot("MuMu_allpairs",func__MuMu_allpairs,{"SelectedMuon"})
.DefineSlot("MuMu",func__MuMu,{"MuMu_allpairs"})
.DefineSlot("MuMu0",func__MuMu0,{"MuMu_allpairs","MuMu"})
.DefineSlot("MuMu1",func__MuMu1,{"MuMu_allpairs","MuMu"})
.DefineSlot("MuMu0_charge",func__MuMu0_charge,{"SelectedMuon_charge","MuMu0"})
.DefineSlot("MuMu1_charge",func__MuMu1_charge,{"SelectedMuon_charge","MuMu1"})
.DefineSlot("OppositeSignMuMu",func__OppositeSignMuMu,{"MuMu1_charge","MuMu0_charge"})
.DefineSlot("twoOppositeSignMuons",func__twoOppositeSignMuons,{"OppositeSignMuMu"})
.DefineSlot("Mu_index",func__Mu_index,{"OppositeSignMuMu"})
.DefineSlot("Mu0",func__Mu0,{"Mu_index","MuMu0"})
.DefineSlot("Mu0_p4",func__Mu0_p4,{"Mu0","SelectedMuon_p4"})
.DefineSlot("Mu1",func__Mu1,{"MuMu1","Mu_index"})
.DefineSlot("Mu1_p4",func__Mu1_p4,{"Mu1","SelectedMuon_p4"})
.DefineSlot("Z",func__Z,{"Mu0_p4","Mu1_p4"})
.DefineSlot("Reco_Zpt",func__Reco_Zpt,{"Z"})
.DefineSlot("Reco_ZMass",func__Reco_ZMass,{"Z"})
.DefineSlot("GenMuon",func__GenMuon,{"GenPart_pt","GenPart_pdgId","GenPart_status","GenPart_eta"})
.DefineSlot("GenMuon_eta",func__GenMuon_eta,{"GenPart_eta","GenMuon"})
.DefineSlot("GenMuon_mass",func__GenMuon_mass,{"GenMuon","GenPart_mass"})
.DefineSlot("GenMuon_phi",func__GenMuon_phi,{"GenMuon","GenPart_phi"})
.DefineSlot("GenMuon_pt",func__GenMuon_pt,{"GenPart_pt","GenMuon"})
.DefineSlot("GenMuon_pdgId",func__GenMuon_pdgId,{"GenPart_pdgId","GenMuon"})
.DefineSlot("nGenMuon",func__nGenMuon,{"GenMuon"})
.DefineSlot("twoGenMuons",func__twoGenMuons,{"nGenMuon"})
.DefineSlot("GenMuon_p4",func__GenMuon_p4,{"GenMuon_pt","GenMuon_phi","GenMuon_mass","GenMuon_eta"})
.DefineSlot("GenMuon_charge",func__GenMuon_charge,{"GenMuon_pdgId"})
.DefineSlot("GenMuMu_allpairs",func__GenMuMu_allpairs,{"GenMuon"})
.DefineSlot("GenMuMu",func__GenMuMu,{"GenMuMu_allpairs"})
.DefineSlot("GenMuMu0",func__GenMuMu0,{"GenMuMu","GenMuMu_allpairs"})
.DefineSlot("GenMuMu1",func__GenMuMu1,{"GenMuMu","GenMuMu_allpairs"})
.DefineSlot("GenMuMu0_charge",func__GenMuMu0_charge,{"GenMuon_charge","GenMuMu0"})
.DefineSlot("GenMuMu1_charge",func__GenMuMu1_charge,{"GenMuon_charge","GenMuMu1"})
.DefineSlot("OppositeSignGenMuMu",func__OppositeSignGenMuMu,{"GenMuMu0_charge","GenMuMu1_charge"})
.DefineSlot("twoOppositeSignGenMuons",func__twoOppositeSignGenMuons,{"OppositeSignGenMuMu"})
.DefineSlot("GenMu_index",func__GenMu_index,{"OppositeSignGenMuMu"})
.DefineSlot("GenMu0",func__GenMu0,{"GenMu_index","GenMuMu0"})
.DefineSlot("GenMu0_p4",func__GenMu0_p4,{"GenMu0","GenMuon_p4"})
.DefineSlot("GenMu1",func__GenMu1,{"GenMu_index","GenMuMu1"})
.DefineSlot("GenMu1_p4",func__GenMu1_p4,{"GenMu1","GenMuon_p4"})
.DefineSlot("GenZ",func__GenZ,{"GenMu0_p4","GenMu1_p4"})
.DefineSlot("Gen_Zpt",func__Gen_Zpt,{"GenZ"})
.DefineSlot("Gen_ZMass",func__Gen_ZMass,{"GenZ"})
.DefineSlot("twoGenMuons_twoOppositeSignGenMuonsWeight__Central",func__twoGenMuons_twoOppositeSignGenMuonsWeight__Central,{"genWeight"})
.DefineSlot("Weight__Central",func__Weight__Central,{"genWeight"})
.DefineSlot("twoMuonsWeight__Central",func__twoMuonsWeight__Central,{"genWeight"})
.DefineSlot("twoMuons_twoOppositeSignMuonsWeight__Central",func__twoMuons_twoOppositeSignMuonsWeight__Central,{"genWeight"})
.DefineSlot("twoGenMuonsWeight__Central",func__twoGenMuonsWeight__Central,{"genWeight"})
.DefineSlot("twoOppositeSignMuonsWeight__Central",func__twoOppositeSignMuonsWeight__Central,{"genWeight"})
.DefineSlot("twoOppositeSignGenMuonsWeight__Central",func__twoOppositeSignGenMuonsWeight__Central,{"genWeight"})
;
auto toplevel=rdf0;
std::vector<ROOT::RDF::RResultPtr<TH1D>> histos;
r.rdf.emplace("",rdf0);
{}auto selection_twoOppositeSignMuons=rdf0.Filter("twoMuons","twoMuons").Filter("twoOppositeSignMuons","twoOppositeSignMuons");
r.rdf.emplace("twoOppositeSignMuons",selection_twoOppositeSignMuons);
{}auto selection_twoOppositeSignGenMuons=rdf0.Filter("twoGenMuons","twoGenMuons").Filter("twoOppositeSignGenMuons","twoOppositeSignGenMuons");
r.rdf.emplace("twoOppositeSignGenMuons",selection_twoOppositeSignGenMuons);
{}
;

            r.histos=histosWithSelection_eventProcessor(r.rdf); 
            for( auto [ name, sel ]  : outSplit){
                r.histosOutSplit[name]=histosWithSelection_eventProcessor(r.rdf,sel);
            }
            return r;}

std::vector<ROOT::RDF::RResultPtr<TH1D>> histosWithSelection_eventProcessor(std::map<std::string,RNode> &rdf, std::string sel){

std::vector<ROOT::RDF::RResultPtr<TH1D>> histos;
histos.emplace_back(rdf.find("")->second.Filter(sel).Histo1D({"LHE_Zpt___", "LHE_Zpt {}", 1000,0,1000},"LHE_Zpt","Weight__Central"));
histos.emplace_back(rdf.find("twoOppositeSignMuons")->second.Filter(sel).Histo1D({"LHE_Zpt___twoOppositeSignMuons", "LHE_Zpt {twoOppositeSignMuons}", 1000,0,1000},"LHE_Zpt","twoOppositeSignMuonsWeight__Central"));
histos.emplace_back(rdf.find("twoOppositeSignMuons")->second.Filter(sel).Histo1D({"Reco_Zpt___twoOppositeSignMuons", "Reco_Zpt {twoOppositeSignMuons}", 1000,0,1000},"Reco_Zpt","twoOppositeSignMuonsWeight__Central"));
histos.emplace_back(rdf.find("twoOppositeSignMuons")->second.Filter(sel).Histo1D({"Reco_ZMass___twoOppositeSignMuons", "Reco_ZMass {twoOppositeSignMuons}", 1000,0,1000},"Reco_ZMass","twoOppositeSignMuonsWeight__Central"));
histos.emplace_back(rdf.find("twoOppositeSignGenMuons")->second.Filter(sel).Histo1D({"LHE_Zpt___twoOppositeSignGenMuons", "LHE_Zpt {twoOppositeSignGenMuons}", 1000,0,1000},"LHE_Zpt","twoOppositeSignGenMuonsWeight__Central"));
histos.emplace_back(rdf.find("twoOppositeSignGenMuons")->second.Filter(sel).Histo1D({"Gen_Zpt___twoOppositeSignGenMuons", "Gen_Zpt {twoOppositeSignGenMuons}", 1000,0,1000},"Gen_Zpt","twoOppositeSignGenMuonsWeight__Central"));
histos.emplace_back(rdf.find("twoOppositeSignGenMuons")->second.Filter(sel).Histo1D({"Gen_ZMass___twoOppositeSignGenMuons", "Gen_ZMass {twoOppositeSignGenMuons}", 1000,0,1000},"Gen_ZMass","twoOppositeSignGenMuonsWeight__Central"));


return histos; }