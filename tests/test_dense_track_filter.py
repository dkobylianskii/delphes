import math
import pytest
from conftest import make_candidate, make_config


def make_module_config(**extra):
    params = {
        "TrackInputArray": "Delphes/inputTracks",
        "TrackOutputArray": "tracks",
        "ChargedHadronOutputArray": "chargedHadrons",
        "ElectronOutputArray": "electrons",
        "MuonOutputArray": "muons",
        "EtaPhiRes": 0.0,
        "EtaPhiBins": [[-1.0, 0.0, 1.0, 2.0], [4]],
    }
    params.update(extra)
    return make_config("DenseTrackFilter", **params)


def run_filter_test(load_delphes, config, particles):
    module, factory = load_delphes(config)

    input_array = module.ExportArray("inputTracks")

    for pt, eta, phi, charge, pid in particles:
        energy = pt
        r = 1000.0
        z = r / math.tan(2.0 * math.atan(math.exp(-eta)))
        x = r * math.cos(phi)
        y = r * math.sin(phi)

        c = make_candidate(factory, pt, eta, phi, energy=energy, pid=pid, charge=charge)
        c.Position.SetXYZT(x, y, z, 0.0)

        mother = make_candidate(factory, pt, eta, phi, energy=energy, pid=pid, charge=charge)
        mother.Position.SetXYZT(x, y, z, 0.0)
        c.AddCandidate(mother)

        input_array.Add(c)

    module.Init()
    module.Process()

    return {
        "tracks": module.ImportArray("TestModule/tracks"),
        "chargedHadrons": module.ImportArray("TestModule/chargedHadrons"),
        "electrons": module.ImportArray("TestModule/electrons"),
        "muons": module.ImportArray("TestModule/muons"),
    }


def test_keeps_single_track(load_delphes):
    results = run_filter_test(load_delphes, make_module_config(), [(50.0, 0.5, 0.5, 1, 211)])
    assert results["tracks"].GetEntries() == 1
    assert results["chargedHadrons"].GetEntries() == 1


def test_keeps_leading_track(load_delphes):
    results = run_filter_test(load_delphes, make_module_config(), [(50.0, 0.5, 0.5, 1, 211), (10.0, 0.5, 0.5, 1, 211)])
    assert results["tracks"].GetEntries() == 1
    assert results["tracks"].At(0).Momentum.Pt() == pytest.approx(50.0, rel=1e-3)


def test_electron_classification(load_delphes):
    results = run_filter_test(load_delphes, make_module_config(), [(50.0, 0.5, 0.5, -1, 11)])
    assert results["electrons"].GetEntries() == 1
    assert results["chargedHadrons"].GetEntries() == 0


def test_muon_classification(load_delphes):
    results = run_filter_test(load_delphes, make_module_config(), [(50.0, 0.5, 0.5, -1, 13)])
    assert results["muons"].GetEntries() == 1
    assert results["chargedHadrons"].GetEntries() == 0
