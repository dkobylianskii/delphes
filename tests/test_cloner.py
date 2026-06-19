import pytest
from conftest import make_config


def test_clones_single_candidate(run_test_module):
    config = make_config("Cloner")
    output = run_test_module(config, [(50.0, 0.5)])
    assert output.GetEntries() == 1
    assert output.At(0).Momentum.Pt() == 50.0


def test_clones_multiple_candidates(run_test_module):
    config = make_config("Cloner")
    output = run_test_module(config, [(50.0, 0.5), (30.0, 1.0), (10.0, 2.0)])
    assert output.GetEntries() == 3
    assert output.At(0).Momentum.Pt() == 50.0
    assert output.At(1).Momentum.Pt() == 30.0
    assert output.At(2).Momentum.Pt() == 10.0


def test_preserves_eta_phi(run_test_module):
    config = make_config("Cloner")
    output = run_test_module(config, [(50.0, 1.2, 0.7)])
    smeared = output.At(0)
    assert smeared.Momentum.Eta() == pytest.approx(1.2, rel=1e-6)
    assert smeared.Momentum.Phi() == pytest.approx(0.7, rel=1e-6)
