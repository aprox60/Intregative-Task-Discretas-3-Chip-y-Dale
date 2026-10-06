from __future__ import annotations

from resumelens.models import Candidate


def candidate_to_dsl(candidate: Candidate) -> str:
    """Serialize a Candidate dataclass to a DSL document string."""

    skills_block = "\n".join(f"skill {skill}" for skill in candidate.skills)
    experience_lines = candidate.experience or ["General experience"]
    education_lines = candidate.academic_qualifications or ["Bachelor's degree"]
    experiences = "\n".join(
        f"experience \"{exp}\" years 3" for exp in experience_lines
    )
    education = "\n".join(
        f"education \"{qual}\" institution \"University\"" for qual in education_lines
    )
    profile_name = next(iter(candidate.profile_results), "FULL_STACK_DEVELOPER") if candidate.profile_results else "FULL_STACK_DEVELOPER"
    status = "ACCEPTED" if candidate.profile_results.get(profile_name, False) else "REJECTED"

    text = f'''candidate "{candidate.full_name or 'Candidate'}"
email {candidate.email or 'example@example.com'}
phone {candidate.phone or '+0000000000'}
links {candidate.links[0] if candidate.links else 'https://example.com'}
{experiences}
{education}
{skills_block}
profile {profile_name} status {status}
'''
    return text
