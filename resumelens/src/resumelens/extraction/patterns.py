# Stage 1: regular expressions used to find information in the resume text.
#
# These patterns only find strings. Deciding that "JS" and "JavaScript" are the same
# thing is done by the transducers (stage 2), and deciding if a candidate fits a
# profile is done by the automata (stage 3).

import re

# Python's \b does not work well with names like "Node.js" or "C#", because "." "+" and
# "#" are not word characters. So we use our own boundaries:
# BEFORE: the previous character is not a letter, digit, "_", "+", "#", "&" or "."
# (that way the "JS" of "Node.JS" is not taken as a language)
# AFTER: the next character is not one of those either, and it can't be ".something"
# (that way "github" inside "github.com/..." is not taken as the tool Git)
BEFORE = r"(?<![\w+#&.])"
AFTER = r"(?![\w+#&]|\.\w)"

# Optional separator between the parts of a name: "Scikit-learn", "scikit learn", "scikitlearn"
SEP = r"[\s.\-]?"


# ---------- Personal and contact information ----------

NAME_REGEX = re.compile(r"[A-ZÀ-Ý][A-Za-zÀ-ÿ'\-]+(\s+[A-ZÀ-Ý][A-Za-zÀ-ÿ'\-]+){1,4}")

EMAIL_REGEX = re.compile(r"(?<![\w.+-])[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}(?![\w-])")

PHONE_REGEX = re.compile(r"(?<![\w+])(\+?\(?\d{1,4}\)?([\s.\-]\d{2,4}){2,4}|\+?\d{7,15})(?!\w)")

URL_REGEX = re.compile(
    r"(https?://|www\.)[^\s,;]*[^\s,;.]|(?<![\w.])(linkedin|github)\.com/[^\s,;]*[^\s,;.]",
    re.IGNORECASE,
)


# ---------- Technical qualifications (each category has its own transducer in stage 2) ----------

LANGUAGE_REGEX = re.compile(
    BEFORE + r"(java[\s\-]?script|type[\s\-]?script|python(\s?3)?|java|golang|kotlin|c\s?#|c[\s\-]sharp|csharp)" + AFTER,
    re.IGNORECASE,
)

# Short names that are also normal words ("go home", "R&D"), so they only count
# when they are written exactly like this
LANGUAGE_SHORT_REGEX = re.compile(BEFORE + r"(JS|TS|Go|R)" + AFTER)

FRAMEWORK_REGEX = re.compile(
    BEFORE
    + r"(react(" + SEP + r"js)?|angular(" + SEP + r"js)?|vue(" + SEP + r"js)?|node(" + SEP + r"js)?"
    + r"|express" + SEP + r"js|django|flask|fast[\s\-]?api|spring[\s\-]?boot"
    + r"|asp\.net(\s?core)?|\.net(\s?core)?|dotnet)"
    + AFTER,
    re.IGNORECASE,
)

# "express" alone is a normal word, so without ".js" it has to start with a capital letter
FRAMEWORK_SHORT_REGEX = re.compile(BEFORE + r"(Express)" + AFTER)

LIBRARY_REGEX = re.compile(
    BEFORE
    + r"(pandas|num[\s\-]?py|scikit[\s\-]?learn|sk[\s\-]?learn|tensor[\s\-]?flow|py[\s\-]?torch|keras"
    + r"|matplotlib|seaborn|plotly)"
    + AFTER,
    re.IGNORECASE,
)

DATABASE_REGEX = re.compile(
    BEFORE + r"(postgres|postgre\s?sql|my\s?sql|mongo(\s?db)?|sqlite|redis|sql)" + AFTER,
    re.IGNORECASE,
)

TOOL_REGEX = re.compile(
    BEFORE + r"(git|github|gitlab|docker|kubernetes|k8s|tableau|power[\s\-]?bi)" + AFTER,
    re.IGNORECASE,
)

OTHER_REGEX = re.compile(
    BEFORE + r"(rest(ful)?[\s\-]?apis?|restful|graph\s?ql|statistics|statistical(\s+(analysis|modeling|modelling))?)" + AFTER,
    re.IGNORECASE,
)

# "rest" alone is a normal word, so it only counts in upper case
OTHER_SHORT_REGEX = re.compile(BEFORE + r"(REST)" + AFTER)

# Each technical category with the regexes that find it
TECHNICAL_REGEXES = {
    "programming_languages": [LANGUAGE_REGEX, LANGUAGE_SHORT_REGEX],
    "frameworks": [FRAMEWORK_REGEX, FRAMEWORK_SHORT_REGEX],
    "libraries": [LIBRARY_REGEX],
    "databases": [DATABASE_REGEX],
    "tools": [TOOL_REGEX],
    "other_qualifications": [OTHER_REGEX, OTHER_SHORT_REGEX],
}


# ---------- Education, experience and skills section ----------

EDUCATION_REGEX = re.compile(
    r"(?<!\w)(?P<degree>Ph\.?\s?D\.?|M\.?\s?Sc\.?|B\.?\s?Sc\.?|M\.?S\.?|B\.?S\.?|B\.?A\.?|M\.?A\.?|Doctorate"
    r"|(Bachelor|Master)('s)?(\s+of\s+(Science|Arts|Engineering))?)"
    r"(\s+degree)?\s+(in|of)\s+"
    r"(?P<field>[A-Z][A-Za-z&/ ]*?[A-Za-z])"
    r"((\s*[,\-]\s*|\s+(at|from)\s+)(?P<institution>[A-Z][\w&.' ]*?\w))?"
    r"\s*(?=[.;\n]|$)"
)

EXPERIENCE_REGEX = re.compile(
    r"(?<!\w)(?P<years>\d{1,2})\+?\s*(years?|yrs?)\s+of\s+(professional\s+)?experience(\s+(?P<description>[^.\n]+))?",
    re.IGNORECASE,
)

SKILLS_SECTION_REGEX = re.compile(r"^\s*(technical\s+)?skills\s*:\s*(?P<items>.+)$", re.IGNORECASE | re.MULTILINE)

SKILL_SEPARATOR_REGEX = re.compile(r"\s*[,;|]\s*")

LEADING_PREPOSITION_REGEX = re.compile(r"^(in|as|with|on)\s+", re.IGNORECASE)


# Language recognized by each pattern (used in the docs)
DESCRIPTIONS = {
    "name": "Two to five capitalized words separated by spaces. It is only checked against the first non-empty line.",
    "emails": "local part, '@', domain labels separated by dots and a top level domain of 2 or more letters.",
    "phones": "Optional '+', then a prefix (can be in parentheses) followed by 2 to 4 digit blocks, each one "
              "after exactly one space, dot or hyphen. Or 7 to 15 digits together.",
    "links": "Text that starts with http://, https:// or www. (or linkedin.com/, github.com/) until the next space or comma.",
    "programming_languages": "JavaScript, TypeScript, Python, Java, Go, Kotlin, C# and R with their usual spellings. "
                             "JS, TS, Go and R only with that exact capitalization.",
    "frameworks": "React, Angular, Vue, Node and Express with or without '.js'/'JS', plus Django, Flask, FastAPI, "
                  "Spring Boot and .NET.",
    "libraries": "Python data, machine learning and plotting libraries, allowing a space or hyphen inside "
                 "compound names (Tensor Flow, Scikit-learn, Py Torch).",
    "databases": "PostgreSQL/Postgres, MySQL, MongoDB/Mongo, SQLite, Redis and the SQL language.",
    "tools": "Git, GitHub, GitLab, Docker, Kubernetes/k8s, Tableau and Power BI.",
    "other_qualifications": "REST, RESTful, REST APIs, GraphQL, statistics and statistical analysis. "
                            "REST alone only in upper case.",
    "education": "A degree (BS, BSc, MSc, PhD, Bachelor's, Master's...) followed by 'in' or 'of', a field that starts "
                 "with a capital letter and optionally ', Institution' or 'at Institution'.",
    "experience": "A number of years, 'years of experience' and an optional description until the end of the sentence.",
    "skills_section": "A line that starts with 'Skills:' or 'Technical Skills:'. Its items are split by commas, "
                      "semicolons or bars.",
}
