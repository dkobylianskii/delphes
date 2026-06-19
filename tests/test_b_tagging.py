from conftest import make_config, make_jet


def run_b_tag_test(load_delphes, config, jet_pt=50.0, jet_eta=0.5, flavor=5):
    module, factory = load_delphes(config)

    jet_array = module.ExportArray("inputJets")

    j = make_jet(factory, jet_pt, jet_eta)
    j.Flavor = flavor
    j.FlavorAlgo = flavor
    j.FlavorPhys = flavor
    jet_array.Add(j)

    module.Init()
    module.Process()

    return jet_array


def test_b_tags_b_jet(load_delphes):
    config = make_config("BTagging", JetInputArray="Delphes/inputJets", BitNumber=0, EfficiencyFormula=[5, 0.8])
    jets = run_b_tag_test(load_delphes, config, flavor=5)
    assert jets.GetEntries() == 1
    jet = jets.At(0)
    assert jet.BTag & 1 == 1


def test_no_b_tag_light_jet(load_delphes):
    config = make_config("BTagging", JetInputArray="Delphes/inputJets", BitNumber=0, EfficiencyFormula=[5, 0.8, 0, 0.0])
    jets = run_b_tag_test(load_delphes, config, flavor=1)
    assert jets.GetEntries() == 1
    jet = jets.At(0)
    assert jet.BTag & 1 == 0


def test_b_tag_with_high_efficiency(load_delphes):
    config = make_config("BTagging", JetInputArray="Delphes/inputJets", BitNumber=0, EfficiencyFormula=[5, 1.0])
    jets = run_b_tag_test(load_delphes, config, flavor=5)
    assert jets.At(0).BTag & 1 == 1


def test_bit_number_1(load_delphes):
    config = make_config("BTagging", JetInputArray="Delphes/inputJets", BitNumber=1, EfficiencyFormula=[5, 1.0])
    jets = run_b_tag_test(load_delphes, config, flavor=5)
    assert jets.At(0).BTag & 1 == 0
    assert jets.At(0).BTag & 2 == 2


def test_c_tagging(load_delphes):
    config = make_config("BTagging", JetInputArray="Delphes/inputJets", BitNumber=0, EfficiencyFormula=[4, 1.0])
    jets = run_b_tag_test(load_delphes, config, flavor=4)
    assert jets.At(0).BTag & 1 == 1
