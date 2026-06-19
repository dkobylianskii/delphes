from conftest import make_config, make_jet, make_particle, make_parton


def make_module_config(**extra):
    params = {
        "PartonInputArray": "Delphes/inputPartons",
        "ParticleInputArray": "Delphes/inputParticles",
        "JetInputArray": "Delphes/inputJets",
        "DeltaR": 0.5,
        "PartonPTMin": 0.0,
        "PartonEtaMax": 10.0,
    }
    params.update(extra)
    return make_config("JetFlavorAssociation", **params)


def run_flavor_test(load_delphes, config, jets, partons, particles):
    module, factory = load_delphes(config)

    jet_array = module.ExportArray("inputJets")
    for pt, eta in jets:
        j = make_jet(factory, pt, eta)
        jet_array.Add(j)

    parton_array = module.ExportArray("inputPartons")
    for pt, eta, pid, status in partons:
        p = make_parton(factory, pt, eta, pid, status)
        parton_array.Add(p)

    particle_array = module.ExportArray("inputParticles")
    for pt, eta, pid, status in particles:
        p = make_particle(factory, pt, eta, pid, status)
        particle_array.Add(p)

    module.Init()
    module.Process()

    return jet_array


def test_sets_flavor(load_delphes):
    jets = run_flavor_test(
        load_delphes, make_module_config(), jets=[(50.0, 0.5)], partons=[(50.0, 0.5, 5, 3)], particles=[]
    )
    assert jets.GetEntries() == 1
    assert jets.At(0).Flavor == 5


def test_c_quark_flavor(load_delphes):
    jets = run_flavor_test(
        load_delphes, make_module_config(), jets=[(50.0, 0.5)], partons=[(50.0, 0.5, 4, 3)], particles=[]
    )
    assert jets.At(0).Flavor == 4


def test_no_parton_in_cone(load_delphes):
    jets = run_flavor_test(
        load_delphes, make_module_config(), jets=[(50.0, 0.5)], partons=[(50.0, 3.0, 5, 3)], particles=[]
    )
    assert jets.At(0).Flavor == 0


def test_light_quark_flavor(load_delphes):
    jets = run_flavor_test(
        load_delphes, make_module_config(), jets=[(50.0, 0.5)], partons=[(50.0, 0.5, 1, 3)], particles=[]
    )
    assert jets.At(0).Flavor == 1
