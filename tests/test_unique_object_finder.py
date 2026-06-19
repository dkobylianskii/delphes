from conftest import make_candidate, make_config


def make_module_config(**extra):
    params = {
        "UseUniqueID": True,
        "InputArray": ["Delphes/inputElectrons", "outputElectrons"],
    }
    params.update(extra)
    return make_config("UniqueObjectFinder", **params)


def test_unique_objects_pass_through(load_delphes):
    config = make_module_config(
        InputArray=["Delphes/inputElectrons", "outputElectrons", "Delphes/inputPhotons", "outputPhotons"]
    )
    module, factory = load_delphes(config)

    arr1 = module.ExportArray("inputElectrons")
    c1 = make_candidate(factory, 50.0, 0.5, pid=11, charge=-1)
    arr1.Add(c1)

    arr2 = module.ExportArray("inputPhotons")
    c2 = make_candidate(factory, 30.0, 1.5, pid=22, charge=0)
    arr2.Add(c2)

    module.Init()
    module.Process()

    electrons = module.ImportArray("TestModule/outputElectrons")
    photons = module.ImportArray("TestModule/outputPhotons")
    assert electrons.GetEntries() == 1
    assert photons.GetEntries() == 1


def test_empty_input(load_delphes):
    module, factory = load_delphes(make_module_config())
    module.ExportArray("inputElectrons")
    module.Init()
    module.Process()
    electrons = module.ImportArray("TestModule/outputElectrons")
    assert electrons.GetEntries() == 0


def test_preserves_particle(load_delphes):
    module, factory = load_delphes(make_module_config())
    arr = module.ExportArray("inputElectrons")
    c = make_candidate(factory, 42.0, 1.0, pid=11, charge=-1)
    arr.Add(c)
    module.Init()
    module.Process()
    electrons = module.ImportArray("TestModule/outputElectrons")
    assert electrons.GetEntries() == 1
    assert electrons.At(0).Momentum.Pt() == 42.0
