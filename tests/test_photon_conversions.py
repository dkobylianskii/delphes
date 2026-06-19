from conftest import make_candidate, make_config


def make_module_config(**extra):
    params = {
        "Radius": 1.0,
        "HalfLength": 3.0,
        "EtaMin": 2.0,
        "EtaMax": 5.0,
        "Step": 0.1,
        "ConversionMap": 0.0,
    }
    params.update(extra)
    return make_config("PhotonConversions", **params)


def run_conversion_test(load_delphes, config, pid=22, pt=50.0, eta=3.0):
    module, factory = load_delphes(config)

    input_array = module.ExportArray("inputParticles")

    c = make_candidate(factory, pt, eta, pid=pid)
    input_array.Add(c)

    module.Init()
    module.Process()

    return module.ImportArray("TestModule/outputParticles")


def test_non_photon_passes_through(load_delphes):
    output = run_conversion_test(load_delphes, make_module_config(), pid=211, pt=50.0, eta=3.0)
    assert output.GetEntries() == 1
    assert output.At(0).PID == 211


def test_photon_with_zero_conversion(load_delphes):
    output = run_conversion_test(load_delphes, make_module_config(), pid=22, pt=50.0, eta=3.0)
    assert output.GetEntries() == 1
    assert output.At(0).PID == 22
