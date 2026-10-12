import os

from resumelens.ui import cli


def test_batch_processes_every_sample(tmp_path):
    summary = cli.run_batch(cli.SAMPLES_DIR, str(tmp_path))
    for filename in cli.list_samples():
        assert filename in summary


def test_batch_summary_has_the_expected_results(tmp_path):
    summary = cli.run_batch(cli.SAMPLES_DIR, str(tmp_path))
    rows = {}
    for line in summary.splitlines()[2:]:
        rows[line.split()[0]] = line
    assert rows["wednesday_addams.txt"].split()[1:] == ["ACCEPTED", "-", "-", "-", "valid"]
    assert rows["kim_possible_multi_profile.txt"].split()[1:] == ["ACCEPTED", "-", "ACCEPTED", "-", "valid"]
    assert "rejected (syntax)" in rows["invalid_edge_case.txt"]


def test_batch_saves_outputs_of_each_resume(tmp_path):
    cli.run_batch(cli.SAMPLES_DIR, str(tmp_path))
    files = os.listdir(str(tmp_path))
    assert "mary_jane_watson.json" in files
    assert "mary_jane_watson.resume" in files
    assert "mary_jane_watson.html" in files
    # The edge case has no HTML because its DSL is not valid
    assert "invalid_edge_case.resume" in files
    assert "invalid_edge_case.html" not in files


def test_main_with_all_option(capsys, monkeypatch):
    # run_batch is replaced so the test does not write in data/output
    def fake_batch():
        return "batch summary"
    monkeypatch.setattr(cli, "run_batch", fake_batch)
    assert cli.main(["--all"]) == 0
    assert "batch summary" in capsys.readouterr().out
