
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
float func__Z_pt(unsigned int __slot , const Float_t & LHE_Vpt) {  return LHE_Vpt; }
float func__Weight__Central(unsigned int __slot , const Float_t & genWeight) {  return genWeight; }

Result eventProcessor_nail(RNode rdf,int nThreads) {
     Result r;
     if(nThreads > 0)
     ROOT::EnableImplicitMT(nThreads);
	
	   auto rdf0 =rdf.DefineSlot("Z_pt",func__Z_pt,{"LHE_Vpt"})
.DefineSlot("Weight__Central",func__Weight__Central,{"genWeight"})
;
auto toplevel=rdf0;
std::vector<ROOT::RDF::RResultPtr<TH1D>> histos;
{histos.emplace_back(rdf0.Histo1D({"Z_pt___", "Z_pt {}", 500,0,1000},"Z_pt","Weight__Central"));
}
;
r.rdf.emplace("",rdf0);
r.histos=histos; return r;}