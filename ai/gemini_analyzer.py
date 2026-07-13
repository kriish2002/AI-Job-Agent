import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY missing in .env file")

client = genai.Client(api_key=GEMINI_API_KEY)


def analyze_job(job_description):
    prompt = f"""
You are an AI Job Matching Assistant.

Candidate Profile:
- DevOps and Cloud Engineer
- 2+ years of experience
- Azure
- AWS
- Terraform
- Azure DevOps
- Jenkins
- GitHub Actions
- Docker
- Kubernetes
- Linux
- CI/CD
- Infrastructure Automation

Preferred Roles:
- DevOps Engineer
- Cloud Engineer
- Azure DevOps Engineer
- SRE
- Platform Engineer
- Cloud Infrastructure Engineer

Analyze this job description:

{job_description}

Return exactly in this format:

MATCH_SCORE: <0-100>
ROLE: <job role>
EXPERIENCE_REQUIRED: <experience>
MATCH_REASON: <short reason>
RECOMMENDATION: <APPLY or SKIP>
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt,
        )

        return response.text

    except Exception as error:
        return f"❌ Gemini Error: {error}"


if __name__ == "__main__":
    test_job = """
We are hiring a DevOps Engineer with 1-3 years of experience.

Required skills:
Azure, Terraform, Docker, Kubernetes, Linux and CI/CD.

Candidate should have experience with Azure DevOps pipelines.
"""

    result = analyze_job(test_job)

    print("\n🤖 GEMINI JOB ANALYSIS\n")
    print(result)