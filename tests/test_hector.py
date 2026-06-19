from conftest import make_candidate, make_config


def make_module_config(**extra):
    params = {
        "OutputArray": "hits",
        "Direction": 1,
        "BeamLineLength": 430.0,
        "Distance": 420.0,
        "OffsetX": 0.0,
        "OffsetS": 120.0,
        "SigmaE": 0.0,
        "SigmaX": 0.0,
        "SigmaY": 0.0,
        "SigmaT": 0.0,
        "EtaMin": 5.0,
        "BeamLineFile": "cards/LHCB1IR5_5TeV.tfs",
        "IPName": "IP5",
    }
    params.update(extra)
    return make_config("Hector", **params)


def test_forward_particle_propagates(load_delphes):
    module, factory = load_delphes(make_module_config())

    input_array = module.ExportArray("inputParticles")
    c = make_candidate(factory, 50.0, 6.0, pid=211, charge=1)
    input_array.Add(c)

    module.Init()
    module.Process()

    hits = module.ImportArray("TestModule/hits")
    assert hits.GetEntries() == 1
    assert hits.At(0).Momentum.E() > 0


def test_low_eta_particle_rejected(load_delphes):
    module, factory = load_delphes(make_module_config())

    input_array = module.ExportArray("inputParticles")
    c = make_candidate(factory, 50.0, 0.5, pid=211, charge=1)
    input_array.Add(c)

    module.Init()
    module.Process()

    hits = module.ImportArray("TestModule/hits")
    assert hits.GetEntries() == 0
