import re
import requests

from jobs.base_provider import BaseProvider
from models.job import Job


class JobicyJobs(BaseProvider):

    URL = "https://jobicy.com/api/v2/remote-jobs"

    SEARCH_TERMS = [
        "devops",
        "azure",
        "terraform",
        "cloud engineer",
        "site reliability",
        "platform engineer",
        "kubernetes"
    ]

    def clean_description(self, description):

        if not description:
            return ""

        clean_text = re.sub(
            r"<[^>]+>",
            " ",
            description
        )

        clean_text = re.sub(
            r"\s+",
            " ",
            clean_text
        )

        return clean_text.strip()

    def fetch_jobs(self):

        print("🌐 Fetching jobs from Jobicy...")

        jobs = []
        seen_urls = set()

        headers = {
            "User-Agent": "AI-Job-Agent/1.0"
        }

        for search_term in self.SEARCH_TERMS:

            try:

                response = requests.get(
                    self.URL,
                    params={
                        "count": 100,
                        "tag": search_term
                    },
                    headers=headers,
                    timeout=30
                )

                response.raise_for_status()

                data = response.json()

                api_jobs = data.get("jobs", [])

                print(
                    f"🔎 {search_term} : "
                    f"{len(api_jobs)} jobs"
                )

                for item in api_jobs:

                    apply_url = item.get("url", "")

                    if not apply_url:
                        continue

                    if apply_url in seen_urls:
                        continue

                    seen_urls.add(apply_url)

                    description = self.clean_description(
                        item.get("jobDescription", "")
                    )

                    salary_min = item.get(
                        "annualSalaryMin"
                    )

                    salary_max = item.get(
                        "annualSalaryMax"
                    )

                    if salary_min and salary_max:

                        salary = (
                            f"{salary_min} - "
                            f"{salary_max}"
                        )

                    elif salary_min:

                        salary = str(salary_min)

                    else:

                        salary = "Not Mentioned"

                    job = Job(
                        title=item.get(
                            "jobTitle",
                            "Unknown"
                        ),
                        company=item.get(
                            "companyName",
                            "Unknown"
                        ),
                        location=item.get(
                            "jobGeo"
                        ) or "Remote",
                        salary=salary,
                        apply_url=apply_url,
                        source="Jobicy",
                        description=description
                    )

                    jobs.append(job)

            except Exception as e:

                print(
                    f"❌ Jobicy Error "
                    f"[{search_term}] : {e}"
                )

        print(
            f"🎯 Unique Jobicy Jobs : {len(jobs)}"
        )

        return jobs