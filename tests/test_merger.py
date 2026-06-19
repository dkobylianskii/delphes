from conftest import make_candidate, make_config


def make_module_config(**extra):
    params = {
        "InputArray": ["Delphes/inputA", "Delphes/inputB"],
        "OutputArray": "outputCandidates",
        "MomentumOutputArray": "momentum",
        "EnergyOutputArray": "energy",
    }
    params.update(extra)
    return make_config("Merger", **params)


def run_merger_test(load_delphes, config, arrays_data):
    module, factory = load_delphes(config)

    for array_name, candidates in arrays_data:
        arr = module.ExportArray(array_name)
        for pt, eta in candidates:
            c = make_candidate(factory, pt, eta)
            arr.Add(c)

    module.Init()
    module.Process()

    return module.ImportArray("TestModule/outputCandidates")


def test_merge_two_arrays(load_delphes):
    arrays = [("inputA", [(50.0, 0.5)]), ("inputB", [(30.0, 1.0)])]
    output = run_merger_test(load_delphes, make_module_config(), arrays)
    assert output.GetEntries() == 2


def test_merge_single_array(load_delphes):
    arrays = [("inputA", [(50.0, 0.5), (30.0, 1.0)])]
    output = run_merger_test(load_delphes, make_module_config(InputArray=["Delphes/inputA"]), arrays)
    assert output.GetEntries() == 2
