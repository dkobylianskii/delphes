import pytest
from conftest import make_config, make_jet, make_vertex


def make_module_config(**extra):
    params = {
        "JetInputArray": "Delphes/inputJets",
        "RhoInputArray": "Delphes/inputRho",
        "OutputArray": "jets",
        "JetPTMin": 0.0,
    }
    params.update(extra)
    return make_config("JetPileUpSubtractor", **params)


def run_subtractor_test(load_delphes, config, jet_pt=50.0, rho_pt=5.0, jet_area=0.5):
    module, factory = load_delphes(config)

    jet_array = module.ExportArray("inputJets")
    jet = make_jet(factory, jet_pt, 0.5)
    jet.Area.SetPtEtaPhiE(jet_area, 0.5, 0.0, jet_area)
    jet_array.Add(jet)

    rho_array = module.ExportArray("inputRho")
    rho = make_vertex(factory)
    rho.Momentum.SetPtEtaPhiE(rho_pt, 0.0, 0.0, rho_pt)
    rho.Edges[0] = -2.5
    rho.Edges[1] = 2.5
    rho_array.Add(rho)

    module.Init()
    module.Process()

    return module.ImportArray("TestModule/jets")


def test_subtracts_rho(load_delphes):
    output = run_subtractor_test(load_delphes, make_module_config(), jet_pt=50.0, rho_pt=5.0, jet_area=2.0)
    assert output.GetEntries() == 1
    subtracted_pt = output.At(0).Momentum.Pt()
    assert subtracted_pt == pytest.approx(50.0 - 5.0 * 2.0, rel=1e-3)


def test_drops_low_pt_jet(load_delphes):
    output = run_subtractor_test(load_delphes, make_module_config(JetPTMin=20.0), jet_pt=15.0, rho_pt=5.0, jet_area=2.0)
    assert output.GetEntries() == 0
