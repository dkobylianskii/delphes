from conftest import make_config, make_vertex_finder_track


def make_module_config(**extra):
    params = {
        "InputArray": "Delphes/inputTracks",
        "OutputArray": "tracks",
        "VertexOutputArray": "vertices",
        "Sigma": 3.0,
        "MinPT": 0.0,
        "MaxEta": 10.0,
        "SeedMinPT": 0.0,
        "MinNDF": 4,
        "GrowSeeds": 1,
    }
    params.update(extra)
    return make_config("VertexFinder", **params)


def run_vertex_test(load_delphes, config, tracks):
    module, factory = load_delphes(config)

    input_array = module.ExportArray("inputTracks")

    for pt, eta, dz, error_dz, is_pu in tracks:
        c = make_vertex_finder_track(factory, pt, eta, dz, error_dz, is_pu)
        input_array.Add(c)

    module.Init()
    module.Process()

    return module.ImportArray("TestModule/tracks"), module.ImportArray("TestModule/vertices")


def test_finds_vertex_with_enough_tracks(load_delphes):
    tracks, vertices = run_vertex_test(
        load_delphes,
        make_module_config(),
        [
            (50.0, 0.5, 0.0, 0.001, 0),
            (40.0, 0.5, 0.001, 0.001, 0),
            (30.0, 0.5, -0.001, 0.001, 0),
            (20.0, 0.5, 0.002, 0.001, 0),
        ],
    )
    assert vertices.GetEntries() >= 1
    assert vertices.At(0).ClusterNDF >= 4


def test_no_vertex_with_few_tracks(load_delphes):
    tracks, vertices = run_vertex_test(
        load_delphes, make_module_config(), [(50.0, 0.5, 0.0, 0.001, 0), (40.0, 0.5, 0.001, 0.001, 0)]
    )
    assert vertices.GetEntries() == 0


def test_tracks_assigned_to_vertex(load_delphes):
    tracks, vertices = run_vertex_test(
        load_delphes,
        make_module_config(),
        [
            (50.0, 0.5, 0.0, 0.001, 0),
            (40.0, 0.5, 0.001, 0.001, 0),
            (30.0, 0.5, -0.001, 0.001, 0),
            (20.0, 0.5, 0.002, 0.001, 0),
        ],
    )
    assert tracks.GetEntries() == 4
    for i in range(tracks.GetEntries()):
        assert tracks.At(i).ClusterIndex >= 0
