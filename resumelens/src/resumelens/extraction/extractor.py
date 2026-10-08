# Stage 1: applies the regular expressions of patterns.py to a resume

import os

from resumelens.extraction.patterns import (
    EDUCATION_REGEX,
    EMAIL_REGEX,
    EXPERIENCE_REGEX,
    LEADING_PREPOSITION_REGEX,
    NAME_REGEX,
    PHONE_REGEX,
    SKILL_SEPARATOR_REGEX,
    SKILLS_SECTION_REGEX,
    TECHNICAL_REGEXES,
    URL_REGEX,
)
from resumelens.models import Education, Experience, ExtractionResult


def remove_duplicates(values):
    # Keeps the first appearance of each value
    result = []
    for value in values:
        if value not in result:
            result.append(value)
    return result


def find_all(regex, text):
    # All the strings of the text that the regex recognizes
    found = []
    for match in regex.finditer(text):
        found.append(match.group(0).strip())
    return remove_duplicates(found)


def find_all_in_order(regexes, text):
    # Same as find_all but with several regexes, keeping the order in which they appear in the text
    matches = []
    for regex in regexes:
        for match in regex.finditer(text):
            # the negative length puts the longest match first when two start at the same place
            matches.append((match.start(), -len(match.group(0)), match.group(0).strip()))
    matches.sort()

    found = []
    last_end = 0
    for start, negative_length, value in matches:
        # skip matches inside a longer one, like "REST" inside "REST APIs"
        if start >= last_end:
            found.append(value)
            last_end = start - negative_length
    return remove_duplicates(found)


def extract_name(text):
    # The name is the first line that is not empty, only if it looks like a name
    for line in text.splitlines():
        line = line.strip()
        if line != "":
            if NAME_REGEX.fullmatch(line):
                return line
            return ""
    return ""


def extract_education(text):
    education = []
    for match in EDUCATION_REGEX.finditer(text):
        institution = match.group("institution")
        if institution is None:
            institution = ""
        education.append(Education(match.group("degree").strip(), match.group("field").strip(), institution.strip()))
    return education


def extract_experience(text):
    experience = []
    for match in EXPERIENCE_REGEX.finditer(text):
        description = match.group("description")
        if description is None:
            description = ""
        # "in full-stack development" -> "full-stack development"
        description = LEADING_PREPOSITION_REGEX.sub("", description.strip())
        experience.append(Experience(int(match.group("years")), description))
    return experience


def extract_skills_section(text):
    # Items after "Skills:" or "Technical Skills:", exactly as the candidate wrote them
    items = []
    for match in SKILLS_SECTION_REGEX.finditer(text):
        for item in SKILL_SEPARATOR_REGEX.split(match.group("items")):
            item = item.strip().rstrip(".").strip()
            if item != "":
                items.append(item)
    return remove_duplicates(items)


def extract_resume(text):
    result = ExtractionResult()
    result.name = extract_name(text)
    result.emails = find_all(EMAIL_REGEX, text)
    result.phones = find_all(PHONE_REGEX, text)
    result.links = find_all(URL_REGEX, text)

    result.programming_languages = find_all_in_order(TECHNICAL_REGEXES["programming_languages"], text)
    result.frameworks = find_all_in_order(TECHNICAL_REGEXES["frameworks"], text)
    result.libraries = find_all_in_order(TECHNICAL_REGEXES["libraries"], text)
    result.databases = find_all_in_order(TECHNICAL_REGEXES["databases"], text)
    result.tools = find_all_in_order(TECHNICAL_REGEXES["tools"], text)
    result.other_qualifications = find_all_in_order(TECHNICAL_REGEXES["other_qualifications"], text)

    result.education = extract_education(text)
    result.experience = extract_experience(text)
    result.skills_section = extract_skills_section(text)
    return result


class ResumeExtractor:

    def __init__(self, text):
        self.text = text

    @staticmethod
    def from_file(path):
        with open(path, encoding="utf-8") as file:
            return ResumeExtractor(file.read())

    def extract(self):
        return extract_resume(self.text)

    def to_json(self):
        return self.extract().to_json()

    def save_json(self, path):
        # The assignment asks to keep the extracted information in a file or a data structure
        folder = os.path.dirname(path)
        if folder != "":
            os.makedirs(folder, exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            file.write(self.to_json())
        return path
