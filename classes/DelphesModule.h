/*
 *  Delphes: a framework for fast simulation of a generic collider experiment
 *  Copyright (C) 2012-2014  Universite catholique de Louvain (UCL), Belgium
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef DelphesModule_h
#define DelphesModule_h

/** \class DelphesModule
 *
 *  Base class for all Delphes modules
 *
 *  \author P. Demin - UCL, Louvain-la-Neuve
 *
 */

#include "TNamed.h"

#include "ExRootAnalysis/ExRootConfReader.h"

class TClass;
class TIterator;
class TList;

class ExRootTreeBranch;
class ExRootTreeWriter;

class DelphesFactory;

class DelphesModule: public TNamed
{
public:
  DelphesModule();
  ~DelphesModule();

  virtual void Init();
  virtual void Process();
  virtual void Finish();

  int GetInt(const char *name, int defaultValue, int index = -1);
  long GetLong(const char *name, long defaultValue, int index = -1);
  double GetDouble(const char *name, double defaultValue, int index = -1);
  bool GetBool(const char *name, bool defaultValue, int index = -1);
  const char *GetString(const char *name, const char *defaultValue, int index = -1);
  ExRootConfParam GetParam(const char *name);

  TList *GetArrays() const { return fArrays; }
  ExRootConfReader *GetConfReader() const { return fConfReader; }
  ExRootTreeWriter *GetTreeWriter() const { return fTreeWriter; }
  DelphesFactory *GetFactory() const { return fFactory; }

  void SetArrays(TList *arrays) { fArrays = arrays; }
  void SetConfReader(ExRootConfReader *reader) { fConfReader = reader; }
  void SetTreeWriter(ExRootTreeWriter *writer) { fTreeWriter = writer; }
  void SetFactory(DelphesFactory *factory) { fFactory = factory; }

  TObjArray *ImportArray(const char *name);
  TObjArray *ExportArray(const char *name);

  ExRootTreeBranch *NewBranch(const char *name, TClass *cl);
  void AddInfo(const char *name, Double_t value);

private:
  TList *fArrays = nullptr; //!
  ExRootConfReader *fConfReader = nullptr; //!
  ExRootTreeWriter *fTreeWriter = nullptr; //!
  DelphesFactory *fFactory = nullptr; //!

  ClassDef(DelphesModule, 1)
};

#endif /* DelphesModule_h */
