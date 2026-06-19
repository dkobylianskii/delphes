import pytest
from conftest import make_candidate, make_config


def test_zero_resolution(run_test_module):
    config = make_config("EnergySmearing", ResolutionFormula=0.0)
    output = run_test_module(config, [(50.0, 0.5)])
    assert output.GetEntries() == 1
    smeared = output.At(0)
    assert smeared.Momentum.Pt() == pytest.approx(50.0, rel=1e-6)


def test_sets_track_resolution(load_delphes):
    config = make_config("EnergySmearing", ResolutionFormula=0.1)
    module, factory = load_delphes(config)

    input_array = module.ExportArray("inputParticles")

    energy = 50.0
    c = make_candidate(factory, 50.0, 0.5)
    c.Position.SetPtEtaPhiE(50.0, 0.5, 0.0, energy)
    input_array.Add(c)

    module.Init()
    module.Process()

    output = module.ImportArray("TestModule/outputParticles")
    smeared = output.At(0)
    assert smeared.TrackResolution > 0
    assert smeared.TrackResolution < 1.0


def test_smears_energy(load_delphes):
    config = make_config("EnergySmearing", ResolutionFormula=0.1)
    module, factory = load_delphes(config)

    input_array = module.ExportArray("inputParticles")

    c = make_candidate(factory, 50.0, 0.5)
    c.Position.SetPtEtaPhiE(50.0, 0.5, 0.0, 50.0)
    input_array.Add(c)

    module.Init()
    module.Process()

    output = module.ImportArray("TestModule/outputParticles")
    smeared = output.At(0)
    assert smeared.Momentum.Pt() != 50.0
