from conftest import make_candidate, make_config


def run_rho_test(load_delphes, config, particles):
    module, factory = load_delphes(config)

    input_array = module.ExportArray("inputParticles")

    for pt, eta, phi in particles:
        c = make_candidate(factory, pt, eta, phi, pid=22, charge=0)
        input_array.Add(c)

    module.Init()
    module.Process()

    return module.ImportArray("TestModule/rho")


def test_computes_rho(load_delphes):
    config = make_config(
        "FastJetGridMedianEstimator",
        InputArray="Delphes/inputParticles",
        RhoOutputArray="rho",
        GridRange=[-5.0, 5.0, 1.0, 1.0],
    )
    output = run_rho_test(load_delphes, config, [(10.0, 0.5, 0.0), (10.0, 1.0, 0.0)])
    assert output.GetEntries() == 1
