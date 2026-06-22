#ifndef OldCalorimeter_h
#define OldCalorimeter_h

/** \class OldCalorimeter
 *
 *  Fills calorimeter towers, performs calorimeter resolution smearing,
 *  preselects towers hit by photons and creates energy flow objects.
 *
 *  $Date$
 *  $Revision$
 *
 *
 *  \author P. Demin - UCL, Louvain-la-Neuve
 *
 */

#include "classes/DelphesModule.h"

#include <map>
#include <memory>
#include <set>
#include <vector>

class TObjArray;
class DelphesFormula;
class Candidate;

class OldCalorimeter: public DelphesModule
{
public:
  OldCalorimeter();
  ~OldCalorimeter();

  void Init();
  void Process();
  void Finish();

private:
  typedef std::map<Long64_t, std::pair<Double_t, Double_t> > TFractionMap; //!
  typedef std::map<Double_t, std::set<Double_t> > TBinMap; //!

  Candidate *fTower = nullptr;
  Double_t fTowerEta, fTowerPhi, fTowerEdges[4];
  Double_t fTowerECalEnergy, fTowerHCalEnergy;
  Double_t fTowerECalNeutralEnergy, fTowerHCalNeutralEnergy;
  Int_t fTowerPhotonHits, fTowerECalHits, fTowerHCalHits, fTowerAllHits;
  Int_t fTowerECalTrackHits, fTowerHCalTrackHits, fTowerTrackAllHits;

  TFractionMap fFractionMap; //!
  TBinMap fBinMap; //!

  std::vector<Double_t> fEtaBins;
  std::vector<std::unique_ptr<std::vector<Double_t> > > fPhiBins;

  std::vector<Long64_t> fTowerHits;

  std::vector<Double_t> fECalFractions;
  std::vector<Double_t> fHCalFractions;

  std::unique_ptr<DelphesFormula> fECalResolutionFormula; //!
  std::unique_ptr<DelphesFormula> fHCalResolutionFormula; //!

  std::unique_ptr<TIterator> fItParticleInputArray; //!
  std::unique_ptr<TIterator> fItTrackInputArray; //!

  const TObjArray *fParticleInputArray = nullptr; //!
  const TObjArray *fTrackInputArray = nullptr; //!

  TObjArray *fTowerOutputArray = nullptr; //!
  TObjArray *fPhotonOutputArray = nullptr; //!

  TObjArray *fEFlowTrackOutputArray = nullptr; //!
  TObjArray *fEFlowTowerOutputArray = nullptr; //!

  std::unique_ptr<TObjArray> fTowerECalArray; //!
  std::unique_ptr<TIterator> fItTowerECalArray; //!

  std::unique_ptr<TObjArray> fTowerHCalArray; //!
  std::unique_ptr<TIterator> fItTowerHCalArray; //!

  std::unique_ptr<TObjArray> fTowerTrackArray; //!
  std::unique_ptr<TIterator> fItTowerTrackArray; //!

  std::unique_ptr<TObjArray> fTowerECalTrackArray; //!
  std::unique_ptr<TIterator> fItTowerECalTrackArray; //!

  std::unique_ptr<TObjArray> fTowerHCalTrackArray; //!
  std::unique_ptr<TIterator> fItTowerHCalTrackArray; //!

  void FinalizeTower();
  Double_t LogNormal(Double_t mean, Double_t sigma);

  ClassDef(OldCalorimeter, 1)
};

#endif
