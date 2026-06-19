from conftest import make_config, make_vertex_finder_track


def make_module_config(**extra):
    params = {
        "InputArray": "Delphes/inputTracks",
        "OutputArray": "tracks",
        "VertexOutputArray": "vertices",
        "MinPT": 0.0,
        "VertexSpaceSize": 0.5,
        "VertexTimeSize": 10.0,
        "UseTc": 0,
        "BetaMax": 0.1,
        "BetaStop": 1.0,
        "CoolingFactor": 0.8,
        "MaxIterations": 100,
        "DzCutOff": 40.0,
        "D0CutOff": 30.0,
        "DtCutOff": 100.0,
    }
    params.update(extra)
    return make_config("VertexFinderDA4D", **params)


def run_vertex_test(load_delphes, config, tracks):
    module, factory = load_delphes(config)

    input_array = module.ExportArray("inputTracks")

    for pt, eta, dz, error_dz, is_pu in tracks:
        c = make_vertex_finder_track(factory, pt, eta, dz, error_dz, is_pu)
        input_array.Add(c)

    module.Init()
    module.Process()

    return module.ImportArray("TestModule/tracks"), module.ImportArray("TestModule/vertices")


def test_finds_vertex(load_delphes):
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


def test_single_track_vertex(load_delphes):
    tracks, vertices = run_vertex_test(load_delphes, make_module_config(), [(50.0, 0.5, 0.0, 0.001, 0)])
    assert vertices.GetEntries() == 1
    assert vertices.At(0).ClusterNDF == 1
