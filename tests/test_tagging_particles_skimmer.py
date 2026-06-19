from conftest import make_config, make_particle, make_parton


def run_skimmer_test(load_delphes, config, partons, particles):
    module, factory = load_delphes(config)

    parton_array = module.ExportArray("inputPartons")
    for pt, eta, pid, status, d1, d2 in partons:
        c = make_parton(factory, pt, eta, pid, status)
        c.D1 = d1
        c.D2 = d2
        parton_array.Add(c)

    particle_array = module.ExportArray("inputParticles")
    for pt, eta, pid, status in particles:
        p = make_particle(factory, pt, eta, pid, status)
        particle_array.Add(p)

    module.Init()
    module.Process()

    return module.ImportArray("TestModule/taggingParticles")


def test_skims_partons_with_tau(load_delphes):
    config = make_config(
        "TaggingParticlesSkimmer",
        PartonInputArray="Delphes/inputPartons",
        ParticleInputArray="Delphes/inputParticles",
        OutputArray="taggingParticles",
        PTMin=0.0,
        EtaMax=10.0,
    )
    output = run_skimmer_test(
        load_delphes,
        config,
        partons=[(50.0, 0.5, 15, 3, 0, 1)],
        particles=[(20.0, 0.4, 211, 1), (15.0, 0.6, -211, 1)],
    )
    assert output.GetEntries() >= 1
