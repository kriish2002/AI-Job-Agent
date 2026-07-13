import requests

from jobs.base_provider import BaseProvider
from models.job import Job


class RemotiveJobs(BaseProvider):

    URL = "https://remotive.com/api/remote-jobs"

    ALLOWED_CATEGORIES = [
        "devops",
        "information technology",
        "operations"
    ]

    TARGET_KEYWORDS = [
        "devops",
        "devsecops",
        "cloud",
        "azure",
        "aws",
        "platform engineer",
        "site reliability",
        "sre",
        "infrastructure",
        "terraform",
        "kubernetes"
    ]

    def fetch_jobs(self):

        print("🌐 Fetching jobs from Remotive...")

        headers = {
            "User-Agent": "AI-Job-Agent/1.0"
        }

        try:

            response = requests.get(
                self.URL,
                headers=headers,
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

        except Exception as e:

            print(f"❌ Remotive Error : {e}")
            return []

        api_jobs = data.get("jobs", [])

        print(f"📦 API Jobs : {len(api_jobs)}")

        jobs = []

        for item in api_jobs:

            title = item.get("title", "").strip()
            category = item.get("category", "").lower().strip()

            if not title:
                continue

            title_lower = title.lower()

            category_match = category in self.ALLOWED_CATEGORIES

            keyword_match = any(
                keyword in title_lower
                for keyword in self.TARGET_KEYWORDS
            )

            if not category_match and not keyword_match:
                continue

            job = Job(
                title=title,
                company=item.get(
                    "company_name",
                    "Unknown"
                ),
                location=item.get(
                    "candidate_required_location"
                ) or "Remote",
                salary=item.get(
                    "salary"
                ) or "Not Mentioned",
                apply_url=item.get(
                    "url",
                    ""
                ),
                source="Remotive"
            )

            jobs.append(job)

        print(f"🎯 Profile Matched Jobs : {len(jobs)}")

        return jobs