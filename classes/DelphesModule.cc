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

/** \class DelphesModule
 *
 *  Base class for all Delphes modules
 *
 *  \author P. Demin - UCL, Louvain-la-Neuve
 *
 */

#include "classes/DelphesModule.h"

#include "classes/DelphesFactory.h"

#include "ExRootAnalysis/ExRootTreeBranch.h"
#include "ExRootAnalysis/ExRootTreeWriter.h"

#include "TROOT.h"

#include <iostream>
#include <sstream>
#include <stdexcept>

using namespace std;

DelphesModule::DelphesModule()
{
}

//------------------------------------------------------------------------------

DelphesModule::~DelphesModule()
{
}

//------------------------------------------------------------------------------

void DelphesModule::Init()
{
}

//------------------------------------------------------------------------------

void DelphesModule::Process()
{
}

//------------------------------------------------------------------------------

void DelphesModule::Finish()
{
}

//------------------------------------------------------------------------------

ExRootConfParam DelphesModule::GetParam(const char *name)
{
  return fConfReader->GetParam(TString(GetName()) + "::" + name);
}

//------------------------------------------------------------------------------

int DelphesModule::GetInt(const char *name, int defaultValue, int index)
{
  return fConfReader->GetInt(TString(GetName()) + "::" + name, defaultValue, index);
}

//------------------------------------------------------------------------------

long DelphesModule::GetLong(const char *name, long defaultValue, int index)
{
  return fConfReader->GetLong(TString(GetName()) + "::" + name, defaultValue, index);
}

//------------------------------------------------------------------------------

double DelphesModule::GetDouble(const char *name, double defaultValue, int index)
{
  return fConfReader->GetDouble(TString(GetName()) + "::" + name, defaultValue, index);
}

//------------------------------------------------------------------------------

bool DelphesModule::GetBool(const char *name, bool defaultValue, int index)
{
  return fConfReader->GetBool(TString(GetName()) + "::" + name, defaultValue, index);
}

//------------------------------------------------------------------------------

const char *DelphesModule::GetString(const char *name, const char *defaultValue, int index)
{
  return fConfReader->GetString(TString(GetName()) + "::" + name, defaultValue, index);
}

//------------------------------------------------------------------------------

TObjArray *DelphesModule::ImportArray(const char *name)
{
  stringstream message;
  TObjArray *object;

  object = static_cast<TObjArray *>(fArrays->FindObject(name));
  if(!object)
  {
    message << "can't access input list '" << name;
    message << "' in module '" << GetName() << "'";
    throw runtime_error(message.str());
  }

  return object;
}

//------------------------------------------------------------------------------

TObjArray *DelphesModule::ExportArray(const char *name)
{
  TObjArray *array;

  array = GetFactory()->NewPermanentArray();

  array->SetName(TString(GetName()) + "/" + name);
  fArrays->Add(array);

  return array;
}

//------------------------------------------------------------------------------

ExRootTreeBranch *DelphesModule::NewBranch(const char *name, TClass *cl)
{
  return fTreeWriter->NewBranch(name, cl);
}

//------------------------------------------------------------------------------

void DelphesModule::AddInfo(const char *name, Double_t value)
{
  fTreeWriter->AddInfo(name, value);
}

//------------------------------------------------------------------------------
