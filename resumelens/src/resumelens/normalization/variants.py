# Stage 2: the transformations that the transducers have to do.
#
# For each technical category we list the variants (already preprocessed: lower case and
# without spaces, dots, hyphens, underscores or slashes) and the canonical token for each one.
# Every category becomes its own transducer.

LANGUAGE_VARIANTS = {
    "javascript": "JAVASCRIPT",
    "js": "JAVASCRIPT",
    "typescript": "TYPESCRIPT",
    "ts": "TYPESCRIPT",
    "python": "PYTHON",
    "python3": "PYTHON",
    "java": "JAVA",
    "go": "GO",
    "golang": "GO",
    "kotlin": "KOTLIN",
    "c#": "CSHARP",
    "csharp": "CSHARP",
    "r": "R",
}

FRAMEWORK_VARIANTS = {
    "react": "REACT",
    "reactjs": "REACT",
    "angular": "ANGULAR",
    "angularjs": "ANGULAR",
    "vue": "VUE",
    "vuejs": "VUE",
    "node": "NODE_JS",
    "nodejs": "NODE_JS",
    "express": "EXPRESS",
    "expressjs": "EXPRESS",
    "django": "DJANGO",
    "flask": "FLASK",
    "fastapi": "FASTAPI",
    "springboot": "SPRING_BOOT",
    "net": "DOTNET",
    "netcore": "DOTNET",
    "aspnet": "DOTNET",
    "aspnetcore": "DOTNET",
    "dotnet": "DOTNET",
}

LIBRARY_VARIANTS = {
    "pandas": "PANDAS",
    "numpy": "NUMPY",
    "scikitlearn": "SCIKIT_LEARN",
    "sklearn": "SCIKIT_LEARN",
    "tensorflow": "TENSORFLOW",
    "pytorch": "PYTORCH",
    "keras": "KERAS",
    "matplotlib": "MATPLOTLIB",
    "seaborn": "SEABORN",
    "plotly": "PLOTLY",
}

DATABASE_VARIANTS = {
    "postgres": "POSTGRESQL",
    "postgresql": "POSTGRESQL",
    "mysql": "MYSQL",
    "mongo": "MONGODB",
    "mongodb": "MONGODB",
    "sqlite": "SQLITE",
    "redis": "REDIS",
    "sql": "SQL",
}

TOOL_VARIANTS = {
    "git": "GIT",
    "github": "GIT",
    "gitlab": "GIT",
    "docker": "DOCKER",
    "kubernetes": "KUBERNETES",
    "k8s": "KUBERNETES",
    "tableau": "TABLEAU",
    "powerbi": "POWER_BI",
}

OTHER_VARIANTS = {
    "rest": "REST_API",
    "restful": "REST_API",
    "restapi": "REST_API",
    "restapis": "REST_API",
    "restfulapi": "REST_API",
    "restfulapis": "REST_API",
    "graphql": "GRAPHQL",
    "statistics": "STATISTICS",
    "statistical": "STATISTICS",
    "statisticalanalysis": "STATISTICS",
    "statisticalmodeling": "STATISTICS",
    "statisticalmodelling": "STATISTICS",
}

# Same category names used by the extraction stage
VARIANTS_BY_CATEGORY = {
    "programming_languages": LANGUAGE_VARIANTS,
    "frameworks": FRAMEWORK_VARIANTS,
    "libraries": LIBRARY_VARIANTS,
    "databases": DATABASE_VARIANTS,
    "tools": TOOL_VARIANTS,
    "other_qualifications": OTHER_VARIANTS,
}
