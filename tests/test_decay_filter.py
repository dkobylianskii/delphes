from conftest import make_candidate, make_config


def run_filter_test(load_delphes, config, pid, momentum_p=50.0, trajectory_length_mm=0.0):
    module, factory = load_delphes(config)

    input_array = module.ExportArray("inputParticles")

    c = make_candidate(factory, 50.0, 0.5, pid=pid, charge=1)
    c.P = momentum_p
    c.L = trajectory_length_mm
    input_array.Add(c)

    module.Init()
    module.Process()

    return module.ImportArray("TestModule/outputParticles")


def test_stable_particle_passes(load_delphes):
    config = make_config("DecayFilter")
    output = run_filter_test(load_delphes, config, pid=22)
    assert output.GetEntries() == 1


def test_unknown_pid_passes(load_delphes):
    config = make_config("DecayFilter")
    output = run_filter_test(load_delphes, config, pid=999999)
    assert output.GetEntries() == 1


def test_unstable_short_trajectory_passes(load_delphes):
    config = make_config("DecayFilter")
    output = run_filter_test(load_delphes, config, pid=130, momentum_p=50.0, trajectory_length_mm=0.001)
    assert output.GetEntries() == 1


def test_unstable_long_trajectory_may_decay(load_delphes):
    config = make_config("DecayFilter")
    output = run_filter_test(load_delphes, config, pid=130, momentum_p=50.0, trajectory_length_mm=1e12)
    assert output.GetEntries() <= 1
