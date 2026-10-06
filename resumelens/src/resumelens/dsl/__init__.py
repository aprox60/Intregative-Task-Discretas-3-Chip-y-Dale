"""Domain-specific language (DSL) support for validated candidate models."""

from resumelens.dsl.generator import candidate_to_dsl
from resumelens.dsl.parser import ResumeParser
from resumelens.dsl.validator import validate_resume_dsl
from resumelens.dsl.visualizer import render_html

__all__ = ["ResumeParser", "candidate_to_dsl", "validate_resume_dsl", "render_html"]
