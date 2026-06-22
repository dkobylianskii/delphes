//------------------------------------------------------------------------------

#ifndef BeamSpotFilter_h
#define BeamSpotFilter_h

/** \class BeamSpotFilter
 *
 *  Extracts beam spot 
 *
 *  \author Michele Selvaggi
 *
 */

#include "classes/DelphesModule.h"

#include <memory>

class TIterator;
class TObjArray;

class BeamSpotFilter: public DelphesModule
{
public:
  BeamSpotFilter();
  ~BeamSpotFilter();

  void Init();
  void Process();
  void Finish();

private:
  Float_t fPassedOne;

  std::unique_ptr<TIterator> fItInputArray; //!

  const TObjArray *fInputArray = nullptr; //!

  TObjArray *fOutputArray = nullptr; //!

  ClassDef(BeamSpotFilter, 1)
};

#endif
