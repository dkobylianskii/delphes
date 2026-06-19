from conftest import make_candidate, make_config, make_jet


def make_module_config(**extra):
    params = {
        "TrackInputArray": "Delphes/inputTracks",
        "JetInputArray": "Delphes/inputJets",
        "BitNumber": 0,
        "TrackPtMin": 1.0,
        "DeltaR": 0.5,
        "TrackIPMax": 2.0,
        "SigMin": 3.0,
        "Ntracks": 3,
        "Use3D": False,
    }
    params.update(extra)
    return make_config("TrackCountingBTagging", **params)


def run_b_tag_test(load_delphes, config, tracks, jet_pt=50.0):
    module, factory = load_delphes(config)

    jet_array = module.ExportArray("inputJets")
    jet = make_jet(factory, jet_pt, 0.5)
    jet_array.Add(jet)

    track_array = module.ExportArray("inputTracks")
    for pt, eta, charge in tracks:
        c = make_candidate(factory, pt, eta, pid=211, charge=charge)
        track_array.Add(c)

    module.Init()
    module.Process()

    return jet_array


def test_no_b_tag_without_enough_tracks(load_delphes):
    jets = run_b_tag_test(load_delphes, make_module_config(), tracks=[(10.0, 0.5, 1)])
    assert jets.GetEntries() == 1
    assert jets.At(0).BTag & 1 == 0


def test_no_b_tag_tracks_far_from_jet(load_delphes):
    config = make_module_config(DeltaR=0.3, SigMin=0.1, Ntracks=1, TrackPtMin=0.0)
    jets = run_b_tag_test(load_delphes, config, tracks=[(10.0, 3.0, 1)])
    assert jets.GetEntries() == 1
    assert jets.At(0).BTag & 1 == 0
