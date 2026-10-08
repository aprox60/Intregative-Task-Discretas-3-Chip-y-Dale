import json

# Technical categories found in stage 1. Each one is normalized later by its own transducer.
TECHNICAL_CATEGORIES = [
    "programming_languages",
    "frameworks",
    "libraries",
    "databases",
    "tools",
    "other_qualifications",
]


class Education:
    # An academic qualification, for example "BS in Computer Science"

    def __init__(self, degree, field, institution=""):
        self.degree = degree
        self.field = field
        self.institution = institution

    def to_dict(self):
        return {"degree": self.degree, "field": self.field, "institution": self.institution}


class Experience:
    # For example "3 years of experience developing web applications"

    def __init__(self, years, description=""):
        self.years = years
        self.description = description

    def to_dict(self):
        return {"years": self.years, "description": self.description}


class ExtractionResult:
    # Raw strings found by the regular expressions (nothing is normalized yet)

    def __init__(self):
        self.name = ""
        self.emails = []
        self.phones = []
        self.links = []
        self.programming_languages = []
        self.frameworks = []
        self.libraries = []
        self.databases = []
        self.tools = []
        self.other_qualifications = []
        self.education = []
        self.experience = []
        self.skills_section = []

    def get_technical_items(self):
        # Technical strings by category, this is the input of stage 2
        return {
            "programming_languages": self.programming_languages,
            "frameworks": self.frameworks,
            "libraries": self.libraries,
            "databases": self.databases,
            "tools": self.tools,
            "other_qualifications": self.other_qualifications,
        }

    def get_all_technical_strings(self):
        result = []
        items = self.get_technical_items()
        for category in TECHNICAL_CATEGORIES:
            for value in items[category]:
                result.append(value)
        return result

    def get_unrecognized_skills(self):
        # Items written under "Skills:" that no technical regex found
        found = []
        for value in self.get_all_technical_strings():
            found.append(value.lower())

        unrecognized = []
        for item in self.skills_section:
            if item.lower() not in found:
                unrecognized.append(item)
        return unrecognized

    def to_dict(self):
        education = []
        for entry in self.education:
            education.append(entry.to_dict())
        experience = []
        for entry in self.experience:
            experience.append(entry.to_dict())

        data = {
            "name": self.name,
            "emails": self.emails,
            "phones": self.phones,
            "links": self.links,
        }
        data.update(self.get_technical_items())
        data["education"] = education
        data["experience"] = experience
        data["skills_section"] = self.skills_section
        return data

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)


class Candidate:
    # Candidate information used by the rest of the pipeline

    def __init__(self, full_name="", email="", phone="", links=None, skills=None,
                 academic_qualifications=None, experience=None, profile_results=None):
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.links = links if links is not None else []
        self.skills = skills if skills is not None else []
        self.academic_qualifications = academic_qualifications if academic_qualifications is not None else []
        self.experience = experience if experience is not None else []
        self.profile_results = profile_results if profile_results is not None else {}


class PipelineResult:
    # Everything the pipeline produces for one resume

    def __init__(self, candidate, extracted, normalized_tokens, classification, dsl_text="", html="", notes=None):
        self.candidate = candidate
        self.extracted = extracted
        self.normalized_tokens = normalized_tokens
        self.classification = classification
        self.dsl_text = dsl_text
        self.html = html
        self.notes = notes if notes is not None else []
