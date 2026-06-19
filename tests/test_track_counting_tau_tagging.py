from conftest import make_candidate, make_config, make_jet, make_particle, make_parton


def run_tau_tag_test(load_delphes, config, jets, partons, particles, tracks):
    module, factory = load_delphes(config)

    jet_array = module.ExportArray("inputJets")
    for pt, eta in jets:
        j = make_jet(factory, pt, eta)
        jet_array.Add(j)

    parton_array = module.ExportArray("inputPartons")
    for pt, eta, pid, status, d1, d2 in partons:
        p = make_parton(factory, pt, eta, pid, status)
        p.D1 = d1
        p.D2 = d2
        parton_array.Add(p)

    particle_array = module.ExportArray("inputParticles")
    for pt, eta, pid, status in particles:
        p = make_particle(factory, pt, eta, pid, status)
        particle_array.Add(p)

    track_array = module.ExportArray("inputTracks")
    for pt, eta, charge in tracks:
        t = make_candidate(factory, pt, eta, pid=211, charge=charge)
        track_array.Add(t)

    module.Init()
    module.Process()

    return jet_array


def test_tau_tagging(load_delphes):
    config = make_config(
        "TrackCountingTauTagging",
        ParticleInputArray="Delphes/inputParticles",
        PartonInputArray="Delphes/inputPartons",
        TrackInputArray="Delphes/inputTracks",
        JetInputArray="Delphes/inputJets",
        BitNumber=0,
        DeltaR=0.5,
        DeltaRTrack=0.3,
        TrackPTMin=0.0,
        TauPTMin=0.0,
        TauEtaMax=10.0,
        EfficiencyFormula=[[15, 1.0]],
    )
    jets = run_tau_tag_test(
        load_delphes,
        config,
        jets=[(50.0, 0.5)],
        partons=[(50.0, 0.5, 15, 3, 0, 1)],
        particles=[(20.0, 0.4, 211, 1), (15.0, 0.6, -211, 1)],
        tracks=[(10.0, 0.5, 1), (10.0, 0.5, 1)],
    )
    assert jets.GetEntries() == 1
