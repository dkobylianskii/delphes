from conftest import make_candidate, make_config


def make_module_config(**extra):
    params = {
        "InputArray": "Delphes/inputTracks",
        "OutputArray": "tracks",
        "ResolutionFormula": 0.001,
    }
    params.update(extra)
    return make_config("ImpactParameterSmearing", **params)


def run_smearing_test(load_delphes, config):
    module, factory = load_delphes(config)

    input_array = module.ExportArray("inputTracks")

    c = make_candidate(factory, 50.0, 0.5, pid=211, charge=1)
    c.D0 = 0.0
    c.ErrorD0 = 0.001
    c.DZ = 0.0
    c.TrackResolution = 0.01

    mother = make_candidate(factory, 50.0, 0.5, pid=211, charge=1)
    c.AddCandidate(mother)

    input_array.Add(c)

    module.Init()
    module.Process()

    return module.ImportArray("TestModule/tracks")


def test_smears_impact_parameters(load_delphes):
    output = run_smearing_test(load_delphes, make_module_config())
    assert output.GetEntries() == 1
    smeared = output.At(0)
    assert smeared.D0 != 0.0


def test_zero_resolution_preserves(load_delphes):
    output = run_smearing_test(load_delphes, make_module_config(ResolutionFormula=0.0))
    smeared = output.At(0)
    assert smeared.D0 == 0.0


def test_sets_error_d0(load_delphes):
    output = run_smearing_test(load_delphes, make_module_config(ResolutionFormula=0.002))
    smeared = output.At(0)
    assert smeared.ErrorD0 != 0.001
