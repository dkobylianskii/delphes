from conftest import make_candidate, make_config


def run_filter_test(load_delphes, config, is_pu_list):
    module, factory = load_delphes(config)

    input_array = module.ExportArray("inputParticles")

    for is_pu in is_pu_list:
        c = make_candidate(factory, 50.0, 0.5, pid=211, charge=1)
        c.IsPU = is_pu
        input_array.Add(c)

    module.Init()
    module.Process()

    return module.ImportArray("TestModule/outputParticles")


def test_passes_non_pu(load_delphes):
    config = make_config("BeamSpotFilter")
    output = run_filter_test(load_delphes, config, [0])
    assert output.GetEntries() == 1


def test_passes_until_first_non_pu(load_delphes):
    config = make_config("BeamSpotFilter")
    output = run_filter_test(load_delphes, config, [1, 1, 0])
    assert output.GetEntries() == 3


def test_all_pu(load_delphes):
    config = make_config("BeamSpotFilter")
    output = run_filter_test(load_delphes, config, [1, 1, 1])
    assert output.GetEntries() == 3


def test_stops_after_first_non_pu(load_delphes):
    config = make_config("BeamSpotFilter")
    output = run_filter_test(load_delphes, config, [0, 0, 0])
    assert output.GetEntries() == 1


def test_preserves_particle_properties(load_delphes):
    module, factory = load_delphes(make_config("BeamSpotFilter"))
    input_array = module.ExportArray("inputParticles")
    c = make_candidate(factory, 42.0, 1.5, pid=13, charge=-1)
    c.IsPU = 0
    input_array.Add(c)
    module.Init()
    module.Process()
    output = module.ImportArray("TestModule/outputParticles")
    assert output.GetEntries() == 1
    assert output.At(0).Momentum.Pt() == 42.0
    assert output.At(0).PID == 13
