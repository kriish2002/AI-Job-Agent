import json

from utils.gemini_client import GeminiClient


class EligibilityAgent:

    def __init__(self):

        self.gemini = GeminiClient()

    def check(self, resume_text, job):

        prompt = f"""
You are a strict job eligibility checker.

CANDIDATE INFORMATION:

Candidate is based in India.
Preferred jobs:
- India
- Remote India
- Worldwide Remote

Candidate experience:
2+ years.

Candidate target roles:
- DevOps Engineer
- Cloud Engineer
- Azure DevOps Engineer
- Site Reliability Engineer
- SRE
- Platform Engineer
- Cloud Infrastructure Engineer

CANDIDATE RESUME:

{resume_text}

JOB TITLE:

{job.title}

JOB COMPANY:

{job.company}

JOB LOCATION:

{job.location}

JOB DESCRIPTION:

{job.description}

STRICT ELIGIBILITY RULES:

Reject the job if:

1. Job is restricted to USA only.
2. Job is restricted to Europe only.
3. Job is restricted to Canada only.
4. Job requires US citizenship.
5. Job requires security clearance.
6. Job requires local work authorization outside India.
7. Job is Senior, Staff, Principal, Director, Head, Architect or Manager level.
8. Job clearly requires more than 4 years of experience.
9. Job role is not related to DevOps, Cloud, SRE, Platform or Infrastructure.
10. Candidate is clearly not geographically eligible.

Accept the job if:

1. Job is India based.
2. Job is worldwide remote.
3. Job explicitly allows candidates from India.
4. Job location is flexible and there is no clear country restriction.
5. Experience requirement reasonably matches a candidate with 2+ years.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "eligible": true,
    "reason": "Short reason"
}}

OR

{{
    "eligible": false,
    "reason": "Short reason"
}}
"""

        try:

            response = self.gemini.generate(
                prompt
            )

            response = response.strip()

            response = response.replace(
                "```json",
                ""
            )

            response = response.replace(
                "```",
                ""
            )

            result = json.loads(
                response.strip()
            )

            return {
                "eligible": result.get(
                    "eligible",
                    False
                ),
                "reason": result.get(
                    "reason",
                    "No reason provided"
                )
            }

        except Exception as e:

            print(
                f"\n⚠️ Eligibility Check Error : {e}"
            )

            return {
                "eligible": False,
                "reason": "AI eligibility check failed"
            }