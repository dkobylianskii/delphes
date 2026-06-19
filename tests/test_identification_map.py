from conftest import make_candidate, make_config


def run_id_test(load_delphes, config, pid, charge=1):
    module, factory = load_delphes(config)

    input_array = module.ExportArray("inputParticles")

    c = make_candidate(factory, 50.0, 0.5, pid=pid, charge=charge)
    input_array.Add(c)

    module.Init()
    module.Process()

    return module.ImportArray("TestModule/outputParticles")


def test_remapping(load_delphes):
    config = make_config("IdentificationMap", EfficiencyFormula=[13, 11, 1.0])
    output = run_id_test(load_delphes, config, pid=13)
    assert output.GetEntries() == 1
    assert output.At(0).PID == 11


def test_no_match_passes_through(load_delphes):
    config = make_config("IdentificationMap", EfficiencyFormula=[13, 11, 1.0])
    output = run_id_test(load_delphes, config, pid=211)
    assert output.GetEntries() == 1
    assert output.At(0).PID == 211


def test_zero_efficiency_rejects(load_delphes):
    config = make_config("IdentificationMap", EfficiencyFormula=[13, 11, 0.0])
    output = run_id_test(load_delphes, config, pid=13)
    assert output.GetEntries() == 0
