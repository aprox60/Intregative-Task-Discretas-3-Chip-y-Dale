from resumelens.pipeline import run_resume_pipeline


def test_end_to_end_pipeline_generates_html():
    text = """
    Wednesday Addams
    Email: wednesday@example.com
    Phone: +573001234567
    Skills: JS, React.js, NodeJS, Postgres, Git
    Education: BS in Computer Science
    Experience: 3 years of experience in full-stack development
    """
    result = run_resume_pipeline(text)
    assert result.normalized_tokens
    assert "FULL_STACK_DEVELOPER" in result.classification
    assert "<html" in result.html.lower()
    assert "ResumeLens Candidate Report" in result.html
