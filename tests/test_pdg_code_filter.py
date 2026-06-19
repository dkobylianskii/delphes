from conftest import make_candidate, make_config


def run_filter_test(load_delphes, config, pid, pt=50.0, eta=0.5):
    module, factory = load_delphes(config)

    input_array = module.ExportArray("inputParticles")

    c = make_candidate(factory, pt, eta, pid=pid, charge=1)
    input_array.Add(c)

    module.Init()
    module.Process()

    return module.ImportArray("TestModule/outputParticles")


def test_removes_matching_pdg(load_delphes):
    config = make_config("PdgCodeFilter", PdgCode=["13"])
    output = run_filter_test(load_delphes, config, pid=13)
    assert output.GetEntries() == 0


def test_keeps_non_matching_pdg(load_delphes):
    config = make_config("PdgCodeFilter", PdgCode=["13"])
    output = run_filter_test(load_delphes, config, pid=11)
    assert output.GetEntries() == 1


def test_pt_min_filter(load_delphes):
    config = make_config("PdgCodeFilter", PdgCode=["13"], PTMin=100.0)
    output = run_filter_test(load_delphes, config, pid=11, pt=50.0)
    assert output.GetEntries() == 0


def test_pt_min_pass(load_delphes):
    config = make_config("PdgCodeFilter", PdgCode=["13"], PTMin=10.0)
    output = run_filter_test(load_delphes, config, pid=11, pt=50.0)
    assert output.GetEntries() == 1


def test_invert_keeps_matching(load_delphes):
    config = make_config("PdgCodeFilter", PdgCode=["13"], Invert=True)
    output = run_filter_test(load_delphes, config, pid=13)
    assert output.GetEntries() == 1


def test_require_status(load_delphes):
    module, factory = load_delphes(make_config("PdgCodeFilter", PdgCode=["13"], RequireStatus=True, Status=3))
    input_array = module.ExportArray("inputParticles")
    c = make_candidate(factory, 50.0, 0.5, pid=13, charge=-1)
    c.Status = 1
    input_array.Add(c)
    module.Init()
    module.Process()
    output = module.ImportArray("TestModule/outputParticles")
    assert output.GetEntries() == 0


def test_require_charge(load_delphes):
    module, factory = load_delphes(make_config("PdgCodeFilter", PdgCode=["13"], RequireCharge=True, Charge=-1))
    input_array = module.ExportArray("inputParticles")
    c = make_candidate(factory, 50.0, 0.5, pid=13, charge=1)
    input_array.Add(c)
    module.Init()
    module.Process()
    output = module.ImportArray("TestModule/outputParticles")
    assert output.GetEntries() == 0


def test_require_not_pileup(load_delphes):
    module, factory = load_delphes(make_config("PdgCodeFilter", PdgCode=["13"], RequireNotPileup=True))
    input_array = module.ExportArray("inputParticles")
    c = make_candidate(factory, 50.0, 0.5, pid=13, charge=-1)
    c.IsPU = 1
    input_array.Add(c)
    module.Init()
    module.Process()
    output = module.ImportArray("TestModule/outputParticles")
    assert output.GetEntries() == 0


def test_multiple_pdg_codes(load_delphes):
    module, factory = load_delphes(make_config("PdgCodeFilter", PdgCode=["11", "13"]))
    input_array = module.ExportArray("inputParticles")
    c1 = make_candidate(factory, 50.0, 0.5, pid=11, charge=-1)
    input_array.Add(c1)
    c2 = make_candidate(factory, 30.0, 0.5, pid=211, charge=1)
    input_array.Add(c2)
    module.Init()
    module.Process()
    output = module.ImportArray("TestModule/outputParticles")
    assert output.GetEntries() == 1
