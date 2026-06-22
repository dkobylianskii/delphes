#ifndef VertexFinderDA4D_h
#define VertexFinderDA4D_h

/** \class VertexFinderDA4D
 *
 *  Cluster vertices from tracks using deterministic annealing and timing information
 *
 *  \authors M. Selvaggi, L. Gray
 *
 */

#include "classes/DelphesModule.h"

#include <memory>
#include <vector>

class TObjArray;
class TIterator;
class Candidate;

class VertexFinderDA4D: public DelphesModule
{
public:
  VertexFinderDA4D();
  ~VertexFinderDA4D();

  void Init();
  void Process();
  void Finish();

  void clusterize(const TObjArray &tracks, TObjArray &clusters);
  std::vector<Candidate *> vertices();

private:
  Bool_t fVerbose;
  Double_t fMinPT;

  Double_t fVertexSpaceSize;
  Double_t fVertexTimeSize;
  Bool_t fUseTc;
  Double_t fBetaMax;
  Double_t fBetaStop;
  Double_t fCoolingFactor;
  Int_t fMaxIterations;
  Double_t fDzCutOff;
  Double_t fD0CutOff;
  Double_t fDtCutOff; // for when the beamspot has time

  std::unique_ptr<TObjArray> fClusterArray; //!
  std::unique_ptr<TIterator> fItClusterArray; //!

  TObjArray *fInputArray = nullptr;
  std::unique_ptr<TIterator> fItInputArray; //!

  TObjArray *fOutputArray = nullptr;
  TObjArray *fVertexOutputArray = nullptr;

  ClassDef(VertexFinderDA4D, 1)
};

#endif
