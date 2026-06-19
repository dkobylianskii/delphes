from conftest import make_candidate, make_config, make_jet


def run_pujetid_test(load_delphes, config, jet_pt=50.0, n_tracks=5, track_is_pu_list=None):
    module, factory = load_delphes(config)

    jet_array = module.ExportArray("inputJets")
    jet = make_jet(factory, jet_pt, 0.5)

    track_array = module.ExportArray("inputTracks")
    if track_is_pu_list is None:
        track_is_pu_list = [0] * n_tracks
    for i, is_pu in enumerate(track_is_pu_list):
        t = make_candidate(factory, 10.0, 0.5, 0.1 * i, pid=211, charge=1)
        t.IsPU = is_pu
        track_array.Add(t)
        jet.AddCandidate(t)

    jet_array.Add(jet)

    module.ExportArray("inputNeutrals")

    module.Init()
    module.Process()

    return module.ImportArray("TestModule/jets")


def test_jet_passes_puid(load_delphes):
    config = make_config(
        "PileUpJetID",
        JetInputArray="Delphes/inputJets",
        TrackInputArray="Delphes/inputTracks",
        NeutralInputArray="Delphes/inputNeutrals",
        OutputArray="jets",
        NeutralsInPassingJets="eflowtowers",
        JetPTMin=0.0,
        UseConstituents=0,
        MeanSqDeltaRMaxBarrel=10.0,
        BetaMinBarrel=0.0,
        MeanSqDeltaRMaxEndcap=10.0,
        BetaMinEndcap=0.0,
        MeanSqDeltaRMaxForward=10.0,
        JetPTMinForNeutrals=0.0,
        NeutralPTMin=0.0,
    )
    output = run_pujetid_test(load_delphes, config, n_tracks=5, track_is_pu_list=[0, 0, 0, 0, 0])
    assert output.GetEntries() == 1
