from conftest import make_candidate, make_config


def make_module_config(**extra):
    params = {
        "InputPhotonArray": "Delphes/inputPhotons",
        "InputGenArray": "Delphes/inputGen",
        "OutputArray": "photons",
        "PromptFormula": 1.0,
        "NonPromptFormula": 1.0,
        "FakeFormula": 1.0,
        "PTMin": 0.0,
        "RelIsoMax": 0.3,
    }
    params.update(extra)
    return make_config("PhotonID", **params)


def run_photonid_test(load_delphes, config, recos, gens):
    module, factory = load_delphes(config)

    reco_array = module.ExportArray("inputPhotons")
    for pt, eta, iso_var in recos:
        c = make_candidate(factory, pt, eta, pid=22)
        c.Position.SetXYZT(1000.0, eta, 0.0, pt)
        c.IsolationVar = iso_var
        reco_array.Add(c)

    gen_array = module.ExportArray("inputGen")
    for pt, eta in gens:
        c = make_candidate(factory, pt, eta, pid=22)
        gen_array.Add(c)

    module.Init()
    module.Process()

    return module.ImportArray("TestModule/photons")


def test_prompt_photon(load_delphes):
    output = run_photonid_test(load_delphes, make_module_config(), recos=[(50.0, 0.5, 0.1)], gens=[(50.0, 0.5)])
    assert output.GetEntries() == 1
    assert output.At(0).Status == 1


def test_fake_photon_no_gen_match(load_delphes):
    output = run_photonid_test(load_delphes, make_module_config(), recos=[(50.0, 0.5, 0.1)], gens=[])
    assert output.GetEntries() == 1
    assert output.At(0).Status == 3


def test_nonprompt_photon(load_delphes):
    output = run_photonid_test(load_delphes, make_module_config(), recos=[(50.0, 0.5, 0.5)], gens=[(50.0, 0.5)])
    assert output.GetEntries() == 1
    assert output.At(0).Status == 2
