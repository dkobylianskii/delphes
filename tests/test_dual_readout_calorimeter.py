import math
import pytest
from conftest import make_candidate, make_config


def run_calo_test(load_delphes, config, particles, tracks=None):
    module, factory = load_delphes(config)

    particle_array = module.ExportArray("inputParticles")
    for pt, eta, phi, pid in particles:
        c = make_candidate(factory, pt, eta, phi, pid=pid)
        c.Position.SetPtEtaPhiE(1.0, eta, phi, 0)
        particle_array.Add(c)

    track_array = module.ExportArray("inputTracks")
    if tracks:
        for pt, eta, phi, charge, pid, track_resolution in tracks:
            c = make_candidate(factory, pt, eta, phi, pid=pid, charge=charge)
            c.Position.SetPtEtaPhiE(1.0, eta, phi, 0)
            c.TrackResolution = track_resolution
            track_array.Add(c)

    module.Init()
    module.Process()

    return module.ImportArray("TestModule/towers")


def make_module_config(**extra):
    params = {
        "ParticleInputArray": "Delphes/inputParticles",
        "TrackInputArray": "Delphes/inputTracks",
        "TowerOutputArray": "towers",
        "PhotonOutputArray": "photons",
        "EFlowTrackOutputArray": "eflowTracks",
        "EFlowPhotonOutputArray": "eflowPhotons",
        "EFlowNeutralHadronOutputArray": "eflowNeutralHadrons",
        "SmearTowerCenter": False,
        "SmearLogNormal": False,
        "ECalResolutionFormula": 0.0,
        "HCalResolutionFormula": 0.0,
        "ECalMinSignificance": 0.0,
        "HCalMinSignificance": 0.0,
        "TimingEnergyMin": 0.0,
        "EtaPhiBins": [
            [-1.0, 0.0, 1.0, 2.0],
            [4],
        ],
        "EnergyFraction": [
            0,
            [0.0, 1.0],
            11,
            [1.0, 0.0],
            22,
            [1.0, 0.0],
        ],
    }
    params.update(extra)
    return make_config("DualReadoutCalorimeter", **params)


def test_photon_creates_tower(load_delphes):
    config = make_module_config()
    results = run_calo_test(
        load_delphes,
        config,
        particles=[
            (50.0, 0.5, 0.0, 22),
        ],
    )
    assert results.GetEntries() >= 1


def test_energy_conservation(load_delphes):
    config = make_module_config()

    pt = 50.0
    eta = 0.5
    expected_energy = pt * math.cosh(eta)
    results = run_calo_test(
        load_delphes,
        config,
        particles=[
            (pt, eta, 0.0, 22),
        ],
    )
    total_energy = 0.0
    for i in range(results.GetEntries()):
        total_energy += results.At(i).Momentum.E()
    assert total_energy == pytest.approx(expected_energy, rel=1e-3)


def test_ecal_sets_eem(load_delphes):
    config = make_module_config()
    results = run_calo_test(
        load_delphes,
        config,
        particles=[
            (50.0, 0.5, 0.0, 22),
        ],
    )
    tower = results.At(0)
    assert tower.Eem > 0
    assert tower.Ehad == 0


def test_hcal_sets_ehad(load_delphes):
    config = make_module_config()
    results = run_calo_test(
        load_delphes,
        config,
        particles=[
            (50.0, 0.5, 0.0, 130),
        ],
    )
    tower = results.At(0)
    assert tower.Ehad > 0
    assert tower.Eem == 0


def test_tower_eta_phi_edges(load_delphes):
    config = make_module_config()
    results = run_calo_test(
        load_delphes,
        config,
        particles=[
            (50.0, 1.0, 0.0, 22),
        ],
    )
    tower = results.At(0)
    assert tower.Edges[0] == pytest.approx(0.0, abs=1e-6)
    assert tower.Edges[1] == pytest.approx(1.0, abs=1e-6)
    assert tower.Edges[2] == pytest.approx(-1.570796, abs=1e-6)
    assert tower.Edges[3] == pytest.approx(0.0, abs=1e-6)


def test_charged_track_in_tower(load_delphes):
    config = make_module_config()
    results = run_calo_test(
        load_delphes,
        config,
        particles=[(50.0, 0.5, 0.0, 130)],
        tracks=[(50.0, 0.5, 0.0, 1, 211, 0.01)],
    )
    assert results.GetEntries() >= 1
    tower = results.At(0)
    assert tower.Etrk > 0
