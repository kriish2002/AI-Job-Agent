import requests

from jobs.base_provider import BaseProvider
from models.job import Job


class RemoteOKJobs(BaseProvider):

    URL = "https://remoteok.com/api"

    KEYWORDS = [
        "devops",
        "azure",
        "terraform",
        "cloud",
        "platform",
        "sre",
        "site reliability",
        "kubernetes",
        "docker",
        "infrastructure",
        "sysadmin",
        "operations"
    ]

    def fetch_jobs(self):

        print("🌐 Fetching jobs from RemoteOK...")

        headers = {
            "User-Agent": "Mozilla/5.0"
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

            print(f"❌ RemoteOK Error : {e}")
            return []

        print(f"✅ Total Records : {len(data)}")

        jobs = []

        for item in data:

            if not isinstance(item, dict):
                continue

            title = item.get("position", "")

            if not title:
                continue

            tags = item.get("tags", [])

            if not isinstance(tags, list):
                tags = []

            searchable_text = (
                title + " " + " ".join(tags)
            ).lower()

            matched = False

            for keyword in self.KEYWORDS:

                if keyword in searchable_text:
                    matched = True
                    break

            if not matched:
                continue

            job = Job(
                title=title,
                company=item.get("company", "Unknown"),
                location=item.get("location") or "Remote",
                salary=item.get("salary") or "Not Mentioned",
                apply_url=item.get("url", ""),
                source="RemoteOK"
            )

            jobs.append(job)

        print(f"🎯 Relevant RemoteOK Jobs : {len(jobs)}")

        return jobs