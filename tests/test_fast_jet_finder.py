import pytest
from conftest import make_candidate, make_config


def make_module_config(**extra):
    params = {
        "InputArray": "Delphes/inputParticles",
        "OutputArray": "jets",
        "JetAlgorithm": 6,
        "ParameterR": 0.5,
        "JetPTMin": 5.0,
    }
    params.update(extra)
    return make_config("FastJetFinder", **params)


def run_jet_test(load_delphes, config, particles):
    module, factory = load_delphes(config)

    input_array = module.ExportArray("inputParticles")

    for pt, eta, phi, charge in particles:
        c = make_candidate(factory, pt, eta, phi, pid=211, charge=charge)
        input_array.Add(c)

    module.Init()
    module.Process()

    return module.ImportArray("TestModule/jets")


def test_clusters_close_particles(load_delphes):
    particles = [(20.0, 0.0, 0.0, 1), (20.0, 0.1, 0.0, 1), (20.0, 0.2, 0.0, 1)]
    jets = run_jet_test(load_delphes, make_module_config(), particles)
    assert jets.GetEntries() == 1
    assert jets.At(0).Momentum.Pt() == pytest.approx(60.0, rel=1e-3)


def test_separates_distant_particles(load_delphes):
    particles = [(20.0, 0.0, 0.0, 1), (30.0, 3.0, 0.0, 1)]
    jets = run_jet_test(load_delphes, make_module_config(), particles)
    assert jets.GetEntries() == 2


def test_jet_pt_min_filter(load_delphes):
    particles = [(20.0, 0.0, 0.0, 1), (20.0, 0.1, 0.0, 1)]
    jets = run_jet_test(load_delphes, make_module_config(JetPTMin=100.0), particles)
    assert jets.GetEntries() == 0


def test_kt_algorithm(load_delphes):
    particles = [(20.0, 0.0, 0.0, 1), (20.0, 0.1, 0.0, 1), (20.0, 0.2, 0.0, 1)]
    jets = run_jet_test(load_delphes, make_module_config(JetAlgorithm=4), particles)
    assert jets.GetEntries() == 1


def test_cambridge_algorithm(load_delphes):
    particles = [(20.0, 0.0, 0.0, 1), (20.0, 0.1, 0.0, 1), (20.0, 0.2, 0.0, 1)]
    jets = run_jet_test(load_delphes, make_module_config(JetAlgorithm=5), particles)
    assert jets.GetEntries() == 1


def test_jet_constituents(load_delphes):
    particles = [(20.0, 0.0, 0.0, 1), (20.0, 0.1, 0.0, 1), (20.0, 0.2, 0.0, 1), (30.0, 3.0, 0.0, 1)]
    jets = run_jet_test(load_delphes, make_module_config(), particles)
    assert jets.GetEntries() == 2
    assert jets.At(0).GetCandidates().GetEntries() == 3


def test_jet_charge(load_delphes):
    particles = [(20.0, 0.0, 0.0, 1), (20.0, 0.1, 0.0, -1)]
    jets = run_jet_test(load_delphes, make_module_config(), particles)
    assert jets.GetEntries() == 1
    assert jets.At(0).Charge == 0
