from conftest import make_candidate, make_config


def run_filter_test(load_delphes, config, pid, status, pt=50.0, eta=0.5):
    module, factory = load_delphes(config)

    input_array = module.ExportArray("inputParticles")

    c = make_candidate(factory, pt, eta, pid=pid, charge=1)
    c.Status = status
    input_array.Add(c)

    module.Init()
    module.Process()

    return module.ImportArray("TestModule/outputParticles")


def test_keeps_hard_scattering(load_delphes):
    config = make_config("StatusPidFilter", PTMin=0.0)
    output = run_filter_test(load_delphes, config, pid=13, status=3)
    assert output.GetEntries() == 1


def test_keeps_stable_lepton(load_delphes):
    config = make_config("StatusPidFilter", PTMin=0.0)
    output = run_filter_test(load_delphes, config, pid=13, status=1)
    assert output.GetEntries() == 1


def test_rejects_non_physical(load_delphes):
    config = make_config("StatusPidFilter", PTMin=0.0)
    output = run_filter_test(load_delphes, config, pid=1, status=1)
    assert output.GetEntries() == 0


def test_pt_min_filter(load_delphes):
    config = make_config("StatusPidFilter", PTMin=100.0)
    output = run_filter_test(load_delphes, config, pid=13, status=3, pt=50.0)
    assert output.GetEntries() == 0


def test_keeps_gauge_boson(load_delphes):
    config = make_config("StatusPidFilter", PTMin=0.0)
    output = run_filter_test(load_delphes, config, pid=23, status=3)
    assert output.GetEntries() == 1


def test_keeps_heavy_quark(load_delphes):
    config = make_config("StatusPidFilter", PTMin=0.0)
    output = run_filter_test(load_delphes, config, pid=5, status=3)
    assert output.GetEntries() == 1


def test_keeps_stable_photon(load_delphes):
    config = make_config("StatusPidFilter", PTMin=0.0)
    output = run_filter_test(load_delphes, config, pid=22, status=1)
    assert output.GetEntries() == 1


def test_rejects_stable_hadron(load_delphes):
    config = make_config("StatusPidFilter", PTMin=0.0)
    output = run_filter_test(load_delphes, config, pid=211, status=1)
    assert output.GetEntries() == 0


def test_keeps_susy_particle(load_delphes):
    config = make_config("StatusPidFilter", PTMin=0.0)
    output = run_filter_test(load_delphes, config, pid=1000022, status=1)
    assert output.GetEntries() == 1


def test_keeps_pythia8_status(load_delphes):
    config = make_config("StatusPidFilter", PTMin=0.0)
    output = run_filter_test(load_delphes, config, pid=13, status=23)
    assert output.GetEntries() == 1


def test_pt_min_exempts_b_quark(load_delphes):
    config = make_config("StatusPidFilter", PTMin=100.0)
    output = run_filter_test(load_delphes, config, pid=5, status=3, pt=10.0)
    assert output.GetEntries() == 1
