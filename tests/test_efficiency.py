from conftest import make_config


def test_pass_all(run_test_module):
    config = make_config("Efficiency", EfficiencyFormula=1.0)
    output = run_test_module(config, [(50.0, 0.5)])
    assert output.GetEntries() == 1


def test_reject_all(run_test_module):
    config = make_config("Efficiency", EfficiencyFormula=0.0)
    output = run_test_module(config, [(50.0, 0.5)])
    assert output.GetEntries() == 0


def test_conditional_pt_cut(run_test_module):
    config = make_config("Efficiency", EfficiencyFormula="(pt > 10) * 1.0")
    output = run_test_module(config, [(50.0, 0.5), (5.0, 0.5)])
    assert output.GetEntries() == 1


def test_conditional_eta_cut(run_test_module):
    config = make_config("Efficiency", EfficiencyFormula="(abs(eta) < 1.5) * 1.0", UseMomentumVector=True)
    output = run_test_module(config, [(50.0, 1.0), (50.0, 3.0)])
    assert output.GetEntries() == 1
