from conftest import make_candidate, make_config


def run_filter_test(load_delphes, config, pid, pt=50.0, eta=0.5):
    module, factory = load_delphes(config)

    input_array = module.ExportArray("inputParticles")

    c = make_candidate(factory, pt, eta, pid=pid, charge=1)
    c.D1 = -1
    c.D2 = -1
    input_array.Add(c)

    module.Init()
    module.Process()

    return module.ImportArray("TestModule/outputParticles")


def test_keeps_matching_llp(load_delphes):
    config = make_config("LLPFilter", PdgCode=[1000022])
    output = run_filter_test(load_delphes, config, pid=1000022)
    assert output.GetEntries() == 1


def test_rejects_non_matching(load_delphes):
    config = make_config("LLPFilter", PdgCode=[1000022])
    output = run_filter_test(load_delphes, config, pid=13)
    assert output.GetEntries() == 0


def test_pt_min_filter(load_delphes):
    config = make_config("LLPFilter", PdgCode=[1000022], PTMin=100.0)
    output = run_filter_test(load_delphes, config, pid=1000022, pt=50.0)
    assert output.GetEntries() == 0


def test_daughter_number_filter(load_delphes):
    config = make_config("LLPFilter", PdgCode=[1000022], DaughterNumber=2)
    output = run_filter_test(load_delphes, config, pid=1000022)
    assert output.GetEntries() == 0
