from __future__ import annotations

from resumelens.models import Candidate


def render_html(candidate: Candidate) -> str:
    """Generate a minimal HTML summary from a validated candidate model."""

    skills_html = "".join(f"<li>{skill}</li>" for skill in candidate.skills)
    experience_html = "".join(f"<li>{entry}</li>" for entry in candidate.experience)
    qualification_html = "".join(f"<li>{item}</li>" for item in candidate.academic_qualifications)
    profile_status = "ACCEPTED" if any(candidate.profile_results.values()) else "REJECTED"

    html = f"""
    <!DOCTYPE html>
    <html lang=\"en\">
    <head>
      <meta charset=\"utf-8\" />
      <title>ResumeLens Candidate Report</title>
      <style>
        body {{ font-family: Arial, sans-serif; margin: 2rem; }}
        h1 {{ color: #1b4f72; }}
        section {{ margin-bottom: 1.5rem; }}
      </style>
    </head>
    <body>
      <h1>ResumeLens Candidate Report</h1>
      <section>
        <h2>Candidate</h2>
        <p><strong>Name:</strong> {candidate.full_name or 'Candidate'}</p>
        <p><strong>Email:</strong> {candidate.email or 'example@example.com'}</p>
        <p><strong>Status:</strong> {profile_status}</p>
      </section>
      <section>
        <h2>Skills</h2>
        <ul>{skills_html}</ul>
      </section>
      <section>
        <h2>Experience</h2>
        <ul>{experience_html}</ul>
      </section>
      <section>
        <h2>Academic qualifications</h2>
        <ul>{qualification_html}</ul>
      </section>
    </body>
    </html>
    """
    return html.strip()
