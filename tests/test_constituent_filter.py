from conftest import make_candidate, make_config, make_jet


def make_module_config(**extra):
    params = {
        "JetPTMin": 0.0,
        "JetInputArray": "Delphes/inputJets",
        "ConstituentInputArray": ["Delphes/inputConstituents", "outputConstituents"],
    }
    params.update(extra)
    return make_config("ConstituentFilter", **params)


def run_filter_test(load_delphes, config, jet_pt=50.0, n_constituents=3):
    module, factory = load_delphes(config)

    jet_array = module.ExportArray("inputJets")
    jet = make_jet(factory, jet_pt, 0.5)
    constituent_array = module.ExportArray("inputConstituents")
    for i in range(n_constituents):
        c = make_candidate(factory, 10.0, 0.5, 0.1 * i, pid=211, charge=1)
        constituent_array.Add(c)
        jet.AddCandidate(c)

    jet_array.Add(jet)

    module.Init()
    module.Process()

    return module.ImportArray("TestModule/outputConstituents")


def test_filters_constituents(load_delphes):
    output = run_filter_test(load_delphes, make_module_config(), n_constituents=3)
    assert output.GetEntries() == 3


def test_jet_pt_min_rejects(load_delphes):
    output = run_filter_test(load_delphes, make_module_config(JetPTMin=100.0), jet_pt=50.0, n_constituents=3)
    assert output.GetEntries() == 0


def test_preserves_candidate_properties(load_delphes):
    output = run_filter_test(load_delphes, make_module_config(), n_constituents=1)
    assert output.GetEntries() == 1
    assert output.At(0).Momentum.Pt() == 10.0
