from conftest import make_candidate, make_config


def make_module_config(**extra):
    params = {
        "InputArray": "Delphes/inputParticles",
        "OutputArray": "outputParticles",
        "UseMomentumVector": False,
        "EtaBins": [-5.0, -3.0, -1.0, 0.0, 1.0, 3.0, 5.0],
        "PhiBins": [-3.14159, -1.5708, 0.0, 1.5708, 3.14159],
    }
    params.update(extra)
    return make_config("ParticleDensity", **params)


def run_density_test(load_delphes, config, particles):
    module, factory = load_delphes(config)

    input_array = module.ExportArray("inputParticles")

    for pt, eta, phi in particles:
        c = make_candidate(factory, pt, eta, phi, pid=22)
        c.Position.SetPtEtaPhiE(1000.0, eta, phi, pt)
        input_array.Add(c)

    module.Init()
    module.Process()

    return module.ImportArray("TestModule/outputParticles")


def test_sets_density(load_delphes):
    output = run_density_test(load_delphes, make_module_config(), [(10.0, 0.5, 0.0), (10.0, 0.5, 0.1)])
    assert output.GetEntries() == 2
    assert output.At(0).ParticleDensity > 0


def test_single_particle_density(load_delphes):
    output = run_density_test(load_delphes, make_module_config(), [(10.0, 0.5, 0.0)])
    assert output.GetEntries() == 1


def test_different_eta_bins(load_delphes):
    config = make_module_config(EtaBins=[-2.5, 0.0, 2.5], PhiBins=[-3.14159, 0.0, 3.14159])
    output = run_density_test(load_delphes, config, [(10.0, 0.5, 0.0)])
    assert output.GetEntries() == 1
