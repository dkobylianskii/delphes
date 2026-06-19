import pytest
from conftest import make_candidate, make_config


def make_module_config(**extra):
    params = {
        "InputArray": "Delphes/inputTracks",
        "OutputArray": "outputParticles",
        "Bz": 3.8,
        "D0ResolutionFormula": "{0.001}",
        "DZResolutionFormula": "{0.002}",
        "PResolutionFormula": "{0.01}",
        "CtgThetaResolutionFormula": "{0.003}",
        "PhiResolutionFormula": "{0.004}",
    }
    params.update(extra)
    return make_config("TrackSmearing", **params)


def run_smearing_test(load_delphes, config, pt=50.0, eta=0.5):
    module, factory = load_delphes(config)

    input_array = module.ExportArray("inputTracks")

    c = make_candidate(factory, pt, eta, pid=211, charge=1)
    c.D0 = 0.0
    c.DZ = 0.0
    c.P = pt
    c.CtgTheta = 1.0
    c.Phi = 0.0
    c.IsPU = 0
    c.InitialPosition.SetXYZT(0.0, 0.0, 0.0, 0.0)
    input_array.Add(c)

    module.Init()
    module.Process()

    return module.ImportArray("TestModule/outputParticles")


def test_smears_track(load_delphes):
    output = run_smearing_test(load_delphes, make_module_config(), pt=50.0, eta=0.5)
    assert output.GetEntries() == 1


def test_sets_errors(load_delphes):
    output = run_smearing_test(load_delphes, make_module_config(), pt=50.0, eta=0.5)
    smeared = output.At(0)
    assert smeared.ErrorD0 == pytest.approx(0.001, rel=1e-3)
    assert smeared.ErrorDZ == pytest.approx(0.002, rel=1e-3)
    assert smeared.ErrorCtgTheta == pytest.approx(0.003, rel=1e-3)
    assert smeared.ErrorPhi == pytest.approx(0.004, rel=1e-3)


def test_sets_track_resolution(load_delphes):
    output = run_smearing_test(load_delphes, make_module_config(), pt=50.0, eta=0.5)
    smeared = output.At(0)
    assert smeared.TrackResolution > 0
