from conftest import make_candidate, make_config


def run_id_test(load_delphes, config, decay_r=500.0, decay_z=1000.0, eta=3.5):
    module, factory = load_delphes(config)

    input_array = module.ExportArray("inputParticles")

    c = make_candidate(factory, 50.0, eta, pid=130, charge=0)
    c.DecayPosition.SetXYZT(decay_r, 0.0, decay_z, 0.0)
    c.Ehad = 50.0
    c.Eem = 0.0
    input_array.Add(c)

    module.Init()
    module.Process()

    return module.ImportArray("TestModule/outputParticles")


def test_pass_all(load_delphes):
    config = make_config("CscClusterId", EfficiencyFormula=1.0, EtaCutFormula=10.0, EtaCutMax=10.0)
    output = run_id_test(load_delphes, config)
    assert output.GetEntries() == 1


def test_reject_all(load_delphes):
    config = make_config("CscClusterId", EfficiencyFormula=0.0, EtaCutFormula=0.0, EtaCutMax=0.0)
    output = run_id_test(load_delphes, config)
    assert output.GetEntries() == 0
