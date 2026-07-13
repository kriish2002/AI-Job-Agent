from jobs.jobicy_jobs import JobicyJobs
from utils.job_scorer import JobScorer


class SearchAgent:

    def __init__(self):

        self.providers = [
            JobicyJobs()
        ]

        self.job_scorer = JobScorer()

    def search(self):

        all_jobs = []

        for provider in self.providers:

            try:

                jobs = provider.fetch_jobs()

                all_jobs.extend(jobs)

            except Exception as e:

                print(
                    f"❌ Provider Error : {e}"
                )

        scored_jobs = []

        for job in all_jobs:

            scored_job = (
                self.job_scorer.calculate_score(job)
            )

            if scored_job.score >= 40:

                scored_jobs.append(
                    scored_job
                )

        scored_jobs.sort(
            key=lambda job: job.score,
            reverse=True
        )

        print(
            f"🤖 Profile Matched Jobs : "
            f"{len(scored_jobs)}"
        )

        return scored_jobs