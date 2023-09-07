#include <ROOT/RDF/RActionImpl.hxx>
#include <TH1F.h>
#include <TROOT.h>
#include <iostream>
#include <ROOT/RVec.hxx>
// The template class inherits from ROOT::Detail::RDF::RActionImpl
const float upsamplingFactor=5.;
class TTreeReader;

template <typename TH>
class OversampledTH : public ROOT::Detail::RDF::RActionImpl<OversampledTH<TH>> {
public:
  // Define the type of the histogram
  using Result_t = TH;

private:
  // Number of slots (threads)
  int nSlots;
  // Use unordered_map instead of map for faster access times
  std::unordered_map<long int, std::unordered_map<int, TH*>> fHistos;  // (One histo per slot) per genEvent
  // Vector to keep track of the current event per slot
  std::vector<long int> current;
  // Shared pointer to the final histogram
  std::shared_ptr<TH> fFinalHisto;
  // Keep track of the last flushed event
  long int lastFlush = -1; // default = -1 since genEvent starts from 0


public:
  // Constructor with parameters for histogram creation
  // The initialization list is used for more efficient variable initialization
  OversampledTH(std::string_view name, std::string_view title, int nbin, double xmin, double xmax)
    : nSlots(ROOT::IsImplicitMTEnabled() ? ROOT::GetThreadPoolSize() : 1),
      current(nSlots, -1),
      fFinalHisto(std::make_shared<TH>(std::string(name).c_str(), std::string(title).c_str(), nbin, xmin, xmax)) {
//     cout << "bins" <<  fFinalHisto->GetNbinsX() << std::endl;
//cout << "nSlots: " << nSlots << endl;
  }

  // Move constructor and deletion of copy constructor
  OversampledTH(OversampledTH &&) = default;
  OversampledTH(const OversampledTH &) = delete;

  // Function to return the pointer to the final histogram
  std::shared_ptr<TH> GetResultPtr() const { return fFinalHisto; }

  // Initialize() and InitTask() functions are not used in this implementation
  void Initialize() {}
  void InitTask(TTreeReader *, unsigned int) {}

  // Exec function is called for each event and fills the histogram
  // The unordered_map for each event is filled only if it doesn't exist yet
  // Then, it checks if the event has changed, and if so, it flushes the histograms
//  template <typename... ColumnTypes>
//
//
  template <typename ColumnType>
  void Exec(unsigned int slot, unsigned long genEvent, ROOT::VecOps::RVec<ColumnType> values, double weight = 1) {
          for(auto v : values) Exec(slot,genEvent,v,weight); 
      }

  void Exec(unsigned int slot, unsigned long genEvent, double values, double weight = 1) {
    if (!fFinalHisto) {
      std::cerr << "Error: fFinalHisto is null" << std::endl;
      return;
    }
    if ((fHistos[genEvent].find(slot) == fHistos[genEvent].end())) {
//p      cout << "fHistos[genEvent][slot] exists" << endl;
  // std::cerr << "here" << std::endl;
    //  cout << "bins orig" <<  ((TH *)fFinalHisto->Clone())->GetNbinsX() << std::endl;
      TH * h=(TH *)fFinalHisto->Clone();
      //cout << "bins cl" <<  h->GetNbinsX() << std::endl;
      fHistos[genEvent].emplace(slot, h);
     // cout << "bins " << fHistos[genEvent][slot]->GetNbinsX() << std::endl;
      fHistos[genEvent][slot]->Reset();
     // cout << "bins reset " << fHistos[genEvent][slot]->GetNbinsX() << std::endl;
    }
  //  cerr<< values<<  endl;
    fHistos[genEvent][slot]->Fill(values, weight);
//    cout << "genEvent: " << genEvent << " Slot: " << slot << endl;
    if (genEvent != current[slot]) {
//      cout << "genEvent" << genEvent << " != current[slot]" << current[slot] << endl;
      // print all entries of current
      // cout << "current: " << endl;
      // for (auto i : current) {
      //   cout << i << endl;
      // }
      Flush();
      current[slot] = genEvent; // Update current event for this slot (thread)
    }
  }

  // Function to fill the final histogram with the values from the different slots
  // The for loop uses a const reference to avoid unnecessary copies
  void fillOversampledHisto(const std::unordered_map<int, TH*> &histosFromSlots) {
    for (const auto &kv : histosFromSlots) {
      auto histo = *kv.second;
      for(size_t bin=0; bin <= histo.GetNbinsX(); bin++){
            fFinalHisto->Fill(histo.GetBinCenter(bin),histo.GetBinContent(bin)/upsamplingFactor);
  //          cout<< bin << " center: " << histo.GetBinCenter(bin) << " w: " << histo.GetBinContent(bin)/upsamplingFactor << endl;
      }
     // cout << "deleting " << kv.second << endl;
      delete(kv.second);
//      fFinalHisto->Add(&histo);
    }
  }

  // Flush function to clean up the filled histograms
  // It takes an optional 'all' argument to decide whether to flush all histograms or not
  void Flush(bool all = false) {
    // Gets the minimum genEvent from all the slots
    auto minGen = *std::min_element(current.begin(), current.end());
//    cout << "minGen: " << minGen << endl;
//    cout << "lastFlush: " << lastFlush << endl;
    // If the last flushed genEvent is less than (minGen - 1) or 'all' is true, it starts flushing histograms
    // 'all' would be true when Finalize() function is called at the end of event loop
    if ((lastFlush < (minGen - 1)) || all) {
      // Iterate through fHistos
      for (auto it = fHistos.begin(); it != fHistos.end();) {
        auto genEvent = it->first;
        // If the genEvent is less than minGen, it means this event has been processed by all slots
        // So it's safe to fill the final histogram with this event's data and then remove it from fHistos
        if (genEvent < minGen) {
          fillOversampledHisto(it->second);
          lastFlush = genEvent;
          // Erase this event from fHistos. Since erasing invalidates the iterator,
          // we use the returned iterator which points to the next valid item
        it = fHistos.erase(it);
        } else {
          // If this event is not ready to be flushed, move to the next event
          ++it;
        }
      }
    }
  }

  void Finalize() {
    Flush(true); 
  }

  std::string GetActionName() { return "OversampledTH"; }
};

