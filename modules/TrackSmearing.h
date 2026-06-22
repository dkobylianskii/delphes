#ifndef TrackSmearing_h
#define TrackSmearing_h

/** \class TrackSmearing
 *
 *  Performs d0, dZ, p, Theta, Phi smearing of tracks.
 *
 *
 *
 *  \author A. Hart, M. Selvaggi
 *
 */

#include "classes/DelphesModule.h"

#include <memory>

class TIterator;
class TObjArray;
class DelphesFormula;

class TrackSmearing: public DelphesModule
{
public:
  TrackSmearing();
  ~TrackSmearing();

  void Init();
  void Process();
  void Finish();

private:
  Double_t ptError(const Double_t, const Double_t, const Double_t, const Double_t);

  Double_t fBz;

  std::unique_ptr<DelphesFormula> fD0Formula; //!
  std::string fD0ResolutionFile;
  std::string fD0ResolutionHist;
  Bool_t fUseD0Formula;

  std::unique_ptr<DelphesFormula> fDZFormula; //!
  std::string fDZResolutionFile;
  std::string fDZResolutionHist;
  Bool_t fUseDZFormula;

  std::unique_ptr<DelphesFormula> fPFormula; //!
  std::string fPResolutionFile;
  std::string fPResolutionHist;
  Bool_t fUsePFormula;

  std::unique_ptr<DelphesFormula> fCtgThetaFormula; //!
  std::string fCtgThetaResolutionFile;
  std::string fCtgThetaResolutionHist;
  Bool_t fUseCtgThetaFormula;

  std::unique_ptr<DelphesFormula> fPhiFormula; //!
  std::string fPhiResolutionFile;
  std::string fPhiResolutionHist;
  Bool_t fUsePhiFormula;

  Bool_t fApplyToPileUp;

  std::unique_ptr<TIterator> fItInputArray; //!

  const TObjArray *fInputArray = nullptr; //!
  const TObjArray *fBeamSpotInputArray = nullptr; //!

  TObjArray *fOutputArray = nullptr; //!

  ClassDef(TrackSmearing, 1)
};

#endif
