import os

from utils.gemini_client import GeminiClient


class CoverLetterGenerator:

    def __init__(self):

        self.gemini = GeminiClient()

    def generate(self, resume_text, job, match_result):

        matched_skills = match_result.get(
            "matched_skills",
            []
        )

        missing_skills = match_result.get(
            "missing_skills",
            []
        )

        prompt = f"""
Write a factual professional cover letter.

Use ONLY information explicitly present in the resume.

RESUME:
{resume_text}

JOB TITLE:
{job.title}

COMPANY:
{job.company}

JOB DESCRIPTION:
{job.description}

VERIFIED MATCHED SKILLS:
{", ".join(matched_skills)}

MISSING SKILLS:
{", ".join(missing_skills)}

RULES:

- Use only facts from the resume.
- Never invent achievements.
- Never invent metrics.
- Never invent awards or recognition.
- Never claim missing skills.
- Do not exaggerate experience.
- Do not use phrases like deep expertise, extensive experience,
  proven track record, exceptional, highly skilled, or industry-leading.
- Write simple professional English.
- Write 180 to 230 words.
- Mention the candidate is an immediate joiner.
- Start with "Dear Hiring Manager,"
- End with:

Sincerely,
Krishan Kumar Rawat

Return only the cover letter.
"""

        try:

            print(
                "\n🤖 Gemini is writing cover letter..."
            )

            draft = self.gemini.generate(
                prompt
            )

            print(
                "🔍 Gemini is validating facts..."
            )

            validation_prompt = f"""
You are a strict factual resume validator.

RESUME:
{resume_text}

GENERATED COVER LETTER:
{draft}

MISSING SKILLS:
{", ".join(missing_skills)}

TASK:

Review the cover letter against the resume.

Remove or rewrite ANY statement that:

- is not explicitly supported by the resume
- exaggerates experience
- invents achievements
- invents responsibilities
- invents awards
- invents metrics
- claims a missing skill
- uses exaggerated language

Keep company name and job title.

Keep the candidate as an immediate joiner.

Use simple and natural professional English.

The final cover letter must be factual.

Start exactly with:

Dear Hiring Manager,

End exactly with:

Sincerely,
Krishan Kumar Rawat

Return ONLY the corrected cover letter.
"""

            final_letter = self.gemini.generate(
                validation_prompt
            )

            return final_letter.strip()

        except Exception as e:

            print(
                f"\n❌ AI Cover Letter Error : {e}"
            )

            return ""

    def save(self, cover_letter):

        if not cover_letter:
            return

        os.makedirs(
            "database",
            exist_ok=True
        )

        file_path = (
            "database/cover_letter.txt"
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                cover_letter
            )

        print(
            "\n💾 AI Cover Letter Saved : "
            f"{file_path}"
        )