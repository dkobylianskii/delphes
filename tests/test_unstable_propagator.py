from conftest import make_candidate, make_config


def make_module_config(**extra):
    params = {
        "InputArray": "Delphes/inputParticles",
        "Radius": 1.29,
        "HalfLength": 3.0,
        "Bz": 3.8,
        "Lmin": 0.001,
    }
    params.update(extra)
    return make_config("UnstablePropagator", **params)


def test_unstable_particle_processes(load_delphes):
    module, factory = load_delphes(make_module_config())

    input_array = module.ExportArray("inputParticles")

    c = make_candidate(factory, 50.0, 0.5, pid=321, charge=1)
    c.D1 = 1
    c.D2 = 2
    input_array.Add(c)

    d1 = make_candidate(factory, 20.0, 0.5, pid=211, charge=1)
    d1.Position.SetXYZT(100.0, 0.0, 0.0, 0.0)
    d1.M1 = 0
    input_array.Add(d1)

    d2 = make_candidate(factory, 20.0, 0.5, pid=-211, charge=-1)
    d2.Position.SetXYZT(200.0, 0.0, 0.0, 0.0)
    d2.M1 = 0
    input_array.Add(d2)

    module.Init()
    module.Process()

    assert input_array.GetEntries() == 3


def test_stable_particle_passes_through(load_delphes):
    module, factory = load_delphes(make_module_config())
    input_array = module.ExportArray("inputParticles")
    c = make_candidate(factory, 50.0, 0.5, pid=211, charge=1)
    input_array.Add(c)
    module.Init()
    module.Process()
    assert input_array.GetEntries() == 1


def test_daughters_repositioned(load_delphes):
    module, factory = load_delphes(make_module_config())
    input_array = module.ExportArray("inputParticles")
    c = make_candidate(factory, 50.0, 0.5, pid=321, charge=1)
    c.D1 = 1
    c.D2 = 2
    input_array.Add(c)
    d1 = make_candidate(factory, 20.0, 0.5, pid=211, charge=1)
    d1.Position.SetXYZT(100.0, 0.0, 0.0, 0.0)
    d1.M1 = 0
    input_array.Add(d1)
    d2 = make_candidate(factory, 20.0, 0.5, pid=-211, charge=-1)
    d2.Position.SetXYZT(200.0, 0.0, 0.0, 0.0)
    d2.M1 = 0
    input_array.Add(d2)
    module.Init()
    module.Process()
    assert d1.Position.X() != 100.0 or d2.Position.X() != 200.0
