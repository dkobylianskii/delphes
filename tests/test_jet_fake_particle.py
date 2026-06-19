from conftest import make_config, make_jet


def make_module_config(**extra):
    params = {
        "InputArray": "Delphes/inputJets",
        "JetOutputArray": "jets",
        "ElectronOutputArray": "fakeElectrons",
        "MuonOutputArray": "fakeMuons",
        "PhotonOutputArray": "fakePhotons",
        "EfficiencyFormula": [11, 0.0, 13, 0.0, 22, 0.0],
    }
    params.update(extra)
    return make_config("JetFakeParticle", **params)


def run_fake_test(load_delphes, config, jet_pt=50.0, jet_eta=0.5):
    module, factory = load_delphes(config)

    input_array = module.ExportArray("inputJets")
    c = make_jet(factory, jet_pt, jet_eta)
    input_array.Add(c)

    module.Init()
    module.Process()

    return {
        "jets": module.ImportArray("TestModule/jets"),
        "electrons": module.ImportArray("TestModule/fakeElectrons"),
        "muons": module.ImportArray("TestModule/fakeMuons"),
        "photons": module.ImportArray("TestModule/fakePhotons"),
    }


def test_jet_passes_through(load_delphes):
    results = run_fake_test(load_delphes, make_module_config())
    assert results["jets"].GetEntries() == 1
    assert results["electrons"].GetEntries() == 0
    assert results["muons"].GetEntries() == 0
    assert results["photons"].GetEntries() == 0


def test_fake_electrons_generated(load_delphes):
    results = run_fake_test(load_delphes, make_module_config(EfficiencyFormula=[11, 1.0]))
    assert results["jets"].GetEntries() == 0
    assert results["electrons"].GetEntries() == 1


def test_fake_muons_generated(load_delphes):
    results = run_fake_test(load_delphes, make_module_config(EfficiencyFormula=[13, 1.0]))
    assert results["jets"].GetEntries() == 0
    assert results["muons"].GetEntries() == 1


def test_fake_photons_generated(load_delphes):
    results = run_fake_test(load_delphes, make_module_config(EfficiencyFormula=[22, 1.0]))
    assert results["jets"].GetEntries() == 0
    assert results["photons"].GetEntries() == 1
