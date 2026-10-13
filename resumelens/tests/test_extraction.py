import os

from resumelens.extraction.extractor import ResumeExtractor, extract_name, find_all, find_all_in_order
from resumelens.extraction.patterns import (
    DATABASE_REGEX,
    EMAIL_REGEX,
    LIBRARY_REGEX,
    PHONE_REGEX,
    TECHNICAL_REGEXES,
    TOOL_REGEX,
    URL_REGEX,
)

SAMPLES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "sample_resumes")


def load_sample(filename):
    return ResumeExtractor.from_file(os.path.join(SAMPLES, filename)).extract()


def check_each_variant_is_found(regexes, variants):
    for variant in variants:
        assert find_all_in_order(regexes, variant) == [variant], variant


# Example from the assignment

def test_reference_fragment_gives_the_five_strings():
    text = "Wednesday Addams\n3 years of experience developing web applications.\nTechnical Skills:\nJS, React.js, NodeJS, Postgres, Git."
    result = ResumeExtractor(text).extract()
    assert result.name == "Wednesday Addams"
    assert result.get_all_technical_strings() == ["JS", "React.js", "NodeJS", "Postgres", "Git"]
    assert result.experience[0].years == 3
    assert result.experience[0].description == "developing web applications"


# Technical categories

def test_programming_languages():
    variants = ["JavaScript", "Javascript", "Java Script", "TypeScript", "python3", "C#", "c sharp", "Golang", "Kotlin", "JS", "Go", "R"]
    check_each_variant_is_found(TECHNICAL_REGEXES["programming_languages"], variants)


def test_short_language_names_are_not_normal_words():
    regexes = TECHNICAL_REGEXES["programming_languages"]
    assert find_all_in_order(regexes, "I want to go home") == []
    assert find_all_in_order(regexes, "Read the js file") == []
    assert find_all_in_order(regexes, "R&D department") == []


def test_java_is_not_found_inside_javascript():
    assert find_all_in_order(TECHNICAL_REGEXES["programming_languages"], "JavaScript") == ["JavaScript"]


def test_frameworks():
    variants = ["React", "React.js", "ReactJS", "Node.js", "NodeJS", "Vue.js", "Spring Boot", "SpringBoot", "FastAPI", ".NET", "Express.js", "Express"]
    check_each_variant_is_found(TECHNICAL_REGEXES["frameworks"], variants)


def test_libraries():
    variants = ["Scikit-learn", "scikit learn", "sklearn", "Tensor Flow", "TensorFlow", "Py Torch", "PyTorch", "NumPy", "Matplotlib"]
    check_each_variant_is_found([LIBRARY_REGEX], variants)


def test_databases():
    variants = ["Postgres", "PostgreSQL", "MySQL", "MongoDB", "Mongo", "SQLite", "SQL"]
    check_each_variant_is_found([DATABASE_REGEX], variants)


def test_sql_is_not_found_inside_nosql():
    assert find_all(DATABASE_REGEX, "NoSQL") == []


def test_tools():
    variants = ["Git", "GitHub", "GitLab", "Docker", "Kubernetes", "k8s", "Power BI", "Tableau"]
    check_each_variant_is_found([TOOL_REGEX], variants)


def test_tools_are_not_found_inside_urls():
    assert find_all(TOOL_REGEX, "github.com/arivera") == []


def test_other_qualifications():
    variants = ["REST", "RESTful", "REST APIs", "rest api", "GraphQL", "Statistics", "statistical analysis"]
    check_each_variant_is_found(TECHNICAL_REGEXES["other_qualifications"], variants)


def test_rest_as_a_normal_word_is_ignored():
    assert find_all_in_order(TECHNICAL_REGEXES["other_qualifications"], "the rest of the team") == []


# Contact information

def test_email():
    assert find_all(EMAIL_REGEX, "Email: jane.doe+cv@mail.example.co") == ["jane.doe+cv@mail.example.co"]
    assert find_all(EMAIL_REGEX, "Email: not-an-email") == []


def test_phone():
    assert find_all(PHONE_REGEX, "Phone: +57 300 123 4567") == ["+57 300 123 4567"]
    assert find_all(PHONE_REGEX, "Phone: (602) 555-0187") == ["(602) 555-0187"]
    assert find_all(PHONE_REGEX, "Phone: +573001234567") == ["+573001234567"]
    assert find_all(PHONE_REGEX, "Worked 2019-2023") == []


def test_links():
    assert find_all(URL_REGEX, "See https://wednesday.dev.") == ["https://wednesday.dev"]
    assert find_all(URL_REGEX, "linkedin.com/in/mjwatson") == ["linkedin.com/in/mjwatson"]


def test_name_only_from_a_capitalized_first_line():
    assert extract_name("\n  Mary Jane Watson\nEmail: x@y.com") == "Mary Jane Watson"
    assert extract_name("Candidate with weird punctuation !!!") == ""


# Education, experience and skills section

def test_education_and_experience():
    text = ("Education: BSc in Software Engineering at Universidad Icesi.\n"
            "Master's in Applied Statistics, University of Leeds.\n"
            "5+ years of professional experience in backend services.")
    result = ResumeExtractor(text).extract()

    assert result.education[0].degree == "BSc"
    assert result.education[0].field == "Software Engineering"
    assert result.education[0].institution == "Universidad Icesi"
    assert result.education[1].degree == "Master's"
    assert result.education[1].field == "Applied Statistics"
    assert result.education[1].institution == "University of Leeds"
    assert result.experience[0].years == 5
    assert result.experience[0].description == "backend services"


def test_unrecognized_skills():
    result = ResumeExtractor("Skills: Python, Haskell, SQL.").extract()
    assert result.skills_section == ["Python", "Haskell", "SQL"]
    assert result.get_unrecognized_skills() == ["Haskell"]


# Sample resumes

def test_backend_sample():
    result = load_sample("alex_rivera_backend.txt")
    assert result.programming_languages == ["Java"]
    assert result.frameworks == ["Spring Boot"]
    assert result.tools == ["GitHub", "Docker", "Kubernetes"]
    assert "REST APIs" in result.other_qualifications


def test_data_scientist_sample():
    result = load_sample("nina_patel_data_scientist.txt")
    assert result.programming_languages == ["R", "Python"]
    assert "Statistics" in result.other_qualifications
    assert "Power BI" in result.tools


def test_edge_case_sample_has_no_technical_information():
    result = load_sample("invalid_edge_case.txt")
    assert result.name == ""
    assert result.emails == []
    assert result.get_all_technical_strings() == []


def test_extraction_is_saved_as_json(tmp_path):
    path = os.path.join(str(tmp_path), "out.json")
    ResumeExtractor.from_file(os.path.join(SAMPLES, "wednesday_addams.txt")).save_json(path)
    with open(path, encoding="utf-8") as file:
        assert '"React.js"' in file.read()
