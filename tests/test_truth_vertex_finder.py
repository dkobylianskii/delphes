from conftest import make_candidate, make_config


def make_module_config(**extra):
    params = {
        "InputArray": "Delphes/inputParticles",
        "VertexOutputArray": "vertices",
        "Resolution": 0.001,
    }
    params.update(extra)
    return make_config("TruthVertexFinder", **params)


def run_vertex_test(load_delphes, config, particles):
    module, factory = load_delphes(config)

    input_array = module.ExportArray("inputParticles")

    for x, y, z, pt, pid in particles:
        c = make_candidate(factory, pt, 0.5, pid=pid)
        c.Position.SetXYZT(x, y, z, 0.0)
        input_array.Add(c)

    module.Init()
    module.Process()

    return module.ImportArray("TestModule/vertices")


def test_creates_vertex(load_delphes):
    output = run_vertex_test(load_delphes, make_module_config(), [(0.0, 0.0, 0.0, 50.0, 211)])
    assert output.GetEntries() >= 1


def test_same_vertex(load_delphes):
    output = run_vertex_test(
        load_delphes, make_module_config(), [(0.0, 0.0, 0.0, 50.0, 211), (0.0005, 0.0005, 0.0005, 30.0, 211)]
    )
    assert output.GetEntries() == 1
