import pytest
from conftest import make_config


def test_scale_by_factor(run_test_module):
    config = make_config("EnergyScale", ScaleFormula=0.5)
    output = run_test_module(config, [(50.0, 0.5)])
    assert output.GetEntries() == 1
    assert output.At(0).Momentum.Pt() == 25.0


def test_scale_by_one(run_test_module):
    config = make_config("EnergyScale", ScaleFormula=1.0)
    output = run_test_module(config, [(50.0, 0.5)])
    assert output.GetEntries() == 1
    assert output.At(0).Momentum.Pt() == 50.0


def test_scale_formula_by_pt(run_test_module):
    config = make_config("EnergyScale", ScaleFormula="{(pt > 10) * 0.8 + (pt <= 10) * 0.5}")
    output = run_test_module(config, [(50.0, 0.5), (5.0, 0.5)])
    assert output.GetEntries() == 2
    assert output.At(0).Momentum.Pt() == 40.0
    assert output.At(1).Momentum.Pt() == 2.5


def test_preserves_eta_phi(run_test_module):
    config = make_config("EnergyScale", ScaleFormula=0.5)
    output = run_test_module(config, [(50.0, 1.2, 0.7)])
    smeared = output.At(0)
    assert smeared.Momentum.Eta() == 1.2
    assert smeared.Momentum.Phi() == pytest.approx(0.7, abs=1e-6)
