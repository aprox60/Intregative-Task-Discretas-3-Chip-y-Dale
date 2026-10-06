from resumelens.extraction.extractor import ResumeExtractor


def test_reference_skill_extraction():
    text = "Technical Skills: JS, React.js, NodeJS, Postgres, Git."
    extracted = ResumeExtractor(text).extract()
    skills = extracted["skills"]
    for expected in ["JS", "React.js", "NodeJS", "Postgres", "Git"]:
        assert expected in skills


def test_contact_and_experience_extraction():
    text = "Email: jane@example.com | Phone: +573001234567 | Experience: 3 years of experience"
    extracted = ResumeExtractor(text).extract()
    assert "jane@example.com" in extracted["email"]
    assert "+573001234567" in extracted["phone"]
    assert "3 years of experience" in extracted["experience"]
