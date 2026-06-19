import pytest
from conftest import make_candidate, make_config


def make_module_config(**extra):
    params = {
        "InputArray": "Delphes/inputTracks",
        "OutputArray": "tracks",
        "Bz": 3.8,
        "Rmin": 0.3,
        "Rmax": 2.0,
        "Zmin": -2.1,
        "Zmax": 2.1,
        "GasOption": 0,
    }
    params.update(extra)
    return make_config("ClusterCounting", **params)


def run_cluster_counting_test(load_delphes, config, pt=10.0, eta=0.5, pid=211, charge=1):
    module, factory = load_delphes(config)

    input_array = module.ExportArray("inputTracks")

    c = make_candidate(factory, pt, eta, pid=pid, charge=charge)
    mother = make_candidate(factory, pt, eta, pid=pid, charge=charge)
    c.AddCandidate(mother)
    input_array.Add(c)

    module.Init()
    module.Process()

    return module.ImportArray("TestModule/tracks")


def test_initialization(load_delphes):
    config = make_module_config()
    module, factory = load_delphes(config)
    input_array = module.ExportArray("inputTracks")
    c = make_candidate(factory, 10.0, 0.5, pid=211, charge=1)
    input_array.Add(c)
    module.Init()


def test_process_produces_output(load_delphes):
    output = run_cluster_counting_test(load_delphes, make_module_config())
    assert output.GetEntries() == 1


def test_preserves_momentum(load_delphes):
    output = run_cluster_counting_test(load_delphes, make_module_config(), pt=10.0)
    assert output.At(0).Momentum.Pt() == pytest.approx(10.0, rel=1e-3)


def test_preserves_charge(load_delphes):
    output = run_cluster_counting_test(load_delphes, make_module_config(), charge=1)
    assert output.At(0).Charge == 1


def test_preserves_pid(load_delphes):
    output = run_cluster_counting_test(load_delphes, make_module_config(), pid=211)
    assert output.At(0).PID == 211


def test_multiple_tracks(load_delphes):
    module, factory = load_delphes(make_module_config())

    input_array = module.ExportArray("inputTracks")

    for pt, charge in [(5.0, 1), (10.0, 1), (50.0, -1)]:
        c = make_candidate(factory, pt, 0.5, pid=211, charge=charge)
        mother = make_candidate(factory, pt, 0.5, pid=211, charge=charge)
        c.AddCandidate(mother)
        input_array.Add(c)

    module.Init()
    module.Process()

    output = module.ImportArray("TestModule/tracks")
    assert output.GetEntries() == 3


def test_gas_optionhelium(load_delphes):
    output = run_cluster_counting_test(load_delphes, make_module_config(GasOption=0))
    assert output.GetEntries() == 1


def test_gas_option_argon(load_delphes):
    output = run_cluster_counting_test(load_delphes, make_module_config(GasOption=2))
    assert output.GetEntries() == 1


def test_negative_charge(load_delphes):
    output = run_cluster_counting_test(load_delphes, make_module_config(), charge=-1, pid=-211)
    assert output.GetEntries() == 1
    assert output.At(0).Charge == -1
