import math
import pytest
import ROOT

from delphes.dict2tcl import dict2tcl

ROOT.gSystem.Load("libDelphes")


@pytest.fixture(scope="function")
def load_delphes():
    modules = []
    refs = []

    def load(config):
        conf_reader = ROOT.ExRootConfReader()
        if isinstance(config, dict):
            data = dict2tcl(config).encode()
            conf_reader.ReadData(".", data, len(data))
        else:
            conf_reader.ReadFile(config)
        writer = ROOT.ExRootTreeWriter()
        module = ROOT.Delphes("Delphes")
        module.SetConfReader(conf_reader)
        module.SetTreeWriter(writer)
        factory = module.GetFactory()
        modules.append(module)
        refs.extend([conf_reader, writer])
        return module, factory

    yield load

    for m in modules:
        m.Finish()
    modules.clear()
    refs.clear()


def make_config(class_name, input_array="Delphes/inputParticles", output_array="outputParticles", **kwargs):
    return {
        "RandomSeed": 42,
        "ExecutionPath": ["TestModule"],
        "TestModule": {
            "Class": class_name,
            "InputArray": input_array,
            "OutputArray": output_array,
            **kwargs,
        },
    }


def make_candidate(factory, pt, eta, phi=0.0, energy=None, pid=0, charge=0, status=1, m1=-1):
    if energy is None:
        energy = pt * math.cosh(eta)
    c = factory.NewCandidate()
    c.Momentum.SetPtEtaPhiE(pt, eta, phi, energy)
    c.Position.SetPtEtaPhiE(0.0, 0.0, 0.0, 0.0)
    c.PID = pid
    c.Charge = charge
    c.Status = status
    c.M1 = m1
    return c


def make_jet(factory, pt, eta, phi=0.0, energy=None):
    return make_candidate(factory, pt, eta, phi, energy, pid=0, charge=0)


def make_parton(factory, pt, eta, pid, status=3, d1=-1, d2=-1, phi=0.0, energy=None):
    charge = 1 if pid > 0 else -1
    c = make_candidate(factory, pt, eta, phi, energy, pid=pid, charge=charge, status=status)
    c.D1 = d1
    c.D2 = d2
    return c


def make_particle(factory, pt, eta, pid, status=1, phi=0.0, energy=None):
    charge = 1 if pid > 0 else -1
    return make_candidate(factory, pt, eta, phi, energy, pid=pid, charge=charge, status=status)


def make_vertex_finder_track(factory, pt, eta, dz, error_dz, is_pu):
    c = make_candidate(factory, pt, eta, charge=1, pid=211)
    c.Position.SetXYZT(0.0, 0.0, dz * 1000.0, 0.0)
    c.InitialPosition.SetXYZT(0.0, 0.0, dz * 1000.0, 0.0)
    c.DZ = dz * 1000.0
    c.ErrorDZ = error_dz * 1000.0
    c.D0 = 0.0
    c.ErrorD0 = 0.001
    c.P = pt
    c.CtgTheta = 1.0
    c.Phi = 0.0
    c.IsPU = is_pu
    return c


def make_vertex(factory, x=0.0, y=0.0, z=0.0, t=0.0, is_pu=0):
    c = make_candidate(factory, 0.0, 0.0)
    c.Position.SetXYZT(x, y, z, t)
    c.IsPU = is_pu
    return c


@pytest.fixture(scope="function")
def run_test_module(load_delphes):
    def run(config, candidates):
        module, factory = load_delphes(config)
        input_array = module.ExportArray("inputParticles")
        for args in candidates:
            pt, eta, *extra = args
            phi = extra[0] if extra else 0.0
            input_array.Add(make_candidate(factory, pt, eta, phi))
        module.InitTask()
        module.ProcessTask()
        return module.ImportArray("TestModule/outputParticles")

    yield run
