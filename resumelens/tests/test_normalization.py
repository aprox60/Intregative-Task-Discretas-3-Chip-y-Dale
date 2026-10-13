from resumelens.classification.profiles import PROFILES
from resumelens.extraction.extractor import ResumeExtractor
from resumelens.normalization.normalizer import normalize_extraction, normalize_string
from resumelens.normalization.sorter import sort_for_profile


def test_examples_from_the_assignment():
    assert normalize_string("JS", "programming_languages") == "JAVASCRIPT"
    assert normalize_string("Javascript", "programming_languages") == "JAVASCRIPT"
    assert normalize_string("React.js", "frameworks") == "REACT"
    assert normalize_string("ReactJS", "frameworks") == "REACT"
    assert normalize_string("NodeJS", "frameworks") == "NODE_JS"
    assert normalize_string("Node.js", "frameworks") == "NODE_JS"
    assert normalize_string("Postgres", "databases") == "POSTGRESQL"
    assert normalize_string("PostgreSQL", "databases") == "POSTGRESQL"
    assert normalize_string("pandas", "libraries") == "PANDAS"
    assert normalize_string("sklearn", "libraries") == "SCIKIT_LEARN"
    assert normalize_string("scikit learn", "libraries") == "SCIKIT_LEARN"
    assert normalize_string("Scikit-learn", "libraries") == "SCIKIT_LEARN"
    assert normalize_string("Tensor Flow", "libraries") == "TENSORFLOW"
    assert normalize_string("PyTorch", "libraries") == "PYTORCH"


def test_our_own_transformations():
    assert normalize_string("C#", "programming_languages") == "CSHARP"
    assert normalize_string("Golang", "programming_languages") == "GO"
    assert normalize_string(".NET", "frameworks") == "DOTNET"
    assert normalize_string("Spring Boot", "frameworks") == "SPRING_BOOT"
    assert normalize_string("GitHub", "tools") == "GIT"
    assert normalize_string("k8s", "tools") == "KUBERNETES"
    assert normalize_string("Power BI", "tools") == "POWER_BI"
    assert normalize_string("RESTful APIs", "other_qualifications") == "REST_API"
    assert normalize_string("statistical analysis", "other_qualifications") == "STATISTICS"


def test_unknown_strings_are_rejected():
    assert normalize_string("Haskell", "programming_languages") is None
    assert normalize_string("React", "databases") is None


def test_repeated_qualifications_are_kept_once():
    extraction = ResumeExtractor("Skills: JavaScript, JS, React, ReactJS, Git, GitHub").extract()
    result = normalize_extraction(extraction)
    assert result.tokens == ["JAVASCRIPT", "REACT", "GIT"]


def test_sorting_example_from_the_assignment():
    tokens = ["GIT", "NODE_JS", "JAVASCRIPT", "POSTGRESQL", "REACT"]
    expected = ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]
    assert sort_for_profile(tokens, PROFILES["FULL_STACK_DEVELOPER"]) == expected


def test_sorting_leaves_out_tokens_of_other_profiles():
    tokens = ["GIT", "PYTHON", "DOCKER", "PANDAS"]
    assert sort_for_profile(tokens, PROFILES["MACHINE_LEARNING_ENGINEER"]) == ["PYTHON", "PANDAS", "GIT"]
