from conftest import make_candidate, make_config


def run_filter_test(load_delphes, config, is_reco_pu):
    module, factory = load_delphes(config)

    input_array = module.ExportArray("inputParticles")

    c = make_candidate(factory, 50.0, 0.5, pid=211, charge=1)
    c.IsRecoPU = is_reco_pu
    input_array.Add(c)

    module.Init()
    module.Process()

    return module.ImportArray("TestModule/outputParticles")


def test_keeps_non_pileup(load_delphes):
    config = make_config("RecoPuFilter")
    output = run_filter_test(load_delphes, config, 0)
    assert output.GetEntries() == 1


def test_rejects_pileup(load_delphes):
    config = make_config("RecoPuFilter")
    output = run_filter_test(load_delphes, config, 1)
    assert output.GetEntries() == 0


def test_mixed_pu_non_pu(load_delphes):
    module, factory = load_delphes(make_config("RecoPuFilter"))
    input_array = module.ExportArray("inputParticles")
    for is_pu in [0, 1, 0, 1, 0]:
        c = make_candidate(factory, 50.0, 0.5, pid=211, charge=1)
        c.IsRecoPU = is_pu
        input_array.Add(c)
    module.Init()
    module.Process()
    output = module.ImportArray("TestModule/outputParticles")
    assert output.GetEntries() == 3
