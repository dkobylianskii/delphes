from conftest import make_candidate, make_config


def run_efficiency_test(load_delphes, config, decay_r=500.0, decay_z=1000.0, ehad=50.0, eem=0.0):
    module, factory = load_delphes(config)

    input_array = module.ExportArray("inputParticles")

    c = make_candidate(factory, 50.0, 3.5, pid=130, charge=0)
    c.DecayPosition.SetXYZT(decay_r, 0.0, decay_z, 0.0)
    c.Ehad = ehad
    c.Eem = eem
    input_array.Add(c)

    module.Init()
    module.Process()

    return module.ImportArray("TestModule/outputParticles")


def test_pass_all(load_delphes):
    config = make_config("CscClusterEfficiency", EfficiencyFormula=1.0)
    output = run_efficiency_test(load_delphes, config)
    assert output.GetEntries() == 1


def test_reject_all(load_delphes):
    config = make_config("CscClusterEfficiency", EfficiencyFormula=0.0)
    output = run_efficiency_test(load_delphes, config)
    assert output.GetEntries() == 0
