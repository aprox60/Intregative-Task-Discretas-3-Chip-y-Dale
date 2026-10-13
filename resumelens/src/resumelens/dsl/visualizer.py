# Stage 4: builds a short HTML page from a candidate profile that was already validated.
# It reads the textX model, not the raw resume, so only valid information is shown.

import html

from resumelens.classification.profiles import PROFILES

STYLE = """
:root { --bg: #f6f7f9; --card: #ffffff; --text: #1d2330; --muted: #5b6475; --line: #e3e6ec;
        --accent: #2f5bd3; --ok-bg: #e3f5e9; --ok: #1e7a3c; --no-bg: #f8e6e6; --no: #a12a2a; }
@media (prefers-color-scheme: dark) {
  :root { --bg: #14171d; --card: #1d2129; --text: #e7eaf0; --muted: #9aa3b2; --line: #2e3440;
          --accent: #7c9cf5; --ok-bg: #173523; --ok: #7fd69b; --no-bg: #3a1c1c; --no: #f09a9a; }
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--text); font-family: Segoe UI, Roboto, Arial, sans-serif; line-height: 1.5; }
main { max-width: 760px; margin: 0 auto; padding: 32px 16px; }
header { border-bottom: 3px solid var(--accent); padding-bottom: 12px; margin-bottom: 20px; }
h1 { margin: 0; font-size: 28px; }
.contact { color: var(--muted); margin-top: 4px; word-break: break-word; }
.contact a { color: var(--accent); }
section { background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 16px 20px; margin-bottom: 16px; }
h2 { font-size: 15px; text-transform: uppercase; letter-spacing: .05em; color: var(--muted); margin: 0 0 10px; }
ul { margin: 0; padding-left: 20px; }
.skills { display: flex; flex-wrap: wrap; gap: 8px; }
.skill { border: 1px solid var(--line); border-radius: 999px; padding: 2px 12px; font-size: 13px; font-family: Consolas, monospace; }
.result { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid var(--line); }
.result:last-child { border-bottom: none; }
.badge { border-radius: 6px; padding: 2px 10px; font-size: 13px; font-weight: 600; }
.accepted { background: var(--ok-bg); color: var(--ok); }
.rejected { background: var(--no-bg); color: var(--no); }
footer { color: var(--muted); font-size: 12px; text-align: center; margin-top: 24px; }
"""


def escape(text):
    if text is None:
        return ""
    return html.escape(str(text))


def profile_display_name(profile_name):
    if profile_name in PROFILES:
        return PROFILES[profile_name].display_name
    return profile_name


def render_contact(contact):
    parts = ['<a href="mailto:' + escape(contact.email) + '">' + escape(contact.email) + "</a>"]
    if contact.phone is not None:
        parts.append(escape(contact.phone))
    for link in contact.links:
        url = link.url
        if not url.startswith("http"):
            url = "https://" + url
        parts.append('<a href="' + escape(url) + '">' + escape(link.url) + "</a>")
    return " · ".join(parts)


def render_experience(model):
    if len(model.experiences) == 0:
        return ""
    items = ""
    for experience in model.experiences:
        text = "<strong>" + str(experience.years) + " years</strong>"
        if experience.description:
            text = text + " of experience " + escape(experience.description)
        items = items + "<li>" + text + "</li>"
    return "<section><h2>Experience</h2><ul>" + items + "</ul></section>"


def render_education(model):
    if len(model.educations) == 0:
        return ""
    items = ""
    for education in model.educations:
        text = "<strong>" + escape(education.degree) + "</strong> in " + escape(education.field)
        if education.institution:
            text = text + " — " + escape(education.institution)
        items = items + "<li>" + text + "</li>"
    return "<section><h2>Education</h2><ul>" + items + "</ul></section>"


def render_skills(model):
    chips = ""
    for token in model.skills.tokens:
        chips = chips + '<span class="skill">' + escape(token) + "</span>"
    if chips == "":
        chips = "<span>No normalized skills.</span>"
    return '<section><h2>Normalized skills</h2><div class="skills">' + chips + "</div></section>"


def render_evaluation(model):
    rows = ""
    for result in model.evaluation.results:
        css = "rejected"
        if result.status == "ACCEPTED":
            css = "accepted"
        rows = rows + '<div class="result"><span>' + escape(profile_display_name(result.profile)) + "</span>"
        rows = rows + '<span class="badge ' + css + '">' + escape(result.status) + "</span></div>"
    return "<section><h2>Profile patterns</h2>" + rows + "</section>"


def render_html(model):
    page = "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
    page = page + '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    page = page + "<title>" + escape(model.name) + " - ResumeLens</title>\n"
    page = page + "<style>" + STYLE + "</style>\n</head>\n<body>\n<main>\n"
    page = page + "<header><h1>" + escape(model.name) + "</h1>"
    page = page + '<div class="contact">' + render_contact(model.contact) + "</div></header>\n"
    page = page + render_evaluation(model) + "\n"
    page = page + render_skills(model) + "\n"
    page = page + render_experience(model) + "\n"
    page = page + render_education(model) + "\n"
    page = page + "<footer>Generated by ResumeLens from a validated candidate profile. "
    page = page + "The result only says whether explicit qualification patterns are present; it is not a hiring decision.</footer>\n"
    page = page + "</main>\n</body>\n</html>\n"
    return page
