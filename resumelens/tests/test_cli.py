import os

from resumelens.pipeline import run_resume_file
from resumelens.ui import cli


def sample(filename):
    return os.path.join(cli.SAMPLES_DIR, filename)


def fake_input(answers):
    # Returns a function that answers like a user typing, one answer each time
    remaining = list(answers)

    def ask(prompt):
        return remaining.pop(0)
    return ask


def test_report_has_the_four_stages():
    report = cli.format_report(run_resume_file(sample("wednesday_addams.txt")))
    assert "Stage 1" in report and "Stage 2" in report and "Stage 3" in report and "Stage 4" in report
    assert "Full Stack Developer [ENFA]: ACCEPTED" in report
    assert "VALID" in report


def test_detailed_report_shows_transducer_steps_and_dsl():
    report = cli.format_report(run_resume_file(sample("wednesday_addams.txt")), details=True)
    assert "React.js" in report and "reactjs" in report
    assert 'candidate "Wednesday Addams"' in report


def test_report_explains_missing_groups():
    report = cli.format_report(run_resume_file(sample("invalid_missing_qualification.txt")))
    assert "missing:  VERSION_CONTROL" in report


def test_report_shows_dsl_rejection():
    report = cli.format_report(run_resume_file(sample("invalid_edge_case.txt")))
    assert "REJECTED: Syntax error" in report


def test_main_saves_outputs(tmp_path, capsys):
    html_path = os.path.join(str(tmp_path), "report.html")
    code = cli.main([sample("mary_jane_watson.txt"), "--output-html", html_path])
    assert code == 0
    with open(html_path, encoding="utf-8") as file:
        assert "Mary Jane Watson" in file.read()


def test_save_outputs_writes_three_files(tmp_path):
    result = run_resume_file(sample("alex_rivera_backend.txt"))
    saved = cli.save_outputs(result, "alex", str(tmp_path))
    names = []
    for path in saved:
        names.append(os.path.basename(path))
    assert names == ["alex.json", "alex.resume", "alex.html"]


def test_main_with_missing_file():
    assert cli.main(["does_not_exist.txt"]) == 1


def test_interactive_menu_analyzes_a_sample(capsys):
    samples = cli.list_samples()
    number = str(samples.index("nina_patel_data_scientist.txt") + 1)
    cli.interactive_menu(fake_input(["1", number, "n", "5"]))
    output = capsys.readouterr().out
    assert "Data Scientist [ENFA]: ACCEPTED" in output
    assert "Bye!" in output


def test_interactive_menu_with_pasted_text(capsys):
    answers = ["3", "Ana Lopez", "Email: ana@example.com", "Skills: Python, Pandas, Scikit-learn, SQL, Git", "END", "n", "5"]
    cli.interactive_menu(fake_input(answers))
    output = capsys.readouterr().out
    assert "Name:       Ana Lopez" in output
    assert "Machine Learning Engineer [DFA]: ACCEPTED" in output


def test_interactive_menu_shows_profiles_and_handles_bad_options(capsys):
    cli.interactive_menu(fake_input(["4", "9", "5"]))
    output = capsys.readouterr().out
    assert "Backend Developer (NFA)" in output
    assert "Invalid option." in output
